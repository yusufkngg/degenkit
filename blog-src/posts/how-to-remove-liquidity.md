---
title: 'How to Remove Liquidity from a Raydium Pool (and What Buyers See)'
slug: how-to-remove-liquidity
date: '2026-10-30'
excerpt: Removing liquidity returns your share of a pool, which is rarely the same amounts you put in. Learn how it works, what comes back, how it changes trading and how to do it openly.
cover: /blog/img/how-to-remove-liquidity-cover.webp
cover_alt: A pool position card with a 50 percent removal selected and the estimated token and SOL amounts shown.
tags:
- Guide
- Liquidity
- Solana
---

Adding liquidity makes a token tradable. Removing it takes some or all of that market away again. It is a normal tool for adjusting a position, and also the action buyers watch most closely. This guide covers both sides.

## What removing liquidity does

When you added liquidity, the pool gave you **LP tokens**. They represent your share of the pool. [Raydium's documentation](https://docs.raydium.io/user-flows/choosing-a-pool-type) explains that to exit, you burn LP tokens and receive your proportional share of the pool's reserves, including the trading fees the pool has earned.

So you don't get back "your deposit". You get back your **share of whatever the pool holds now**.

## Why the amounts change

Trades change what a pool holds. If people bought your token, the pool now has fewer tokens and more SOL. If they sold, it has more tokens and less SOL.

A simple illustration: you created a pool with 100,000,000 tokens and 10 SOL and own all of it. After net buying, the pool holds 80,000,000 tokens and 12.5 SOL. Removing 100% returns about 80,000,000 tokens and 12.5 SOL, plus any fees, not the original amounts.

![A pool that started at 100M tokens and 10 SOL and, after net buying, returns 80M tokens and 12.5 SOL when fully withdrawn.](/blog/img/how-to-remove-liquidity-1.webp "Illustrative constant-product numbers. Trading fees add a little on top.")

## What buyers see

Removing liquidity makes the pool smaller, and that is visible to everyone.

- **Partial removal** leaves a thinner market. The same buy or sell moves the price more. In the example above, a 1 SOL buy into a 10 SOL pool has about 9.1% price impact. Remove a quarter of the pool and the same buy has about 11.8%.
- **Full removal** empties the pool. Nobody can trade the token there anymore, and scanners flag a missing pair. DegenKit's Scanner, for example, lowers the score when no pair is found.

Pulling all liquidity right after people bought is the classic rug-pull pattern. That is why buyers look for locked or burned LP tokens, and why unlocked liquidity is something to explain, not hide.

![What partial and full removal do to a pool's depth and to the price impact of a 1 SOL buy.](/blog/img/how-to-remove-liquidity-2.webp "Illustrative constant-product math, before fees. Thin pools make every trade move the price more.")

:::warning Locked means locked
If your LP tokens are locked or burned, you cannot remove that liquidity. That is the point of locking, so decide before you lock.
:::

## Removing liquidity on DegenKit

DegenKit's **Remove Liquidity** tool works with Raydium standard (CPMM) pools.

1. **Connect the wallet that holds the LP tokens.** The tool lists your Raydium pools with the estimated amounts on each side and your share of the pool. If a new pool isn't listed yet, paste its pool ID.
2. **Choose how much to remove:** 25%, 50%, 75% or 100% of your position.
3. **Set slippage tolerance:** 0.5%, 1% or 3%; 1% is selected by default. It protects you if the pool changes while your transaction confirms.
4. **Review and sign.** The tool shows what you should receive and a 0.02 SOL service fee. Withdrawn SOL arrives as regular SOL.

![Pools are found from the wallet's LP tokens, a percentage is chosen, the estimate and fee are reviewed, and tokens and SOL return to the wallet.](/blog/img/how-to-remove-liquidity-demo.mp4)

## Doing it openly

If you need to adjust liquidity, say so before you do it and share the transaction afterwards. Explain the reason, the amount and what you plan next, such as moving to a different pair or rebalancing. A clear note turns a scary on-chain event into a known one.

## Questions people ask

### Can I remove only part of my position?

Yes. Choose 25%, 50% or 75%, and the rest stays in the pool earning its share of fees.

### Do I need the LP tokens?

Yes. Only the wallet that holds the LP tokens can withdraw. If they are lost or locked, so is that liquidity.

## Wrap up

Removing liquidity burns LP tokens and returns your share of the pool as it stands now. It thins or empties the market, and buyers notice. Use it carefully, communicate first and publish the transaction. [Open Remove Liquidity on DegenKit](https://degenkit.app/launch/solana/) when you are ready.
