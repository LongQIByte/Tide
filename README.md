# 🌊 Tide

**English** | [中文](./README.zh-CN.md)

> Information arrives like the tide — wave after wave, never stopping. You cannot hold back the ocean, but you can learn to read it.

**Tide** is an open-source AI information website: every day it ingests the sources that matter (arXiv papers, Twitter/X voices, AI lab blogs…), selects the waves worth reading, and publishes **deep interpretations** — not one-line summaries — on a web page anyone can open and read. A daily tide report for people who want to actually understand what's happening, not just scroll past it.

## Why "Tide"?

News, papers, and hot takes come in daily like the tide. Most aggregation tools try to *drink the ocean*: collect everything, compress it into bullet points, and call it a day. The result is a feed you skim and forget.

Tide takes the opposite stance. The tide will come regardless — the question is not "how do I see everything?" but "**what do I let shape my thinking, and how deeply?**". Tide watches the water for you, picks out the waves worth studying, and helps you engage with them seriously.

## The Core Belief: Understanding Cannot Be Outsourced

This project is built on one idea, borrowed from Andrej Karpathy:

> **"Understanding cannot be outsourced."**

In the AI era, it has never been easier to outsource *reading*. Any LLM will happily summarize a paper into five bullet points. But a summary you didn't struggle with is a summary you don't own. If AI does all the digesting, you end up with a well-organized library of things you never actually understood.

So Tide deliberately does **not** aim to "save you from reading." It aims to:

1. **Filter** — surface the small number of items genuinely worth attention each day, instead of a 50-item dump.
2. **Interpret deeply** — for each selected item, publish a real analysis: what problem it attacks, what's actually new, why it matters, and where it might be wrong.
3. **Invite you in** — every interpretation links back to the original source. Tide's write-up is the on-ramp, not the destination.
4. **Leave the understanding to you** — Tide prepares the material and asks the questions; the final act of understanding stays human.

Think of it as a research assistant that pre-reads for everyone — not a replacement for your own reading.

## What Tide Is

A website, updated daily, where you can:

- 🌊 **Browse today's tide** — the day's selected papers, tweets, and posts, each with a deep interpretation, not a one-liner.
- 📄 **Read paper deep-dives** — background → contribution → critique → connections, written to be read, with a link to the original.
- 🐦 **Follow the conversation** — what the researchers and builders worth listening to are actually saying, with context on why it matters.
- 🗂 **Look back** — a browsable archive by date and topic, so the tide leaves a record instead of washing away.

Behind the page, a fully automated pipeline:

- 📡 **Subscribe** — arXiv topics/keywords, selected Twitter/X accounts, blogs and other RSS-able sources.
- 🧹 **Collect & deduplicate** — daily ingestion, cross-source dedup, noise removal. Collection is the dirty work; it should be boring and reliable.
- 🔍 **Score & select** — relevance scoring so the daily selection stays small and worth reading.
- 🧠 **Deep interpretation** — a multi-step LLM analysis chain (not one-shot summarization).
- 🚀 **Publish** — the day's report goes live on the site automatically, every morning.

## Status

🚧 **Early stage.** This README is the founding document — written before the code, on purpose. The "why" should outlive any particular implementation.

Rough roadmap:

- [ ] v0: the website — arXiv ingestion → daily selection → deep-interpretation pages, auto-published daily
- [ ] v1: Twitter/X sources on the site
- [ ] v2: archive & topic navigation, search
- [ ] v3: subscriptions on top of the site (RSS / email / Feishu)

## Acknowledgements

- Andrej Karpathy, for the "personal LLM wiki" idea and the line that started this project.
- The many open-source daily-digest projects (arXiv digests, KOL aggregators, meridian and friends) that proved the collection layer is a solved problem — Tide focuses its energy on the interpretation layer instead.

## License

MIT
