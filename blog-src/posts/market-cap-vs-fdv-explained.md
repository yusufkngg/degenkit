---
title: 'Price, Market Cap and FDV: What the Numbers on a Token Page Mean'
slug: market-cap-vs-fdv-explained
date: '2026-10-30'
excerpt: Price, market cap and fully diluted valuation are calculated from the same few inputs, yet they answer different questions. Learn how each is worked out and what none of them tells you.
cover: /blog/img/market-cap-vs-fdv-explained-cover.webp
cover_alt: A token page showing price, market cap and FDV side by side, with the pool's liquidity shown separately below.
tags:
- Guide
- Tokenomics
- Liquidity
---

Open any token on a chart site and three numbers sit near the top: price, market cap and FDV. They look like three separate facts. In reality they come from the same inputs, and the difference between them is usually a question about supply.

This guide explains how each number is calculated, why they sometimes match, and why none of them is the amount of money you could actually take out of the market.

## Price comes from the pool

For a new token, price is set by its liquidity pool. When you create a pool, the ratio of the two sides sets the starting price. Deposit 100,000,000 tokens and 10 SOL, and one token starts at 0.0000001 SOL.

After that, every trade changes the ratio, and with it the price. If you want the full mechanics, read [creating a token vs. adding liquidity](/blog/creating-a-token-vs-adding-liquidity/).

## Market cap and FDV are price times supply

[CoinGecko's explainer](https://www.coingecko.com/learn/what-is-fully-diluted-valuation-fdv-in-crypto) gives the two formulas:

- **Market cap** = price × circulating supply
- **Fully diluted valuation (FDV)** = price × total supply

The only difference is which supply you multiply by. Circulating supply is what is currently in circulation. Total supply also counts tokens that exist but are still pending distribution, such as team allocations or vesting, and leaves out burned tokens.

![The three numbers on a token page and how each one is calculated from price and supply.](/blog/img/market-cap-vs-fdv-explained-1.webp "Same price, different supply. When everything circulates, market cap and FDV are the same number.")

## When they match, and when they don't

If every token is already circulating and tradable, the two numbers are the same. Many simple launches look like this.

They split apart when part of the supply is locked, vesting or held back for later. CoinGecko notes that market cap does not account for vested tokens, while FDV hints at the value if they all arrive. A big gap means more supply is still to come, and the price per token can drop if demand does not grow with it.

:::note How DegenKit shows it
When you add liquidity, DegenKit's **Create Liquidity** tool shows a starting price and a **starting market cap**. That figure is your token's total supply multiplied by the starting price, in SOL or USDC. It treats the whole supply as if it were circulating.
:::

![Price comes from the pool ratio, market cap and FDV multiply it by supply, and liquidity shows how much can actually be traded.](/blog/img/market-cap-vs-fdv-explained-demo.mp4)

## Market cap is not money in the pool

This is the most common misunderstanding. Market cap multiplies the last price by every token. It does not mean anyone could sell all those tokens at that price.

Take the example above. The supply is 1,000,000,000 tokens and the price is 0.0000001 SOL, so the market cap is 100 SOL. But the pool only holds 10 SOL. If someone sold 100,000,000 tokens (10% of the supply) into that pool, they would receive about 5 SOL, not 10 SOL. The price would fall by about 75% in one trade.

What makes trading stable is **liquidity**, the amount sitting in the pool. Compare it with the market cap, not the other way round.

![A 100 SOL market cap next to a 10 SOL pool, showing that selling 10% of the supply returns about 5 SOL and drops the price about 75%.](/blog/img/market-cap-vs-fdv-explained-2.webp "Illustrative constant-product math, before fees. Real pools also charge a trading fee.")

## Why the creator's wallet matters

On DegenKit, the whole supply goes to your wallet when the token is created. Until you distribute it, those tokens count in total supply, and they also count in a market cap calculated the simple way.

Chart sites can only adjust for this if they know which wallets hold locked supply. [DEX Screener's Enhanced Token Info](https://marketplace.dexscreener.com/product/token-info), for example, lets projects designate such wallets so the market cap displays correctly. Publishing your allocations also helps buyers check the numbers themselves.

## Questions people ask

### Is a low market cap a good sign?

Not on its own. A low market cap with very thin liquidity can move sharply in either direction. Look at liquidity, holder spread and supply plans together.

### Can market cap change without any trades?

Yes, if the token is paired with SOL. The token's price in SOL stays put, but its dollar value follows SOL. Our guide on [choosing SOL or USDC for your pool](/blog/sol-or-usdc-liquidity-pair/) explains this.

## Wrap up

Price comes from the pool. Market cap and FDV multiply that price by supply: circulating for market cap, total for FDV. None of them shows how much could really be sold, which is why liquidity matters most. [Open Create Liquidity on DegenKit](https://degenkit.app/launch/solana/) to see the starting price and market cap before you sign.
