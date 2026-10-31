---
title: 'What Is DegenKit? Every Tool on Every Network'
slug: what-is-degenkit
date: '2026-10-31'
excerpt: DegenKit is a no-code, non-custodial token launcher for Solana, Ethereum, BNB Chain, Base and Robinhood Chain. Here is what it does, which tools each network has and how they fit together.
cover: /blog/img/what-is-degenkit-cover.webp
cover_alt: The DegenKit launcher with five network cards and a grid of its token tools.
tags:
- DegenKit
- Guide
- Token Launch
---

DegenKit is a no-code token launcher. You fill in a form, sign a transaction from your own wallet, and a token exists on-chain. There is no account to create and no code to write.

It works on five networks: **Solana**, **Ethereum**, **BNB Chain**, **Base** and **Robinhood Chain**. DegenKit never holds your keys or funds; every action is a transaction you sign yourself.

## On Solana: a full toolkit

The [Solana launcher](https://degenkit.app/launch/solana/) has the most tools, covering a token from creation to trading.

**Create**

- **Token Creator** — an SPL token in one transaction, with name, symbol, decimals, supply, image and description. Mint and freeze authority are revoked by default and metadata is locked.
- **Vanity Address** — generates an address that starts with text you choose, in your browser.

**Manage**

- **My Tokens** — the tokens your wallet created.
- **Authorities** — revoke mint or freeze authority on a token you control.
- **Update Metadata** — change name, symbol or image where metadata is still editable.
- **Burn Token** — permanently remove tokens from your wallet.

**Distribute**

- **Airdrop** — the same amount to many wallets.
- **Multisender** — different amounts to many wallets, from a list.

**Trade and check**

- **Swap** — swaps through Jupiter quotes.
- **Create Liquidity** and **Remove Liquidity** — open and withdraw Raydium pools.
- **Scanner** — a risk check: authorities, metadata, top holders and trading pair.

![DegenKit's Solana tools grouped by stage: create, manage, distribute, and trade and check.](/blog/img/what-is-degenkit-1.webp "Every tool works from your own wallet. Most have a small service fee shown before you sign.")

## On EVM networks: create and manage

On [Ethereum](https://degenkit.app/launch/ethereum/), [BNB Chain](https://degenkit.app/launch/bnb/), [Base](https://degenkit.app/launch/base/) and [Robinhood Chain](https://degenkit.app/launch/robinhood/), DegenKit offers:

- **Token Creator** — a fixed-supply token with 18 decimals and no mint function.
- **Tax Token** — the same, plus buy and sell taxes you set.
- **My Tokens** — your tokens, and for tax tokens the **Manage tax** controls: rates, pools, tax wallet, transfer and renounce ownership.

Liquidity on these networks is added on a DEX such as Uniswap or PancakeSwap.

![A creator picks a network, creates a token, manages it in My Tokens and moves on to liquidity and distribution.](/blog/img/what-is-degenkit-demo.mp4)

## How it fits together

A typical Solana launch on DegenKit:

1. Create the token, with authorities revoked and metadata locked.
2. Create a Raydium pool with SOL or USDC.
3. Distribute with Airdrop or Multisender if you planned to.
4. Check the result in Scanner, the same way buyers will.

On EVM networks: create, add liquidity on a DEX, and for a tax token mark the pool in Manage tax.

![The networks DegenKit supports and the tools available on each.](/blog/img/what-is-degenkit-2.webp "Solana has the full toolkit. EVM networks focus on creating and managing tokens.")

:::note Learn as you go
The [DegenKit blog](https://degenkit.app/blog/) has a guide for almost every step, from [fees](/blog/degenkit-fees-explained/) to [what makes the tool safe to use](/blog/is-degenkit-safe/).
:::

## Questions people ask

### Do I need an account?

No. You connect a wallet. There is nothing to sign up for.

### Can I rehearse first?

On Solana, yes. The launcher supports Devnet, where test SOL costs nothing.

## Wrap up

DegenKit turns token creation into a form and a signature, on five networks. Solana gets the full toolkit; EVM networks get creation and tax management. [Choose a network](https://degenkit.app/launch/) to start.
