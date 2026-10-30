---
title: 'Ethereum Gas Fees Explained for Token Creators'
slug: ethereum-gas-fees-explained
date: '2026-10-30'
excerpt: Gas, gwei, base fee and priority fee decide what a transaction costs on Ethereum. Learn how the fee is calculated, why it changes and how to read your wallet's estimate.
cover: /blog/img/ethereum-gas-fees-explained-cover.webp
cover_alt: A wallet confirmation screen breaking an Ethereum network fee into gas used, base fee and priority fee.
tags:
- Guide
- Ethereum
- Fees
---

Every transaction on Ethereum pays a network fee, called **gas**. For a token creator, gas is part of the cost of creating the token, adding liquidity, setting approvals and managing a tax token. It is also the part that changes the most.

This guide explains where the number in your wallet comes from.

## Gas is a unit of work

[Ethereum's documentation](https://ethereum.org/developers/docs/gas/) describes gas as the unit that measures the computational effort an operation needs. Simple actions use little gas. A plain ETH transfer uses exactly 21,000 gas. Creating a contract or adding liquidity uses much more.

The **price** of each unit of gas is quoted in **gwei**. One gwei is one-billionth of an ETH.

## The fee formula

Ethereum's docs give the formula:

**fee = gas used × (base fee + priority fee)**

- **Base fee** is set by the network for each block. It rises when blocks are busy and falls when they are quiet, by up to 12.5% per block. The base fee is burned, not paid to anyone.
- **Priority fee**, or tip, goes to the validator and encourages them to include your transaction.

Your wallet also sets a **max fee**. If the actual base fee plus tip comes in lower, you are refunded the difference.

![How an Ethereum fee is built: gas used multiplied by the base fee plus the priority fee, with the base fee burned.](/blog/img/ethereum-gas-fees-explained-1.webp "Gas used depends on what you do. The price per gas depends on how busy the network is.")

## A worked example

Suppose a contract interaction uses 500,000 gas. The numbers below are illustrative.

- At **2 gwei** (base fee plus tip), the fee is 500,000 × 2 gwei = 1,000,000 gwei = **0.001 ETH**.
- At **20 gwei**, the same action costs **0.01 ETH**.
- At **60 gwei**, it costs **0.03 ETH**.

Same action, thirty times the cost. The only difference is how busy Ethereum was.

![The same 500,000-gas transaction at 2, 20 and 60 gwei, showing how the fee scales.](/blog/img/ethereum-gas-fees-explained-2.webp "Illustrative numbers. Your wallet shows the live estimate before you sign.")

## Why your fee changes before you sign

Because the base fee moves with every block, the estimate in your wallet can change while you look at it. That is normal. A higher max fee gives your transaction more room if the base fee rises; you only pay what is actually needed, up to that max.

![A transaction's gas use is estimated, the base fee moves with network demand, a tip is added and the final fee is paid with the unused part refunded.](/blog/img/ethereum-gas-fees-explained-demo.mp4)

## Gas in a token launch

A typical Ethereum launch involves several transactions, each with its own gas:

1. **Creating the token.** One transaction. DegenKit also shows its own service fee before you sign; that is separate from gas.
2. **Approving the DEX** to use your tokens when you add liquidity.
3. **Adding liquidity.**
4. For a tax token, **marking the pool** and any later changes to rates or ownership.

:::tip Plan for more than one transaction
Keep enough ETH for the whole sequence, not just the first step. Running out halfway leaves a token without a pool.
:::

## Questions people ask

### Can I make a transaction cheaper?

You can wait for a quieter time, since the base fee falls when blocks are less full. Lowering the max fee too far only makes the transaction wait or fail.

### Why do Layer 2 networks cost less?

Networks such as Robinhood Chain process transactions on their own chain and settle to Ethereum in batches, so each transaction pays much less. Our comparison of [Ethereum and Robinhood Chain](/blog/ethereum-vs-robinhood-chain/) explains the trade-offs.

## Wrap up

An Ethereum fee is gas used multiplied by the base fee plus a tip. Gas used depends on the action; the price depends on how busy the network is. Check the estimate in your wallet, keep ETH for every step, and [open the Ethereum launcher](https://degenkit.app/launch/ethereum/) when the timing suits you.
