---
title: 'Token Approvals Explained: What You Allow and How to Revoke It'
slug: erc20-token-approvals-explained
date: '2026-10-30'
excerpt: Before a DEX can move your ERC-20 tokens, you approve it. Learn what an approval is, why unlimited approvals carry risk, and how to check and revoke them.
cover: /blog/img/erc20-token-approvals-explained-cover.webp
cover_alt: A wallet approval request showing a spender, a token and an allowance amount, next to a list of approvals with a revoke button.
tags:
- Guide
- Safety
- Ethereum
---

The first time you sell a token on a DEX or add it to a pool, your wallet asks for an **approval**. It looks like a formality. It is actually a permission that stays in place after the trade, and it is worth understanding.

## What an approval is

The [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20) defines three pieces:

- **approve** lets a *spender* (a contract or address) withdraw your tokens, multiple times, up to an amount you set.
- **allowance** returns how much that spender may still withdraw.
- **transferFrom** is what the spender calls to move tokens on your behalf.

A DEX router can't take your tokens without this. That is why adding liquidity on Uniswap asks you to approve first, then confirm. [Uniswap's v2 guide](https://support.uniswap.org/hc/en-us/articles/20915582427917) notes the approval is its own step with its own network cost.

![How an ERC-20 approval works: you approve a spender, the allowance is stored, and the spender can later move tokens up to that amount.](/blog/img/erc20-token-approvals-explained-1.webp "An approval is per token, per spender, per network. It stays until it's used up or changed.")

## Exact vs. unlimited

Many apps ask for an unlimited allowance so you don't have to approve again. That's convenient, but the permission stays open. If that contract is later exploited, or the approval was given to a malicious site, tokens up to the allowance can be taken without another prompt from you.

An exact approval covers only what you are about to do. It costs one extra approval next time.

:::warning Read the spender
Before approving, check the spender's address and the amount in your wallet. A site you don't recognize asking to approve your tokens is a red flag.
:::

![A wallet shows an approval request, an exact amount is chosen, the trade uses it, and later an old unlimited approval is found and revoked.](/blog/img/erc20-token-approvals-explained-demo.mp4)

## How to check and revoke

On Ethereum, [Etherscan's Token Approval Checker](https://etherscan.io/TOKENAPPROVALCHECKER) lists the contracts approved to spend your tokens and how much is at risk. Connect your wallet, select the approvals you no longer need and choose **Revoke Selected**.

A few facts to keep in mind:

- **Revoking costs gas.** [OpenSea's help article](https://support.opensea.io/en/articles/8867133-how-can-i-revoke-token-approvals-and-permissions-on-ethereum) notes that both approving and revoking require a network fee.
- **Revoking sets the allowance to zero.** It does not move any tokens.
- **Approvals are per network.** An approval on Ethereum is separate from one on Robinhood Chain. Use a tool that supports the network you are checking.

![A short routine for approvals: approve exact amounts, review the spender, check regularly and revoke what you no longer use.](/blog/img/erc20-token-approvals-explained-2.webp "Four habits that limit what any single approval can cost you.")

## For token creators

Creating a token on DegenKit is a single transaction to the factory; it doesn't need an approval. Approvals come later, when you add liquidity or move tokens through other apps. After your launch setup is done, it is worth reviewing what you approved from the creator wallet, since it usually holds a large share of the supply.

## Questions people ask

### Does revoking cancel a past trade?

No. It only stops future transfers by that spender.

### Why does my wallet sometimes ask me to sign instead of approve?

Some apps use signed permits. Uniswap v4, for example, asks for a Permit2 signature with no network cost alongside a normal approval. Read what you are signing as carefully as an approval.

## Wrap up

An approval lets a contract move your tokens up to an allowance, and it stays until used or revoked. Prefer exact amounts, check the spender, and revoke what you no longer use. Then [create your token on Ethereum](https://degenkit.app/launch/ethereum/) or [Robinhood Chain](https://degenkit.app/launch/robinhood/) with a clean setup.
