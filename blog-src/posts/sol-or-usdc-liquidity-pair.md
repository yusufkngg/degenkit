---
title: 'SOL or USDC: Choosing the Pair for Your Liquidity Pool'
slug: sol-or-usdc-liquidity-pair
date: '2026-10-30'
excerpt: Your token's pool pairs it with either SOL or USDC. That choice decides what your price is measured in, what buyers need, and how the dollar value moves. Here is how to choose.
cover: /blog/img/sol-or-usdc-liquidity-pair-cover.webp
cover_alt: Two pool cards side by side, one pairing a token with SOL and the other with USDC.
tags:
- Guide
- Liquidity
- Solana
---

When you create a liquidity pool, you put your token on one side and something people already value on the other. On Solana, that is usually **SOL** or **USDC**. Both work. They behave differently, and the choice is permanent for that pool.

## What each one is

**SOL** is Solana's native token. It pays every network fee, and most traders on Solana already hold it.

**USDC** is a stablecoin. [Circle](https://www.circle.com/multi-chain-usdc/solana) describes it as a digital dollar, fully reserved and redeemable 1:1 for US dollars. Its official Solana mint address is `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`.

:::warning Check the mint, not the name
Anyone can create a token called "USDC". When you pair with USDC, the address must be the official one above. DegenKit's USDC option uses that mint.
:::

## The price is measured in whatever you pair with

Your pool's ratio sets the price in the paired asset. Pair 100,000,000 tokens with 10 SOL and the price is 0.0000001 SOL. Pair them with 1,500 USDC and the price is 0.000015 USDC.

That has one big consequence for the dollar value.

- In a **SOL pool**, your token's price in SOL changes only when people trade it. But its dollar value also follows SOL. If SOL rises 20% against the dollar, your token's dollar price rises about 20%, with no trades at all. If SOL falls, it falls too.
- In a **USDC pool**, the price is already in dollars. Without trades, it stays where it is.

![What changes when you pair with SOL versus USDC: price unit, what buyers need, dollar exposure and fees.](/blog/img/sol-or-usdc-liquidity-pair-1.webp "Both pairs work. The difference is what your price is measured in.")

![If SOL rises 20% against the dollar, a SOL-paired token's dollar price rises with it while a USDC-paired one stays flat.](/blog/img/sol-or-usdc-liquidity-pair-2.webp "Illustrative numbers. A SOL pair carries SOL's own price movements on top of your token's.")

## How to choose

**Pair with SOL if:**

- Your buyers are mostly Solana traders who already hold SOL.
- You are comfortable with your dollar value moving with SOL.
- You want the most familiar setup for new tokens.

**Pair with USDC if:**

- You want a price that reads in dollars and doesn't drift with SOL.
- Your audience is more likely to hold stablecoins.
- You already hold USDC for the deposit.

Buyers who hold the other asset can still trade. Swap aggregators such as Jupiter look for routes across pools, so someone with USDC can often reach a SOL pool and the other way round. Every extra hop can add a little cost, though.

![A pair is chosen, both amounts are entered, the starting price appears in that unit, and the fees are shown in SOL.](/blog/img/sol-or-usdc-liquidity-pair-demo.mp4)

## Creating the pool on DegenKit

In **Create Liquidity**, choose your token, then pick **SOL** or **USDC** under "Pair with". Enter both amounts. DegenKit shows the starting price and starting market cap in the unit you picked.

Two details are worth knowing:

- **Fees are always paid in SOL.** Raydium's pool creation fee and DegenKit's service fee come out in SOL even for a USDC pool, so keep some SOL in your wallet.
- **USDC is mainnet only.** On Devnet, where you can rehearse for free, the USDC option is hidden and pools pair with SOL.

## Questions people ask

### Can I switch the pair later?

Not for the same pool. You would have to remove liquidity from it and create a new pool with the other asset. Buyers will see that as a big change, so explain it publicly first. Our guide on [removing liquidity](/blog/how-to-remove-liquidity/) covers what they see.

### Does USDC remove all risk?

No. It only removes SOL's price movement from your token's dollar value. Your own token can still move a lot with every trade.

## Wrap up

SOL pairs are familiar and follow SOL's dollar price. USDC pairs read in dollars and hold steady without trades. Choose based on your audience and how you want your price to behave, and keep SOL for fees either way. [Open Create Liquidity on DegenKit](https://degenkit.app/launch/solana/) when your amounts are ready.
