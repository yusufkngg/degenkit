#!/usr/bin/env python3
"""Inserts a crawlable how-to guide + FAQ (with FAQPage JSON-LD) into each launch page. Idempotent."""
import re, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape

EVM_STEPS = lambda net, native, wallet, explorer: [
 ("Connect your wallet", f"Open the {net} launcher and connect {wallet}. DegenKit is non-custodial: it never sees your keys, and every action is a transaction you sign yourself."),
 ("Switch to " + net, f"If your wallet is on another network, the page asks it to switch to {net}. You need a little {native} to pay network gas."),
 ("Choose a token type", "Pick a plain fixed-supply ERC-20 or a Tax Token with your own buy and sell tax. Both have no mint function, so the supply you set is final."),
 ("Fill in name, symbol and supply", "Name and symbol become the permanent on-chain identity. Decimals are fixed at 18, the ERC-20 standard."),
 ("Review the fee and sign once", f"The summary shows the service fee (if any) and you confirm one transaction. When it lands, the full supply is in your wallet and the contract is verifiable on {explorer}."),
 ("Add liquidity", "Create a pool on a DEX of your choice. For a Tax Token, open Manage and mark the pool address so the tax starts applying."),
]
CHAINS = {
 "ethereum": dict(name="Ethereum", native="ETH", std="ERC-20", explorer="Etherscan", wallet="MetaMask, Rabby or any EIP-1193 wallet",
   intro="Ethereum is the deepest liquidity and the most trusted venue for a token. DegenKit lets you create a fixed-supply ERC-20 or a tax token on Ethereum mainnet without writing Solidity, from your own wallet, in one transaction.",
   when="Choose Ethereum when you want maximum credibility and deep DEX liquidity and are comfortable with higher gas costs than Layer 2s or BNB Chain.",
   faq=[("How do I create an ERC-20 token on Ethereum without coding?","Open the Ethereum launcher, connect your wallet, enter the name, symbol and supply, and sign one transaction. The full supply lands in your wallet and the contract has no mint function."),
        ("Can I make an Ethereum token with a buy and sell tax?","Yes. Use the Tax Token view to set separate buy and sell tax rates and a wallet that receives the tax. The tax only applies to trades against a pool you mark, never to normal transfers."),
        ("What does it cost to create a token on Ethereum?","You pay Ethereum network gas plus DegenKit's service fee shown in the summary before you sign. Gas varies with network congestion.")]),
 "bnb": dict(name="BNB Chain", native="BNB", std="BEP-20", explorer="BscScan", wallet="MetaMask, Trust Wallet or any EIP-1193 wallet",
   intro="BNB Smart Chain has low fees and an active retail trading scene. DegenKit lets you create a BEP-20 token or a tax token on BNB Chain without writing code, signed from your own wallet.",
   when="Choose BNB Chain when you want low transaction costs and access to PancakeSwap-style liquidity and a large retail audience.",
   faq=[("How do I create a BEP-20 token on BNB Chain without coding?","Open the BNB Chain launcher, connect your wallet, fill in name, symbol and supply, and sign one transaction. The whole supply is minted to your wallet and cannot be increased."),
        ("Can I launch a tax token on BNB Chain?","Yes. Set your own buy and sell tax and a tax receiver. Taxes can be changed later or frozen forever by renouncing ownership."),
        ("Do I need BNB to create a token?","Yes, a small amount of BNB pays the network gas and the service fee shown before you sign.")]),
 "base": dict(name="Base", native="ETH", std="ERC-20", explorer="BaseScan", wallet="MetaMask, Coinbase Wallet or any EIP-1193 wallet",
   intro="Base is Coinbase's low-fee Ethereum Layer 2. DegenKit lets you create an ERC-20 or tax token on Base with no code, with the same one-form, one-signature flow as every other network.",
   when="Choose Base when you want Ethereum-grade security with cheap transactions and the Coinbase user base nearby.",
   faq=[("How do I create a token on Base without coding?","Open the Base launcher, connect your wallet (it will switch to Base), enter name, symbol and supply, and sign once."),
        ("Do I need ETH on Base?","Yes. Base uses ETH for gas, so bridge a small amount of ETH to Base first."),
        ("Can I create a tax token on Base?","Yes. The Tax Token view lets you set buy and sell taxes and a receiver wallet. Tax applies only to pool trades you mark.")]),
 "robinhood": dict(name="Robinhood Chain", native="ETH", std="ERC-20", explorer="the Robinhood Chain explorer", wallet="MetaMask or any EIP-1193 wallet",
   intro="Robinhood Chain is Robinhood's EVM network. DegenKit lets you create a fixed-supply or tax token there with no code, signed from your own wallet in a single transaction.",
   when="Choose Robinhood Chain if you want to be early on a new network and build for its audience.",
   faq=[("How do I create a token on Robinhood Chain?","Open the Robinhood Chain launcher, connect your wallet so it switches to the network, enter name, symbol and supply, and sign one transaction."),
        ("Is the token supply fixed?","Yes. The contract has no mint function, so the supply you choose is final for everyone, including DegenKit."),
        ("Can I add a tax?","Yes, the Tax Token view lets you set buy and sell tax rates and a receiver wallet.")]),
 "solana": dict(name="Solana", native="SOL", std="SPL", explorer="Solscan", wallet="Phantom, Solflare, Backpack or MetaMask",
   intro="Solana is the fastest, cheapest place to launch a token. DegenKit creates an SPL token in one signature with mint and freeze authority revoked and metadata locked, then gives you Swap, Create/Remove Liquidity, Airdrop, Multisender and Scanner in the same app.",
   when="Choose Solana for near-instant launches, tiny network fees and the largest memecoin trading crowd.",
   steps=[("Connect your Solana wallet","Open the Solana launcher and connect Phantom, Solflare, Backpack or MetaMask's Solana wallet. Use Devnet first if you want to rehearse for free."),
          ("Enter name, symbol, decimals and supply","Upload an image and a short description. This metadata is locked at creation."),
          ("Review the fee and sign once","The 0.28 SOL service fee plus the network fee are included in one transaction. Mint and freeze authority are revoked automatically."),
          ("Create a liquidity pool","Use Create Liquidity to open a Raydium pool with your token and SOL or USDC, set the starting price, and sign."),
          ("Share and grow","Use Airdrop and Multisender for distribution, and Scanner to check holders.")],
   faq=[("How do I create a Solana token without coding?","Connect your wallet, fill in name, symbol, decimals, supply and image, and sign one transaction. Mint and freeze authority are revoked and metadata is locked automatically."),
        ("How much does it cost to create a Solana token on DegenKit?","A 0.28 SOL service fee plus the standard Solana network fee, both in the single transaction you sign."),
        ("Can I add liquidity on Raydium from DegenKit?","Yes. Create Liquidity opens a Raydium CPMM pool and Remove Liquidity withdraws it, all signed from your own wallet.")]),
}

def build(slug, c):
    steps = c.get("steps") or EVM_STEPS(c["name"], c["native"], c["wallet"], c["explorer"])
    faq = c["faq"]
    ol = "".join(f"<li><strong>{E(t)}</strong><br>{E(d)}</li>" for t, d in steps)
    qa = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    others = "".join(f'<a href="/launch/{s}/">{E(v["name"])}</a>' for s, v in CHAINS.items() if s != slug)
    sec = f'''<!-- dk-guide:start -->
<section class="dk-guide" aria-labelledby="dkg-h">
<h2 id="dkg-h">How to create a {E(c["name"])} token with DegenKit</h2>
<p>{E(c["intro"])}</p>
<p>{E(c["when"])}</p>
<ol>{ol}</ol>
<h3>{E(c["name"])} token creator FAQ</h3>
{qa}
<p class="dk-guide-more">Launching elsewhere? {others}</p>
</section>
<!-- dk-guide:end -->'''
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    ldtag = '<!-- dk-guide-ld --><script type="application/ld+json">%s</script><!-- /dk-guide-ld -->' % json.dumps(ld, ensure_ascii=False, separators=(",",":")).replace("</","<\\/")
    return sec, ldtag

for slug, c in CHAINS.items():
    p = ROOT / "launch" / slug / "index.html"
    h = p.read_text(encoding="utf-8")
    h = re.sub(r"<!-- dk-guide:start -->.*?<!-- dk-guide:end -->\n?", "", h, flags=re.S)
    h = re.sub(r"<!-- dk-guide-ld -->.*?<!-- /dk-guide-ld -->\n?", "", h, flags=re.S)
    sec, ldtag = build(slug, c)
    h, n = re.subn(r"(</main>\s*</div>\n)", lambda m: m.group(1) + sec + "\n", h, count=1)
    assert n == 1, slug
    h = h.replace("</head>", ldtag + "\n</head>", 1)
    p.write_text(h, encoding="utf-8")
    print("ok", slug)

css = """
/* dk-guide */
.dk-guide{max-width:860px;margin:48px auto 40px;padding:0 clamp(20px,3vw,40px);color:var(--ink);line-height:1.65;position:relative;z-index:1}
.dk-guide h2{font-size:clamp(22px,3vw,30px);margin:0 0 12px}
.dk-guide h3{font-size:18px;margin:28px 0 10px}
.dk-guide p{color:var(--muted);margin:0 0 12px}
.dk-guide ol{padding-left:22px;color:var(--muted)}
.dk-guide li{margin:0 0 12px}.dk-guide li strong{color:var(--ink)}
.dk-guide details{border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:12px 16px;margin:0 0 10px}
.dk-guide summary{cursor:pointer;font-weight:600;color:var(--ink)}
.dk-guide details p{margin:10px 0 0}
.dk-guide-more a{margin-left:10px;color:var(--ink);text-decoration:underline}
"""
f = ROOT / "assets/dk-ui.css"; t = f.read_text(encoding="utf-8")
t = re.sub(r"\n/\* dk-guide \*/.*?(?=\Z)", "", t, flags=re.S) if "/* dk-guide */" in t else t
f.write_text(t + css, encoding="utf-8")
