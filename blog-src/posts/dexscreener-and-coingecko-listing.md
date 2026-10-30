---
title: 'Getting Your Token on DEX Screener and CoinGecko'
slug: dexscreener-and-coingecko-listing
date: '2026-10-30'
excerpt: DEX Screener lists a token automatically once it trades. CoinGecko needs an application. Learn how each one works, what you can control and what to prepare.
cover: /blog/img/dexscreener-and-coingecko-listing-cover.webp
cover_alt: A token's chart page with a logo and social links, next to a listing request form marked under review.
tags:
- Guide
- Marketing
- Listings
---

After launch, most buyers look for your token on two kinds of sites: chart sites such as **DEX Screener**, and data aggregators such as **CoinGecko**. The two work very differently. One finds you automatically. The other reviews an application.

## DEX Screener: automatic once you trade

You don't apply to DEX Screener. According to its [documentation](https://docs.dexscreener.com/), tokens are listed automatically as soon as they are added to a liquidity pool and have at least one transaction.

That means two things must happen first:

1. Your token has a pool on a DEX that DEX Screener tracks, such as Raydium.
2. At least one trade has gone through.

When you create a pool with DegenKit's **Create Liquidity**, the success screen links straight to the chart on DEX Screener.

## The logo and links come later

An automatic page shows prices and trades. Your logo, description and social links are a separate step. DEX Screener's [help center](https://help.dexscreener.com/en/articles/1147201) explains that it pulls token information from external lists, such as CoinGecko's.

If you don't want to wait for that, DEX Screener sells **Enhanced Token Info**. Its [product page](https://marketplace.dexscreener.com/product/token-info) says it adds your logo and socials, lets you share your project's details, and lets you designate wallets that hold locked supply so the market cap displays correctly. At the time of writing it was listed at $299, with most orders processed in minutes and up to 12 hours.

![The order of events from creating a token to having a chart page, token info and a CoinGecko listing.](/blog/img/dexscreener-and-coingecko-listing-1.webp "DEX Screener follows trading. CoinGecko follows a review.")

## CoinGecko: apply after you trade

CoinGecko lists tokens by request. Its [listing guide](https://support.coingecko.com/hc/en-us/articles/7291312302617) sets one basic requirement: the token must be actively tradable on an exchange CoinGecko tracks.

The steps in the guide are:

1. Log in to a CoinGecko account.
2. Open the request form and choose **New Coin/Token Listing**.
3. Pick an active listing, or a preview listing if the token has not launched yet.
4. Fill in the details, upload the token image and choose a review speed.

A regular review takes up to 5 days. A paid Fast Pass speeds review to within 24 hours. The guide also warns that if your community spams CoinGecko with listing demands, the token can be disqualified.

![A pool is created, the first trade lands, a chart page appears automatically, and a CoinGecko request is submitted for review.](/blog/img/dexscreener-and-coingecko-listing-demo.mp4)

## What to prepare

Both sites read what you publish, so collect it once:

- The **mint address** and the **pool address**.
- A square **logo** that matches your on-chain metadata.
- A short, factual **description**.
- **Website and social links** that you control.
- Where possible, the addresses of team, treasury and locked wallets.

:::tip Be wary of guaranteed listings
Anyone who promises a listing for a fee, outside these sites' own forms and products, is selling something they don't control. Use the official channels.
:::

![How DEX Screener and CoinGecko compare on how you get listed, cost, timing and what you control.](/blog/img/dexscreener-and-coingecko-listing-2.webp "Prices and timings are taken from each site's own pages and can change.")

## Questions people ask

### Why is my token not on DEX Screener yet?

Check that the pool exists and that at least one trade has happened. A pool with no trades won't appear yet.

### Does a CoinGecko listing make my token safer?

No. It means your data is tracked and displayed. Buyers should still check authorities, holders and liquidity.

## Wrap up

DEX Screener lists your token on its own once it has a pool and a trade. Token info comes from external lists or the paid Enhanced Token Info. CoinGecko needs an application, and the token must already trade. Prepare your addresses, logo and links in one place. [Create your pool on DegenKit](https://degenkit.app/launch/solana/) to get the first step done.
