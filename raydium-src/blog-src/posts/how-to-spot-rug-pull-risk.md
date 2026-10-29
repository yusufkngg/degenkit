---
title: How to Spot Rug-Pull Risk Before You Buy a Token
slug: how-to-spot-rug-pull-risk
date: '2026-10-25'
excerpt: Learn which on-chain signals point to rug-pull risk — authorities, metadata, holder concentration and liquidity — and what a scanner can and cannot tell you.
cover: /blog/img/how-to-spot-rug-pull-risk-cover.webp
cover_alt: A token scanner card shows a risk score ring next to mint, freeze, metadata and holder checks.
tags:
- Guide
- Safety
- Solana
---

A rug pull happens when the people behind a token take value out of it at the holders' expense. They might drain the liquidity pool, mint new supply and sell it, or stop holders from moving their tokens. No single check proves that a token is safe. Several on-chain signals, however, make some of these moves easier or harder.

This guide focuses on Solana tokens and the checks that DegenKit's Scanner runs. The goal is to read a token's state before you buy, not to predict its price.

## What a rug pull usually looks like

Most rug pulls rely on one of four levers:

- **Liquidity removed.** The funds backing a trading pool are withdrawn, so holders can no longer sell at a meaningful price.
- **Supply inflated.** Someone who can still mint creates new tokens and sells them into the market.
- **Holders blocked.** A freeze authority stops token accounts from sending or receiving tokens.
- **Identity changed.** Editable metadata lets the name, symbol or image change after a token gets attention.

Each lever leaves a trace you can check on-chain. The sections below follow them in order.

![Four on-chain signals — mint authority, freeze authority, holder concentration and liquidity — each mapped to the risk it reveals.](/blog/img/how-to-spot-rug-pull-risk-1.webp "Each signal shows what is possible, not what will happen.")

## Check 1: Is the mint authority still active?

The mint authority can [mint new token units](https://solana.com/docs/tokens/basics/mint-tokens) to any token account. While it exists, the supply you see today is not final. According to [Solana's authority documentation](https://solana.com/docs/tokens/basics/set-authority), setting an authority to `None` permanently removes that role.

A revoked mint authority does not make a token valuable. It only means that no one can add supply later.

## Check 2: Is the freeze authority still active?

A freeze authority can [freeze a token account](https://solana.com/docs/tokens/basics/freeze-account), which prevents it from receiving, transferring or burning tokens until it is thawed. If the freeze authority has been revoked, accounts for that mint can no longer be frozen.

Some regulated assets keep a freeze authority for compliance reasons. For a community token, an active freeze authority mostly means that someone could stop your tokens from moving.

## Check 3: Can the metadata still change?

On Solana, token names, symbols and image links usually live in a metadata account. [Metaplex's documentation](https://www.metaplex.com/docs/smart-contracts/token-metadata/update) explains that an update authority can change these fields while the metadata is mutable. Once it is marked immutable, future updates fail.

Mutable metadata is not proof of bad intent. It does mean that the token you research today could look different tomorrow.

## Check 4: Who holds the supply?

Look at the share held by the largest wallet and by the top ten wallets together. When a few addresses control most of the supply, a single sale can move the price sharply.

Context matters here. A large holder might be a liquidity pool, an exchange or a vesting contract rather than a person. A holder bubblemap makes the distribution visible at a glance, but you still need to find out what each large address is.

## Check 5: Is there liquidity, and who controls it?

A token without a trading pool cannot be sold on a DEX at all. A token with a pool can still be risky if the provider can withdraw that liquidity at any time. A burned or locked liquidity position makes withdrawal harder. Verify that claim with evidence for that specific pool rather than a screenshot.

:::warning A score is a starting point
Any risk score is a heuristic. DegenKit's Scanner says it plainly: it does not verify liquidity lock or burn status, team allocations or off-chain intent. Never treat the score as a guarantee.
:::

![Animated scan: a mint address is pasted, mint and freeze authority show revoked, metadata locked, holder concentration appears with a bubblemap, and a heuristic score ring fills to 87.](/blog/img/how-to-spot-rug-pull-risk-demo.mp4)

## How DegenKit's Scanner scores a token

Paste a Solana mint address and the Scanner reads the token's current state. It starts at 100 and deducts points for:

- an active mint authority, which carries the largest deduction;
- an active freeze authority;
- metadata that can still be changed;
- a single holder above 20% or 50% of supply;
- top ten holders above 50% or 80% of supply;
- no tradable pair found.

A score of 80 or more is labeled low risk, 50 to 79 medium risk and anything lower high risk. Liquidity information comes from a public market-data source and is shown for context.

## Token extensions deserve a manual look

Tokens created with the Token Extensions program can carry extra features. One example is a [permanent delegate](https://solana.com/docs/tokens/extensions/permanent-delegate), which can authorize transfers and burns for any token account of that mint. Account owners cannot revoke it. The Scanner's score does not cover extensions, so check the mint in an explorer if the token uses this program.

![Three score bands explain what a heuristic risk score can and cannot confirm.](/blog/img/how-to-spot-rug-pull-risk-2.webp "Bands follow DegenKit's Scanner. No band verifies intent or a liquidity lock.")

## What a scan cannot tell you

On-chain data cannot show who controls a wallet, what a team has promised or what will happen next week. It cannot confirm that a large holder is really a vesting contract, or that a liquidity lock lasts as long as the announcement says. It also cannot protect you from a fake token that copies a real project's name.

Use the scan to narrow your questions. Then answer them with the project's own evidence.

## Wrap up

Rug-pull risk is easier to judge when you check the same levers every time: mint authority, freeze authority, metadata, holder concentration and liquidity. Each signal needs context, and none of them predicts price. [Scan a Solana token with DegenKit](https://degenkit.app/launch/solana/) before you decide.
