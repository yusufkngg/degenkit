---
title: 'How to Create an ERC-20 Token on Ethereum Without Coding'
slug: create-erc20-token-on-ethereum
date: '2026-10-30'
excerpt: A step-by-step guide to creating an ERC-20 token on Ethereum mainnet — wallet, ETH for gas, plain or tax token, and how to check the result on Etherscan.
cover: /blog/img/create-erc20-token-on-ethereum-cover.webp
cover_alt: An Ethereum token creator form next to a finished ERC-20 token card showing a fixed supply.
tags:
- Guide
- Ethereum
- Token Launch
---

Ethereum is where the ERC-20 standard started, and it is still the network many buyers trust most. Creating a token there no longer needs code. It does need a few decisions made carefully, because the important ones can't be undone.

This guide walks through the whole process on DegenKit's [Ethereum launcher](https://degenkit.app/launch/ethereum/).

## What you need

- An EVM wallet such as MetaMask or Rabby.
- Some **ETH on Ethereum mainnet** for the network fee (gas) and DegenKit's service fee.
- Your token's name, symbol and total supply, written down and checked.
- A decision on whether you want a plain token or a tax token.

Gas on Ethereum changes from minute to minute. Our guide to [Ethereum gas fees](/blog/ethereum-gas-fees-explained/) explains how it is calculated and how to read the estimate in your wallet.

## Step 1: Connect and switch to Ethereum

Open the launcher and connect your wallet. DegenKit is non-custodial: it never sees your keys, and every action is a transaction you sign. If your wallet is on another network, the page asks it to switch to Ethereum.

## Step 2: Choose plain or tax

**Token Creator** makes a standard ERC-20 token. It uses 18 decimals and has no mint function, so the supply you enter is the final supply. The whole supply goes to your wallet.

**Tax Token** works the same way but adds a buy tax and a sell tax that you set, paid in your token to a wallet you choose. Taxes only start once you add liquidity and mark the pool. You can change them later, or freeze them forever by renouncing ownership. Our guide to [managing a tax token](/blog/manage-tax-token-renounce-ownership/) covers every control.

![The choices you make when creating an ERC-20 on Ethereum, and which of them are permanent.](/blog/img/create-erc20-token-on-ethereum-1.webp "Name, symbol and supply are permanent. Only a tax token's tax settings can change later.")

## Step 3: Enter the details

Type the name, symbol and supply. Check the number of zeros twice; there is no way to add or remove supply later. For a tax token, also set the buy and sell rates and the tax wallet.

:::warning Permanent from the first block
Name, symbol and supply can't be edited once the transaction confirms. If something is wrong, the only fix is to create a new token.
:::

## Step 4: Review the fees and sign

DegenKit reads its service fee from the contract and shows it before you sign. Your wallet then shows the network fee estimate. Approve, and the token is created in one transaction.

![A wallet connects on Ethereum, the token details are entered, the fees are reviewed and the new contract is checked on Etherscan.](/blog/img/create-erc20-token-on-ethereum-demo.mp4)

## Step 5: Check it on Etherscan

DegenKit shows the contract address and a link to Etherscan. Open it and check:

1. The network is Ethereum mainnet.
2. The name, symbol and 18 decimals match.
3. The total supply is correct.
4. Your wallet holds the full supply.

Our guide to [reading a token page on Etherscan and Blockscout](/blog/read-token-page-etherscan-blockscout/) shows where each of these lives.

![A short verification checklist for a new ERC-20 token on Etherscan.](/blog/img/create-erc20-token-on-ethereum-2.webp "Check these four things before you share the contract address.")

## After the token exists

The token can't be traded until it has a liquidity pool. On Ethereum that usually means a DEX such as Uniswap. Our guide to [adding liquidity on Uniswap](/blog/add-liquidity-uniswap-erc20/) covers that step, including what tax tokens need.

When you announce the token, always publish the full contract address and say it is on Ethereum. A token with the same name on another network is a different contract.

## Questions people ask

### Can I mint more tokens later?

No. DegenKit's Ethereum tokens have no mint function, so the supply is final for everyone, including DegenKit.

### Should I test first?

If you are unsure, rehearse the flow on a cheaper network first, then repeat it on Ethereum with the exact values you want.

## Wrap up

Creating an ERC-20 on Ethereum takes one transaction: connect, choose plain or tax, enter the details, review the fees and sign. The decisions are permanent, so prepare them before you start. [Open the Ethereum launcher](https://degenkit.app/launch/ethereum/) when you are ready.
