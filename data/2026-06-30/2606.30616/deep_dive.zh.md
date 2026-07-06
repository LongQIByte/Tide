# Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent

[arXiv](https://arxiv.org/abs/2606.30616) · [HuggingFace](https://huggingface.co/papers/2606.30616) · ▲88

## 摘要（原文）

> We introduce Agents-A1, a 35B Mixture-of-Experts Agentic Model that reaches trillion-parameter-level performance by scaling the agent horizon. We investigate agent-horizon scaling from two perspectives: scaling long-horizon trajectories and scaling heterogeneous agent abilities. To support this goal, we build a long-horizon knowledge-action infrastructure that connects external knowledge, actions, observations, and verifier outcomes, producing agentic trajectories with an average length of 45K tokens. Based on this, we train Agents-A1 with a three-stage recipe. First, we perform full-domain supervised fine-tuning to align the base model with broad agentic behaviors. Second, we train domain-level teacher models to capture specialized expertise in each domain. Third, we propose a multi-teacher domain-routed on-policy distillation with salient vocabulary alignment to improve knowledge transfer efficiency across different domains, unifying six heterogeneous domains into one deployable student model. Agents-A1 achieves strong and broad performance for long-horizon agent benchmarks. Compared with 1T-parameter model such as Kimi-K2.6 and DeepSeek-V4-pro, Agents-A1 achieves leading results on SEAL-0 (56.4), IFBench (80.6), HiPhO (46.4), FrontierScience-Olympiad (79.0), and MolBench-Bind (56.8), and remains highly competitive on SciCode (44.3), HLE (47.6) and BrowseComp (75.5). We hope this work provides the community with a practical path for scaling the horizon using a 35B agent that can reach or match the performance of 1T models on long-horizon tasks.

## 摘要（中译）

我们介绍了Agents - A1，这是一个350亿参数的混合专家智能体模型，通过扩展智能体视野（agent horizon）达到了万亿参数级别的性能。我们从两个方面研究智能体视野扩展：扩展长视野轨迹和扩展异构智能体能力。为了支持这一目标，我们构建了一个长视野知识 - 行动基础设施，它连接外部知识、行动、观察和验证器结果，生成平均长度为45000个token的智能体轨迹。基于此，我们通过一个三阶段方案训练Agents - A1。首先，我们进行全领域监督微调，使基础模型与广泛的智能体行为保持一致。其次，我们训练领域级教师模型，以捕捉每个领域的专业专业知识。第三，我们提出了一种多教师领域路由的策略梯度蒸馏（on - policy distillation），并带有显著词汇对齐，以提高不同领域之间的知识转移效率，将六个异构领域统一为一个可部署的学生模型。Agents - A1在长视野智能体基准测试中取得了强大而广泛的表现。与如Kimi - K2.6和DeepSeek - V4 - pro这样的1万亿参数模型相比，Agents - A1在SEAL - 0（56.4）、IFBench（80.6）、HiPhO（46.4）、FrontierScience - Olympiad（79.0）和MolBench - Bind（56.8）上取得了领先的结果，并且在SciCode（44.3）、HLE（47.6）和BrowseComp（75.5）上仍然具有很强的竞争力。我们希望这项工作为社区提供一种实用的路径，即使用一个350亿参数的智能体来扩展视野，使其在长视野任务上能够达到或匹配1万亿参数模型的性能。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
近年来，大语言模型（LLM）的发展推动AI从被动响应转向主动决策，例如在软件工程、科学研究和复杂决策场景中，AI需要像人类一样执行“长程任务”——比如规划步骤、调用工具、验证结果并动态调整策略。这类任务的核心需求是**让AI具备持续解决问题的能力**，而非仅回答单轮问题。例如，科学家可能需要AI协助设计实验、分析数据并修正错误，而软件工程师需要AI编写代码、调试并优化程序。这些场景要求AI不仅理解语言，还要在多轮交互中保持逻辑连贯性，并从反馈中学习。  

**2. 之前的问题与瓶颈**  
现有方法主要依赖两种路径提升长程任务能力：一是**扩大模型参数**（如万亿参数模型），但这种方法需要巨大的计算资源和数据，且难以复制；二是**显式扩展任务规划能力**，但面临两个关键挑战：  
- **知识基础设施不足**：长程任务需要模型与环境（如工具、数据库）动态交互，但缺乏统一的训练环境，导致模型难以从实际反馈中学习（例如，无法验证中间结果或从错误中恢复）。  
- **异构能力整合困难**：不同领域（如科学、编程）需要不同的技能（如信息检索、约束跟踪），这些技能往往难以统一到一个模型中，容易产生冲突。  

**3. 本文的解法**  
论文提出了**Agents-A1**模型，通过“扩展任务边界而非参数”来突破瓶颈：  
- **构建知识-行动基础设施**：创建一个连接外部知识、工具、观察和验证信号的统一环境，生成平均长度为45K token的长程任务轨迹，让模型从实际交互中学习规划、工具调用和错误恢复。  
- **三阶段训练策略**：  
  1. **全领域监督微调**：训练一个具备广泛长程能力的基础模型。  
  2. **领域专家模型训练**：针对特定领域（如科学计算）优化专业技能。  
  3. **跨领域蒸馏**：通过“多教师领域路由蒸馏”将不同领域的技能统一到一个35B参数的模型中，避免能力冲突。  

**4. 与前人的关键差异**  
与依赖参数扩展的方法不同，Agents-A1的核心创新在于：  
- **显式解决长程任务的基础设施问题**：通过动态环境支持模型从反馈中学习，而非仅依赖文本训练。  
- **高效整合异构能力**：通过蒸馏技术将六个领域的技能（如工具使用、结果验证）统一到一个模型中，而非独立训练。  
- **性能对标万亿模型**：仅用35B参数就达到了万亿参数模型的长程任务表现（如在SEAL-0、IFBench等基准上超越Kimi-K2.6和DeepSeek-V4）。  

这一工作为社区提供了一条可行的路径：通过优化任务边界和技能整合，而非盲目扩大参数，实现长程智能的高效扩展。

## 方法图解

![Figure 2 : Overview of the three-stage training pipeline of Agents-A1. From mult](fig2_1.webp)

> Figure 2 : Overview of the three-stage training pipeline of Agents-A1. From multi-domain data to domain-specific teachers and multi-teacher on-policy distillation. First, Agents-A1 is trained with full-domain supervised fine-tuning on multi-domain long-horizon data, including search, scientific research, engineering, agentic tasks, and instruction following. Then, domain-specific teacher models are trained on each domain, and their expertise is transferred to the student model through domain-routed on-policy distillation with salient vocabulary alignment.

这张图展示了Agents - A1的三阶段训练管道的概述，重点是从多领域数据到领域特定教师模型以及多教师在线策略蒸馏的过程。

首先看最左侧的“Multi - domain Data”部分，这里包含了多种领域的数据，如“Search”（搜索）、“Science”（科学）、“Engineering”（工程）、“Agent Tasks”（智能体任务）和“Inst. Following”（指令遵循）等，这些是训练的基础数据来源，代表了不同类型的多领域长 horizon 数据。

接下来，数据流向中间的“full - domain supervised fine - tuning”（全领域监督微调）部分。在这个阶段，Agents - A1模型会使用这些多领域的长期 horizon 数据进行全领域的监督微调，目的是让基础模型与广泛的智能体行为对齐。从图中可以看到，数据通过箭头进入这个微调模块，经过处理后，模型的能力得到初步的对齐。

然后，进入到“domain - specific teacher models”（领域特定教师模型）的训练阶段。图中显示有四个教师模型：“Search Teacher”、“Science Teacher”、“Inst. Teacher”和“Tools Teacher”，每个教师模型对应一个特定的领域。这些教师模型是在各自的领域数据上进行训练的，以捕获每个领域的专业 expertise（专业知识）。从微调后的模型或者原始的多领域数据中，会有数据流向这些教师模型的训练过程，图中用箭头表示了数据的流动方向，比如从之前的模块指向这些教师模型的训练区域。

之后是“multi - teacher domain - routed on - policy distillation with salient vocabulary alignment”（多教师领域路由的在线策略蒸馏与显著词汇对齐）阶段。在这个阶段，学生模型（图中未明确画出，但可以理解为最终要得到的Agents - A1模型）会从这些领域特定的教师模型中学习。图中下方的模块显示了数据的处理流程，包括一些查询（如“Queries of Search data”、“Queries of Science data”等）的处理，然后通过损失函数（图中的公式\(\mathcal{L}(\theta_s^{(t)})=\frac{1}{B}\sum_{d\in\mathcal{D}}\sum_{i\in\mathcal{B}_d}\ell^{(i)}(\theta_s^{(t)};\theta_s,\theta_{t,i})=\frac{1}{B}\sum_{i = 1}^{B}\ell^{(i)}(\theta_s^{(t)};\theta_s,\theta_{t,i})\)）来优化学生模型的参数，这个损失函数用于衡量学生模型的输出与教师模型的输出之间的差异，从而指导学生模型的学习。同时，图中还有直方图（蓝色和橙色的柱状图），可能表示的是不同阶段的分布或者性能指标的变化，比如教师模型的输出分布和学生模型的输出分布，或者是训练过程中的损失分布等。

数据或信息的流动顺序总结如下：
1. 多领域数据（搜索、科学、工程、智能体任务、指令遵循等）首先用于全领域监督微调，使基础模型对齐广泛的智能体行为。
2. 微调后的模型或相关数据用于训练各个领域的特定教师模型，每个教师模型专注于一个领域的专业知识。
3. 学生模型（最终的Agents - A1）通过多教师领域路由的在线策略蒸馏，结合显著词汇对齐，从这些教师模型中学习，优化自身的参数，以获得跨领域的知识和能力。

这张图揭示的方法运作方式是：通过三个阶段的训练，首先让模型在多领域数据上对齐基本行为，然后让每个领域的教师模型学习该领域的专业知识，最后让学生模型从这些教师模型中高效地蒸馏知识，从而在不增加参数数量（35B）的情况下，通过扩展智能体的horizon（长轨迹和异质能力）来达到万亿参数级别的性能。具体来说，全领域监督微调是为了让模型有一个广泛的行为基础；领域特定教师模型的训练是为了捕获每个领域的深度知识；多教师在线策略蒸馏则是为了将这些领域知识高效地转移到学生模型中，实现跨领域的统一部署。

---

![Figure 3 : Overview of the knowledge-action infrastructure of Agents-A1. Heterog](fig3_1.webp)

> Figure 3 : Overview of the knowledge-action infrastructure of Agents-A1. Heterogeneous corpora are decomposed into atomic abilities and organized into a knowledge-action graph (KAG) that records evidence, actions, observations, and verifier outcomes. A tool-augmented self-play loop expands the KAG into domain-specific sub-KAGs for downstream task construction.

这张图展示了Agents - A1的知识 - 行动基础设施的整体架构，我们可以按照数据或信息的流动顺序来拆解每个组件和板块：

首先看最左侧的“Training corpus”（训练语料库），这里包含了多种类型的数据源，从上到下依次是Web - scale（网页规模数据）、Books（书籍）、Papers（论文）、TXT（文本文件）、Papers（再次出现的论文？可能是不同类型的文本）、Semi - structured data（半结构化数据）、Code（代码）、Data base（数据库）、Synthetic Data（合成数据）等。这些异构语料库是整个系统的输入，它们会被分解为原子能力，这对应图中上方的“Atomic Abilities Extraction”（原子能力提取）模块。这个模块包含五个子功能：Information Acquisition（信息获取）、Tool Calling（工具调用）、Executable Iteration（可执行迭代）、Evidence Verification（证据验证）、Constraint Tracking（约束跟踪），这些功能从训练语料库中提取出原子级别的能力。

接下来，提取出的原子能力被组织成“Knowledge - Action Graph (KAG)”（知识 - 行动图）。在KAG的模块中，我们可以看到节点（如Observation0、Action1、Wrong Target、Verifier、Action_n、Observation_n、True Target等）和边（蓝色实线和橙色虚线）。蓝色的边可能代表正常的行动 - 观察流程，比如从Observation0出发，经过Action1、Action2等，产生Observation1、Observation_n等，最终指向True Target；而橙色的虚线可能代表错误路径或者验证相关的路径，比如Wrong Target和Verifier的连接，Verifier会对行动或观察进行验证，以确定是否朝着True Target前进。KAG记录了证据、行动、观察和验证者的结果，这是知识 - 行动基础设施的核心结构，用于表示智能体的行为轨迹和相关信息。

然后看下方的“Self - play Graph Search and Expansion”（自博弈图搜索与扩展）模块。这个模块中的节点（如Action2、几个中间节点、Observation_n等）之间有带权重的边（如0.43、0.78、0.25、0.65、0.81、0.56等），还有一个公式\(\tau = [(s_1, q_1, o_1), \dots, (s_1, q_1, o_1), y]\)和\(U(q, \tau) \geq 0.6\)。这里的自博弈过程会扩展KAG，通过模拟不同的行动和观察序列（带权重的边可能代表不同行动或状态转移的概率或得分），生成更多的节点和边，从而丰富KAG的结构，为后续的领域特定子图构建提供基础。

再看右侧的“Self - evolving KAG Enhancement”（自进化KAG增强）模块。首先，有一个流程从Query（查询）开始，经过Search（搜索）、Scholar（学者工具）、Code（代码工具）、Agent（智能体工具）、Workflow（工作流工具）等，然后进入“Choose”（选择）和“Enhance”（增强）阶段。“Choose”阶段会根据Domain（领域）选择对应的“Sub - KAG”（子知识 - 行动图），这些子KAG包括Coding KAG、Agentic KAG、Instruction KAG、MLE KAG、Scientific KAG、Mid - train KAG等。“Enhance”阶段会结合Tool（工具）来增强子KAG。然后有一个“Judge & Verifier”（判断与验证器）模块，如果判断结果为“No”，则回到之前的流程重新选择或调整；如果为“Yes”，则进入“Domain - specific Task”（领域特定任务），完成任务的构建。

整体来看，这个基础设施的运作方式是：首先从异构训练语料库中提取原子能力，构建初始的KAG；然后通过自博弈的方式扩展KAG，丰富其结构和内容；接着根据不同的领域选择或构建子KAG，并结合工具进行增强，最后通过判断与验证来确定是否能用于领域特定任务。这个过程支持了Agents - A1的长轨迹缩放和异质能力缩放，使得模型能够处理长 horizon（长轨迹）的代理任务，并且整合了多种异质领域的知识和能力。

总结一下，图中的信息流动顺序是：训练语料库→原子能力提取→KAG构建→自博弈图扩展→领域选择与子KAG构建→工具增强→判断验证→领域特定任务。每个模块都有其特定的功能，共同构成了Agents - A1的知识 - 行动基础设施，使得模型能够在长轨迹和异质能力的缩放下达到万亿参数级别的性能（通过35B的模型实现）。

---

![Figure 4 : Optimization trajectory of Agents-A1 on the ICML 2013 Whale Challenge](fig4_1.webp)

> Figure 4 : Optimization trajectory of Agents-A1 on the ICML 2013 Whale Challenge [ undefal ] over a 12-hour run. The curve shows the best validation AUC achieved over wall-clock time, with annotated breakthrough moments corresponding to distinct algorithmic improvements. The shaded band indicates run-to-run variance across independent seeds.

这张图展示了Agents - A1模型在ICML 2013鲸鱼挑战任务上，经过12小时训练过程中的优化轨迹。我们先看坐标轴：横轴是时间（小时），从0到12，代表训练的时长；纵轴是AUC（Area Under Curve，曲线下面积，常用于衡量模型性能，值越接近1性能越好），范围从0.5到1.0。

接下来分析曲线和标注的内容：
- 蓝色的线（标注为“A1 (Ours)”）是模型在不同时间点的最佳验证AUC变化曲线。曲线的走势反映了随着时间推移，模型性能的提升过程，并且有一个浅蓝色的阴影带，这代表不同独立随机种子（实验重复）之间的结果方差，也就是多次实验的性能波动范围。
- 时间从0开始，初始阶段（0小时左右）是“Initial baseline Simple CNN on raw audio”（初始基线：原始音频上的简单CNN模型），此时AUC约为0.6。这是模型的初始性能，作为后续改进的起点。
- 然后，在某个时间点（约3小时左右），进行了“Audio augmentation (noise + gain variation) AUC +0.13”（音频增强：噪声+增益变化，AUC提升0.13）。这个步骤通过给音频数据添加噪声和调整增益来扩充数据，从而提升模型性能，此时AUC从约0.6 - 0.7的水平提升到约0.7 - 0.8的水平（结合曲线和标注的位置）。
- 接下来，在约5小时左右，“Train on most recent date (March 29 ≈ test dist.) AUC +0.10”（在最近日期（3月29日，接近测试分布）训练，AUC提升0.10）。这一步是调整训练数据的分布，使其更接近测试数据的分布，进一步提升性能，AUC从约0.8的水平提升到约0.9的水平。
- 然后，在约7小时左右，“Mel - CNN + deep ensemble AUC +0.08”（Mel - CNN + 深度集成，AUC提升0.08）。这里使用了Mel频谱的CNN模型并结合深度集成方法（多个模型组合），性能再次提升，AUC从约0.9的水平提升到约0.95左右的水平（结合后续的点）。
- 最后，在约10小时左右，“Heavy augmentation (10x) + final tuning”（重度增强（10倍）+ 最终微调，AUC达到0.9935）。这一步进行了更大量的数据增强（10倍）并最终微调模型，使得AUC接近1.0，达到很高的性能水平。

整个过程展示了模型通过一系列算法改进（数据增强、训练数据分布调整、模型结构改进、集成方法和最终微调等）逐步提升性能的过程。我们可以看到，随着时间的推移，每次算法改进都带来了AUC的提升，最终在12小时左右的训练后，模型的最佳验证AUC达到了0.9935，说明这些改进措施有效地提升了模型在ICML 2013鲸鱼挑战任务上的性能。

从结果的角度看，对比的是不同时间点（对应不同算法改进）的AUC性能，结论是Agents - A1模型通过逐步的算法优化（如数据增强、训练数据分布调整、模型结构和方法改进等），在12小时的训练过程中性能不断提升，最终达到了很高的AUC值（0.9935），证明了这些改进措施的有效性。
