// DegenKit — thin wrapper around the Raydium SDK v2 (CPMM pools).
// Bundled into assets/dk-raydium.js and lazy-loaded by the Solana page.
import { Raydium, TxVersion, Percent, CREATE_CPMM_POOL_PROGRAM, CREATE_CPMM_POOL_FEE_ACC,
  DEVNET_PROGRAM_ID, getCpmmPdaAmmConfigId } from "@raydium-io/raydium-sdk-v2";
import { Connection, PublicKey, Transaction, VersionedTransaction } from "@solana/web3.js";
import { NATIVE_MINT, TOKEN_PROGRAM_ID, getMint } from "@solana/spl-token";
import BN from "bn.js";

export type SignTx = (bytes: Uint8Array) => Promise<Uint8Array>;
export interface Ctx { rpc: string; cluster: "mainnet" | "devnet"; owner: string; signTx: SignTx; }

const cache = new Map<string, Promise<Raydium>>();
function getRaydium(c: Ctx): Promise<Raydium> {
  const key = c.cluster + "|" + c.owner + "|" + c.rpc;
  let p = cache.get(key);
  if (!p) {
    const connection = new Connection(c.rpc, "confirmed");
    p = Raydium.load({
      connection, cluster: c.cluster, owner: new PublicKey(c.owner), disableLoadToken: true, disableFeatureCheck: true,
      signAllTransactions: async (txs: any[]) => {
        const out: any[] = [];
        for (const tx of txs) {
          if (tx instanceof VersionedTransaction) {
            const signed = await c.signTx(tx.serialize());
            out.push(VersionedTransaction.deserialize(signed));
          } else {
            const signed = await c.signTx((tx as Transaction).serialize({ requireAllSignatures: false, verifySignatures: false }));
            out.push(Transaction.from(signed));
          }
        }
        return out;
      },
    } as any);
    p.catch(() => cache.delete(key));
    cache.set(key, p);
  }
  return p;
}

const programs = (cluster: string) => cluster === "devnet"
  ? { programId: DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_PROGRAM, feeAcc: DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_FEE_ACC }
  : { programId: CREATE_CPMM_POOL_PROGRAM, feeAcc: CREATE_CPMM_POOL_FEE_ACC };

async function feeConfig(r: Raydium, cluster: string) {
  const cfgs: any[] = await r.api.getCpmmConfigs();
  if (!cfgs || !cfgs.length) throw new Error("Could not load Raydium pool configuration. Try again in a moment.");
  if (cluster === "devnet") cfgs.forEach((c) => { c.id = getCpmmPdaAmmConfigId(DEVNET_PROGRAM_ID.CREATE_CPMM_POOL_PROGRAM, c.index).publicKey.toBase58(); });
  // Raydium's default (lowest-fee, 0.25%) tier is index 0 — what the Raydium UI preselects.
  return cfgs.find((c) => c.index === 0) || cfgs[0];
}

/** Raydium's pool creation fee in SOL (charged by Raydium, not DegenKit). */
export async function getCreateFeeSol(c: Ctx): Promise<number> {
  try {
    const r = await getRaydium(c);
    const cfg: any = await feeConfig(r, c.cluster);
    return Number(cfg.createPoolFee) / 1e9;
  } catch { return 0.15; }
}

async function tokenInfo(conn: Connection, mint: string) {
  const pk = new PublicKey(mint);
  if (mint === NATIVE_MINT.toBase58()) return { address: mint, decimals: 9, programId: TOKEN_PROGRAM_ID.toBase58() };
  const acc = await conn.getAccountInfo(pk);
  if (!acc) throw new Error("Token mint not found on this network: " + mint);
  const m = await getMint(conn, pk, "confirmed", acc.owner);
  return { address: mint, decimals: m.decimals, programId: acc.owner.toBase58() };
}

export interface CreateArgs { tokenMint: string; quoteMint: string; tokenAmountRaw: string; quoteAmountRaw: string; }

export async function createPool(c: Ctx, a: CreateArgs, onStep?: (s: string) => void) {
  const r = await getRaydium(c);
  const conn = r.connection;
  onStep?.("Preparing pool…");
  const [mintA, mintB] = await Promise.all([tokenInfo(conn, a.tokenMint), tokenInfo(conn, a.quoteMint)]);
  const cfg = await feeConfig(r, c.cluster);
  const { programId, feeAcc } = programs(c.cluster);
  const { execute, extInfo } = await r.cpmm.createPool({
    programId, poolFeeAccount: feeAcc,
    mintA: mintA as any, mintB: mintB as any,
    mintAAmount: new BN(a.tokenAmountRaw), mintBAmount: new BN(a.quoteAmountRaw),
    startTime: new BN(0), feeConfig: cfg, associatedOnly: false,
    ownerInfo: { useSOLBalance: true }, txVersion: TxVersion.V0,
    computeBudgetConfig: { units: 600000, microLamports: 100000 },
  } as any);
  onStep?.("Waiting for wallet signature…");
  const { txId } = await execute({ sendAndConfirm: true } as any);
  const addr: any = (extInfo as any).address;
  return { txId, poolId: String(addr.poolId.toBase58 ? addr.poolId.toBase58() : addr.poolId), lpMint: addr.lpMint ? String(addr.lpMint.toBase58()) : "" };
}

export interface Position {
  poolId: string; lpMint: string; lpRaw: string; lpDecimals: number;
  symbolA: string; symbolB: string; mintA: string; mintB: string;
  estA: number; estB: number; tvl: number; share: number;
}

function sym(t: any) { return (t && (t.symbol || t.address?.slice(0, 4))) || "?"; }

/** Finds the user's Raydium CPMM LP positions (via Raydium's public API). */
export async function listPositions(c: Ctx): Promise<Position[]> {
  const r = await getRaydium(c);
  const owner = new PublicKey(c.owner);
  const resp = await r.connection.getParsedTokenAccountsByOwner(owner, { programId: TOKEN_PROGRAM_ID });
  const held = new Map<string, { amount: string; decimals: number }>();
  for (const a of resp.value) {
    const i: any = a.account.data.parsed.info;
    if (i.tokenAmount.amount !== "0") held.set(i.mint, { amount: i.tokenAmount.amount, decimals: i.tokenAmount.decimals });
  }
  const mints = [...held.keys()].slice(0, 400);
  const out: Position[] = [];
  const cpmm = programs(c.cluster).programId.toBase58();
  for (let i = 0; i < mints.length; i += 50) {
    const chunk = mints.slice(i, i + 50);
    let pools: any[] = [];
    try { pools = await r.api.fetchPoolByLpMints({ ids: chunk.join(",") }); } catch { continue; }
    for (const p of pools || []) {
      if (!p || !p.lpMint || p.programId !== cpmm) continue;
      const h = held.get(p.lpMint.address);
      if (!h) continue;
      const supply = Number(p.lpAmount) || 0;
      const lpUi = Number(h.amount) / 10 ** h.decimals;
      const share = supply > 0 ? Math.min(1, lpUi / supply) : 0;
      out.push({
        poolId: p.id, lpMint: p.lpMint.address, lpRaw: h.amount, lpDecimals: h.decimals,
        symbolA: sym(p.mintA), symbolB: sym(p.mintB), mintA: p.mintA.address, mintB: p.mintB.address,
        estA: Number(p.mintAmountA) * share, estB: Number(p.mintAmountB) * share, tvl: Number(p.tvl) || 0, share,
      });
    }
  }
  return out;
}

/** Look up a pool by its id directly from chain (fallback when the API has not indexed it yet). */
export async function lookupPool(c: Ctx, poolId: string): Promise<Position | null> {
  const r = await getRaydium(c);
  const { poolInfo, rpcData } = (await r.cpmm.getPoolInfoFromRpc(poolId)) as any;
  const lpMint = poolInfo.lpMint.address;
  const resp = await r.connection.getParsedTokenAccountsByOwner(new PublicKey(c.owner), { mint: new PublicKey(lpMint) });
  const first: any = resp.value[0]?.account.data.parsed.info.tokenAmount;
  if (!first || first.amount === "0") return null;
  const supply = Number(rpcData.lpAmount?.toString?.() ?? 0) / 10 ** first.decimals;
  const lpUi = Number(first.amount) / 10 ** first.decimals;
  const share = supply > 0 ? Math.min(1, lpUi / supply) : 0;
  return {
    poolId, lpMint, lpRaw: first.amount, lpDecimals: first.decimals,
    symbolA: sym(poolInfo.mintA), symbolB: sym(poolInfo.mintB), mintA: poolInfo.mintA.address, mintB: poolInfo.mintB.address,
    estA: Number(poolInfo.mintAmountA) * share, estB: Number(poolInfo.mintAmountB) * share, tvl: 0, share,
  };
}

export async function removeLiquidity(c: Ctx, poolId: string, lpRaw: string, slippagePct: number, onStep?: (s: string) => void) {
  const r = await getRaydium(c);
  onStep?.("Preparing withdrawal…");
  const { poolInfo, poolKeys } = (await r.cpmm.getPoolInfoFromRpc(poolId)) as any;
  const { execute } = await r.cpmm.withdrawLiquidity({
    poolInfo, poolKeys, lpAmount: new BN(lpRaw), slippage: new Percent(Math.round(slippagePct * 100), 10000),
    txVersion: TxVersion.V0, closeWsol: true,
    computeBudgetConfig: { units: 400000, microLamports: 100000 },
  } as any);
  onStep?.("Waiting for wallet signature…");
  const { txId } = await execute({ sendAndConfirm: true } as any);
  return { txId };
}
