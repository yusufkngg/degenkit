---
title: 'DegenKit Fees Explained: Every Tool, Every Network'
slug: degenkit-fees-explained
date: '2026-10-31'
excerpt: A plain list of DegenKit's service fees on Solana and EVM networks, how they are charged, and how they differ from network fees, rent and DEX fees.
cover: /blog/img/degenkit-fees-explained-cover.webp
cover_alt: A fee table listing DegenKit's Solana tools and their service fees in SOL.
tags:
- DegenKit
- Fees
- Guide
---

DegenKit charges a service fee on some tools. It is always shown before you sign. This page lists every fee in one place and explains what else you pay that doesn't go to DegenKit.

Fees can change. The amount shown in the tool when you sign is the one that applies.

## Solana tools

All Solana fees are in SOL.

- **Token Creator:** 0.28 SOL. Wallets on DegenKit's free list pay no service fee for token creation.
- **Authorities:** 0.05 SOL to revoke mint authority, 0.05 SOL to revoke freeze authority.
- **Update Metadata:** 0.05 SOL.
- **Burn Token:** 0.02 SOL.
- **Airdrop:** 0.02 SOL per batch. Each batch sends to up to 8 wallets.
- **Multisender:** 0.02 SOL per batch, up to 8 wallets per batch.
- **Swap:** 0.01 SOL.
- **Create Liquidity:** 0.05 SOL, plus Raydium's own pool creation fee, shown as about 0.15 SOL.
- **Remove Liquidity:** 0.02 SOL.
- **Scanner** and **Vanity Address:** no service fee.

![DegenKit's Solana service fees by tool, with the tools that have no fee.](/blog/img/degenkit-fees-explained-1.webp "Fees as listed in the Solana launcher in October 2026. The tool shows the current amount before you sign.")

## Ethereum, BNB Chain, Base and Robinhood Chain

On EVM networks, DegenKit has two creators: **Token Creator** and **Tax Token**. Each has a service fee stored in its factory contract. DegenKit reads it from the contract and shows it on the form before you sign. You pay it in the network's native token (ETH or BNB), in the same transaction that creates the token.

Managing a tax token afterwards — changing rates, marking pools, changing the tax wallet, transferring or renouncing ownership — is a direct call to your token's contract. You pay only gas.

## How fees are charged

On Solana, the service fee is a transfer inside the same transaction as the action in most wallets. If the action fails, the fee isn't taken. With some wallets, such as Solflare, DegenKit collects the token creation fee in a second small transaction right after the token is created, to avoid wallet warnings.

On EVM networks, the fee is sent with the create call itself, so it succeeds or fails together with it.

![An action is chosen, the service fee is shown, the network fee appears in the wallet, and both are paid in one signed transaction.](/blog/img/degenkit-fees-explained-demo.mp4)

## What doesn't go to DegenKit

- **Network fees.** Solana's base and priority fees, or gas on EVM networks. See [Solana fees and rent](/blog/solana-fees-and-rent-explained/) and [Ethereum gas fees](/blog/ethereum-gas-fees-explained/).
- **Rent on Solana.** A deposit held in the new accounts, not a payment.
- **DEX fees.** Raydium's pool creation fee, and trading fees on any DEX.
- **Token taxes.** On a tax token, the tax goes to the tax wallet the creator chose.

![The four kinds of cost in a launch and who receives each one.](/blog/img/degenkit-fees-explained-2.webp "Only the service fee goes to DegenKit. Everything else goes to the network, the DEX or the token's tax wallet.")

:::tip Budget for the whole launch
Creating the token is one fee. Revoking, metadata, liquidity and airdrops each add their own. Add them up before you start.
:::

## Questions people ask

### Is there a subscription?

No. You pay per action, only when you use a tool.

### Do failed transactions cost a service fee?

When the fee is in the same transaction, no. You may still pay the network fee, which networks charge even for failures.

## Wrap up

DegenKit's fees are per action, shown before you sign and separate from network fees, rent and DEX fees. Check the amount in the tool, then [choose your network](https://degenkit.app/launch/) to start.
