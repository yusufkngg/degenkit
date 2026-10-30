---
title: 'Slippage vs. Price Impact: Why Your Swap Got a Different Price'
slug: slippage-vs-price-impact
date: '2026-10-30'
excerpt: Price impact comes from your own trade moving the pool. Slippage comes from the market moving before your trade lands. Learn the difference and how to set a sensible tolerance.
cover: /blog/img/slippage-vs-price-impact-cover.webp
cover_alt: A swap card showing a quoted amount, a price impact line and a slippage tolerance selector.
tags:
- Guide
- Trading
- Liquidity
---

You ask for a quote, it says one number, and the tokens that arrive are a little fewer. Two different things can cause that, and they are often mixed up: **price impact** and **slippage**.

Knowing the difference helps you as a buyer, and it helps you as a creator decide how much liquidity a new token needs.

## Price impact: your trade moves the pool

[Jupiter's documentation](https://docs.jup.ag/guides/jupiter-swap/price-impact-slippage-price-warning) defines price impact as the change in an asset's price caused by your trade. When you buy from a pool, you add SOL and take tokens out. That changes the ratio, so each extra token costs a little more than the last.

The bigger your trade compared with the pool, the bigger the impact. It is known before you sign, and the quote already includes it.

## Slippage: the market moves before you land

Slippage, according to the same docs, happens when market conditions change between submitting a transaction and its confirmation. Other people can trade in that gap, and the price you get can be different from the one you were quoted.

To protect yourself, you set a **slippage tolerance**. If the final result would be worse than the quote by more than that percentage, the transaction fails instead of filling at a bad price. Jupiter's docs say it directly: if the price falls below the slippage rate, the transaction fails.

![Price impact is caused by your own trade size; slippage is caused by other trades landing first.](/blog/img/slippage-vs-price-impact-1.webp "Price impact is in the quote. Slippage tolerance protects you from what happens after it.")

## A worked example

Picture a pool with 100,000,000 tokens and 10 SOL. One token is quoted at 0.0000001 SOL, so 1 SOL "should" buy 10,000,000 tokens.

In a constant-product pool, before fees, a 1 SOL buy actually returns about 9,090,909 tokens. That is a price impact of about 9.1%, caused entirely by the trade's size. Smaller buys hurt less:

- 0.1 SOL → about 1.0% impact
- 0.5 SOL → about 4.8% impact
- 1 SOL → about 9.1% impact
- 2 SOL → about 16.7% impact

Now set a 1% slippage tolerance on that 1 SOL buy. If other trades land first and your result would drop more than 1% below 9,090,909 tokens, the swap fails and you keep your SOL.

![How much a buy of 0.1, 0.5, 1 and 2 SOL moves the price in a pool holding 10 SOL.](/blog/img/slippage-vs-price-impact-2.webp "Illustrative constant-product math, before fees. Deeper pools lower every number on this chart.")

![A swap is quoted, the price impact is shown, a slippage tolerance is chosen, and the trade either fills within it or fails.](/blog/img/slippage-vs-price-impact-demo.mp4)

## Swapping on DegenKit

DegenKit's **Swap** tool gets its quotes from Jupiter. You can choose a slippage tolerance of 0.5%, 1% or 3%; 0.5% is selected by default. Once a quote loads, the price impact is shown under it, and impacts above 3% are highlighted. A small service fee is shown before you sign.

:::tip Set tolerance on purpose
A very low tolerance can make swaps fail on busy tokens. A very high one lets you fill at a much worse price. Start low and raise it only if you understand why trades are failing.
:::

## What this means for creators

Price impact is mostly a liquidity question. If your pool is thin, even small buys move the price a lot, and the chart looks jumpy. Adding more to both sides of the pool lowers price impact for everyone. Keep in mind that the starting price comes from the ratio, not the size, so a deeper pool does not need to change your price.

## Questions people ask

### Why did my swap fail?

Often because the market moved more than your slippage tolerance allowed while the transaction was confirming. Request a fresh quote and try again, or raise the tolerance slightly if the token is very active.

### Is high price impact a warning sign?

It means the pool is small compared with your trade. That is not proof of anything bad, but it tells you selling later could be just as costly.

## Wrap up

Price impact is caused by your trade and is shown in the quote. Slippage is caused by the market and is limited by your tolerance. Watch both, and as a creator, give your pool enough depth that ordinary trades don't move it too far. [Open Swap on DegenKit](https://degenkit.app/launch/solana/) to see both numbers before you sign.
