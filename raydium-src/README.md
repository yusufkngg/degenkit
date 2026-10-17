# dk-raydium (Raydium SDK v2 bundle)
`assets/dk-raydium.js` is a self-hosted bundle of the Raydium SDK (CPMM pools) so the site never depends on a CDN for it.
Rebuild after changing `src/dk-raydium.ts` or upgrading the SDK:

    npm init -y && npm i @raydium-io/raydium-sdk-v2 @solana/web3.js@1.95.4 @solana/spl-token@0.4.9 bn.js buffer esbuild
    node build.mjs
