# DegenKit

No-code Solana token creator and toolkit. Create, manage, burn, airdrop, and swap tokens — one signature at a time, with mint and freeze authority revoked by default.

🌐 [degenkit.app](https://degenkit.app)
🐦 [@DegenKitApp](https://x.com/DegenKitApp)
✉️ [support@degenkit.app](mailto:support@degenkit.app)

## What's here

This repo contains the DegenKit website and web app — a static, client-side site with no backend server. Every on-chain action (creating a token, revoking an authority, burning, swapping) is a transaction built in the browser and signed directly by the user's own wallet. DegenKit never holds funds or private keys.

```
/                     Marketing homepage
/launch/              Network selector
/launch/solana/       The Solana token toolkit (Token Creator, My Tokens,
                       Authorities, Update Metadata, Burn, Tax Token,
                       Airdrop, Multisender, Scanner, Vanity Address, Swap)
/launch/robinhood/    Robinhood Chain — coming soon
/blog/                Blog
/terms/, /privacy/    Legal pages
/support/             Support / contact
/assets/              Shared logo, favicon, and stylesheet
```

## Stack

Plain HTML/CSS/JS — no build step, no framework. On-chain interaction uses:
- [`@solana/web3.js`](https://github.com/solana-labs/solana-web3.js) and [`@solana/spl-token`](https://github.com/solana-labs/solana-program-library) (loaded from a CDN)
- The [Wallet Standard](https://github.com/wallet-standard/wallet-standard) for multi-wallet support (Phantom, Solflare, Backpack, MetaMask, and others)
- [Jupiter's](https://station.jup.ag/docs/apis/swap-api) aggregator API for the Swap tool
- [Supabase](https://supabase.com) for admin-only usage logs and configurable fees
- [Pinata](https://pinata.cloud) for token image/metadata storage on IPFS

## Running locally

There's no build step — clone the repo and open `index.html`, or serve the folder with any static file server:

```bash
npx serve .
```

## Security

If you find a security issue, please email [support@degenkit.app](mailto:support@degenkit.app) rather than opening a public issue.

## License

See [LICENSE](./LICENSE).
