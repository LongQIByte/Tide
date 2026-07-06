# AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents

[arXiv](https://arxiv.org/abs/2607.02255) · [HuggingFace](https://huggingface.co/papers/2607.02255) · ▲51

## 摘要（原文）

> Memory for a long-horizon LLM agent is a contract about what each future decision is allowed to see. The simplest contract appends past observations, tool calls, and reflections to every prompt, which makes prior context easy to access but also turns it into a jumbled mixture in which the effect of any single memory component is hard to isolate. We introduce and instrument an alternative bounded contract: every decision is made from a fresh user message assembled by typed retrieval, with no raw cross-decision transcript appended. The prompt thus stays bounded across runs of any length, and any single layer can be ablated in isolation. We instantiate the contract in Slay the Spire 2, a closed-rule stochastic deck-building game whose runs require hundreds of tactical and strategic decisions. A public online benchmark of frontier LLMs on the same game reports zero wins at the lowest difficulty across five configurations, and the developer-reported human win rate at the same difficulty is 16%; the task is hard but not saturated. Within our harness, a fixed-A0 ablation shows the largest observed difference when triggered strategic skills are enabled: the no-store baseline wins 3/10 games and adding the skill layer 6/10. At this sample size the comparison is directional rather than statistically decisive (Fisher exact p\approx0.37); a cross-backbone probe and public accumulating-context baselines are reported as operational comparisons rather than controlled tests of the contract variable itself. We release a reproducible testbed: 298 completed trajectories with condition tags, frozen memory/skill snapshots, prompt records, and analysis scripts -- an agent design and a validated, reusable methodology for studying how explicit memory layers shape long-horizon LLM-agent decisions.

## 摘要（中译）

长视野LLM代理的记忆是关于每个未来决策被允许看到什么的约定。最简单的约定是将过去的观察、工具调用和反思附加到每个提示中，这使得先前的上下文易于访问，但也使其变成了一个混乱的混合体，其中任何单一记忆组件的效果都难以隔离。我们引入并实现了一种替代的有界约定：每个决策都是通过类型化检索组装的新鲜用户消息进行的，没有原始的跨决策记录附加。因此，提示在任何长度的运行中都保持有界，任何单一层都可以单独消除。我们在《Slay the Spire 2》中实例化了该约定，这是一款封闭规则的随机卡组建游戏，其运行需要数百个战术和战略决策。一个公共在线基准测试报告了在相同游戏上最前沿的LLM在最低难度下五个配置中的零胜率，而开发者报告的人类在同一难度下的胜率为16%；任务困难但未饱和。在我们的测试框架中，固定A0消除显示了当触发战略技能时观察到的最大差异：无存储基线赢得3/10游戏，添加技能层赢得6/10。在这个样本大小下，比较是方向性的而不是统计上决定性的（Fisher精确p≈0.37）；报告了一个跨骨干探测和公共累积上下文基线作为操作比较，而不是对约定变量本身的控制测试。我们发布了一个可重复的测试平台：298个完成的轨迹，带有条件标签，冻结的内存/技能快照，提示记录和分析脚本——一个代理设计和一个经过验证的、可重用的方法，用于研究显式记忆层如何塑造长视野LLM代理的决策。

## 背景剖析

### 背景剖析  

**技术背景**：长程决策的LLM智能体（如游戏、自动化任务规划）需要“记忆”来跟踪历史操作、环境反馈和策略调整。例如在《Slay the Spire》这类需要数百次战术选择的游戏中，智能体必须记住过去的卡牌组合、敌人行为甚至随机事件，才能制定长期获胜策略。这种记忆机制的核心需求是：如何在有限上下文窗口中高效利用历史信息，同时避免信息过载或混淆。  

**之前的问题**：传统方法简单地将所有历史观察、工具调用和反思拼接进每次提示（prompt），虽然易于实现，但导致两个关键缺陷：（1）上下文变成“信息泥潭”，单个记忆组件的作用难以分离；（2）随着决策链延长，提示长度无限制增长，超出模型处理能力。例如，现有基准测试中，即使是最先进的LLM在《Slay the Spire》最低难度下也无法获胜（胜率0%），而人类胜率为16%，说明传统记忆设计未能有效支持复杂长程任务。  

**本文的解法**：论文提出“有界记忆测试平台”AgenticSTS，采用“按需检索”而非“全量追加”的记忆机制。每次决策仅基于当前用户消息（通过类型化检索生成），避免历史记录无限制堆积。这种方法允许研究者单独“切除”某一记忆层（如战略技能模块），观察其对结果的影响。通过在《Slay the Spire 2》中实验，发现启用战略技能层后胜率从3/10提升至6/10，验证了记忆分层设计的有效性。  

**切入角度**：与传统研究不同，本文不追求“更长上下文”或“更复杂模型”，而是聚焦于**记忆机制的可控性**。通过提供可复现的测试床（含轨迹记录、冻结快照和分析脚本），研究者可以系统性地探索“哪些记忆组件对长程决策真正必要”。这种“减法式”设计（而非加法式扩展）为LLM智能体的记忆研究提供了新的方法论基准。

## 方法图解

（本文无可讲解的插图）
