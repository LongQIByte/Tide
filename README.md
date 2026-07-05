# 🌊 Tide

**English** | [中文](./README.zh-CN.md)

> Information arrives like the tide — wave after wave, never stopping. You cannot hold back the ocean, but you can learn to read it.

**Tide** is an open-source personal information intake engine: it subscribes to the sources that matter to you (arXiv papers, Twitter/X voices, AI lab blogs…), and instead of merely summarizing them, it produces **deep interpretations** that flow into your personal knowledge base — so that the information you consume actually becomes understanding you own.

## Why "Tide"?

News, papers, and hot takes come in daily like the tide. Most aggregation tools try to *drink the ocean*: collect everything, compress it into bullet points, and call it a day. The result is a feed you skim and forget.

Tide takes the opposite stance. The tide will come regardless — the question is not "how do I see everything?" but "**what do I let shape my thinking, and how deeply?**". Tide watches the water for you, picks out the waves worth studying, and helps you engage with them seriously.

## The Core Belief: Understanding Cannot Be Outsourced

This project is built on one idea, borrowed from Andrej Karpathy:

> **"Understanding cannot be outsourced."**

In the AI era, it has never been easier to outsource *reading*. Any LLM will happily summarize a paper into five bullet points. But a summary you didn't struggle with is a summary you don't own. If AI does all the digesting, you end up with a well-organized library of things you never actually understood.

So Tide deliberately does **not** aim to "save you from reading." It aims to:

1. **Filter** — surface the small number of items genuinely worth your attention, instead of a 50-item daily dump.
2. **Interpret deeply** — for each selected item, generate a real analysis: what problem it attacks, what's actually new, how it connects to what you already know, and where it might be wrong.
3. **Feed your knowledge base** — the output is written to be *merged into* a personal wiki (à la Karpathy's LLM-maintained wiki), not consumed and discarded.
4. **Leave the understanding to you** — Tide prepares the material and asks the questions; the final act of understanding stays human.

Think of it as a research assistant that pre-reads for you — not a replacement for your own reading.

## What Tide Does

- 📡 **Subscribe** — arXiv topics/keywords, selected Twitter/X accounts (researchers, builders, labs), blogs and other RSS-able sources.
- 🌊 **Collect & deduplicate** — daily ingestion, cross-source dedup, noise removal. Collection is the dirty work; it should be boring and reliable.
- 🔍 **Score & select** — relevance scoring against *your* stated interests, so the daily selection is small and personal.
- 🧠 **Deep interpretation** — a multi-step LLM analysis chain (not one-shot summarization): background → contribution → critique → connection to your existing notes.
- 📚 **Knowledge-base output** — Markdown output designed to live inside an Obsidian-style personal wiki, with backlinks to related concepts.

## Status

🚧 **Early stage.** This README is the founding document — written before the code, on purpose. The "why" should outlive any particular implementation.

Rough roadmap:

- [ ] v0: arXiv subscription → daily selection → deep-interpretation Markdown reports
- [ ] v1: Twitter/X source ingestion
- [ ] v2: knowledge-base integration (backlinks into an existing personal wiki)
- [ ] v3: delivery channels (email / Feishu / GitHub Pages)

## Acknowledgements

- Andrej Karpathy, for the "personal LLM wiki" idea and the line that started this project.
- The many open-source daily-digest projects (arXiv digests, KOL aggregators, meridian and friends) that proved the collection layer is a solved problem — Tide focuses its energy on the interpretation layer instead.

## License

MIT
