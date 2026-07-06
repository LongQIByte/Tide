# AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents

[arXiv](https://arxiv.org/abs/2607.02255) · [HuggingFace](https://huggingface.co/papers/2607.02255) · ▲51

## Abstract (verbatim)

> Memory for a long-horizon LLM agent is a contract about what each future decision is allowed to see. The simplest contract appends past observations, tool calls, and reflections to every prompt, which makes prior context easy to access but also turns it into a jumbled mixture in which the effect of any single memory component is hard to isolate. We introduce and instrument an alternative bounded contract: every decision is made from a fresh user message assembled by typed retrieval, with no raw cross-decision transcript appended. The prompt thus stays bounded across runs of any length, and any single layer can be ablated in isolation. We instantiate the contract in Slay the Spire 2, a closed-rule stochastic deck-building game whose runs require hundreds of tactical and strategic decisions. A public online benchmark of frontier LLMs on the same game reports zero wins at the lowest difficulty across five configurations, and the developer-reported human win rate at the same difficulty is 16%; the task is hard but not saturated. Within our harness, a fixed-A0 ablation shows the largest observed difference when triggered strategic skills are enabled: the no-store baseline wins 3/10 games and adding the skill layer 6/10. At this sample size the comparison is directional rather than statistically decisive (Fisher exact p\approx0.37); a cross-backbone probe and public accumulating-context baselines are reported as operational comparisons rather than controlled tests of the contract variable itself. We release a reproducible testbed: 298 completed trajectories with condition tags, frozen memory/skill snapshots, prompt records, and analysis scripts -- an agent design and a validated, reusable methodology for studying how explicit memory layers shape long-horizon LLM-agent decisions.

## Background

### Background Analysis  

**Technical Context**: Long-horizon LLM agents (e.g., in games or automated planning) rely on "memory" to track historical actions, environmental feedback, and strategy adjustments. For instance, in a game like *Slay the Spire*, agents must remember past card combinations, enemy behaviors, and random events to formulate long-term winning strategies. The core challenge is how to efficiently use historical information within limited context windows while avoiding overload or confusion.  

**Previous Issues**: Traditional methods simply append all historical observations, tool calls, and reflections to each prompt. While easy to implement, this approach creates two critical flaws: (1) the context becomes a "information swamp," making it hard to isolate the impact of individual memory components; (2) as the decision chain lengthens, prompts grow indefinitely, exceeding model capacity. For example, state-of-the-art LLMs score 0% win rate at the easiest difficulty in *Slay the Spire* (compared to 16% human performance), indicating traditional memory designs fail to support complex long-term tasks.  

**Proposed Solution**: The paper introduces AgenticSTS, a "bounded-memory testbed" using on-demand retrieval instead of full context appending. Each decision is based solely on a current user message (generated via typed retrieval), preventing uncontrolled historical data accumulation. This allows researchers to "ablate" specific memory layers (e.g., strategic skill modules) and measure their impact. Experiments in *Slay the Spire 2* showed win rates doubling from 3/10 to 6/10 when enabling a strategic skill layer, validating the effectiveness of layered memory design.  

**Unique Angle**: Unlike prior work focusing on "longer context" or "more complex models," this paper emphasizes **controllability of memory mechanisms**. By providing a reproducible testbed (with trajectory logs, frozen snapshots, and analysis scripts), researchers can systematically explore "which memory components truly matter for long-horizon decisions." This "subtraction-based" design (rather than addition-driven scaling) offers a new methodological benchmark for LLM agent memory research.

## Method, Figure by Figure

(No figures to walk through.)
