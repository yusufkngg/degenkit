---
title: 'Mint Authority vs. Freeze Authority: What Revoking Actually Does'
slug: mint-authority-vs-freeze-authority
date: '2026-10-25'
excerpt: Two Solana permissions, two very different powers. Learn what mint and freeze authority control, what revoking changes and how to check both.
cover: /blog/img/mint-authority-vs-freeze-authority-cover.webp
cover_alt: A token sits between two permission cards, mint authority and freeze authority, both marked revoked.
tags:
- Guide
- Solana
- Permissions
---

Every Solana token starts as a mint account, and that account can name two separate authorities. One controls supply. The other controls whether holders can move their tokens. People often say "authorities revoked" as if it were one setting, but these are two different roles with two different effects.

This guide explains what each authority can do, what revoking changes, and how to check a token yourself.

## Two keys on one mint

[Solana's authority documentation](https://solana.com/docs/tokens/basics/set-authority) describes two authority types on a mint:

- **Mint authority** (`MintTokens`) controls the creation of new token units.
- **Freeze authority** (`FreezeAccount`) controls freezing and thawing token accounts.

Each role is held by an address or by no one. They are set and revoked separately, so one can stay active while the other is gone.

## What mint authority controls

The mint authority can [mint new token units](https://solana.com/docs/tokens/basics/mint-tokens) to a token account. While that role exists, total supply can grow at any time. New units dilute every existing holder's share, and anyone who sells them can push the price down.

![A supply example shows how minting another 1,000,000,000 tokens cuts a 1% holder's share to 0.5%.](/blog/img/mint-authority-vs-freeze-authority-1.webp "Illustrative numbers. Minting changes your share without touching your balance.")

Revoking the mint authority fixes the supply ceiling. Supply can still go down, because holders can [burn tokens](https://solana.com/docs/tokens/basics/burn-tokens) from their own balance. It can never go up again.

## What freeze authority controls

The freeze authority can [freeze a token account](https://solana.com/docs/tokens/basics/freeze-account). A frozen account cannot receive, transfer or burn tokens until it is thawed. The owner and balance stay the same, but the tokens are stuck.

Some regulated assets keep a freeze authority so an issuer can meet legal obligations. For a community or meme token, an active freeze authority mainly means one party can stop holders from selling.

![Mint authority and freeze authority compared side by side: what each can do while active and what changes after revoking.](/blog/img/mint-authority-vs-freeze-authority-2.webp "Two separate roles on the same mint. Revoking one does not revoke the other.")

## What revoking changes

Revoking means setting an authority to `None`. According to Solana's documentation, this permanently removes the selected role. There is no way to restore it later, even for the original creator.

- **Mint authority revoked:** no one can create new units. The current supply is the maximum.
- **Freeze authority revoked:** no token account for that mint can be frozen again.

DegenKit's Solana creator revokes both authorities when it creates a token. For tokens you created elsewhere and still control, the Authorities tool lets you load a mint and revoke either role separately.

:::warning Revoking is one-way
Revoked authorities cannot be restored. If your project genuinely needs future minting, decide that before revoking. Then explain the plan publicly.
:::

![Two keys represent mint and freeze authority. Minting doubles the supply and halves a holder's share, freezing blocks a holder's transfer, and revoking both breaks the keys for good.](/blog/img/mint-authority-vs-freeze-authority-demo.mp4)

## What revoking does not change

Revoked authorities answer two specific questions. They do not settle everything else:

- **Metadata** is controlled separately. [Metaplex's documentation](https://www.metaplex.com/docs/smart-contracts/token-metadata/update) explains that an update authority can change the name, symbol and URI while metadata is mutable.
- **Liquidity** is not affected. A pool can still be withdrawn by whoever controls the liquidity position.
- **Holder concentration** stays the same. A wallet holding most of the supply can still sell it.
- **Price and demand** are not set by permissions.

Treat revoked authorities as a baseline, not a safety certificate.

## How to check a token's authorities

You do not need to trust a project's announcement. Check the mint account itself:

1. Open the mint address in a Solana explorer.
2. Find the **Mint Authority** and **Freeze Authority** fields.
3. A revoked role appears as empty or `None`. An active role shows an address.
4. Note who holds any active role and whether the project explains why.

In DegenKit, **My Tokens** shows the authority status of tokens in your connected wallet. The **Scanner** shows it for any Solana mint, alongside holder concentration.

## How EVM tokens differ

Ethereum-style tokens do not use Solana's mint account model. Their permissions live in the contract code. DegenKit's ERC-20 tokens on Ethereum, BNB Chain, Base and Robinhood Chain have no mint function at all. The entire supply is created once, in the deployment transaction.

Other EVM contracts can include an owner who mints, pauses or blocklists. For those tokens, read the contract and its owner functions rather than looking for Solana-style authority fields.

## Questions people ask

### Can a token have mint authority revoked but freeze authority active?

Yes. The roles are independent. Always check both fields.

### Does revoking cost anything?

Revoking is a normal transaction, so it needs a network fee. A tool may add its own service fee, which is shown before you sign.

## Wrap up

Mint authority decides whether supply can grow. Freeze authority decides whether holders can be stopped. Revoking either one is permanent, and neither one replaces checking metadata, liquidity and holders. [Open DegenKit's Authorities tool](https://degenkit.app/launch/solana/) to check or revoke the roles on a token you control.
