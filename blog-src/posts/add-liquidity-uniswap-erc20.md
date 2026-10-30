---
title: 'How to Add Liquidity for a New Token on Uniswap'
slug: add-liquidity-uniswap-erc20
date: '2026-10-30'
excerpt: Your ERC-20 needs a pool before anyone can trade it. Learn how to create one on Uniswap on Ethereum or Robinhood Chain, which version fits a tax token, and what you receive.
cover: /blog/img/add-liquidity-uniswap-erc20-cover.webp
cover_alt: A Uniswap-style new position screen pairing a new token with ETH, with the resulting pool card beside it.
tags:
- Guide
- Liquidity
- Ethereum
---

Creating an ERC-20 gives you a supply in your wallet. To make it tradable, you need a liquidity pool. On Ethereum and on Robinhood Chain, the usual place is **Uniswap**. DegenKit does not create EVM pools itself; you add liquidity on the DEX, then come back to DegenKit if you have a tax token.

If the idea of a pool is new, start with [creating a token vs. adding liquidity](/blog/creating-a-token-vs-adding-liquidity/).

## Which Uniswap version?

Uniswap has several versions, and the web app lets you pick one when you start a position.

- **v2** pools hold both tokens across the full price range. You receive **UNI-V2 tokens** that represent your share. Each pair has its own contract address.
- **v3 and v4** let you choose a fee tier and a price range, and you receive an **NFT** that represents your position. If the price moves outside a custom range, the position stops earning fees.

For a plain token from DegenKit, any version works. For a **tax token**, the choice matters. [Uniswap's v3 documentation](https://developers.uniswap.org/docs/protocols/v3/concepts/unsupported-tokens) says fee-on-transfer tokens will not function with its router contracts. Uniswap v2's [troubleshooting guide](https://developers.uniswap.org/docs/protocols/v2/guides/troubleshooting) points to router functions built to support fee-on-transfer tokens.

![Uniswap v2 versus v3 and v4: what you receive, price range, fee tiers and which suits a tax token.](/blog/img/add-liquidity-uniswap-erc20-1.webp "For a tax token, a v2 pair is the safer choice. Plain tokens work with any version.")

## Step by step (v2)

[Uniswap's support guide](https://support.uniswap.org/hc/en-us/articles/20915582427917) lists the steps:

1. Open the Uniswap app, connect your wallet and make sure it is on the right network.
2. Go to **Pool**, start a new position and choose the **v2** option in the version menu.
3. Select your token and ETH (or another pair token). Paste your contract address if your token isn't listed.
4. Enter both amounts. In a new pool, the ratio of the two sets the starting price.
5. **Approve** Uniswap to use your token. This is a separate transaction with its own gas.
6. **Confirm** the position. UNI-V2 tokens arrive in your wallet.

:::warning Check the starting price
Deposit 100,000,000 tokens with 1 ETH and one token starts at 0.00000001 ETH. A wrong number of zeros gives a very different price, and the first trades will follow it.
:::

![A new position is opened, the token and ETH are chosen, both amounts set the starting price, the approval and deposit are signed, and LP tokens arrive.](/blog/img/add-liquidity-uniswap-erc20-demo.mp4)

## Tax tokens: mark the pool

A DegenKit tax token only charges tax on trades against pools you mark. After adding liquidity:

1. Open your liquidity transaction on the explorer and copy the **pair address**.
2. On DegenKit, go to **My Tokens → Manage tax**.
3. Paste the address and choose **Mark as pool**.

Until you do this, no tax is applied. Use the pair contract, not the router or your own wallet.

![The order of steps for a tax token: create, add a v2 pool, copy the pair address, mark it, then taxes apply.](/blog/img/add-liquidity-uniswap-erc20-2.webp "Taxes start only after the pool is marked in My Tokens → Manage tax.")

## What you hold afterwards

Your UNI-V2 tokens (or position NFT) are what let you withdraw the liquidity later. Whoever holds them controls that liquidity. Buyers will ask whether it is locked or burned, so decide in advance and publish the transaction that proves it.

## Questions people ask

### Can I add liquidity on Robinhood Chain the same way?

Yes. Uniswap was available on Robinhood Chain from launch. Switch your wallet to Robinhood Chain first and make sure you have ETH there for gas.

### How much should I add?

Only what you can afford to leave in the pool. A thin pool makes every trade move the price a lot.

## Wrap up

Create the token on DegenKit, open a Uniswap pool with your token and ETH, approve and confirm, and keep the LP tokens safe. For a tax token, use a v2 pair and mark it in My Tokens. Start from the [Ethereum](https://degenkit.app/launch/ethereum/) or [Robinhood Chain](https://degenkit.app/launch/robinhood/) launcher.
