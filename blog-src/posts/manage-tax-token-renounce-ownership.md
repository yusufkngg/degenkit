---
title: 'Managing a Tax Token: Rates, Pools, Ownership and Renouncing'
slug: manage-tax-token-renounce-ownership
date: '2026-10-30'
excerpt: After you create a tax token, the owner can change rates, the tax wallet and the marked pools. Learn what each control does, what buyers check, and what renouncing ownership freezes.
cover: /blog/img/manage-tax-token-renounce-ownership-cover.webp
cover_alt: A Manage tax panel with buy and sell rates, a marked pool address and a renounce ownership button.
tags:
- Guide
- Tax Token
- Ethereum
---

A tax token keeps working after launch. On Ethereum, Robinhood Chain and DegenKit's other EVM networks, the wallet that owns it can still adjust how the tax works. That flexibility is useful, and it is also exactly what buyers want to understand before they trust the token.

If you are new to taxes, start with [how buy and sell taxes work](/blog/how-token-buy-sell-tax-works/).

## Where the controls live

Open **My Tokens** on the network's launcher and connect the owner wallet. Each tax token shows its rates and owner. If your wallet is the owner, **Manage tax** opens five controls.

![The five controls in Manage tax: tax rates, liquidity pool, tax wallet, transfer ownership and renounce ownership.](/blog/img/manage-tax-token-renounce-ownership-1.webp "Every change is a transaction from the owner wallet. Renouncing ends all of them.")

## 1. Tax rates

Set the buy and sell tax anywhere from 0% to 100%; 0% turns that side off. DegenKit's form warns that rates above 10% make buyers wary. A change applies to the next trade.

## 2. Liquidity pool

Taxes only apply to trades against pools you mark. After adding liquidity, paste the pair address and choose **Mark as pool**. You can also remove a pool from the list. Our guide to [adding liquidity on Uniswap](/blog/add-liquidity-uniswap-erc20/) shows where to find that address.

## 3. Tax wallet

The tax is paid in your token to the tax wallet. You can point it at a different address at any time.

## 4. Transfer ownership

Hands every control to a new address, such as a multisig. You lose control immediately. DegenKit warns that a wrong address can't be recovered, so double-check it.

## 5. Renounce ownership

Sets the owner to nobody. The tax rates, tax wallet and marked pools are frozen forever. Nobody can change them afterwards, including you. My Tokens then shows the token as **Ownership renounced · taxes frozen**.

:::warning Order matters
Renouncing freezes the pool list too. If you renounce before marking your pool, the tax will never apply to it. Add liquidity and mark the pool first.
:::

![A pool is marked, the rates are reviewed, ownership is renounced after a confirmation, and the token shows as frozen.](/blog/img/manage-tax-token-renounce-ownership-demo.mp4)

## What buyers see

Anyone can read the contract on Etherscan or Blockscout. The buy and sell rates are stored in basis points, so 300 means 3%. If an owner exists, buyers know the rates could be raised later. A renounced token shows the zero address as owner.

DegenKit's tax token has no blacklist, no pause and no trading switch. The owner's powers are limited to the controls above, but those still matter.

![What changes for buyers when an owner keeps control versus when ownership is renounced.](/blog/img/manage-tax-token-renounce-ownership-2.webp "Keeping ownership keeps flexibility. Renouncing gives certainty. Both should be explained publicly.")

## Keep or renounce?

**Keep ownership** if you expect to lower taxes over time, add pools on other DEXs or change the tax wallet. Say publicly what you plan and why.

**Renounce** once the setup is final and you want buyers to know it can never change. Check the pools, rates and wallet carefully first.

**Transfer to a multisig** if you want flexibility but not one person holding the keys.

## Questions people ask

### Can I undo a renounce?

No. Once the owner is the zero address, no one can call the owner functions again.

### Does changing the tax wallet move tokens already collected?

No. It only changes where future tax goes.

## Wrap up

A DegenKit tax token gives its owner five controls: rates, pools, tax wallet, transfer and renounce. Mark your pool before anything irreversible, explain your choices and share the transactions. Manage it from My Tokens on the [Ethereum](https://degenkit.app/launch/ethereum/) or [Robinhood Chain](https://degenkit.app/launch/robinhood/) launcher.
