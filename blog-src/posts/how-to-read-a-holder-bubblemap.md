---
title: 'How to Read a Holder Bubblemap Before You Buy'
slug: how-to-read-a-holder-bubblemap
date: '2026-10-29'
excerpt: Big bubbles are not automatically bad news. Learn what a holder bubblemap shows, what the largest accounts usually are, and how to check them yourself.
cover: /blog/img/how-to-read-a-holder-bubblemap-cover.webp
cover_alt: A holder bubblemap with one large labeled pool bubble and smaller holder bubbles around it.
tags:
- Guide
- Safety
- Solana
---

A holder bubblemap turns a list of addresses into a picture. Each bubble is a holder, and bigger bubbles hold more of the supply. It is one of the fastest ways to see whether a token is spread out or concentrated in a few places.

It is also easy to misread. The biggest bubble is often not a person at all. This guide explains what the map shows, what large holders usually are, and how to check them.

## What the map actually shows

DegenKit's Scanner draws the **top 10 holders** of a Solana token. Each bubble's size reflects its share of the supply, compared with the largest holder, and shows its percentage and a shortened address.

The data comes from Solana's [`getTokenLargestAccounts`](https://solana.com/docs/rpc/http/gettokenlargestaccounts) method. According to Solana's documentation, it returns up to 20 of the largest **token accounts** for a mint. That detail matters:

- A token account is not the same as a wallet. One wallet can own several token accounts.
- A liquidity pool keeps its tokens in a token account too, so a pool appears as a holder.

## The usual suspects behind big bubbles

When one bubble dominates, it is usually one of these:

- **A liquidity pool.** The tokens available to trade sit in the pool. A large pool bubble is normal for a new token.
- **A creator or team wallet.** On DegenKit, the full supply goes to the creator's wallet at creation. Until it moves, that wallet holds 100%.
- **An exchange or custody wallet.** Centralized platforms often hold many users' tokens in a few addresses.
- **A locked or vesting contract.** Tokens promised to a team or treasury can sit in a contract that releases them over time.
- **A person who bought or received a lot.** This is the case to look at most carefully.

![The common types of large holders — pool, creator, exchange, vesting contract and individual — and how to tell them apart.](/blog/img/how-to-read-a-holder-bubblemap-1.webp "The biggest bubble is often infrastructure, not a person. Identify it before you judge the map.")

## How to identify a large holder

Copy the address from the bubble and open it in a Solana explorer.

1. **Check the owner.** For a token account, the explorer shows which wallet or program owns it.
2. **Look for a program owner.** If a DEX program owns the account, it is almost certainly a pool vault.
3. **Read the history.** A wallet that received the full supply at creation is the creator. A wallet that bought in many small swaps looks different.
4. **Compare with the project's notes.** A good launch record names its treasury, team and pool addresses.

:::tip Ask the project
If a large holder is unexplained, ask what it is. A project that publishes its key addresses makes this check quick for everyone.
:::

![A scan loads the top holders, the largest bubble is identified as a liquidity pool, and the remaining concentration is re-read without it.](/blog/img/how-to-read-a-holder-bubblemap-demo.mp4)

## Read concentration without the pool

Once you know which bubble is the pool, mentally set it aside. What matters is how the **rest** of the supply is spread.

Take a simple illustration. The pool holds 40%. The next wallet holds 25% and the remaining eight hold 2–3% each. Without the pool, that second wallet controls a large part of the tradable supply. It could move the price sharply in one sale.

The Scanner's score flags a single holder above 20% or 50%, and top ten holders above 50% or 80%. Those thresholds count every token account, including pools. That is why the score is a starting point and the map is where you add context.

## Patterns worth a second look

- **Several mid-sized bubbles of almost the same size.** This can be normal, but it can also mean one person split tokens across wallets.
- **A creator wallet that still holds most of the supply after launch.** Ask what it is for and whether it is locked.
- **A pool bubble that is small compared with individual holders.** Thin liquidity means large sales move the price more.
- **Large holders with no history beyond receiving tokens.** Find out who sent them and why.

None of these prove bad intent. They tell you which questions to ask.

![A reading checklist for a holder map: identify the pool, find the creator, group similar bubbles and compare with published addresses.](/blog/img/how-to-read-a-holder-bubblemap-2.webp "A map shows distribution. Context comes from explorers and the project's own records.")

## What a bubblemap cannot tell you

A top-10 view cannot show the long tail of small holders. It cannot prove that two wallets belong to the same person, or that a vesting contract releases tokens when promised. It also changes over time, so a snapshot from launch day says little about next month.

Use the map together with the other checks: mint and freeze authority, metadata, and liquidity evidence.

## Wrap up

A holder bubblemap is a quick visual of who holds a token. Read it in order: identify the pool, find the creator, then look at how the rest of the supply is spread. Big bubbles need explanations, not panic. [Scan a Solana token with DegenKit](https://degenkit.app/launch/solana/) and open the largest holders in an explorer before you decide.
