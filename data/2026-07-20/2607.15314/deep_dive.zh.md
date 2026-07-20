# Cura 1T: Specialized Model for Agentic Healthcare

[arXiv](https://arxiv.org/abs/2607.15314) · [HuggingFace](https://huggingface.co/papers/2607.15314) · ▲28

## 摘要（原文）

> Healthcare spans high-stakes communication, expert reasoning, and workflow execution, yet specialized LLMs that cover these use cases together remain limited. A healthcare model must handle patient consultation, clinical reasoning over text and images, interactive diagnosis, and electronic health record (EHR) tool use. These capabilities fail in different ways, and a narrow update for one task can degrade another. We present Cura 1T, a healthcare-specialized LLM trained through a human-gated self-evolution loop. In each evolution round, a training agent plans a target capability, trains the model, evaluates benchmark trajectories, and refines the data mixture from observed failures. This data-centered loop improves the model through targeted synthetic and curated examples rather than a single generic medical-data update. Across the healthcare evaluation suite, Cura 1T ranks at or near the top among frontier baselines, while remaining competitive on out-of-domain reasoning and agentic benchmarks.

## 摘要（中译）

医疗保健涵盖了高风险沟通、专家推理和工作流程执行，然而能够同时覆盖这些使用场景的专业大语言模型（LLM）仍然有限。医疗保健模型必须处理患者咨询、基于文本和图像的临床推理、互动诊断以及电子健康记录（EHR）工具的使用。这些能力在不同方面存在不足，针对一项任务的狭隘更新可能会降低另一项任务的表现。我们推出了Cura 1T，这是一款通过人类门控自我进化循环训练的医疗保健专业大语言模型。在每一轮进化中，训练代理会规划目标能力，训练模型，评估基准轨迹，并根据观察到的失败情况优化数据混合。这个以数据为中心的循环通过有针对性的合成和精心挑选的示例来改进模型，而不是进行单一的通用医疗数据更新。在医疗保健评估套件中，Cura 1T在前沿基线中排名前列或接近前列，同时在域外推理和代理基准测试中保持竞争力。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
医疗领域需要兼顾高风险沟通、专业推理和流程执行的能力，例如医生与患者对话需遵循临床指南，诊断时需结合文本和影像分析，以及通过电子健康记录（EHR）工具完成长期诊疗任务。这些场景要求模型既能提供准确的临床建议，又能在多轮交互中保持逻辑一致性，同时避免错误决策（如漏诊或工具调用失败）。然而，现有模型往往只能单一优化某项任务，难以兼顾复杂场景下的综合表现。  

**2. 之前的问题与局限**  
尽管前沿语言模型在单独的医疗任务（如医学问答或影像分析）上取得进展，但实际部署中面临三大挑战：  
- **任务冲突**：针对某项任务优化的模型可能在其他任务中表现下降（例如，增强诊断能力可能导致工具调用格式错误）。  
- **数据碎片化**：医疗数据分散在指南、病历、影像和交互记录中，且高质量监督信号稀缺（如某些诊断结果无法简单验证）。  
- **失败模式多样**：不同任务的错误类型（如遗漏关键信息或推理脆弱性）需要不同的修复策略，单一数据更新难以平衡。  

**3. 本文的解法**  
论文提出Cura 1T，通过**“人类门控自进化循环”**解决上述问题。该框架让AI代理自主规划目标（如提升多轮诊断能力）、训练模型、评估结果，并从失败中迭代优化数据混合策略。例如，若模型在影像分析中漏诊，代理会针对性补充相关数据，而非全局调整。这种方法避免了传统“一刀切”式训练的缺陷，通过合成数据和真实案例的混合，逐步提升模型的综合能力。  

**4. 切入角度的关键差异**  
与先前工作不同，Cura 1T的核心创新在于：  
- **任务协同优化**：同时针对患者互动、临床推理和EHR工具使用设计训练流程，而非孤立优化单个任务。  
- **数据驱动的迭代**：依赖AI代理自动分析失败模式并生成改进方案，减少人工干预，提高效率。  
- **泛化能力保留**：在专注医疗能力的同时，确保模型在数学推理等非医疗基准测试中不损失性能，证明其训练策略的平衡性。  

这一设计使Cura 1T在医疗基准测试中表现领先，同时为未来“通用+专业”的AI模型开发提供了新思路。

## 方法图解

![Figure 1 : Performance of Cura 1T, frontier models, and the Kimi-K2.6 base acros](fig1_1.webp)

> Figure 1 : Performance of Cura 1T, frontier models, and the Kimi-K2.6 base across six healthcare benchmark panels: MedAgentBench (Jiang et al., 2025 ) , HealthBench Professional and Hard (Arora et al., 2025 ; OpenAI, 2026 ) , MedXpertQA (Zuo et al., 2025 ) , and AgentClinic (Schmidgall et al., 2024 ) .

这张图（图1）展示了Cura 1T模型以及多个前沿基线模型在不同医疗健康基准测试面板上的性能表现。我们可以将图分为六个主要部分，每个部分对应一个特定的基准测试，这些基准测试按两行三列的布局排列。

首先，我们来看第一行的三个基准测试：

1.  **HealthBench Hard**：
    *   **坐标与对比对象**：这是一个柱状图，横轴代表不同的模型，纵轴代表性能分数（数值标注在柱子上方）。从左到右的模型依次是：Cura 1T、GPT-5.5、Claude Opus 4.8、Kimi-K2.6 和 Gemini 3.1 Pro。Cura 1T 的得分是 36.8，GPT-5.5 是 31.5，Claude Opus 4.8 是 22.2，Kimi-K2.6 是 22.2，Gemini 3.1 Pro 是 20.6。
    *   **信息解读**：在这个基准测试中，Cura 1T 的性能优于其他所有对比模型。

2.  **HealthBench Professional**：
    *   **坐标与对比对象**：同样是一个柱状图。从左到右的模型依次是：Cura 1T、Claude Fable 5、Claude Opus 4.8、GPT-5.5、Kimi-K2.6 和 Gemini 3.1 Pro。Cura 1T 的得分是 66.2，Claude Fable 5 是 66.0，Claude Opus 4.8 是 55.8，GPT-5.5 是 51.8，Kimi-K2.6 是 50.3，Gemini 3.1 Pro 是 43.8。
    *   **信息解读**：Cura 1T 在此基准测试中表现最佳，略高于 Claude Fable 5。

3.  **MedXpertQA-Text**：
    *   **坐标与对比对象**：柱状图。从左到右的模型依次是：Cura 1T、GPT-5.5、Claude Opus 4.8 和 Kimi-K2.6。Cura 1T 的得分是 60.0，GPT-5.5 是 59.6，Claude Opus 4.8 是 56.2，Kimi-K2.6 是 49.3。
    *   **信息解读**：Cura 1T 在这个文本型医疗问答基准测试中表现最好。

接下来是第二行的三个基准测试：

4.  **MedXpertQA-Multimodal**：
    *   **坐标与对比对象**：柱状图。从左到右的模型依次是：GPT-5.5、Cura 1T、Claude Opus 4.8 和 Kimi-K2.6。GPT-5.5 的得分是 77.1，Cura 1T 是 72.2，Claude Opus 4.8 是 71.0，Kimi-K2.6 是 66.9。
    *   **信息解读**：虽然Cura 1T在此基准测试中的得分（72.2）低于GPT-5.5（77.1），但它仍然优于Claude Opus 4.8和Kimi-K2.6。这表明Cura 1T在多模态医疗问答方面具有竞争力，但可能不是所有情况下都排名第一。

5.  **AgentClinic**：
    *   **坐标与对比对象**：柱状图。从左到右的模型依次是：Cura 1T、Claude Opus 4.8、Kimi-K2.6 和 GPT-5.5。Cura 1T 的得分是 79.6，Claude Opus 4.8 是 79.4，Kimi-K2.6 是 75.4，GPT-5.5 是 68.4。
    *   **信息解读**：Cura 1T 在这个代理诊所相关的基准测试中表现最佳，其得分略高于Claude Opus 4.8。

6.  **MedAgentBench**：
    *   **坐标与对比对象**：柱状图。从左到右的模型依次是：Cura 1T、Claude Opus 4.8、Gemini 3.1 Pro、GPT-5.5 和 Kimi-K2.6。Cura 1T 的得分是 94.0，Claude Opus 4.8 是 93.7，Gemini 3.1 Pro 是 91.3，GPT-5.5 是 89.4，Kimi-K2.6 是 84.7。
    *   **信息解读**：Cura 1T 在这个综合性的医疗代理基准测试中表现最为出色，得分远高于其他模型。

这张图揭示了Cura 1T方法的运作方式及其效果：
*   **方法背景**：根据论文摘要，医疗领域需要模型具备高风险的沟通、专家推理和工作流执行能力，这些能力包括患者咨询、基于文本和图像的临床推理、互动诊断以及电子健康记录（EHR）工具的使用。传统的单一任务更新可能会损害其他能力。
*   **Cura 1T的方法**：Cura 1T 是一个通过“人类门控自进化循环”训练的医疗专用LLM。在每一轮进化中，训练代理会规划一个目标能力，训练模型，评估基准轨迹，并从观察到的失败中优化数据混合。这种方法通过针对性的合成和策划示例来改进模型，而不是进行单一的通用医疗数据更新。
*   **结果展示**：图中的每个基准测试面板都展示了Cura 1T与多个前沿模型（如GPT-5.5、Claude Opus 4.8、Kimi-K2.6等）在特定医疗任务上的性能对比。从结果来看，Cura 1T在大多数基准测试中都取得了顶尖或接近顶尖的成绩，这验证了其“数据中心的循环”改进方法的有效性。它能够在覆盖多种医疗使用场景的同时，在域外推理和代理基准测试中保持竞争力。

总结来说，这张图通过六个不同的医疗基准测试，清晰地展示了Cura 1T作为一个专门的医疗LLM，在处理各种医疗相关任务时的卓越性能，从而支持了论文中提出的方法论的有效性。

---

![Figure 2 : Left: Agent-managed self-evolution loop for Cura 1T. Human review gat](fig2_1.webp)

> Figure 2 : Left: Agent-managed self-evolution loop for Cura 1T. Human review gates the plan before training and the keep, revert, or deploy decision after evaluation. Right: Data refinement pipeline and training stack.

这张图展示了Cura 1T模型的核心训练框架，分为左右两部分：左侧是**代理管理的自进化循环**，右侧是**数据精炼流程和训练栈**。

### 左侧：自进化循环（Agent-managed Self-evolution Loop）
这个循环描述了Cura 1T模型如何通过“计划-训练-评估-精炼”的迭代过程不断优化，且每个关键节点都有人类评审的介入：

1. **Plan（计划）**：
   - 内容：定义目标行为（Define target behaviors）、选择基准和指标（Choose benchmarks & metrics）、设计数据配方（Design data recipe）、提出超参数（Propose hyperparameters）。
   - 流动：计划需要经过“Human Review（人类评审）”的批准（Plan approval），才能进入训练阶段。人类评审在这里起到把关作用，确保计划的合理性。

2. **Train（训练）**：
   - 内容：使用SFT（监督微调）进行混合搜索和合理性检查（SFT for mixture search and sanity check）、使用SDFT（可能是某种特定微调）进行抗遗忘和LoRA训练（SDFT for anti-forgetting & LoRA training on Tinker）。
   - 输入：来自“Refine”阶段的“Training specifications（训练规范）”。
   - 输出：生成“Candidate checkpoints（候选检查点）”，进入评估阶段。

3. **Evaluate（评估）**：
   - 内容：运行基准测试（Run benchmarks）、收集轨迹（Collect trajectories）、分析失败案例（Analyze failures）。
   - 输出：生成“Graded trajectories（分级轨迹）”，进入“Refine”阶段；同时将结果提交给“Human Review”进行决策（Decision: Keep / Continue to refine / Revert / Deploy / Reflect and Re-plan）。

4. **Refine（精炼）**：
   - 内容：根因分析和故障模式（Root cause & failure modes）、针对性合成（Targeted synthesis）、混合策划（Mixture curation）、建议下一步（Suggested next steps）。
   - 输入：来自“Evaluate”阶段的“Graded trajectories”和“Failed Trajectories（失败轨迹）”（从数据精炼部分反馈）。
   - 输出：生成“Refined data mixture（精炼后的数据混合）”，回到“Plan”阶段，形成循环。同时，“Human Review”会根据评估结果决定是“Keep（保留）”、“Continue to refine（继续精炼）”、“Revert（回退）”、“Deploy（部署）”还是“Reflect and Re-plan（反思并重新计划）”。

### 右侧：数据精炼流程和训练栈（Data Refinement Pipeline and Training Stack）
这部分展示了数据如何被处理以支持模型训练，以及训练的具体技术栈：

#### 数据精炼（Data Refinement）
- **Skill-driven Data Synthesis（技能驱动的数据合成）**：
  - 输入：“Failed Trajectories（失败轨迹）”。
  - 处理步骤：Reasoning Correction（推理修正）、Knowledge Injection（知识注入）、Behavior Calibration（行为校准）、Retention Anchors（保留锚点）。
  - 输出：“Curated Data Mixture（策划后的数据混合）”，用于后续训练。
- **Validation & Quality Gates（验证和质量门）**：
  - 处理步骤：Format Check（格式检查）、Safety & PII Filter（安全和PII过滤）、Data Depep（可能是数据加深或数据增强）。
  - 作用：确保数据的质量和安全性，过滤掉不符合要求的数据。

#### 训练栈（Training Stack）
- **Input Mixture（输入混合）**：包含不同类型的输入，如Reasoning（推理）、Behavior（行为）、Knowledge（知识）、Agentic（代理相关）、Retention（保留）。
- **Trainer（训练器）**：
  - 步骤：首先进行SFT（监督微调），然后进行Hyperparam Search（超参数搜索），接着是RL（强化学习），最后是SDFT（特定微调）。
  - 输出：“Candidate Model（候选模型）”，进入评估阶段。

### 方法运作方式
Cura 1T的核心是**人类门控的自进化循环**：
1. 首先，训练代理制定训练计划，经过人类评审后开始训练。
2. 训练完成后，对模型进行评估，分析其在基准测试中的表现和失败案例。
3. 根据评估结果，精炼数据混合（包括针对性合成和数据策划），并再次经过人类评审决定是否继续训练、回退或部署。
4. 数据精炼部分通过技能驱动的数据合成和质量门处理，生成高质量的数据用于训练，而训练栈则通过SFT、超参数搜索、RL和SDFT等技术逐步优化模型。

这种方法的优势在于，它不是简单地更新通用医疗数据，而是通过**针对性的合成和策划数据**来改进模型的特定能力，同时避免对其他任务的性能产生负面影响。通过在多个医疗评估套件上的表现，Cura 1T在前沿基线中排名靠前或名列前茅，同时在域外推理和代理基准测试中也保持竞争力。

---

![Figure 3 : Evolution map from the base model to Cura 1T. Values are changes from](fig3_1.webp)

> Figure 3 : Evolution map from the base model to Cura 1T. Values are changes from benchmark-specific bases; solid and dashed red arrows mark retained and reverted interventions.

这张图展示了从基础模型（Base model）到最终模型Cura 1T的进化路径，也就是方法的具体实施过程。我们可以将其理解为一个迭代优化的流程，通过一系列有针对性的干预（interventions）来逐步提升模型的性能。

首先，流程的起点是“Base model”（基础模型）。从这个基础模型出发，有四条主要的优化路径，每条路径代表一个特定的优化目标或干预措施，这些路径用不同颜色的箭头表示，对应图例中的不同能力领域：

1.  **紫色路径（EHR tool use - EHR工具使用）**：
    *   `Tool-use +0.060`：这是第一个干预步骤，目标是提升模型使用工具的能力，性能提升了0.060。
    *   `Tool-use + retention +0.084`：在工具使用的基础上，增加了“retention”（保留/维持）的考虑，性能进一步提升到+0.084。
    *   `Harness bug fix +0.090`：针对之前步骤中可能出现的“bug”进行修复，性能再次提升到+0.090。
    *   这条路径最终汇入`Consolidated Refinements`（整合优化）。

2.  **蓝色路径（Patient care - 患者护理）**：
    *   `Clean behavior mix Prof. +0.131 / Hard +0.150`：这个干预措施旨在优化模型的行为模式，针对“Professional”（专业）场景性能提升0.131，针对“Hard”（困难）场景性能提升0.150。
    *   从这个步骤出发，有一条虚线红色箭头指向`Behavior correction Subset degradation: Prof. -0.252 / Hard -0.508`，这表示一个被“reverted”（回退）的干预，因为行为修正导致了特定子集的性能下降。
    *   这条路径最终也汇入`Consolidated Refinements`。

3.  **绿色路径（Clinical reasoning - 临床推理）**：
    *   `Knowledge injection + retention +0.034`：这个干预措施是向模型注入知识并考虑保留，性能提升0.034。
    *   `Mixture refinement +0.067`：对数据混合方式进行优化，性能再次提升0.067。
    *   从`Knowledge injection + retention`步骤出发，有一条虚线红色箭头指向`Reasoning correction Insufficient factual coverage: -0.028`，表示一个被回退的干预，因为推理修正导致了事实覆盖不足的问题。
    *   从`Mixture refinement`步骤出发，有一条虚线红色箭头指向`Data mixture tuning Non-termination: -0.129`，表示另一个被回退的干预，因为数据混合调整导致了非终止问题。
    *   这条路径最终汇入`Consolidated Refinements`。

4.  **黄色路径（Interactive diagnosis - 交互式诊断）**：
    *   `Interactive trajectory + retention +0.053`：这个干预措施关注交互式轨迹并考虑保留，性能提升0.053。
    *   从这个步骤出发，有一条虚线红色箭头指向`Single-turn reasoning Premature diagnosis: -0.108`，表示一个被回退的干预，因为单轮推理导致了过早诊断的问题。
    *   这条路径最终也汇入`Consolidated Refinements`。

所有经过优化的路径最终都汇入`Consolidated Refinements`（整合优化）阶段。从这个阶段，有一个实线箭头指向最终的模型`Cura 1T`。

图中的箭头类型很重要：
*   **实线箭头（Retained - 保留）**：表示该干预措施被保留并有效提升了模型性能。
*   **虚线红色箭头（Reverted - 回退）**：表示该干预措施虽然尝试了，但被发现会导致性能下降或其他问题，因此被回退或撤销。

图例解释了不同颜色路径代表的能力领域：
*   紫色：EHR tool use (EHR工具使用)
*   蓝色：Patient care (患者护理)
*   绿色：Clinical reasoning (临床推理)
*   黄色：Interactive diagnosis (交互式诊断)

这张图揭示了Cura 1T的训练方法是一个“human-gated self-evolution loop”（人工门控的自进化循环）。具体来说，每一轮进化中：
1.  一个训练代理（training agent）会规划一个目标能力（例如EHR工具使用、临床推理等）。
2.  针对这个目标能力对模型进行训练。
3.  评估基准测试轨迹（benchmark trajectories）以观察模型的表现和潜在问题。
4.  根据观察到的失败（failures）来精炼数据混合（data mixture）。这个过程是通过针对性的合成和策划示例（synthetic and curated examples）来进行的，而不是单一的通用医学数据更新。

图中展示的各个干预步骤及其性能变化（如+0.060, -0.252等）就是这个评估和精炼过程的体现。那些被回退的干预（虚线红色箭头）表明该方法能够识别并纠正有害的更新，从而避免模型在某一方面的提升以牺牲其他方面为代价。最终，通过整合所有有效的优化措施，模型进化为Cura 1T。

总而言之，这张图清晰地展示了Cura 1T是如何通过一个迭代的、多方面的、数据驱动的优化过程，从基础模型逐步发展成为一个专门用于医疗保健的LLM的。它强调了针对性干预、持续评估以及对不良影响的回退机制在模型开发中的重要性。

---

![Figure 4 : Out-of-domain evaluation results for Cura 1T.](fig4_1.webp)

> Figure 4 : Out-of-domain evaluation results for Cura 1T.

这张图（图4）展示了Cura 1T模型在多个“域外”（Out-of-domain）基准测试中的评估结果。这些基准测试并非专门针对医疗健康领域，而是用来衡量模型在通用或其它专业领域的能力，从而验证Cura 1T作为一个专门化模型是否在其他方面也保持了竞争力。

图的结构清晰地分为六个主要的基准测试部分，每个部分都用一个标签（如 τ²-Airline, τ²-Retail, τ²-Telecom, AIME 2025, AIME 2026, GPQA-Diamond）进行标识。每个基准测试部分都包含一组垂直的条形图，用于比较Cura 1T与其他几个前沿基线模型的性能。

1.  **基准测试部分与对比对象**：
    *   **τ²-Airline**：此基准测试比较了五个模型：Claude Opus 4.5, Qwen3.5, Gemini 3 Pro, Cura 1T, 和 Claude Sonnet 4.5。Cura 1T的得分是76.0，低于Claude Opus 4.5 (84.0) 和 Qwen3.5 (81.5)，但高于Gemini 3 Pro (80.5) 和 Claude Sonnet 4.5 (72.0)。
    *   **τ²-Retail**：此基准测试比较了五个模型：Cura 1T, Claude Sonnet 4.5, Gemini 3 Pro, Qwen3.5, 和 DeepSeek V3.2。Cura 1T的得分是88.6，是所有比较模型中最高的，表明其在该基准测试中表现最佳。
    *   **τ²-Telecom**：此基准测试比较了五个模型：Cura 1T, Qwen3-Max, Claude Sonnet 4.5, Gemini 3 Pro, 和 Qwen3.5。Cura 1T的得分是100.0，远高于其他模型，显示出显著的优势。
    *   **AIME 2025**：此基准测试比较了五个模型：Cura 1T, DeepSeek V3.2, gpt-oss 120B, Nova 2.0 Pro, 和 Claude Haiku 4.5。Cura 1T的得分是96.7，并列第一（与DeepSeek V3.2相同），表明其在该基准测试中表现优异。
    *   **AIME 2026**：此基准测试比较了五个模型：Kimi-K2.6, Qwen3.6 Plus, MAI-Thinking-1, Seed 2.0 Pro, 和 Cura 1T。Cura 1T的得分是93.3，是所有比较模型中最高的，再次证明了其竞争力。
    *   **GPQA-Diamond**：此基准测试比较了五个模型：Gemini 3.1 Pro, GPT-5.5, Claude Opus 4.8, Kimi-K2.6, 和 Cura 1T。Cura 1T的得分是89.9，虽然不是最高（Gemini 3.1 Pro得分为94.1），但仍然处于较高水平，显示了其在更难基准测试上的能力。

2.  **方法运作的揭示**：
    虽然这张图本身是结果展示，但它间接揭示了Cura 1T方法的核心理念。根据论文摘要，Cura 1T是通过一个“人类门控的自进化循环”训练的。这个循环包括：规划目标能力、训练模型、评估基准轨迹、并从观察到的失败中细化数据混合。这张图中的多个基准测试（如AIME系列、GPQA-Diamond）以及域外交叉任务（如τ²系列）正是用来评估模型在不同能力上的表现。图中Cura 1T在多个基准测试中取得领先或接近领先的排名，表明这种方法有效地提升了模型的综合能力，而不仅仅是在单一医疗任务上。图中的对比对象（各种前沿基线模型）也说明了Cura 1T是在与当前最先进的模型进行比较，从而验证其有效性。

3.  **坐标、对比对象和结论**：
    *   **坐标**：每个条形图的Y轴代表模型的得分（通常是百分比或某种标准化分数），X轴则列出了参与比较的不同模型。
    *   **对比对象**：对比对象包括了多种当前前沿的大型语言模型（LLMs），如Claude系列（Opus, Sonnet, Haiku）、Qwen系列（Qwen3.5, Qwen3.6 Plus）、Gemini系列（Gemini 3 Pro, Gemini 3.1 Pro）、以及其他模型如DeepSeek V3.2, gpt-oss 120B, Kimi-K2.6, MAI-Thinking-1, Seed 2.0 Pro等。
    *   **结论**：这张图清晰地表明，Cura 1T作为一个专门针对医疗健康的LLM，在多个域外基准测试中表现出色，能够与当前最先进的模型竞争甚至在某些基准测试中超越它们。这支持了论文的论点，即Cura 1T不仅擅长医疗任务，而且在通用和其它专业领域的推理能力上也保持了高水平，证明了其训练方法的有效性。图中的数据流动是从各个基准测试的名称开始，到各个模型的得分比较，最终得出Cura 1T在这些测试中的相对排名和性能表现。
