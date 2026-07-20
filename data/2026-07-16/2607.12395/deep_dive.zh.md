# Ring-Zero: Scaling Zero RL to a Trillion Parameters for Emergent Reasoning

[arXiv](https://arxiv.org/abs/2607.12395) · [HuggingFace](https://huggingface.co/papers/2607.12395) · ▲91

## 摘要（原文）

> Reinforcement learning with verifiable rewards without human-annotated data, often referred to as zero RL, has emerged as a powerful paradigm for eliciting chain-of-thought reasoning. However, due to computational constraints, existing studies are largely restricted to small models, leaving the training dynamics and emergent capabilities at a large scale unexplored. To meaningfully explore this frontier, we aim to elicit high-quality reasoning behaviors from the model. However, we find that naive scaling often suffers from poor readability, token redundancy, and a lack of adaptive reasoning depth. To address these challenges, we present a stable and efficient training pipeline, incorporating algorithmic and system optimizations such as clipped importance sampling, training-inference ratio correction, and mixed-precision control. Our experiments offer three key findings that validate the "bitter lesson" of scaling: (1) scaling to 1T parameters significantly enhances sample efficiency and performance ceilings; (2) the training process progresses sequentially through an initial discovery phase followed by a sharpening phase; and (3) the model spontaneously develops advanced cognitive behaviors, including anthropomorphism, structured formatting, self-verification, parallel reasoning, and context anxiety, rendering hand-crafted heuristics redundant. Evaluated on seven mathematical benchmarks, Ring-2.5-1T-Zero achieves competitive performance. Additionally, to assess CoT quality beyond final-answer correctness, we propose a structured evaluation framework across three dimensions: comprehensibility, reproducibility, and efficiency, where our model demonstrates clear advantages in producing structured and concise reasoning traces. By sharing our observed emergent phenomena, we hope to provide the community with deeper insights into scaling behaviors, particularly at the 1-trillion scale.

## 摘要（中译）

无需人类标注数据的可验证奖励强化学习（通常称为零样本强化学习（zero RL））已成为引发链式思维推理的有力范式。然而，由于计算限制，现有研究主要局限于小型模型，大规模模型的训练动态和新兴能力仍未被探索。为了有意义地探索这一前沿领域，我们旨在从模型中引发高质量的推理行为。然而，我们发现简单扩展通常会导致可读性差、标记冗余和自适应推理深度不足。为应对这些挑战，我们提出了一个稳定高效的训练流程，结合了算法和系统优化，如裁剪重要性采样（clipped importance sampling）、训练-推理比率校正（training-inference ratio correction）和混合精度控制（mixed-precision control）。我们的实验提供了三个关键发现，验证了扩展的“苦涩教训”：（1）扩展到1万亿参数显著提高了样本效率和性能上限；（2）训练过程依次通过初始发现阶段，然后是锐化阶段；（3）模型自发地发展出高级认知行为，包括拟人化、结构化格式化、自我验证、并行推理和上下文焦虑，使手工设计的启发式方法变得多余。在七个数学基准测试上进行评估，Ring-2.5-1T-Zero取得了具有竞争力的性能。此外，为了评估链式思维（CoT）质量超越最终答案的正确性，我们提出了一个结构化评估框架，涵盖三个维度：可理解性、可重复性和效率，我们的模型在生成结构化和简洁的推理轨迹方面表现出明显优势。通过分享我们观察到的新兴现象，我们希望为社区提供关于扩展行为的更深入见解，特别是在1万亿规模上。

## 背景剖析

### 背景剖析  

**1. 技术背景与需求**  
链式思维（Chain-of-Thought, CoT）推理是当前大语言模型（LLM）解决复杂任务的核心能力，尤其在数学推理、代码生成等需要多步逻辑的场景中至关重要。传统方法依赖人工标注的推理数据（如监督微调）来引导模型学习，但这种方法成本高昂且难以覆盖所有任务场景。零强化学习（Zero RL）应运而生，它通过直接从预训练模型出发，利用可验证的奖励信号（如答案正确性）进行自主优化，避免了人工数据的限制。其目标是让模型自发涌现出高效的推理策略，例如在数学问题中逐步推导步骤、自我验证答案的正确性。然而，现有研究受限于计算资源，大多停留在小模型（如百亿参数级别），无法探索大规模模型（如万亿参数）的潜力。  

**2. 先前方法的局限性**  
尽管零RL展示了潜力，但现有方法存在三大问题：  
- **可读性差**：生成的推理过程缺乏逻辑结构，人类难以理解和验证；  
- **冗余与效率低下**：标准算法（如GRPO）倾向于奖励更长的输出，导致推理步骤冗余、计算资源浪费；  
- **缺乏动态深度**：固定响应预算限制了模型对不同复杂度任务的适应性，无法灵活调整推理深度。  
此外，小模型的研究无法揭示大规模下的训练动态，例如是否会出现新的认知行为（如自我组织或并行推理）。  

**3. 本文的解决方案**  
针对这些问题，本文提出了一种针对万亿参数模型的零RL训练框架（Ring-Zero）。核心思路是通过**轻量级算法与系统优化**实现稳定训练：  
- **算法改进**：采用裁剪重要性采样（clipped importance sampling）避免长度偏差，结合训练-推理比率校正（training-inference ratio correction）激励高质量推理；  
- **系统优化**：使用混合精度计算和上下文并行技术提升训练效率；  
- **自适应深度**：通过分层训练（tier-based adaptive training）动态调整推理深度，适应不同任务需求。  
这些优化无需复杂的工程改造，仅通过简单修改即可稳定训练万亿模型，并激发其自主涌现高级推理行为（如结构化格式、自我验证）。  

**4. 与前人的关键差异**  
本文的独特之处在于：  
- **规模突破**：首次验证了万亿参数下零RL的有效性，发现大规模模型会自发涌现人类级别的推理策略（如“情境焦虑”机制）；  
- **质量评估**：提出多维度的CoT评估框架（可理解性、可复现性、效率），超越了仅关注最终答案的传统评估方式；  
- **极简设计**：相比依赖人工设计的启发式方法，本文通过纯强化学习训练，让模型自主优化推理过程，证明“规模即能力”的“苦涩教训”。  

综上，本文通过技术优化与规模探索，为理解零RL在大模型中的行为提供了新视角，并展示了无监督推理的潜力。

## 方法图解

![Figure 1 : Overview of Ring-2.5-1T-Zero. (a) The multi-stage training pipeline. ](fig1_1.webp)

> Figure 1 : Overview of Ring-2.5-1T-Zero. (a) The multi-stage training pipeline. First-stage RL incentivizes reasoning from the base model. Self-Distillation compresses CoT traces and resets the training-inference engine gap. Second-stage RL shifts to a sample-level loss for sustained improvement. Third-stage RL introduces tier-based training for adaptive reasoning depth. (b) Infrastructure optimizations for stable and efficient training at scale. (c) Emergent behaviors that arise spontaneously without explicit supervision.

这张图（图1）是论文《Ring - Zero: Scaling Zero RL to a Trillion Parameters for Emergent Reasoning》中关于Ring - 2.5 - 1T - Zero方法的概述图，分为三个主要部分：(a)训练管道、(b)基础设施优化和(c)涌现行为。

首先看(a)训练管道部分，它展示了多阶段的训练流程，数据的流动顺序是从左到右的。最左边是基础模型Ling - 2.5 - 1T - Base，然后通过箭头进入第一阶段强化学习（First - stage RL）。第一阶段RL的目标是激励推理，它包含两个组件：Token - level Loss（标记级损失）和Stability Strategies（稳定性策略），这一阶段从基础模型开始激发推理能力。接着，第一阶段之后是Self - Distillation（自蒸馏）阶段，它的作用是压缩和稳定，包含CoT Compression（思维链压缩）和Train - Infer Gap Reset（训练 - 推理差距重置），这个阶段会压缩思维链轨迹并调整训练和推理之间的差距。之后，自蒸馏阶段之后是第二阶段强化学习（Second - stage RL），目标是持续改进，包含Sample - level Loss（样本级损失）和Remove KL Penalty（移除KL惩罚），这一阶段将损失函数切换到样本级以实现持续的性能提升。最后是第三阶段强化学习（Third - stage RL），目标是自适应深度，采用Tier - based Training（基于层级的训练），并且有Low（低）、Medium（中）、High（高）三个层级，用于实现自适应的推理深度。

然后是(b)基础设施优化部分，这部分是为了在大规模训练中实现稳定和高效的训练。它包含两个优化策略：Mixed - precision Control（混合精度控制），具体是FP32 Attn & LM head（FP32注意力机制和语言模型头）；以及Context Parallel Optimization（上下文并行优化），具体是MLA & Lightning Attn All - to - all CP（MLA和闪电注意力全对全通信原语）。

最后是(c)涌现行为部分，这部分展示了在没有显式监督的情况下自发出现的先进认知行为，包括五个方面：Anthropomorphism（拟人化），例子是“I might have a brain fart, Genius Idea”（我可能脑子短路了，天才想法）；Structured Format（结构化格式），例子是“Step 1... Step 2... Step 7: Verify”（步骤1……步骤2……步骤7：验证）；Parallel Reasoning（并行推理），例子是“Alternative approach: another way...”（替代方法：另一种方式……）；Context Anxiety（上下文焦虑），例子是“I will proceed to make an educated guess.”（我将进行有根据的猜测）。

整体来看，这张图展示了Ring - 2.5 - 1T - Zero方法的工作流程：首先通过多阶段强化学习和自蒸馏来训练模型，同时通过基础设施优化来保证大规模训练的稳定和高效，最终模型会自发出现多种先进的认知行为，并且在数学基准测试中表现出竞争力。

---

![(a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d](fig2_1.webp)

> (a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d) Seq Length (new data) Figure 2 : Training curves of Ling-2.5-1T-Base during first stage RL. (a,b) First 2800 steps with the initial training data: reward and sequence length increase steadily as the model bootstraps reasoning from scratch. (c,d) After switching to new training data, the model continues to improve with sustained sequence length growth.

这张图（图2a）展示了模型“Ling-2.5-1T-Base”在强化学习（RL）训练**第一阶段**、使用**初始训练数据**时的**奖励（Reward）随训练步骤（Step）的变化曲线**。

### 图的组件与信息流动：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤数（或迭代次数）。从0开始，图中显示到约2000+步（caption提到前2800步）。这表示训练过程的时间推进。
- **纵轴（Y轴）**：标记为“Reward”，代表模型在训练过程中获得的奖励值。奖励值从0.00开始，最高接近1.75。奖励是强化学习中衡量模型行为好坏的关键指标，这里它反映了模型生成的推理（如思维链CoT）的质量。
- **曲线**：蓝色的曲线展示了奖励随训练步骤的变化趋势。我们可以清晰地看到三个阶段：
  1.  **快速上升期**：在训练初期（大约前几百步），奖励值从接近0迅速上升到约1.55左右。这表明模型在“从零开始”学习时，能够快速“发现”有效的推理模式，从而获得更高的奖励。
  2.  **平台期/小幅波动期**：在达到约1.55的奖励后，曲线进入一个相对平稳的阶段，奖励值在1.50到1.60之间小幅波动。这可能意味着模型已经掌握了某些基本的推理技能，但仍在探索更优的策略。
  3.  **再次上升期**：在大约1000步之后，奖励值开始再次缓慢上升，最终稳定在约1.75左右。这表明模型在进一步训练中，其推理能力得到了“锐化”或提升，能够生成更高质量的推理。

### 方法运作方式（从图中揭示）：
这张图揭示了该研究提出的“第一阶段RL”训练方法的具体运作方式：
- **从零开始引导推理（Bootstrapping Reasoning）**：模型在没有任何人类标注数据的情况下，仅通过初始训练数据和强化学习的奖励机制，就能“自发地”学习并提高其推理能力。图中奖励的快速上升证明了这一点。
- **训练过程的阶段性**：如图所示，训练过程并非线性增长，而是经历了“快速发现” -> “稳定/探索” -> “持续提升/锐化”的阶段。这与论文摘要中提到的“训练过程依次经历初始发现阶段，然后是锐化阶段”相吻合。
- **样本效率和性能提升**：奖励的持续增长表明，随着训练的进行，模型在利用初始数据方面变得越来越高效，并且其推理性能（由奖励衡量）也在不断提高。这验证了论文中关于“扩展到1万亿参数显著提高了样本效率和性能上限”的发现。

### 结论（基于图和caption）：
- **坐标与范围**：横轴是训练步骤（Step），纵轴是奖励（Reward）。数据显示，在前2800步的训练中，奖励从接近0增加到约1.75。
- **对比对象**：这张图（图2a）与图2b（初始数据的序列长度）、图2c（新数据的奖励）和图2d（新数据的序列长度）形成对比。图2a专注于**初始数据**上的**奖励**变化。
- **结论**：
  - 使用初始训练数据时，模型的奖励随着训练步骤的增加而**稳步上升**。这表明模型能够从零开始“引导”出推理能力。
  - 训练过程呈现出明显的**阶段性**：初期快速提升，随后进入一个相对稳定的平台期，最后再次提升。
  - 这种训练动态支持了论文的核心观点，即通过适当的训练方法（如论文中提到的算法和系统优化），大规模模型（如1T参数的模型）能够在强化学习中有效地学习和发展复杂的推理行为。

---

![(a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d](fig2_2.webp)

> (a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d) Seq Length (new data) Figure 2 : Training curves of Ling-2.5-1T-Base during first stage RL. (a,b) First 2800 steps with the initial training data: reward and sequence length increase steadily as the model bootstraps reasoning from scratch. (c,d) After switching to new training data, the model continues to improve with sustained sequence length growth.

这张图（图2b）展示了模型“Ling-2.5-1T-Base”在强化学习（RL）训练**第一阶段**中，使用**初始训练数据**时的**序列长度（Sequence Length）**随**训练步骤（Step）**变化的曲线。

### 图的组件与信息流动：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤（或迭代次数），范围从0到约2800步（根据caption描述）。它展示了训练的时间进程。
- **纵轴（Y轴）**：标记为“Sequence Length”，代表模型生成的序列长度（可以理解为模型输出或处理的数据序列的长度，例如推理过程中的token数量）。纵轴刻度从2000到12000以上，显示了序列长度的数值范围。
- **曲线**：蓝色的曲线展示了序列长度随训练步骤的变化趋势。我们可以看到：
  - **初始阶段（0到约1000步）**：序列长度相对较低，在2000左右波动，增长较为缓慢。这对应caption中提到的“模型从零开始引导推理（bootstrap reasoning from scratch）”的阶段，模型正在学习如何生成有意义的序列。
  - **快速增长阶段（约1000到2000步）**：序列长度开始显著增长，从约4000快速上升到8000左右。这表明模型在这个阶段开始更有效地学习，能够生成更长的序列，可能是因为它开始理解任务并发展出更复杂的推理能力。
  - **持续增长阶段（2000步之后）**：序列长度继续增长，最终超过12000，并且有一些波动。这说明模型在持续改进，能够处理更长的序列，推理能力进一步提升。

### 方法的运作方式（从图中推断）：
这张图展示了**第一阶段RL训练**中模型的行为。根据caption，这个阶段使用的是“初始训练数据”。方法的运作可以理解为：
1. **从零开始引导（Bootstrap）**：在训练初期（0到约1000步），模型没有太多的先验知识或经验，因此序列长度较短且增长缓慢。模型正在学习如何生成有效的序列（例如，解决数学问题的推理步骤）。
2. **学习与改进**：随着训练步骤的增加（约1000步之后），模型开始学习到更有效的策略，能够生成更长的序列。这可能是因为模型通过强化学习（RL）获得了奖励信号，从而调整其参数以生成更有价值、更长的序列。
3. **持续优化**：在训练的后期（2000步之后），序列长度继续增长，表明模型在持续优化其推理能力，能够处理更复杂的任务或生成更详细的推理过程。

### 结果与结论（结合caption）：
- **坐标与范围**：横轴是训练步骤（0到约2800步），纵轴是序列长度（2000到12000以上）。
- **对比对象**：这张图（图2b）与图2a（初始数据的奖励曲线）、图2c（新数据的奖励曲线）和图2d（新数据的序列长度曲线）形成对比。图2b专注于初始数据下的序列长度变化。
- **结论**：
  - 在使用初始训练数据的前2800步训练中，模型的**奖励（图2a）**和**序列长度（图2b）**都稳步增长，这表明模型在“从零开始引导推理”的过程中逐渐提高了性能。
  - 序列长度的增长表明模型能够生成更长的、可能更复杂的序列（例如，更详细的推理步骤），这反映了模型推理能力的提升。
  - 这个阶段的训练为后续使用新数据（图2c和图2d）的训练奠定了基础，因为模型在初始数据上已经学会了基本的推理技能，能够在新的数据上继续改进。

总结来说，这张图展示了模型在第一阶段RL训练中，使用初始数据时序列长度随训练步骤的增长趋势，反映了模型从初步学习到持续优化的过程，验证了方法在引导模型发展推理能力方面的有效性。

---

![(a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d](fig2_3.webp)

> (a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d) Seq Length (new data) Figure 2 : Training curves of Ling-2.5-1T-Base during first stage RL. (a,b) First 2800 steps with the initial training data: reward and sequence length increase steadily as the model bootstraps reasoning from scratch. (c,d) After switching to new training data, the model continues to improve with sustained sequence length growth.

这张图（图2a）展示了模型“Ling-2.5-1T-Base”在强化学习（RL）训练第一阶段，使用**初始训练数据**时的**奖励（Reward）随训练步骤（Step）变化的曲线**。

首先，我们来看图的各个组成部分：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤或迭代次数。从图中可以看到，横轴的范围大约从0到800左右的步骤。这表示模型在训练过程中经历了这些步骤。
- **纵轴（Y轴）**：标记为“Reward”，代表模型在训练过程中获得的奖励值。奖励值的范围大约从1.30到1.55以上。奖励通常用于衡量模型行为的优劣，这里的奖励值越高，表明模型的表现越好。
- **曲线**：蓝色的曲线代表了奖励值随训练步骤的变化趋势。这条曲线是整个图的核心信息载体。

数据的流动和信息的呈现顺序如下：
1.  **起点**：在训练的初始阶段（步骤接近0时），奖励值相对较低，大约在1.30左右。这表明模型刚开始训练时，其推理能力或行为表现还不佳，获得的奖励较少。
2.  **发展阶段**：随着训练步骤的增加（从0向右移动），奖励值呈现出明显的上升趋势。曲线从左下角向右上角延伸，表明随着训练的进行，模型的表现越来越好，获得的奖励越来越多。
3.  **趋势细节**：
    *   在训练的前几个步骤（例如0到250步左右），奖励值增长较为迅速。这可能对应于模型的“初始发现阶段”（如原文caption所述），模型开始从零开始探索并初步建立推理能力。
    *   随着训练步骤的继续增加（例如250步之后），奖励值的增长速度可能有所放缓，但总体上仍然保持上升趋势。曲线变得更加平缓，但仍持续向上。这可能对应于模型的“锐化阶段”（如原文caption所述），模型在已有的基础上进一步优化其推理能力，奖励值稳步提升。
    *   曲线并非完全平滑，而是存在一些波动。这表明在训练过程中，模型的表现可能会有起伏，但长期趋势是积极的。

这张图揭示了该方法的具体运作方式：
-   **训练过程**：该方法采用强化学习的方式进行模型训练。在训练的第一阶段，模型使用“初始训练数据”进行学习。
-   **奖励机制**：通过观察奖励值的变化来评估模型的学习效果。奖励值的增加表明模型正在学习到更好的策略或行为，以完成任务（在这种情况下，可能是数学推理或其他需要链式思考的任务）。
-   **学习动态**：图中的曲线展示了模型学习的动态过程。模型从一个较低的奖励水平开始，随着训练的进行，奖励值逐渐增加。这表明模型能够从训练数据中学习，并不断提高其性能。
-   **阶段划分**：根据曲线的形状和原文caption的描述，可以将训练过程大致分为两个阶段：
    *   **初始发现阶段**：在这个阶段，奖励值快速增长，模型开始探索并初步掌握任务的基本技能。
    *   **锐化阶段**：在这个阶段，奖励值继续增长，但速度可能变慢，模型进一步优化其技能，提高推理的质量和效率。

结论：
-   **坐标**：横轴是训练步骤（Step），纵轴是奖励值（Reward）。
-   **对比对象**：这张图（图2a）与其他图（图2b、c、d）形成对比。图2a和图2b关注的是使用“初始训练数据”的情况，而图2c和图2d关注的是切换到“新训练数据”后的情况。在这张特定的图（图2a）中，我们观察的是单一数据集（初始数据）下的奖励变化。
-   **结论**：这张图清晰地表明，在使用初始训练数据进行强化学习训练时，模型“Ling-2.5-1T-Base”的奖励值随着训练步骤的增加而稳步提升。这验证了该方法的有效性，即模型能够通过强化学习从初始数据中学习并提高其性能。具体来说，图中显示了模型在训练初期奖励快速增长，随后进入一个持续但可能增速放缓的提升阶段，这对应了原文提到的“初始发现阶段”和“锐化阶段”。这表明模型的训练过程是有效的，并且模型能够通过这种训练方式获得更好的推理能力。

---

![(a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d](fig2_4.webp)

> (a) Reward (initial data) (b) Seq Length (initial data) (c) Reward (new data) (d) Seq Length (new data) Figure 2 : Training curves of Ling-2.5-1T-Base during first stage RL. (a,b) First 2800 steps with the initial training data: reward and sequence length increase steadily as the model bootstraps reasoning from scratch. (c,d) After switching to new training data, the model continues to improve with sustained sequence length growth.

这张图展示了Ling-2.5-1T-Base模型在第一阶段强化学习（RL）训练中的**序列长度（Sequence Length）**变化曲线，对应于原始caption中的子图(b)，即使用**初始训练数据**时的序列长度变化情况。

首先，我们来看图的各个组成部分：
*   **X轴（横轴）**：标记为“Step”，代表训练的步骤或迭代次数。从图中可以看到，X轴的范围大约从0到略超过600（因为右侧的峰值接近600的位置）。这表示模型在初始数据上的训练进度。
*   **Y轴（纵轴）**：标记为“Sequence Length”，代表模型生成的序列长度。Y轴的刻度从12000到18000，以1000为间隔。这衡量了模型在每次训练步骤中处理的token数量或输出的复杂度。
*   **曲线**：蓝色的折线图展示了随着训练步骤（Step）的增加，序列长度（Sequence Length）的变化趋势。

现在，我们来详细解读这张图所揭示的信息和方法运作方式：

1.  **初始阶段（从Step 0开始）**：
    *   在训练的早期阶段（大约从Step 0到Step 500之前），序列长度从大约12000开始，并呈现出一个总体上升的趋势，但伴随着一些波动。这表明模型在从零开始学习推理能力时，其生成的序列长度逐渐增加。这可能意味着模型正在学习更复杂的任务，或者其表达能力在逐步增强。
    *   这个阶段的“稳步增长”（如caption所述“increase steadily”）反映了模型在初始数据上进行自我引导（bootstraps reasoning from scratch）的过程。模型通过与环境（或训练数据）的交互，逐渐发现有效的策略来生成更长的、可能更有意义的序列。

2.  **中期阶段（大约Step 500前后）**：
    *   在Step 500左右，曲线出现了一些较为明显的波动，甚至有短暂的下降。这可能代表了模型在学习过程中的调整期，或者遇到了某些学习瓶颈。然而，即使有这些波动，整体的上升趋势仍然保持。

3.  **后期阶段（Step 500之后）**：
    *   在Step 500之后，序列长度的增长速度明显加快。曲线变得更加陡峭，表明模型在这一阶段能够生成显著更长的序列。这可能对应于模型能力的“锐化阶段”（sharpening phase），如caption中提到的训练过程的两个阶段：初始发现阶段（discovery phase）后跟着锐化阶段。
    *   到图的末尾，序列长度达到了接近18000的峰值，这显示了模型在初始数据上训练后期所达到的高复杂度输出能力。

**方法运作的理解**：
这张图展示了模型在第一阶段RL训练中，随着训练步骤的增加，其生成序列长度的动态变化。这种方法（即通过观察序列长度来评估训练进展）揭示了：
*   **自我引导学习**：模型能够从初始数据中开始学习，并逐步提高其生成的序列长度，这表明模型在进行自我引导的推理能力发展。
*   **阶段性进展**：训练过程并非线性平滑，而是经历了不同的阶段，包括初期的稳步增长、中期的调整波动，以及后期的快速提升。这验证了caption中提到的“训练过程按顺序经历初始发现阶段，然后是锐化阶段”的观点。
*   **能力提升**：序列长度的增加通常与模型处理更复杂任务的能力相关联。因此，这张图表明模型在初始数据上的训练是有效的，其推理能力在不断提升。

**结论**：
这张图清晰地展示了Ling-2.5-1T-Base模型在第一阶段使用初始训练数据进行RL训练时，序列长度随训练步骤增加而稳步增长的趋势，尤其是在训练后期出现了显著的增长加速。这验证了该方法在引导模型发展推理能力方面的有效性，并揭示了训练过程中存在的阶段性特征。

---

![(a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation o](fig3_1.webp)

> (a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation of CoT quality across three dimensions. (a) Comprehensibility: our model’s reasoning traces are judged to be more comprehensible than all baselines. (b) Reproducibility: distilling from our fewer CoT traces yields much stronger student models compared to DeepSeek-R1, highlighting a significantly higher sample efficiency for ability transfer. (c) Efficiency: our model solves problems using significantly fewer tokens.

这张图（图3c，对应“Efficiency”维度）展示了**我们的模型（Ours）与四个基线模型（MiniMax M2.7、GLM 5.1、Kimi K2.6、Qwen3.5 397B）在“推理效率”上的对比**，核心是比较“解决问题时使用的token数量”——token越少，效率越高。  

### 图的组件与信息流动：  
- **横轴方向**：每个模型的条形图由三部分组成，分别用颜色区分“Win（蓝色）、Tie（绿色）、Lose（红色）”，数值代表该类别下的对比次数（或样本数）。  
- **图例**：蓝色（Win）表示“我们的模型解决问题的token数少于基线模型”；绿色（Tie）表示“token数与基线模型相当”；红色（Lose）表示“token数多于基线模型”。  
- **对比逻辑**：对于每个基线模型，我们统计“我们的模型在token使用上赢、平、输”的次数。例如，MiniMax M2.7的条形图中，蓝色部分占78，绿色12，红色0（图中无红色）——这意味着在78次对比中，我们的模型token数更少；12次对比中token数相当；没有输的情况。  


### 方法的运作逻辑（从结果反推方法优势）：  
我们的方法（结合论文中的“zero RL”训练管道，如clipped importance sampling、训练-推理比校正、混合精度控制等）的目标是**提升推理效率**（即减少解决问题所需的token数）。从图中结果可见：  
- 对于MiniMax M2.7、GLM 5.1、Kimi K2.6、Qwen3.5 397B这四个基线，我们的模型在“Win”的次数上都远高于“Tie”或“Lose”（尤其是MiniMax M2.7和GLM 5.1，Win次数占比极高）。这说明**我们的模型在大多数对比中，解决问题的token数比基线更少**，验证了方法的效率优势。  


### 坐标、对比对象与结论：  
- **对比对象**：我们的模型 vs. 四个基线模型（MiniMax M2.7、GLM 5.1、Kimi K2.6、Qwen3.5 397B）。  
- **坐标（数值含义）**：每个条形图的数值是“对比次数”（或样本数），蓝色=赢（我们的token更少）、绿色=平（token相当）、红色=输（token更多）。  
- **结论**：  
  - MiniMax M2.7：78次赢，12次平，0次输→我们的模型在绝大多数对比中token更少。  
  - GLM 5.1：76次赢，14次平，0次输→效率优势明显。  
  - Kimi K2.6：72次赢，15次平，3次输→赢的次数仍占多数，仅少数情况token更多。  
  - Qwen3.5 397B：64次赢，22次平，4次输→赢的次数最多，平的次数也较多，但整体仍以赢为主。  

综上，这张图通过“token使用的赢/平/输次数对比”，直观展示了**我们的模型在推理效率上显著优于四个基线模型**——即解决问题时使用的token更少，验证了方法在“效率”维度的有效性。

---

![(a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation o](fig3_2.webp)

> (a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation of CoT quality across three dimensions. (a) Comprehensibility: our model’s reasoning traces are judged to be more comprehensible than all baselines. (b) Reproducibility: distilling from our fewer CoT traces yields much stronger student models compared to DeepSeek-R1, highlighting a significantly higher sample efficiency for ability transfer. (c) Efficiency: our model solves problems using significantly fewer tokens.

这张图（图3的某个子图，结合caption推测可能是“效率”或“可迁移性”相关的评估）展示了两种不同规模的基础模型（Qwen-32B和Llama-70B）在经过不同蒸馏方法处理后的**准确率（Accuracy）**表现，以此来验证“Ring-Zero-Distill”方法的优势。我们逐部分拆解：

### 图的组件与数据流动
- **横轴（X轴）**：展示了两个基础模型，分别是`Qwen-32B`（320亿参数）和`Llama-70B`（700亿参数）。这是被蒸馏的“学生模型”的基础版本。
- **纵轴（Y轴）**：表示`Accuracy`（准确率），范围从0到80，衡量模型在某项任务（推测是数学推理或类似需要链式思考的任务）上的表现。
- **图例（Legend）**：三种颜色/填充的柱形代表不同的方法：
  - 灰色（`Base`）：模型的“基础版本”，即未经过额外蒸馏的基础模型性能。
  - 深蓝色（`DeepSeek-R1-Distill`）：使用DeepSeek-R1方法蒸馏后的模型性能。
  - 浅蓝色（`Ring-Zero-Distill`）：使用本文提出的Ring-Zero-Distill方法蒸馏后的模型性能。
- **数据点**：每个模型-方法组合对应一个柱形，高度代表准确率。例如：
  - Qwen-32B的`Base`准确率为5.2，`DeepSeek-R1-Distill`为72.6，`Ring-Zero-Distill`为78.4。
  - Llama-70B的`Base`准确率为26.2，`DeepSeek-R1-Distill`为70.0，`Ring-Zero-Distill`为74.5。

### 方法的运作逻辑（从图中推断）
这张图通过**蒸馏（Distillation）**的过程展示方法的优势：蒸馏是一种知识迁移技术，将大模型（或高性能模型）的知识转移到小模型（或基础模型）中，以提升后者的性能。这里的“基础模型”（Base）性能较低，而经过不同蒸馏方法处理后，性能显著提升。我们的方法（Ring-Zero-Distill）与基线方法（DeepSeek-R1-Distill）对比，展示了更优的性能提升。

### 结果与结论（结合坐标、对比对象）
- **对比对象**：同一基础模型（Qwen-32B或Llama-70B）下，三种方法（Base、DeepSeek-R1-Distill、Ring-Zero-Distill）的准确率对比；以及不同基础模型（Qwen-32B vs Llama-70B）在相同方法下的表现。
- **结论**：
  1. **蒸馏的有效性**：对于两个基础模型，蒸馏后的模型（无论是DeepSeek-R1还是Ring-Zero）的准确率都远高于基础版本（Base）。例如，Qwen-32B的Base准确率仅5.2，而蒸馏后提升到72.6（DeepSeek）或78.4（Ring-Zero）；Llama-70B的Base准确率26.2，蒸馏后提升到70.0（DeepSeek）或74.5（Ring-Zero）。这说明蒸馏能显著提升基础模型的性能。
  2. **Ring-Zero-Distill的优势**：在相同的基础模型上，Ring-Zero-Distill的准确率高于DeepSeek-R1-Distill。例如，Qwen-32B上，Ring-Zero（78.4）比DeepSeek（72.6）高5.8；Llama-70B上，Ring-Zero（74.5）比DeepSeek（70.0）高4.5。这表明我们的方法在知识迁移（蒸馏）过程中更有效，能让学生模型获得更高的性能。
  3. **模型规模的差异**：Llama-70B（700亿参数）的基础准确率（26.2）远高于Qwen-32B（320亿参数，5.2），说明更大的基础模型在未蒸馏时可能有更好的初始性能，但蒸馏后两者的相对提升趋势一致，且我们的方法在大模型和小模型上都能带来显著提升。

总结来说，这张图通过准确率的对比，清晰地展示了**Ring-Zero-Distill方法在蒸馏过程中能更有效地提升基础模型的性能**，无论是小模型（Qwen-32B）还是大模型（Llama-70B），都比基线方法（DeepSeek-R1-Distill）表现更好，同时也验证了蒸馏作为一种知识迁移技术的有效性。

---

![(a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation o](fig3_3.webp)

> (a) Comprehensibility (b) Reproducibility (c) Efficiency Figure 3 : Evaluation of CoT quality across three dimensions. (a) Comprehensibility: our model’s reasoning traces are judged to be more comprehensible than all baselines. (b) Reproducibility: distilling from our fewer CoT traces yields much stronger student models compared to DeepSeek-R1, highlighting a significantly higher sample efficiency for ability transfer. (c) Efficiency: our model solves problems using significantly fewer tokens.

这张图（图3的子图(c) “Efficiency”）展示了不同模型在解决问题时**平均使用的Token数量**，以此衡量方法的效率——即我们的模型（Ours）相比基线模型，能用更少的Token解决问题。

### 图的结构与组件：
- **横轴（X轴）**：列出了不同的模型，包括GLM 5.1、MiniMax M2.7、Qwen3.5 397B、Kimi K2.6和我们的模型（Ours）。这些是对比的对象，其中前四个是基线模型，最后一个是本文提出的方法。
- **纵轴（Y轴）**：表示“平均Token数（Average Tokens）”，数值范围从0到约17000+，用于量化每个模型解决问题时消耗的Token量。Token可以理解为模型处理的基本单位（如单词或子词），Token数越少通常意味着推理过程更简洁、高效。
- **柱状图**：每个模型对应一个柱子，柱子的高度代表该模型的平均Token数。例如：
  - GLM 5.1的平均Token数约为17,220；
  - MiniMax M2.7约为16,627；
  - Qwen3.5 397B约为16,292；
  - Kimi K2.6约为14,115；
  - 我们的模型（Ours，蓝色柱子）仅为6,368。

### 方法的运作逻辑（从结果反推方法设计目标）：
这张图的结果表明，我们的方法（Ours）在**推理效率**上显著优于基线模型。结合论文背景（zero RL训练大规模模型以激发推理能力），我们的方法通过以下方式实现高效推理：
1. **算法优化**：如论文提到的“clipped importance sampling（裁剪重要性采样）”、“training-inference ratio correction（训练-推理比率校正）”和“mixed-precision control（混合精度控制）”，这些优化减少了推理过程中不必要的Token冗余，使模型能更简洁地生成推理轨迹。
2. **系统优化**：可能包括训练管道的稳定性和效率提升，确保模型在大规模训练后仍能高效推理，而不是陷入冗余的Token生成。

### 结论（从图中得出的关键信息）：
- 对比对象：我们的模型与四个基线模型（GLM 5.1、MiniMax M2.7、Qwen3.5 397B、Kimi K2.6）进行对比。
- 坐标与数值：纵轴是平均Token数，我们的模型的平均Token数（约6,368）远低于所有基线模型（基线模型的Token数均在14,000以上，甚至超过17,000）。
- 结论：我们的方法（Ours）在解决问题时**使用的Token数量显著更少**，这验证了方法在“效率（Efficiency）”维度上的优势——即能在更少的Token消耗下完成推理任务，体现了推理过程的简洁性和高效性。

---

![(a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 :](fig4_1.webp)

> (a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 : Comparison of RL algorithms on the flash model. CISPO and DAPO accelerate learning but suffer from greater instability. GSPO maintains high entropy but provides limited sequence length growth.

这张图（图4a）展示了四种强化学习（RL）算法——GRPO、CISPO、DAPO和GSPO——在“flash模型”上的“All-Failed Group Ratio”随训练步骤（Step）的变化情况。这个指标衡量的是在某个时间点，所有尝试都失败的任务组的比例。

**图的组成部分与信息流动：**

*   **横轴（X轴）：** 标记为“Step”，表示训练的步骤或迭代次数，范围从0到约3000。这代表了学习过程的时间进程。
*   **纵轴（Y轴）：** 标记为“All-Failed Group Ratio”，数值范围从0到1.0。值为1.0表示所有任务组都失败了，而值为0表示所有任务组都成功了。这个指标反映了算法在学习初期的探索难度或在后期对任务的掌握程度。
*   **四条曲线：** 分别代表四种不同的RL算法：
    *   **蓝色曲线（GRPO）：** 在训练初期（大约前500步），其“All-Failed Group Ratio”接近1.0，表明大部分任务都失败了。随后，这个比例迅速下降，在大约1000步时降至0.6以下，并在后续的训练中稳定在0.5左右的水平，有小幅波动。这表明GRPO在初期探索阶段遇到较大困难，但随着训练进行，成功率有所提升并趋于稳定。
    *   **红色曲线（CISPO）：** 初期表现与GRPO类似，All-Failed Group Ratio也接近1.0。然而，它在更早的阶段（大约在500到1000步之间）就开始快速下降，并在大约1500步后达到一个较低的稳定水平（约0.2到0.3）。这表明CISPO加速了学习过程，能够更快地减少失败率。
    *   **绿色曲线（DAPO）：** 其趋势与CISPO相似，但下降速度略慢于CISPO。它在初期也有一个高的失败率，然后在大约1000步后开始显著下降，并在后续训练中稳定在0.4左右的水平。这表明DAPO也能加速学习，但其稳定性可能不如CISPO或GSPO。
    *   **橙色曲线（GSPO）：** 在所有算法中，GSPO的“All-Failed Group Ratio”下降最为缓慢。它在整个训练过程中都保持在一个相对较高的水平（大约在0.4到0.5之间波动）。这表明GSPO的学习速度较慢，或者在训练过程中保持了较高的探索性，导致失败率较高。

**方法运作方式（基于图和caption的理解）：**

这张图通过比较不同RL算法在训练过程中“All-Failed Group Ratio”的变化，来评估它们的学习效率和稳定性。

*   **CISPO和DAPO：** 这两种算法能够显著加速学习过程（即更快地降低失败率），如红色和绿色曲线所示。然而，caption指出它们“suffer from greater instability”（遭受更大的不稳定性）。从图中可以看出，CISPO的曲线在后期有较大的波动（例如，在2000步之后有一个明显的上升），而DAPO的曲线虽然相对平滑一些，但其最终的失败率仍然高于GSPO。
*   **GSPO：** 这种算法的“All-Failed Group Ratio”下降较慢，如橙色曲线所示。caption指出它“maintains high entropy but provides limited sequence length growth”（保持高熵但序列长度增长有限）。高熵通常意味着更高的探索性或多样性，这可能解释了为什么它的失败率下降较慢，因为它可能在尝试更多的不同策略。然而，这种高探索性可能以牺牲序列长度的增长为代价，这可能与任务的复杂性或模型的表达能力有关。
*   **GRPO：** 作为对比基准，GRPO的学习过程相对平稳，但其学习速度和最终性能介于CISPO/DAPO和GSPO之间。

**结论：**

这张图清晰地展示了不同RL算法在训练过程中的学习动态差异。CISPO和DAPO能够加速学习，但可能伴随着更大的不稳定性。GSPO则表现出更高的探索性（高熵），但其学习速度较慢，且在序列长度增长方面表现有限。GRPO则提供了一个相对稳定的基准。这些观察结果对于选择合适的RL算法以训练大型模型（如论文中提到的“flash模型”）具有重要意义，特别是在需要平衡学习效率、稳定性和探索性的场景中。

---

![(a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 :](fig4_2.webp)

> (a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 : Comparison of RL algorithms on the flash model. CISPO and DAPO accelerate learning but suffer from greater instability. GSPO maintains high entropy but provides limited sequence length growth.

这张图（图4b）展示了四种强化学习（RL）算法在“flash模型”上的**奖励（Reward）随训练步数（Step）变化**的对比结果。我们可以通过以下几个部分来理解这张图：

### 图的结构与组件
- **横轴（X轴）**：标记为“Step”，表示训练的步骤数，范围从0到约3000。这代表了训练过程中时间或迭代的进展。
- **纵轴（Y轴）**：标记为“Reward”，表示模型在训练过程中获得的奖励值，范围从0到约1.2以上。奖励值越高，通常意味着模型的表现越好。
- **四条曲线**：每条曲线代表一种不同的RL算法，通过颜色和图例区分：
  - **蓝色曲线（GRPO）**：代表GRPO算法。
  - **红色曲线（CISPO）**：代表CISPO算法。
  - **绿色曲线（DAPO）**：代表DAPO算法。
  - **橙色曲线（GSPO）**：代表GSPO算法。

### 数据的流动与解读
- 每条曲线的走势展示了对应算法的奖励随训练步数的增加而变化的趋势。我们可以观察到：
  - **初始阶段（Step < 1000）**：所有算法的奖励都从接近0开始快速增长。其中，GSPO（橙色）、DAPO（绿色）和CISPO（红色）的增长速度较快，而GRPO（蓝色）的增长相对较慢，且在中间有一个小的波动（奖励短暂下降后回升）。
  - **中期阶段（1000 < Step < 2000）**：奖励继续增长并逐渐趋于稳定。GSPO、DAPO和CISPO的奖励在约1.2左右波动，而GRPO的奖励也在接近1.2的水平上稳定下来。
  - **后期阶段（Step > 2000）**：大多数算法的奖励保持在较高水平（约1.2以上），但CISPO（红色）在某个时刻出现了显著的下降（奖励突然降至约0.9以下），随后又恢复到较高水平。这体现了CISPO的不稳定性。

### 方法的运作方式（从图中推断）
这张图展示了不同RL算法在训练过程中的**学习动态**：
- **加速学习**：CISPO（红色）和DAPO（绿色）在初始阶段的奖励增长速度明显快于GRPO（蓝色），这表明它们能够更快地“发现”有效的策略，从而加速学习过程（这与caption中“CISPO and DAPO accelerate learning”一致）。
- **不稳定性**：CISPO的奖励在后期出现了显著的下降，这体现了其不稳定性（与caption中“suffer from greater instability”一致）。DAPO的曲线相对平滑，但也有轻微的波动。
- **熵与序列长度**：虽然这张图主要展示奖励，但结合caption中“GSPO maintains high entropy but provides limited sequence length growth”的描述，我们可以推断GSPO（橙色）可能在保持高熵（探索性）的同时，序列长度的增长有限。不过，这张图本身并未直接展示熵或序列长度，这些信息需要结合其他子图（如图4c和图4d）来理解。

### 对比对象与结论
- **对比对象**：四种RL算法（GRPO、CISPO、DAPO、GSPO）在同一模型（flash模型）上的训练表现。
- **结论**：
  - CISPO和DAPO能够加速学习（奖励快速增长），但CISPO表现出更大的不稳定性（奖励波动大）。
  - GSPO保持高熵（可能意味着更强的探索性），但序列长度的增长有限（这可能与图4d相关，但图中未直接展示）。
  - GRPO的学习速度较慢，但最终也能达到较高的奖励水平，并且相对稳定。

通过这张图，我们可以直观地比较不同RL算法在训练过程中的奖励变化，从而理解它们的学习效率、稳定性和最终性能。

---

![(a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 :](fig4_3.webp)

> (a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 : Comparison of RL algorithms on the flash model. CISPO and DAPO accelerate learning but suffer from greater instability. GSPO maintains high entropy but provides limited sequence length growth.

这张图（图4c）展示了四种不同的强化学习（RL）算法——GRPO、CISPO、DAPO和GSPO——在“flash模型”上训练过程中**熵（Entropy）**随**训练步数（Step）**变化的对比情况。理解这张图的关键在于分析每条曲线的趋势、峰值、波动以及它们之间的相对关系，从而揭示不同算法在训练动态上的特性。

首先，我们来看图的坐标轴：
*   **横轴（X轴）**：表示训练的“步数（Step）”，从0到大约3000步。这代表了训练过程中的时间进度或迭代次数。
*   **纵轴（Y轴）**：表示“熵（Entropy）”，数值范围从0到0.20。在强化学习的上下文中，熵通常用来衡量策略的随机性或多样性。高熵意味着策略在选择动作时更加随机或探索性更强，而低熵则意味着策略更加确定或利用性更强。

接下来，我们逐一分析图中的四条曲线，每条曲线代表一种算法：
1.  **GSPO（橙色曲线）**：
    *   从图中可以看出，GSPO的熵值在整个训练过程中相对较高，并且保持在一个较为稳定的水平。
    *   初始阶段（约0到500步），其熵值与其他算法相近或略高。
    *   随着训练的进行，GSPO的熵值虽然有所波动，但总体上维持在0.10到0.12之间，甚至在后期有轻微上升的趋势。
    *   这表明GSPO能够维持较高的策略多样性或探索性。

2.  **GRPO（蓝色曲线）**：
    *   GRPO的熵值在训练初期（约0到500步）迅速上升，达到了一个非常高的峰值（接近0.20）。
    *   然而，这个高峰值之后是剧烈的下降和显著的波动。
    *   到了训练后期（约1000步之后），GRPO的熵值逐渐降低并趋于稳定，但最终的熵值低于GSPO。

3.  **DAPO（绿色曲线）**：
    *   DAPO的熵值在训练初期也有一个明显的峰值，但峰值高度低于GRPO。
    *   随后，熵值迅速下降，并在后续的训练过程中持续缓慢下降，整体趋势较为平稳，最终达到最低的熵值水平。

4.  **CISPO（红色曲线）**：
    *   CISPO的熵值变化最为剧烈。
    *   初始阶段有一个小峰值，随后经历多次大幅度的波动，包括几次明显的上升和下降。
    *   整体来看，CISPO的熵值在训练过程中逐渐降低，但其波动性明显大于其他算法，尤其是在与DAPO和GSPO的比较中。

根据图中的信息和提供的caption，我们可以得出以下结论：
*   **GSPO**：正如caption所述，“GSPO maintains high entropy”。从图中可以清晰地看到，GSPO在整个训练过程中确实保持了相对较高的熵值，这意味着它可能在探索新策略或保持策略多样性方面表现较好，但caption也提到它“provides limited sequence length growth”（提供有限的序列长度增长），这可能意味着尽管探索性强，但在任务特定的性能提升（如生成更长、更有效的推理序列）方面可能不是最优的。
*   **CISPO和DAPO**：caption指出它们“accelerate learning but suffer from greater instability”。从图中看，CISPO和DAPO在训练初期都有熵的峰值，这可能意味着它们在早期阶段有较强的探索行为，从而加速了某些方面的学习。然而，CISPO的曲线波动性非常大，而DAPO的熵值在达到峰值后迅速且持续地下降，这都体现了“instability”（不稳定性）。这种不稳定性可能与它们的学习率、策略更新方式或其他算法特性有关。
*   **GRPO**：GRPO在初期表现出极高的熵值，这可能意味着它有非常强的探索性。随后熵值的急剧下降可能表明它快速地转向了利用已学到的策略。然而，这种剧烈的变化也可能导致训练过程的不稳定。

这张图通过展示不同RL算法在训练过程中熵的变化，揭示了它们在学习动态上的差异。例如，GSPO倾向于保持稳定的高探索性，而CISPO和DAPO则在早期有较强的探索但随后变得不稳定或探索性迅速降低。GRPO则表现出极端的探索-利用转变。这些特性对于选择适合特定任务的RL算法非常重要，尤其是在需要平衡探索与利用的场景中。图中的数据流向是从左到右，代表时间的推移，每条曲线展示了对应算法在每个训练步骤上的熵值。

---

![(a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 :](fig4_4.webp)

> (a) All-Failed Group Ratio (b) Reward (c) Entropy (d) Sequence Length Figure 4 : Comparison of RL algorithms on the flash model. CISPO and DAPO accelerate learning but suffer from greater instability. GSPO maintains high entropy but provides limited sequence length growth.

这张图（图4d）展示了四种强化学习（RL）算法——GRPO（蓝色）、CISPO（红色）、DAPO（绿色）和GSPO（橙色）——在“flash模型”上训练时，**序列长度（Sequence Length）**随**训练步骤（Step）**变化的对比情况。

首先，我们来看图的坐标轴：
- **横轴（X轴）**代表训练的**步骤（Step）**，范围从0到大约3000，表示训练过程的进展。
- **纵轴（Y轴）**代表**序列长度（Sequence Length）**，数值从0到4000，表示模型在每一步生成的序列（例如，推理链或动作序列）的长度。

接下来，我们分析每条曲线代表的算法及其行为：
1.  **GRPO（蓝色曲线）**：这条曲线在训练初期（大约前500步）迅速上升，达到一个峰值（接近4000），然后急剧下降，并在后续步骤中保持在一个较低且相对稳定的水平（大约在500以下）。这表明GRPO算法在早期可能尝试生成较长的序列，但很快这种行为被抑制或调整，导致序列长度显著减少并趋于稳定。
2.  **CISPO（红色曲线）**：这条曲线的行为最为波动。它也经历了一个初期的上升和下降，但随后在中间阶段（大约500到2000步之间）表现出明显的不稳定性，序列长度在波动中逐渐上升，最后在接近3000步时再次出现一个显著的峰值。这表明CISPO算法在学习过程中可能经历了较大的波动，但其序列长度在后期有增长的潜力。
3.  **DAPO（绿色曲线）**：这条曲线在初期也有一个上升，但峰值低于GRPO和CISPO。随后，它迅速下降并在一个相对较低的水平上稳定下来，其序列长度在整个训练过程中变化不大，保持在一个较低的稳定状态。
4.  **GSPO（橙色曲线）**：这条曲线在初期同样有一个上升，但其峰值是四条曲线中最低的。之后，它迅速下降并稳定在一个非常低的序列长度水平，且在后续训练步骤中几乎没有显著变化。

根据图的原始caption和我们的分析，可以得出以下结论：
-   **CISPO和DAPO**：这两种算法能够加速学习过程（可能在早期阶段表现较好），但它们也表现出更大的不稳定性（如CISPO的波动和DAPO的快速下降后稳定）。
-   **GSPO**：该算法能够维持较高的熵（虽然图中未直接显示熵，但caption提到这一点），这意味着它可能探索了更多的可能性或保持了策略的多样性。然而，GSPO提供的序列长度增长有限，其序列长度在训练过程中迅速下降并保持在较低水平。
-   **整体趋势**：所有算法在训练初期都表现出序列长度的增加，随后大多数算法的序列长度下降并趋于稳定。这可能反映了模型从探索阶段向利用阶段的转变，或者在训练过程中对序列长度的某种优化或约束。

这张图通过对比不同RL算法在训练过程中序列长度的变化，揭示了它们在学习和行为模式上的差异。例如，CISPO虽然不稳定但可能有更高的序列长度潜力，而GSPO则更注重稳定性但牺牲了序列长度的增长。这种分析有助于理解不同算法在特定任务（如这里的“flash模型”）上的表现和行为特征。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Ef](fig5_1.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Effect of KL penalty on training stability. Without KL (blue), the training-inference log-probability gap diverges, causing the reward to crash. With KL (red), all metrics remain healthy.

这张图（图5(a)）的核心是展示**KL惩罚（Kullback-Leibler penalty）对训练稳定性的影响**，通过“对数概率差（Log-Prob Difference）”这一指标来量化训练与推理过程的对齐程度。  

### 图的组件与信息流动  
- **横轴（Step）**：表示训练的步骤（从0到3000左右），代表训练的时间进程。  
- **纵轴（Log-Prob Difference）**：衡量“训练时的对数概率”与“推理时的对数概率”之间的差异。这个差异反映了模型在训练和推理阶段的行为一致性——差异越小，说明训练和推理的对齐度越高，训练越稳定。  
- **两条曲线**：  
  - 蓝色曲线（`w/o KL`，“无KL惩罚”）：代表训练过程中**不使用KL惩罚**时，对数概率差随训练步骤的变化。  
  - 红色曲线（`w/ KL`，“有KL惩罚”）：代表训练过程中**使用KL惩罚**时，对数概率差随训练步骤的变化。  


### 方法的运作逻辑（从图中理解KL惩罚的作用）  
KL惩罚是一种正则化手段，用于约束模型的输出分布（或概率行为），避免训练过程中出现“训练-推理不一致”的问题。从图中可以直观看到：  
- 当**没有KL惩罚**（蓝色曲线）时，在训练后期（约2500步之后），对数概率差突然急剧上升（甚至接近0.4）。这说明训练和推理的对齐度被破坏，模型可能出现“训练时表现好但推理时崩溃”的情况（结合caption的补充：“奖励崩溃”）。  
- 当**有KL惩罚**（红色曲线）时，对数概率差始终保持在很低的水平（接近0），说明训练和推理的行为高度一致，训练过程稳定。  


### 坐标、对比对象与结论  
- **坐标范围**：横轴（Step）从0到3000，纵轴（Log-Prob Difference）从0到0.4。  
- **对比对象**：蓝色（无KL） vs. 红色（有KL）。  
- **结论**：KL惩罚能有效稳定训练过程——无KL时，训练-推理的对数概率差会“发散”（导致奖励崩溃）；有KL时，所有指标（包括对数概率差）都保持“健康”（即稳定、低差异）。这验证了KL惩罚在训练大规模零样本强化学习（zero RL）模型时的必要性，确保训练过程的稳定性，避免因训练-推理不一致导致的性能崩溃。  


简单来说，这张图用“对数概率差”的变化，清晰展示了**KL惩罚如何通过约束概率分布，让训练和推理过程保持对齐，从而提升训练稳定性**。无KL时训练后期会出现严重的对齐问题，而有KL时训练全程稳定。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Ef](fig5_2.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Effect of KL penalty on training stability. Without KL (blue), the training-inference log-probability gap diverges, causing the reward to crash. With KL (red), all metrics remain healthy.

这张图（图5b）展示了在强化学习（特别是零RL，即无人工标注数据的强化学习）训练过程中，**KL惩罚（Kullback-Leibler penalty）对模型输出熵（Entropy）的影响**，从而揭示了训练稳定性。

首先，我们来看图的各个组成部分：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤或迭代次数，范围从大约0到3000。这表示训练过程的时间进程。
- **纵轴（Y轴）**：标记为“Entropy”，代表模型输出的概率分布的熵值。熵值越高，表示模型对输出的不确定性越大，或者说输出分布越均匀；熵值越低，表示模型对某个输出的确定性越高。
- **两条曲线**：
    - **蓝色曲线（标记为“w/o KL”）**：代表在没有使用KL惩罚的情况下，模型熵随训练步骤的变化。
    - **红色曲线（标记为“w/ KL”）**：代表在使用了KL惩罚的情况下，模型熵随训练步骤的变化。

接下来，我们分析这两条曲线的变化趋势和对比：
- **没有KL惩罚（蓝色曲线）**：在训练初期，熵值有一个上升的趋势，达到一个峰值后开始逐渐下降。在大约2000步之后，熵值急剧下降到一个非常低的水平，然后在接近3000步时又突然急剧上升。这种剧烈的波动表明，在没有KL惩罚的情况下，模型的训练过程可能变得不稳定，熵的变化缺乏一致性。
- **有KL惩罚（红色曲线）**：在整个训练过程中，熵值保持在一个相对较高的水平，并且波动较小。虽然在某些点（如1000步左右和2000步左右）有一些小的波动，但整体上熵值维持在一个稳定的范围内，大约在0.10到0.12之间。

这张图揭示了KL惩罚在训练过程中的作用：
- **训练稳定性**：KL惩罚有助于维持模型输出熵的稳定性。在没有KL惩罚的情况下，熵的变化剧烈，可能导致训练过程不稳定，甚至影响模型的性能（如奖励崩溃）。而使用KL惩罚后，熵的变化更加平稳，表明训练过程更加稳定。
- **模型行为**：熵的稳定性可能反映了模型在学习过程中对输出的确定性或不确定性的控制。较高的熵值可能表示模型在探索不同的输出选项，而较低的熵值可能表示模型在利用已学到的知识。KL惩罚可能帮助模型在探索和利用之间找到一个平衡，从而提高训练的稳定性和效果。

结合论文的摘要和图的原始caption，我们可以得出以下结论：
- **训练稳定性**：KL惩罚对于维持训练过程的稳定性至关重要。在没有KL惩罚的情况下，训练过程可能出现不稳定的现象（如熵的剧烈波动），而在使用KL惩罚的情况下，训练过程更加稳定。
- **方法运作**：通过引入KL惩罚，模型能够在训练过程中保持输出熵的稳定性，从而避免训练过程的崩溃。这可能是论文中提到的“稳定高效的训练管道”的一部分，该管道包括算法和系统优化（如裁剪重要性采样、训练-推理比率校正和混合精度控制），以提高训练的稳定性和效率。
- **结论**：KL惩罚有助于提高零RL训练的稳定性，使得模型能够在更大的规模上进行训练，并表现出更好的性能和涌现能力。

总之，这张图通过对比有无KL惩罚情况下模型熵的变化，清晰地展示了KL惩罚在维持训练稳定性方面的重要作用。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Ef](fig5_3.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Effect of KL penalty on training stability. Without KL (blue), the training-inference log-probability gap diverges, causing the reward to crash. With KL (red), all metrics remain healthy.

这张图（图5c）展示了在强化学习（特别是零RL，即无人工标注数据的强化学习）训练过程中，**序列长度（Sequence Length）**随**训练步骤（Step）**的变化情况，并对比了**使用KL惩罚（w/ KL，红色曲线）**和**不使用KL惩罚（w/o KL，蓝色曲线）**两种情况下的训练稳定性。

### 图中组件解释：
- **横轴（X轴）**：表示训练的**步骤（Step）**，范围从0到3000，代表训练过程的时间推进。
- **纵轴（Y轴）**：表示**序列长度（Sequence Length）**，即模型在每一步生成的序列（如推理链、回答）的token数量，范围从0到20000，反映模型输出的长度变化。
- **两条曲线**：
  - 蓝色曲线（w/o KL）：代表**不使用KL惩罚**的训练过程。可以看到，这条曲线波动较大，尤其是在后期（约2500步之后）出现了一个急剧的峰值（接近20000），然后又快速下降，整体稳定性较差。
  - 红色曲线（w/ KL）：代表**使用KL惩罚**的训练过程。这条曲线的波动相对平缓，整体呈上升趋势后趋于稳定，没有出现蓝色曲线那样的剧烈波动或异常峰值。

### 方法运作机制（从图中揭示）：
- **KL惩罚的作用**：KL惩罚（Kullback-Leibler divergence penalty）是一种正则化技术，用于约束模型的输出分布与目标分布（或之前的分布）之间的差异。在这张图中，使用KL惩罚（红色曲线）的训练过程显示出更稳定的序列长度变化，说明KL惩罚有助于**抑制训练过程中的不稳定因素**（如输出长度的剧烈波动），从而提高训练的稳定性。
- **无KL惩罚的问题**：不使用KL惩罚（蓝色曲线）时，序列长度在后期出现急剧的峰值和波动，这可能导致训练过程的不稳定（如奖励崩溃，如caption中提到的“reward to crash”）。这表明，KL惩罚对于维持训练的稳定性至关重要，尤其是在大规模模型训练中（如论文中提到的1万亿参数模型）。

### 结果分析（坐标、对比对象和结论）：
- **坐标范围**：X轴（Step）从0到3000，Y轴（Sequence Length）从0到20000。
- **对比对象**：蓝色曲线（w/o KL）和红色曲线（w/ KL）。
- **结论**：
  - 使用KL惩罚（w/ KL）的训练过程中，序列长度的变化更加平稳，没有出现剧烈的波动或异常峰值，说明KL惩罚有助于**提高训练的稳定性**。
  - 不使用KL惩罚（w/o KL）的训练过程中，序列长度在后期出现急剧的波动和峰值，导致训练不稳定（如caption中提到的“reward to crash”）。
  - 这验证了论文中的发现：KL惩罚对于大规模零RL训练的稳定性至关重要，能够避免训练过程中的不稳定因素（如输出长度的剧烈波动），从而保证训练的健康进行（如caption中提到的“all metrics remain healthy”）。

总结来说，这张图通过对比使用和不使用KL惩罚的训练过程中序列长度的变化，清晰地展示了KL惩罚在提高训练稳定性方面的作用：使用KL惩罚可以使训练过程更加平稳，避免输出长度的剧烈波动，从而保证训练的健康进行。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Ef](fig5_4.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 5 : Effect of KL penalty on training stability. Without KL (blue), the training-inference log-probability gap diverges, causing the reward to crash. With KL (red), all metrics remain healthy.

这张图（图5d）展示了在强化学习训练过程中，**KL惩罚（Kullback-Leibler penalty）对训练稳定性的影响**，特别是它如何影响“奖励（Reward）”这一关键指标随训练步骤（Step）的变化。

首先，我们来看图的各个组成部分：

1.  **坐标轴**：
    *   **横轴（X轴）**：标记为“Step”，代表训练的步骤或迭代次数。从图中可以看到，范围大约是从0到3000步。这表示训练过程随着时间的推移而进行。
    *   **纵轴（Y轴）**：标记为“Reward”，代表模型在训练过程中获得的奖励值。奖励值越高，通常意味着模型的表现越好或学到的策略越优。纵轴的范围大约是从0.8到1.6。

2.  **曲线**：
    *   **蓝色曲线（标记为“w/o KL”）**：这条曲线代表了**没有使用KL惩罚**的训练情况。“w/o”是“without”的缩写。
    *   **红色曲线（标记为“w/ KL”）**：这条曲线代表了**使用了KL惩罚**的训练情况。“w/”是“with”的缩写。

3.  **数据流动与趋势**：
    *   **蓝色曲线（w/o KL）**：在训练的大部分时间里（大约前2500步），这条曲线的奖励值相对稳定，维持在1.3到1.4左右，并伴随一些正常的波动。然而，在接近2500步到3000步的某个点，这条曲线突然急剧下降，奖励值从一个较高的水平（约1.4）骤降至一个非常低的水平（约0.9以下）。这种突然的“崩溃”表明，没有KL惩罚的训练过程在后期变得不稳定，导致模型性能急剧下降。
    *   **红色曲线（w/ KL）**：这条曲线在整个训练过程中（从0到3000步）表现出更高的稳定性和一致性。奖励值从初始的约1.3左右开始，随着训练步骤的增加，总体上呈现出缓慢上升的趋势，最终在3000步时接近1.6。虽然也存在一些波动，但这些波动是正常的，并且奖励值始终保持在较高水平，没有出现像蓝色曲线那样的崩溃现象。

**这张图揭示的方法运作方式（即KL惩罚的作用）**：

*   **KL惩罚的目的**：KL惩罚是一种正则化技术，常用于防止模型过拟合或在生成模型（如语言模型）中确保生成的序列与目标分布保持一致。在这篇论文的上下文中，它被用来提高“零RL”（zero RL）训练的稳定性。
*   **没有KL惩罚（蓝色曲线）**：当不使用KL惩罚时，模型在训练后期可能会“偏离”其预期的行为或分布。这种偏离导致训练-推理的对数概率差距（log-probability gap）发散（如caption所述），进而使得奖励急剧下降。这表明训练过程变得不稳定，模型可能无法继续有效地学习或保持其性能。
*   **有KL惩罚（红色曲线）**：当使用KL惩罚时，它起到了一种“约束”或“引导”的作用，使模型的训练过程更加稳定。这使得奖励能够持续增长或至少保持在较高水平，避免了崩溃。这说明KL惩罚有助于维持训练的稳定性，从而允许模型在更大的规模上学习和表现出更好的性能。

**结论**：

这张图通过对比有无KL惩罚的两种训练情况，清晰地展示了KL惩罚对于提高“零RL”训练稳定性的重要性。具体来说：

*   **对比对象**：蓝色曲线（无KL惩罚）与红色曲线（有KL惩罚）。
*   **坐标**：横轴为训练步骤（Step），纵轴为奖励（Reward）。
*   **结论**：没有KL惩罚的训练（蓝色曲线）在后期会出现奖励的急剧下降（崩溃），表明训练不稳定。而有KL惩罚的训练（红色曲线）则表现出更健康、更稳定的奖励增长趋势。因此，KL惩罚对于确保大规模“零RL”训练的稳定性和有效性至关重要，正如论文摘要中提到的，它是实现稳定高效训练管道的关键优化之一。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Co](fig6_1.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Comparison of ratio correction strategies. The baseline (blue) collapses within 800 steps. IcePop (green) delays the collapse but ultimately fails. Our approach (red) maintains stable training completely.

这张图（图6a）展示了不同训练策略在“对数概率差异”（Log-Prob Difference）指标上随训练步骤（Step）的变化情况，用于比较不同的比率校正策略对训练稳定性的影响。

首先，我们来看图的各个组成部分：
- **横轴（X轴）**：表示训练的步骤（Step），范围从0到3000。这代表了训练过程中的时间进度或迭代次数。
- **纵轴（Y轴）**：表示对数概率差异（Log-Prob Difference）。这个指标可能衡量了模型预测的概率分布与某种目标分布之间的差异，差异越大可能意味着模型的不稳定或崩溃程度越高。
- **三条曲线**：分别代表三种不同的训练策略：
  - **蓝色曲线（Baseline）**：代表基准方法或基线策略。从图中可以看到，这条曲线在大约800步时急剧上升，表明模型在此时发生了崩溃（collapse）。这意味着基线方法在训练过程中很快变得不稳定。
  - **绿色曲线（+ IcePop）**：代表使用了IcePop方法的策略。这条曲线在初始阶段保持平稳，但最终还是出现了上升，表明IcePop方法虽然延迟了崩溃的发生，但最终未能避免模型崩溃。
  - **红色曲线（+ Ours）**：代表作者提出的方法。这条曲线在整个训练过程中（直到3000步）几乎保持在0附近，表明作者的方法能够完全维持稳定的训练，避免了崩溃。

接下来，我们分析这张图揭示的方法运作方式：
- 基线方法（蓝色）在训练早期就出现了崩溃，说明这种方法在训练过程中存在稳定性问题。
- IcePop方法（绿色）虽然在一定程度上延迟了崩溃，但最终还是失败了，这表明IcePop方法虽然有所改进，但仍然不足以保证长期的训练稳定性。
- 作者提出的方法（红色）在整个训练过程中保持了稳定的对数概率差异，说明这种方法通过某种机制（可能是文中提到的算法和系统优化，如裁剪重要性采样、训练-推理比率校正和混合精度控制等）有效地避免了模型崩溃，实现了稳定的训练。

最后，我们总结这张图的结论：
- 基准方法（Baseline）在训练过程中很快崩溃，无法维持稳定的训练。
- IcePop方法虽然延迟了崩溃，但最终仍然失败。
- 作者提出的方法（Ours）能够完全维持稳定的训练，避免了崩溃，显示出更好的训练稳定性。

这张图通过对比不同方法在对数概率差异指标上的表现，清晰地展示了作者提出的方法在训练稳定性方面的优势。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Co](fig6_2.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Comparison of ratio correction strategies. The baseline (blue) collapses within 800 steps. IcePop (green) delays the collapse but ultimately fails. Our approach (red) maintains stable training completely.

这张图（图6b）展示了在强化学习（特别是零RL，即无人工标注数据的可验证奖励强化学习）的训练过程中，不同策略下模型输出的熵（Entropy）随训练步骤（Step）的变化情况。图的横轴是训练步骤（Step），从0到3000；纵轴是熵（Entropy），范围从0.02到0.12。

图中有三条曲线，分别代表三种不同的策略：
- 蓝色曲线（Baseline）：代表基准方法（未使用本文提出的改进策略）。从图中可以看到，这条曲线在大约800步时急剧下降并崩溃（collapse），熵值迅速降低到很低的水平，之后保持在低位波动，说明基准方法在训练早期就出现了不稳定的情况，无法持续有效训练。
- 绿色曲线（+ IcePop）：代表使用了IcePop策略的方法。这条曲线在初期（约0到2000步）的熵值较高且波动较大，虽然延迟了崩溃的发生（相比基准方法，它在2000步之后才开始明显下降），但最终还是失败了（熵值大幅下降），说明IcePop策略虽然能在一定程度上缓解崩溃，但无法完全避免训练的不稳定。
- 红色曲线（+ Ours）：代表使用了本文提出的方法（“Ours”）。这条曲线在整个训练过程中（从0到3000步）都保持了相对稳定的熵值，虽然在某些步骤有波动，但整体上没有出现崩溃的情况，说明本文的方法能够维持稳定的训练过程。

从这张图中我们可以得出结论：基准方法（蓝色）在训练早期（约800步内）就会崩溃；IcePop方法（绿色）虽然能延迟崩溃，但最终还是会失败；而本文提出的方法（红色）能够完全维持稳定的训练，不会崩溃。这验证了本文方法在训练稳定性方面的优势，能够解决零RL在大模型训练中可能出现的训练不稳定问题，为后续的模型训练和推理能力的涌现提供了稳定的训练环境。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Co](fig6_3.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Comparison of ratio correction strategies. The baseline (blue) collapses within 800 steps. IcePop (green) delays the collapse but ultimately fails. Our approach (red) maintains stable training completely.

这张图（图6c）展示了在强化学习（特别是零RL，即无人工标注数据的可验证奖励强化学习）训练过程中，**不同策略下序列长度（Sequence Length）随训练步骤（Step）的变化情况**，用于比较“基线（Baseline）”、“+ IcePop”和“+ Ours（我们的方法）”三种方法的训练稳定性。

### 图的组件与信息流动：
- **横轴（X轴）**：代表训练的“步骤（Step）”，从0到3000，展示了训练过程的时间推进。
- **纵轴（Y轴）**：代表“序列长度（Sequence Length）”，数值从0到17500，反映了模型在训练中生成的序列（如推理链、动作序列等）的长度变化。
- **三条曲线**：
  - 蓝色曲线（Baseline）：代表“基线”方法，即未使用我们提出的优化策略的训练过程。从图中可见，该曲线在约800步时急剧下降（“崩溃”），序列长度大幅降低，说明基线方法在训练中很快出现不稳定，无法持续有效训练。
  - 绿色曲线（+ IcePop）：代表使用了“IcePop”策略的方法。该曲线的序列长度在前期有波动，但最终在约2000步前也出现了明显的下降趋势，说明IcePop策略虽然延迟了崩溃，但最终仍未能维持稳定训练。
  - 红色曲线（+ Ours）：代表使用了“我们的方法”的训练过程。该曲线的序列长度在整个训练步骤（0到3000步）中保持相对稳定，即使在高步骤（如2000步后）仍有较高的序列长度，且没有出现基线和IcePop那样的崩溃现象。

### 方法的运作方式（从图中推断）：
我们的方法（红色曲线）通过**算法和系统优化**（如论文中提到的clipped importance sampling、training-inference ratio correction、mixed-precision control等），解决了基线和IcePop方法中的训练不稳定问题。具体来说：
- 基线方法可能因为缺乏这些优化，在训练中很快出现“崩溃”（序列长度骤降），这可能是因为奖励信号的处理不当、梯度爆炸/消失或其他训练不稳定的因素。
- IcePop方法尝试解决这些问题，但我们的方法通过更有效的优化（如ratio correction策略的改进），使得训练过程在整个步骤范围内保持稳定，序列长度能够持续维持在较高水平，说明模型能够持续学习并生成有效的序列（如推理链）。

### 结果与结论：
- **坐标与对比对象**：横轴是训练步骤（0-3000），纵轴是序列长度（0-17500）。对比对象是三种方法：基线（蓝色）、IcePop（绿色）和我们的方法（红色）。
- **结论**：
  - 基线方法（蓝色）在约800步时“崩溃”（序列长度急剧下降），无法维持稳定训练。
  - IcePop方法（绿色）延迟了崩溃，但最终在约2000步前也失败（序列长度显著下降）。
  - 我们的方法（红色）在整个训练过程中（0-3000步）保持了**稳定的训练**，序列长度没有出现崩溃，说明我们的方法能够有效解决训练不稳定的问题，支持大规模模型（如万亿参数模型）的训练。

这张图清晰地展示了我们的方法在训练稳定性方面的优势，验证了论文中提到的“ratio correction策略”的有效性，即我们的方法能够避免训练崩溃，维持稳定的训练过程，从而为大规模零RL模型的训练提供了可靠的训练管道。

---

![(a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Co](fig6_4.webp)

> (a) Log-Prob Difference (b) Entropy (c) Sequence Length (d) Reward Figure 6 : Comparison of ratio correction strategies. The baseline (blue) collapses within 800 steps. IcePop (green) delays the collapse but ultimately fails. Our approach (red) maintains stable training completely.

这张图（图6d）展示了不同比率校正策略在强化学习训练过程中**奖励（Reward）随训练步骤（Step）的变化情况**，用于比较这些策略的训练稳定性和性能表现。

### 图的组件与信息流动：
- **横轴（X轴）**：代表训练的“步骤（Step）”，从0到3000，展示了训练过程的时间维度，即模型在不同训练阶段的表现。
- **纵轴（Y轴）**：代表“奖励（Reward）”，数值范围约为0.8到1.4，奖励越高通常表示模型的表现越好（例如在任务中获得的反馈更优）。
- **三条曲线**：分别对应三种不同的方法（策略）：
  - **蓝色曲线（Baseline）**：代表“基线”方法（没有使用本文提出的比率校正策略或其他改进策略）。从图中可以看到，这条曲线在约800步时急剧下降（“collapse”），说明基线方法在训练中很快出现了性能崩溃，无法稳定训练。
  - **绿色曲线（+ IcePop）**：代表使用了“IcePop”方法的策略。这条曲线在初始阶段（前约2000步）的奖励较高且相对稳定，但在接近3000步时也出现了明显的下降（崩溃），说明IcePop方法虽然延迟了崩溃，但最终还是无法维持稳定的训练。
  - **红色曲线（+ Ours）**：代表使用了本文提出的“我们的方法”的策略。这条曲线在整个训练过程中（从0到3000步）始终保持较高的奖励，并且没有出现崩溃的情况，说明该方法能够实现完全稳定的训练。

### 方法的运作方式（从图中结果推断）：
- 基线方法（蓝色）：由于没有有效的比率校正策略，在训练过程中（约800步后）性能急剧下降，可能是因为训练不稳定（例如梯度爆炸、策略更新不恰当等），导致模型无法继续有效学习。
- IcePop方法（绿色）：通过某种比率校正策略，暂时提高了训练的稳定性（延迟了崩溃），但最终仍然失败，可能是因为其策略在长期训练中存在缺陷（例如无法适应模型的规模增长或任务的复杂性）。
- 本文的方法（红色）：通过设计的比率校正策略（结合其他优化，如clipped importance sampling、training-inference ratio correction、mixed-precision control等），能够在整个训练过程中保持稳定的奖励，说明该方法有效地解决了训练不稳定的问题，使模型能够持续学习并保持高性能。

### 结论（从图中结果得出）：
- 基线方法（无有效比率校正）在训练早期（约800步）就崩溃，无法稳定训练。
- IcePop方法虽然延迟了崩溃，但最终仍无法维持稳定训练。
- 本文提出的方法（+ Ours）能够在整个训练过程中（3000步）保持稳定的高奖励，证明其比率校正策略（结合其他优化）能够有效解决训练不稳定的问题，实现稳定的训练过程。

这张图通过对比三种方法的奖励-步骤曲线，清晰地展示了本文方法在训练稳定性方面的优势，验证了其在大规模强化学习训练中的有效性。

---

![(a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A cau](fig7_1.webp)

> (a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A causes uncontrolled length growth without reward improvement. Format B ensures proper stopping. (c) Sequence Length (d) Reward Figure 8 : Window size comparison. The 32k window produces much longer responses than the 16k window, but only marginally improves the reward, demonstrating severe token redundancy.

这张图（图7a）展示了**不同奖励格式（Format A vs Format B）对序列长度（Sequence Length）随训练步骤（Step）变化的影响**，用于说明奖励格式设计如何影响模型的输出行为。

### 图的组件与信息流动：
- **横轴（X轴）**：代表训练的“步骤（Step）”，从0到400，展示了训练过程中模型行为随时间（步骤）的演变。
- **纵轴（Y轴）**：代表“序列长度（Sequence Length）”，即模型输出的token数量，范围从0到14000，衡量模型输出的“长度”或“冗余度”。
- **两条曲线**：
  - 红色曲线（Format A）：代表使用“格式A”奖励时的序列长度变化。随着步骤增加，序列长度**持续增长**，从约3000左右上升到超过8000，且没有明显的停止或下降趋势。
  - 蓝色曲线（Format B）：代表使用“格式B”奖励时的序列长度变化。序列长度先增长（到约200步时达到约4500），然后**显著下降**，最终稳定在一个较低的水平（约1000以下）。

### 方法的运作逻辑（从图中揭示的方法设计）：
这张图展示了**奖励格式如何引导模型的输出长度（即推理过程的“长度”或“冗余度”）**：
- **Format A的问题**：它导致模型输出长度“无控制的增长”（uncontrolled length growth）。即使训练步骤增加，模型也不会“停止”输出（或缩短输出），可能意味着模型在Format A的奖励下，会持续生成冗余的token，而没有学到“何时停止”的逻辑。
- **Format B的优势**：它确保模型“适当的停止”（proper stopping）。模型在初始阶段（前200步左右）增长输出长度，之后能“收缩”并稳定在较短的长度，说明Format B的奖励机制让模型学会了“在合适的时候停止输出”，避免了无意义的冗余。

### 坐标、对比对象与结论：
- **坐标**：X轴（Step）：0-400；Y轴（Sequence Length）：0-14000。
- **对比对象**：两种奖励格式（Format A和Format B）。
- **结论**：
  - Format A会导致**无控制的长度增长**，且没有伴随奖励的改善（结合图名“Format reward comparison”和caption，可推断Format A的奖励设计没有有效引导模型优化，反而让输出长度失控）。
  - Format B能**确保适当的停止**，即模型输出长度在增长后能合理收缩，说明Format B的奖励机制更有效地控制了模型的输出行为（如避免冗余、学会停止）。

简单来说，这张图通过对比两种奖励格式下的序列长度变化，展示了**奖励格式设计对模型输出长度（冗余度）的关键影响**：Format A让模型输出越来越长（无控制），而Format B让模型输出先增长后稳定（适当停止），验证了“奖励格式需要引导模型学会合理的输出长度”的设计逻辑。

---

![(a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A cau](fig7_2.webp)

> (a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A causes uncontrolled length growth without reward improvement. Format B ensures proper stopping. (c) Sequence Length (d) Reward Figure 8 : Window size comparison. The 32k window produces much longer responses than the 16k window, but only marginally improves the reward, demonstrating severe token redundancy.

这张图（图7b）展示了两种不同格式（Format A和Format B）在强化学习训练过程中，奖励（Reward）随训练步骤（Step）变化的对比情况。

首先，我们来看图的各个组成部分：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤或迭代次数，范围从0到400。这表示训练过程是按步骤进行的，随着步骤的增加，模型在不断学习和优化。
- **纵轴（Y轴）**：标记为“Reward”，代表模型获得的奖励值，范围从0.0到1.0以上。奖励值越高，通常表示模型的表现越好，或者更接近目标行为。
- **两条曲线**：
    - 红色曲线代表“Format A”。
    - 蓝色曲线代表“Format B”。
- **图例**：在图的右下角，明确标注了红色曲线对应Format A，蓝色曲线对应Format B，方便读者区分。

接下来，我们分析图中的数据流动和信息展示方式：
- 随着训练步骤（Step）的增加，两种格式的奖励值都呈现出上升的趋势，这表明模型在训练过程中逐渐学习到了更好的行为，从而获得更高的奖励。
- 在训练的早期阶段（大约0到100步左右），Format A的奖励增长速度相对较快，其曲线在早期高于Format B的曲线。这可能意味着Format A在初始阶段更容易让模型获得一些基本的奖励。
- 然而，随着训练步骤的进一步增加（超过100步后），Format B的奖励增长速度超过了Format A，并且在后续的训练中（大约200步之后），Format B的奖励值持续高于Format A，并且最终趋于稳定在1.0左右，而Format A的奖励值虽然也趋于稳定，但略低于Format B。

然后，我们结合图的原始caption来理解这张图揭示的方法运作方式和结论：
- 这张图是一个结果图，用于比较两种不同的格式（Format A和Format B）在强化学习训练中的表现。
- 从图中可以看出，Format A在训练初期奖励增长较快，但随后奖励增长停滞，并且可能导致序列长度不受控制地增长（根据caption的描述：“Format A causes uncontrolled length growth without reward improvement”）。这意味着Format A虽然能让模型在早期获得一些奖励，但无法有效提高奖励的上限，并且可能导致生成的序列（比如回答或推理过程）长度过长，而没有相应的奖励提升。
- 相比之下，Format B的奖励增长曲线在后期超过了Format A，并且最终奖励值更高且更稳定。同时，根据caption的描述，Format B能够确保适当的停止（“Format B ensures proper stopping”）。这表明Format B不仅能让模型获得更高的奖励，还能控制序列的长度，避免无限制的增长，从而在奖励和序列长度之间取得更好的平衡。
- 从训练动态的角度来看，这张图展示了两种格式在训练过程中的不同表现：Format A可能在早期有一定的优势，但长期来看，Format B的表现更好，因为它能在训练过程中不断提高奖励，并且控制序列长度，避免了Format A中出现的问题（如无控制的长度增长和奖励停滞）。

总结来说，这张图通过对比两种格式（Format A和Format B）在强化学习训练中的奖励随步骤的变化，揭示了Format B在奖励提升和序列长度控制方面的优势。具体来说，Format B能够确保模型在训练过程中获得更高的奖励，并且避免无控制的长度增长，从而实现了适当的停止。而Format A虽然在早期奖励增长较快，但后续奖励增长停滞，并且可能导致序列长度不受控制地增长，无法有效提高奖励上限。

---

![(a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A cau](fig7_3.webp)

> (a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A causes uncontrolled length growth without reward improvement. Format B ensures proper stopping. (c) Sequence Length (d) Reward Figure 8 : Window size comparison. The 32k window produces much longer responses than the 16k window, but only marginally improves the reward, demonstrating severe token redundancy.

这张图（图8）展示了在“Ring-Zero”研究中，不同窗口大小（window size）对序列长度（Sequence Length）随训练步骤（Step）变化的影响。我们先看图表的基本构成：

- **横轴（X轴）**：代表训练的“Step”（步骤），范围从0到2000，展示了训练过程中不同阶段的情况。
- **纵轴（Y轴）**：代表“Sequence Length”（序列长度），即模型生成的响应或推理过程的长度，数值从0到17500，用于衡量输出的规模。
- **两条曲线**：
  - 蓝色曲线代表“16k window”（16千窗口大小）的情况，即模型在训练或推理时使用的窗口大小为16k。
  - 红色曲线代表“32k window”（32千窗口大小）的情况，窗口大小为32k。

接下来分析数据和趋势：

1. **初始阶段（Step 0到约500）**：两条曲线的序列长度都较低，且增长缓慢，说明在训练初期，无论窗口大小如何，模型的输出长度都较小，可能处于学习或适应的初始阶段。
2. **中期阶段（Step 500到约1500）**：
   - 红色曲线（32k窗口）开始快速增长，从约2500迅速上升到超过10000，甚至在后期接近17500，显示出32k窗口下模型的输出长度显著增加。
   - 蓝色曲线（16k窗口）的增长相对平缓，从约2000缓慢上升到约5000左右，增长幅度远小于红色曲线。
3. **后期阶段（Step 1500到2000）**：
   - 红色曲线（32k窗口）的序列长度出现较大波动，有明显的峰值（接近17500）和谷值（约10000），但整体仍保持在较高水平。
   - 蓝色曲线（16k窗口）的序列长度也有波动，但幅度较小，峰值约为6500，整体低于红色曲线。

**方法的运作方式（结合研究背景）**：
在这项研究中，窗口大小（window size）是影响模型输出长度和训练效率的一个关键参数。通过对比16k和32k窗口的实验结果，研究人员可以观察不同窗口大小下模型的行为：
- 较大的窗口大小（32k）允许模型生成更长的序列，这可能是因为窗口大小限制了模型在处理序列时的“视野”，更大的窗口让模型能够处理更长的上下文信息，从而生成更长的响应。
- 然而，从图中可以看出，虽然32k窗口产生了更长的序列，但奖励（reward）的提升却很有限（根据caption的描述“only marginally improves the reward”），这表明存在“token redundancy”（token冗余），即模型生成了大量不必要的token，导致序列长度增加但性能提升不明显。

**结论**：
这张图清晰地展示了窗口大小对序列长度的影响：
- 32k窗口的模型（红色曲线）产生的序列长度远长于16k窗口的模型（蓝色曲线），说明更大的窗口允许模型生成更长的输出。
- 尽管序列长度显著增加，但奖励的提升很小，这验证了“severe token redundancy”的结论，即模型在生成长序列时包含了大量冗余的token，没有有效地提升性能。

通过这张图，研究人员可以得出结论：单纯增加窗口大小（即允许更长的序列）并不一定能带来显著的性能提升，因为会出现大量的token冗余。这为后续优化模型的训练和推理过程提供了依据，例如需要设计更有效的方法来减少冗余，提高序列的质量而不是仅仅长度。

---

![(a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A cau](fig7_4.webp)

> (a) Sequence Length (b) Reward Figure 7 : Format reward comparison. Format A causes uncontrolled length growth without reward improvement. Format B ensures proper stopping. (c) Sequence Length (d) Reward Figure 8 : Window size comparison. The 32k window produces much longer responses than the 16k window, but only marginally improves the reward, demonstrating severe token redundancy.

这张图（图8）展示了在强化学习（特别是零样本强化学习，Zero RL）的训练过程中，**窗口大小（window size）对模型行为（以“奖励”衡量）的影响**。我们可以通过以下几个部分来理解这张图：

### 图的结构与组件
- **横轴（X轴）**：标记为“Step”，表示训练的步骤（或迭代次数），范围从0到2000。这代表了训练过程的时间线，步骤越多意味着训练进行得越久。
- **纵轴（Y轴）**：标记为“Reward”，表示模型在训练过程中获得的奖励值，范围大约从1.20到1.45。奖励是衡量模型行为（如生成的回答质量、是否符合任务要求等）的指标，数值越高通常表示模型表现越好。
- **两条曲线**：
  - 蓝色曲线：代表使用“16k window”（窗口大小为16k）时的奖励变化。
  - 红色曲线：代表使用“32k window”（窗口大小为32k）时的奖励变化。
- **图例**：明确标注了两条曲线对应的窗口大小，帮助读者区分不同的实验条件。

### 数据流动与方法运作方式
这张图展示的是**训练过程中奖励随步骤的变化趋势**，属于“结果图”。其背后的方法是：在训练模型时，设置不同的“窗口大小”（可以理解为模型处理或生成序列时的上下文长度限制或相关参数），然后观察奖励如何随训练步骤（即训练时长）变化。

具体来说：
1. **训练过程**：模型在每个训练步骤中与环境（或任务）交互，根据其行为获得奖励。随着步骤增加，模型不断学习优化，奖励理论上应逐渐提高（或趋于稳定）。
2. **窗口大小的作用**：“窗口大小”可能影响模型的上下文理解、生成的序列长度或计算效率。这里通过对比16k和32k窗口，观察奖励的变化差异。

### 坐标、对比对象与结论
- **坐标范围**：
  - 横轴（Step）：0到2000，代表训练的进度。
  - 纵轴（Reward）：约1.20到1.45，代表奖励的高低。
- **对比对象**：蓝色曲线（16k窗口）和红色曲线（32k窗口）的奖励变化趋势。
- **结论（从图中可观察到）**：
  1. **奖励增长趋势**：两条曲线都随着训练步骤的增加而上升，说明随着训练进行，模型的奖励（表现）在提高。
  2. **窗口大小的影响**：
     - 红色曲线（32k窗口）的奖励值**整体高于**蓝色曲线（16k窗口），但增长幅度“边际递减”（即后期增长变缓）。
     - 结合图的原始caption（“Window size comparison. The 32k window produces much longer responses than the 16k window, but only marginally improves the reward, demonstrating severe token redundancy.”），可以推断：32k窗口虽然能让模型生成更长的响应（但图中未直接显示响应长度，需结合caption理解），但奖励的提升却很有限，这表明存在“严重的token冗余”——即模型生成的很多token（序列中的元素，如单词、符号等）对奖励（即任务表现）的贡献很小，存在冗余计算或冗余输出。
     - 另外，从曲线的波动来看，32k窗口的奖励曲线（红色）比16k窗口的（蓝色）更“陡峭”或增长更快？不，仔细看，红色曲线在后期（如1500到2000步）的奖励更高，但蓝色曲线在后期也有明显增长。不过核心结论是：更大的窗口（32k）带来更长的响应，但奖励提升有限，体现了token冗余。

### 方法的具体运作（结合论文背景）
论文的目标是探索“零样本强化学习（Zero RL）”在大模型（如万亿参数模型）中的训练动态和涌现能力。为了实现这一点，他们需要设计稳定的训练流程，包括算法和系统优化（如clipped importance sampling、training-inference ratio correction、mixed-precision control等）。这张图是他们的实验结果之一，用于验证“窗口大小”这一参数对训练效果的影响：

- **实验设计**：在训练模型时，分别使用16k和32k的窗口大小，记录每个训练步骤的奖励。
- **分析逻辑**：通过对比两种窗口大小下的奖励曲线，判断窗口大小如何影响模型的学习和表现。结果显示，更大的窗口（32k）虽然能生成更长的响应，但奖励提升有限，说明存在token冗余——即模型生成的很多内容是冗余的，没有有效提升任务表现。

总结来说，这张图通过对比不同窗口大小下的奖励随训练步骤的变化，揭示了“窗口大小”对模型奖励（表现）的影响：更大的窗口（32k）能带来更长的响应，但奖励提升有限，体现了token冗余。这为论文中关于“大模型训练中的挑战（如token冗余）”提供了实验证据。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_1.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（图9a）展示了在“flash”模型的第一阶段强化学习（RL）训练中，**学习率（Learning Rate, LR）对奖励（Reward）的影响**，属于超参数消融实验的一部分。

### 图的组件与信息流动：
- **横轴（X轴）**：标记为“Step”，代表训练的步骤或迭代次数，范围从0到约600。这表示训练过程随时间（或迭代）的推进。
- **纵轴（Y轴）**：标记为“Reward”，代表模型在训练中获得的奖励值，范围从0到1.5。奖励值越高，通常表示模型的表现越好（例如，在任务中解决了更多问题或达到了更好的性能）。
- **曲线**：图中有三条曲线，分别对应不同的学习率（LR）设置：
  - 红色曲线：`lr=1e-6`（学习率为1×10⁻⁶）。
  - 蓝色曲线：`lr=2e-6`（学习率为2×10⁻⁶）。
  - 绿色曲线：`lr=3e-6`（学习率为3×10⁻⁶）。
- **趋势**：所有曲线都呈现出**先快速上升，然后逐渐趋于平缓**的模式。在训练初期（步骤0到约100左右），奖励值迅速从0增加到约1.2到1.3之间；之后，奖励的增长速度减慢，逐渐接近1.5的上限。

### 方法的运作方式（从图中理解）：
这张图展示了**学习率对训练过程中奖励增长的影响**。在强化学习中，学习率决定了模型参数更新的步长：
- 如果学习率太小（如`lr=1e-6`，红色曲线），模型的参数更新较慢，奖励增长也相对较慢（但最终也能达到较高的奖励）。
- 如果学习率适中（如`lr=2e-6`，蓝色曲线）或稍大（如`lr=3e-6`，绿色曲线），模型的参数更新更快，奖励增长也更迅速（尤其是在训练初期）。
- 然而，图中的caption指出“Learning rate has minimal impact in the tested range”（在测试范围内，学习率的影响很小）。这意味着在该实验的学习率范围内（1e-6到3e-6），不同的学习率设置对最终的奖励水平影响不大，所有曲线最终都收敛到相似的奖励值（约1.4到1.5之间）。

### 结果的详细解读：
- **坐标与范围**：
  - X轴（Step）：0到约600，代表训练的迭代次数。
  - Y轴（Reward）：0到1.5，代表模型获得的奖励。
- **对比对象**：三条曲线分别对应不同的学习率（1e-6、2e-6、3e-6）。
- **结论**：
  - 在测试的学习率范围内（1e-6到3e-6），学习率对奖励的影响较小（“minimal impact”）。
  - 所有学习率设置下，奖励都随着训练步骤的增加而增长，最终趋于稳定（收敛）。
  - 训练过程分为两个阶段：**快速上升阶段**（初期，奖励迅速增加）和**平缓增长阶段**（后期，奖励增长减慢并趋于稳定）。

### 总结：
这张图通过展示不同学习率下的奖励变化，说明了在“flash”模型的第一阶段强化学习训练中，学习率在该测试范围内对奖励的影响较小。模型的奖励随着训练步骤的增加而增长，最终收敛到相似的水平，这表明在该学习率范围内，选择不同的学习率对模型的最终性能影响不大。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_2.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（图9b）展示了在“flash”模型的第一阶段强化学习（RL）训练中，**超参数“rollout”对“奖励（Reward）随训练步数（Step）变化”的影响**，属于“超参数消融实验”的一部分，用于探究不同rollout设置下模型的训练动态。

### 图的组件与信息流动：
- **横轴（X轴）**：代表训练的“步数（Step）”，从0到600左右，展示训练过程的时间推进（或迭代次数）。
- **纵轴（Y轴）**：代表“奖励（Reward）”，数值从0到1.5，衡量模型在训练中获得的反馈（可理解为任务表现或学习效果的量化指标）。
- **三条曲线**：分别对应不同的`rollout`值（超参数）：
  - 红色曲线：`rollout=8`（即每次训练或推理时，同时处理的“路径”或“样本组”大小为8）。
  - 蓝色曲线：`rollout=16`（rollout组大小为16）。
  - 绿色曲线：`rollout=32`（rollout组大小为32）。
- **信息流动**：随着训练步数（Step）增加，奖励（Reward）整体呈上升趋势，最终趋于平稳（收敛）。不同rollout的曲线展示了“rollout大小如何影响奖励的增长速度和最终水平”。

### 方法的运作方式（从图中理解实验逻辑）：
这是一个**超参数消融实验**，目的是研究“rollout”（一种可能与会话展开、多路径采样或批量处理相关的超参数）对模型训练效果的影响。实验中，保持其他训练参数（如学习率、损失函数等）不变，仅改变`rollout`的大小（8、16、32），然后观察奖励随训练步数的变化：
- 训练开始时（Step≈0），所有曲线的奖励都接近0，说明模型初始表现差。
- 随着Step增加，奖励快速上升（“发现阶段”），之后增长放缓并趋于平稳（“锐化阶段”，对应论文中“训练过程经历初始发现阶段后进入锐化阶段”的结论）。
- 不同rollout的曲线对比显示：**更大的rollout组（如32）在相同步数下，奖励增长更快（收敛更快）**，但论文caption提到“更大的rollout组每步收敛更快，但墙钟时间（实际运行时间）成本更高”（即虽然训练步数少，但总耗时可能更多，因为每次处理的组更大，计算量更高）。

### 坐标、对比对象与结论：
- **坐标**：X轴（Step）范围0-600，Y轴（Reward）范围0-1.5。
- **对比对象**：三条曲线对比了`rollout=8`、`rollout=16`、`rollout=32`三种设置下的奖励变化。
- **结论**：
  - 奖励随训练步数增加而上升，最终收敛（模型学习到有效行为）。
  - 更大的rollout组（如32）**每步收敛更快**（相同步数下奖励更高），但“墙钟时间”成本更高（即实际运行时间更长，因为每次处理的样本组更大，计算量增加）。
  - 这说明rollout是一个“速度-成本”权衡的超参数：更大的rollout加速训练进度（每步收敛快），但增加计算资源消耗（墙钟时间长）。

总结：这张图通过对比不同rollout设置下的奖励-步数曲线，展示了“rollout大小如何影响模型训练的收敛速度和计算成本”，支持了论文中“超参数消融实验”的结论（如“更大的rollout组每步收敛更快但墙钟时间成本更高”）。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_3.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（图9中的子图(c)，对应“Loss Reduction – Reward”）展示了在Flash模型的第一阶段强化学习（RL）训练中，**不同损失减少策略（Token - level和Sample - level）下，奖励（Reward）随训练步骤（Step）的变化情况**。

### 图的组件与信息流动
- **横轴（X轴）**：代表训练的“Step（步骤）”，从0到600左右，展示了训练过程的时间推进（或迭代次数）。
- **纵轴（Y轴）**：代表“Reward（奖励）”，范围从0.0到1.5，衡量模型在训练中获得的反馈（可以理解为模型行为或输出的“质量得分”）。
- **两条曲线**：
  - 蓝色曲线：标记为“Token - level（token级）”，表示采用token级的损失减少策略时，奖励随步骤的变化。
  - 红色曲线：标记为“Sample - level（样本级）”，表示采用样本级的损失减少策略时，奖励随步骤的变化。
- **信息流动**：随着训练步骤（Step）的增加，两条曲线都呈现上升趋势，说明两种策略都能让模型获得更高的奖励（即模型性能提升）。但它们的上升速度和最终奖励水平有差异。

### 方法的运作方式（从图中理解）
这张图是**超参数消融实验**的一部分，目的是比较“Token - level”和“Sample - level”这两种损失减少策略对模型训练的影响。在强化学习的训练中，“损失减少”通常与优化目标相关：通过调整模型的参数，使得损失函数（衡量模型输出与期望输出的差距）降低，从而让模型学习到更好的行为（这里体现为奖励增加）。
- 对于“Token - level”策略：从图中蓝色曲线的走势看，它在训练过程中（尤其是后期）的奖励增长更明显，最终奖励水平也更高。这可能意味着token级的损失减少策略能更精细地优化模型的输出（比如对每个token的输出进行调整），从而更有效地提升模型的推理能力（因为实验背景是“Emergent Reasoning”，即涌现推理能力）。
- 对于“Sample - level”策略：红色曲线的奖励增长相对平缓，最终奖励低于Token - level策略。这可能是因为样本级的损失减少策略是对整个样本（比如一个问题 - 回答对）进行优化，粒度较粗，不如token级策略精细。

### 结果的结论（结合caption和图）
根据图和caption（“Token - level loss reduction promotes reasoning length growth, whereas sample - level keeps length flat”），这里的“reasoning length”可以理解为模型推理的深度或输出的详细程度（虽然图中直接展示的是奖励，但结合实验背景，奖励的提升可能反映了推理能力的增强，包括推理长度的增长）。具体结论：
- **坐标与对比对象**：横轴是训练步骤（Step），纵轴是奖励（Reward），对比对象是“Token - level”和“Sample - level”两种损失减少策略。
- **结论**：在训练过程中，**Token - level的损失减少策略比Sample - level策略更能促进奖励的提升**（即更能提升模型的推理能力，包括推理长度的增长）。从图中可以看到，随着步骤增加，Token - level的奖励曲线（蓝色）始终在Sample - level的曲线（红色）上方（尤其是在训练后期），且最终奖励更高，说明Token - level策略在优化模型推理能力方面更有效。

总结来说，这张图通过对比两种损失减少策略下的奖励 - 步骤曲线，展示了Token - level策略在提升模型推理能力（以奖励衡量）方面的优势，支持了论文中“Token - level loss reduction promotes reasoning length growth”的结论。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_4.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（对应原始caption中的子图(d)，即“LR – Seq Length”）展示了在模型训练的**第一阶段强化学习（RL）**过程中，**学习率（Learning Rate, LR）**对**序列长度（Sequence Length）**的影响，属于**超参数消融实验**的一部分（实验对象为“flash模型”）。我们可以通过以下角度详细理解这张图：

### 1. 图的组件与信息流动
- **横轴（X轴）**：标记为“Step”，代表训练的**步骤（或迭代次数）**。范围从0到约600，表示训练过程的时间推进。
- **纵轴（Y轴）**：标记为“Sequence Length”，代表模型生成的**序列长度**（可以理解为模型在推理或生成过程中输出的token数量，长度越长通常意味着推理更深入或表达更复杂）。
- **曲线与图例**：图中有三条曲线，分别对应不同的学习率（LR）设置：
  - 红色曲线：`lr=1e-6`（学习率为1×10⁻⁶）
  - 蓝色曲线：`lr=2e-6`（学习率为2×10⁻⁶）
  - 绿色曲线：`lr=3e-6`（学习率为3×10⁻⁶）
- **信息流动**：随着训练步骤（Step）的增加，观察不同学习率下序列长度的变化趋势。曲线的走势反映了“学习率如何影响序列长度随训练的演化”。

### 2. 方法的运作方式（从图中理解实验逻辑）
这张图是**超参数消融实验**的结果，目的是研究“学习率（LR）”这个超参数对模型训练过程中“序列长度”的影响。实验的核心逻辑是：
- 在模型的**第一阶段强化学习（RL）**训练中，固定其他超参数（如训练轮次、批次大小等），仅改变**学习率（LR）**的取值（这里测试了1e-6、2e-6、3e-6三个值）。
- 观察在不同学习率下，**序列长度（Sequence Length）**随**训练步骤（Step）**的变化规律，从而判断学习率对模型推理能力（以序列长度衡量）的影响。

### 3. 结果解读（坐标、对比对象、结论）
- **坐标与趋势**：
  - 横轴（Step）：训练步骤从0开始，逐步增加到约600。在训练初期（Step < 200左右），三条曲线的序列长度都经历了一个“先下降后上升”的过程（可能对应模型的“发现阶段”，如原始caption中提到的“initial discovery phase”）；在训练后期（Step > 200后），序列长度持续上升（对应“sharpening phase”，即“锐化阶段”）。
  - 纵轴（Sequence Length）：范围从约1500到4200。不同学习率下的序列长度增长速度和最终长度存在差异。
- **对比对象**：三条曲线分别对应`lr=1e-6`、`lr=2e-6`、`lr=3e-6`，通过对比它们的走势和最终值，分析学习率的影响。
- **结论（结合原始caption）**：
  - 原始caption指出“(a,d) Learning rate has minimal impact in the tested range.”（学习率在测试范围内影响较小）。从图中看，虽然不同学习率的曲线在后期（Step > 200）的长度有差异（蓝色曲线最高，红色次之，绿色最低），但整体趋势（先降后升、后期持续增长）相似，且差异程度相对较小（尤其是在训练后期，三条曲线都快速增长，只是速率略有不同）。这说明在**测试的学习率范围内（1e-6到3e-6）**，学习率对序列长度的影响相对有限（即“minimal impact”）。
  - 另外，从曲线的长期趋势看，所有学习率下序列长度都随训练步骤增加而增长，这符合强化学习中模型“能力提升”的预期（序列长度增长可能意味着模型的推理深度或表达能力增强）。

### 补充理解（结合论文背景）
论文研究的是“Zero RL”（无人工标注数据的强化学习），目标是让大模型（如1T参数的Ring-1T模型）涌现出推理能力。这张图作为**超参数消融实验**的一部分，验证了“学习率在该测试范围内对序列长度影响较小”的结论，说明在这个超参数区间内，学习率不是影响序列长度（或推理能力）的关键因素，或者模型的训练对学习率的变化具有一定的鲁棒性。这也为后续的训练管道优化（如论文中提到的clipped importance sampling、training-inference ratio correction等）提供了基础——因为学习率的影响有限，所以可以更专注于其他优化策略来提升模型性能。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_5.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（图9中的子图e，标题为“Rollout – Seq Length”）展示了在Flash模型的第一阶段强化学习（RL）训练中，**不同“rollout”参数设置对“序列长度（Sequence Length）”随“训练步数（Step）”变化的影响**。我们可以通过以下角度详细理解这张图：

### 图的组件与信息流动
- **横轴（X轴）**：代表“训练步数（Step）”，范围从0到约600，展示了训练过程的时间推进（以步数为单位）。
- **纵轴（Y轴）**：代表“序列长度（Sequence Length）”，数值从约1800到4300，衡量模型在每一步生成的序列（如推理步骤、token序列）的长度。
- **三条曲线**：分别对应不同的“rollout”参数设置：
  - 红色曲线：`rollout=8`（即每次滚动更新的组大小为8）。
  - 蓝色曲线：`rollout=16`（滚动更新组大小为16）。
  - 绿色曲线：`rollout=32`（滚动更新组大小为32）。
- **图例**：明确标注了每条曲线对应的`rollout`值，帮助读者区分不同实验条件。

### 方法的运作方式（从图中理解实验逻辑）
这张图是**超参数消融实验**的一部分，目的是研究“rollout”（一种强化学习中的超参数，通常与样本收集或更新的批次大小相关）对模型训练动态（这里是“序列长度”的增长）的影响。实验的核心逻辑是：
1. **控制变量**：保持其他超参数（如学习率、损失函数设置等）不变，仅改变`rollout`的值（8、16、32）。
2. **观测指标**：跟踪“序列长度”随“训练步数”的变化，以评估模型推理能力的发展（序列长度越长，通常意味着模型能进行更复杂的推理或生成更长的有效token序列）。
3. **分析趋势**：通过对比不同`rollout`值的曲线，理解“rollout”如何影响训练效率和模型行为。

### 结果解读（坐标、对比对象与结论）
- **坐标与趋势**：
  - 所有曲线在训练初期（Step < 200）都经历了一个“下降-回升”的过程：初始时序列长度约为1800-2000，随后短暂下降（可能是因为模型在探索阶段调整策略），之后开始上升。
  - 训练后期（Step > 200），所有曲线的序列长度都显著增长，最终接近或超过4000。
- **对比对象（不同rollout值）**：
  - **收敛速度（每步的增长速率）**：`rollout=8`（红色曲线）的增长速度最快，其次是`rollout=16`（蓝色），最后是`rollout=32`（绿色）。例如，在Step=400时，红色曲线的序列长度明显高于蓝色和绿色；在Step=600时，红色曲线仍领先。
  - **最终序列长度（稳态值）**：虽然`rollout=8`的增长更快，但最终（Step=600附近）三条曲线的序列长度趋于接近（都在4000以上），说明更大的`rollout`可能在长期收敛到相似的序列长度，但需要更多的“墙钟时间”（因为每步处理的数据量更大）。
- **结论（结合caption的补充）**：
  - 图中显示，**更大的rollout组（如32）收敛速度更慢（每步增长慢），但可能消耗更多的墙钟时间**（因为每次更新需要处理更多的样本或token）。
  - 这与caption中的描述一致：“Larger rollout groups converge faster per step but cost more wall-clock time”（这里需要注意：实际图中`rollout=8`增长更快，可能caption中的“faster per step”是指“每步的进度”，但需要结合实验定义。更准确的理解是：更大的rollout可能在每一步中处理的样本更多，因此“每步的绝对增长”可能更大？不，图中`rollout=8`的曲线在前期增长更快，所以可能caption的描述需要结合实验的具体定义，比如“rollout”是“样本收集的批次大小”，更大的batch可能在每一步中收集更多样本，因此“每步的推理长度增长”更快？但图中`rollout=8`的曲线在Step=200后增长更快，所以可能我的理解需要调整。重新看：图中`rollout=8`的曲线在Step=200后上升得更快，而`rollout=32`的曲线上升得较慢。所以结论是：**较小的rollout值（如8）在训练过程中（每步）的序列长度增长更快，但可能因为每次处理的样本少，总墙钟时间更短？而较大的rollout值（如32）增长较慢，但可能需要更多时间来达到相同的序列长度？这与caption中的“Larger rollout groups converge faster per step but cost more wall-clock time”似乎矛盾，可能我误解了“converge faster per step”的意思。正确的理解应该是：**“rollout”越大，每一步中模型能处理的样本或推理步骤越多，因此“每步的推理长度增长”更快？但图中`rollout=8`的曲线在Step=200后增长更快，所以可能caption的描述需要结合实验的具体设置，比如“rollout”是“样本的滚动窗口大小”，更大的窗口意味着每次更新需要处理更多的样本，因此“每步的计算时间更长”，但“每步的推理长度增长”可能更慢？这需要根据实验的具体定义来理解。不过根据图中的曲线，我们可以明确：

  - 不同`rollout`值的曲线在训练过程中都经历了“初始下降-后续增长”的阶段，说明模型在训练初期有一个调整期，之后推理长度开始增加。
  - 较小的`rollout`值（如8）在训练后期（Step > 200）的序列长度增长速度更快，而较大的`rollout`值（如32）增长较慢，但最终（Step=600）三者的序列长度相近。

### 总结
这张图通过对比不同`rollout`参数下的“序列长度-步数”曲线，展示了**“rollout”超参数如何影响模型训练过程中推理长度的增长动态**：较小的`rollout`值（如8）在训练后期（每步）的序列长度增长更快，而较大的`rollout`值（如32）增长较慢，但可能需要更多的墙钟时间来完成训练。这一结果支持了论文中关于“超参数消融”的结论，即不同的`rollout`设置会影响训练效率和模型的推理行为。

---

![(a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Le](fig8_6.webp)

> (a) LR – Reward (b) Rollout – Reward (c) Loss Reduction – Reward (d) LR – Seq Length (e) Rollout – Seq Length (f) Loss Reduction – Seq Length Figure 9 : Hyperparameter ablation on the flash model during the first stage RL. (a,d) Learning rate has minimal impact in the tested range. (b,e) Larger rollout groups converge faster per step but cost more wall-clock time. (c,f) Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.

这张图（标记为(f) "Loss Reduction – Seq Length"）展示了在“flash模型”第一阶段强化学习（RL）训练中，**损失减少策略（token-level vs. sample-level）对序列长度（Sequence Length）随训练步骤（Step）变化的影响**。

首先，我们来看图的各个组成部分：
- **X轴（横轴）**：代表训练的“步骤”（Step），从0到大约650。这表示训练过程中的迭代次数或时间进程。
- **Y轴（纵轴）**：代表“序列长度”（Sequence Length），从1500到4200左右。这通常指模型生成的回答或推理链中的token数量。
- **两条曲线**：
    - **蓝色曲线（Token-level）**：代表采用“token-level”损失减少策略时的序列长度变化。
    - **红色曲线（Sample-level）**：代表采用“sample-level”损失减少策略时的序列长度变化。
- **图例**：明确区分了这两条曲线所代表的策略。

数据的流动和信息的呈现方式是：随着训练步骤（X轴）的增加，观察两种不同损失减少策略下，序列长度（Y轴）如何演变。读者可以通过比较两条曲线的趋势来理解不同策略的效果。

这张图揭示的方法运作方式如下：
该实验是在“flash模型”的第一阶段强化学习训练中进行的超参数消融研究的一部分。具体来说，它比较了两种不同的“损失减少”策略对模型生成序列长度的影响：
1.  **Token-level（令牌级别）损失减少**：这种方法可能针对每个单独的令牌进行损失优化，鼓励模型生成更长的、可能更详细的序列。从图中蓝色曲线可以看出，随着训练步骤的增加，序列长度显著增长，从大约1800开始，逐渐上升，在200步之后增长加速，最终超过4000。
2.  **Sample-level（样本级别）损失减少**：这种方法可能针对整个样本（例如，一个完整的回答或推理链）进行损失优化，可能更关注样本的整体质量而非单个令牌的长度。从图中红色曲线可以看出，序列长度在整个训练过程中相对稳定，保持在大约1700到1800之间，没有明显的增长趋势。

通过这张图，我们可以得出以下结论：
-   **Token-level损失减少策略能够有效促进推理长度的增长**：这意味着模型在训练过程中会生成越来越长的序列，这可能与更详细的推理或更复杂的思考过程相关。
-   **Sample-level损失减少策略则使序列长度保持相对平坦**：这意味着模型的输出长度在训练过程中不会显著增加，可能更注重答案的准确性和简洁性，或者受到其他因素的限制。
-   图的原始caption进一步指出：“Token-level loss reduction promotes reasoning length growth, whereas sample-level keeps length flat.”（令牌级损失减少促进推理长度增长，而样本级则保持长度不变。）这与我们对图的分析完全一致。

总而言之，这张图清晰地展示了在强化学习训练中，选择不同的损失减少策略会对模型生成的序列长度产生显著不同的影响：令牌级策略倾向于增加序列长度，而样本级策略则倾向于保持序列长度稳定。这对于理解如何通过调整训练策略来引导模型发展特定的行为（如更长的、可能更复杂的推理链）具有重要意义。

---

![(a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10](fig9_1.webp)

> (a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10 : Comprehensive analysis of zero RL dynamics. (a) Model scale effect. Ring-2.5-1T-Zero consistently outperforms Ring-2.5-flash-Zero. A larger model capacity unlocks a higher performance ceiling and accelerates capability acquisition. (b) Reasoning boundary. Pass@1024 expands during early training but soon saturates. This proves that RL first discovers novel reasoning patterns and then shifts to primarily sharpening its existing capabilities. (c) Length inertia. We track the sequence length of simple questions that the model answers perfectly on the first attempt within a batch. As training progresses, the model inflates its token usage for these already-solved problems. It learns a lazy shortcut to accumulate rewards rather than maintaining conciseness. (d) Data distribution mismatch. By using the sequence length required to correctly solve a problem as a proxy for its difficulty, we observe that real-world mathematical data forms a massive long-tail difficulty distribution skewed toward simple problems ( e.g., 67.6% of problems can be solved within just 4k tokens). However, zero RL does not benefit from mimicking this natural frequency. Over-training on this long tail simply wastes computational budget and stalls the learning process.

这张图（对应原文caption中的子图(a)“Model scale effect”）清晰地展示了**模型规模对零强化学习（zero RL）训练动态和性能的影响**，核心是对比两种不同规模的模型在AIME 2024基准测试上的准确率随训练步骤（Step）的变化。

### 图的组件与信息流动：
- **横轴（X轴）**：标注为“Step”，代表训练的步骤数（从0到约4500左右），它反映了训练的进度，数据随训练步骤的增加而变化，展示模型在不同训练阶段的能力提升过程。
- **纵轴（Y轴）**：标注为“AIME 2024 Accuracy”，即模型在AIME 2024数学基准测试上的准确率（百分比形式），数值越高表示模型解决数学问题的能力越强。
- **两条曲线**：
  - 蓝色曲线（带圆点标记）：代表模型“Ling-2.5-flash-Base”，这是一个**较小规模**的模型（从命名中的“flash”和“Base”推测，参数量或计算资源相对有限）。
  - 红色曲线（带方形标记）：代表模型“Ling-2.5-1T-Base”，这是一个**大规模**的模型（命名中的“1T”暗示参数量达到万亿级别，计算资源更充足）。
- **数据流动与趋势**：随着训练步骤（Step）的增加，两条曲线的准确率都呈上升趋势，但**红色曲线（大规模模型）的上升速度更快、最终达到的准确率更高**。例如，在训练步骤为0时，红色模型的准确率约为22%，蓝色模型约为15%；当训练步骤增加到约4000时，红色模型的准确率超过85%，而蓝色模型约为72%。


### 方法的运作方式（从图中推断）：
这张图通过**对比不同规模的模型在相同训练任务（AIME 2024）上的表现**，展示了“模型规模”这一变量对zero RL训练的影响。具体来说：
- 训练过程中，模型通过与环境（这里是数学问题求解任务）的交互（强化学习的试错过程）来学习解题策略。
- 大规模模型（红色曲线）由于具有更多的参数和计算资源，能够**更快地探索和利用有效的解题模式**，因此在训练早期（步骤较少时）就展现出比小模型更快的准确率提升，并且在训练后期（步骤较多时）达到的性能上限更高。
- 小模型（蓝色曲线）虽然也能通过训练提升准确率，但由于资源限制，其学习速度和最终性能都不如大规模模型。


### 结论（从图中得出的发现）：
- **模型规模解锁性能上限**：大规模模型（Ling-2.5-1T-Base）的性能天花板（最终准确率）显著高于小规模模型（Ling-2.5-flash-Base），说明更大的模型容量能够支持更高的解题能力。
- **加速能力获取**：大规模模型在训练过程中（随步骤增加）的准确率提升速度更快，表明更大的模型能够更快地“发现”并“掌握”有效的解题策略，缩短了能力成熟的时间。
- **验证“缩放的苦涩教训”**：这一结果验证了论文中提到的“缩放的苦涩教训”之一——**模型规模的扩大（如达到1万亿参数）能够显著提升样本效率（用更少的训练步骤达到更高准确率）和性能上限**，即“更大规模的模型在zero RL训练中表现更优”。

简言之，这张图通过对比不同规模的模型在AIME 2024上的准确率随训练步骤的变化，直观地展示了**模型规模对zero RL训练动态和最终性能的关键影响**：更大的模型不仅学习更快，而且能达到更高的解题准确率，验证了“缩放有助于提升zero RL性能”的结论。

---

![(a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10](fig9_2.webp)

> (a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10 : Comprehensive analysis of zero RL dynamics. (a) Model scale effect. Ring-2.5-1T-Zero consistently outperforms Ring-2.5-flash-Zero. A larger model capacity unlocks a higher performance ceiling and accelerates capability acquisition. (b) Reasoning boundary. Pass@1024 expands during early training but soon saturates. This proves that RL first discovers novel reasoning patterns and then shifts to primarily sharpening its existing capabilities. (c) Length inertia. We track the sequence length of simple questions that the model answers perfectly on the first attempt within a batch. As training progresses, the model inflates its token usage for these already-solved problems. It learns a lazy shortcut to accumulate rewards rather than maintaining conciseness. (d) Data distribution mismatch. By using the sequence length required to correctly solve a problem as a proxy for its difficulty, we observe that real-world mathematical data forms a massive long-tail difficulty distribution skewed toward simple problems ( e.g., 67.6% of problems can be solved within just 4k tokens). However, zero RL does not benefit from mimicking this natural frequency. Over-training on this long tail simply wastes computational budget and stalls the learning process.

这张图（对应原文caption中的子图(b) "Reasoning boundary"）展示了一个关于“零强化学习（zero RL）训练动态”的关键发现，具体是模型在“Pass@1024”指标上的表现随训练步骤（Step）的变化情况。

首先，我们来理解图中的各个组件：
- **X轴（横轴）**：标记为“Step”，代表训练过程中的步骤或迭代次数。从图中可以看到，范围大约是从0到2000。
- **Y轴（纵轴）**：标记为“AIME 2024 Pass@1024”，这是一个评估指标。“Pass@1024”通常指在给定1024个样本或尝试中，模型能够正确解决问题的比例。“AIME 2024”则指明了这个评估是基于2024年的美国数学邀请赛（AIME）题目。
- **数据点与曲线**：图中有一条蓝色的折线，连接了多个数据点。这些数据点代表了在特定训练步骤（如0、400、800、1200、1600、2000步）时模型的“Pass@1024”值。

数据的流动和信息的呈现顺序是：
- 横轴从左到右表示训练的进展，即时间或计算步骤的增加。
- 纵轴从下到上表示模型性能的提升，即“Pass@1024”值的增加。
- 曲线的走势展示了随着训练步骤的增加，模型性能如何变化。

这张图揭示了方法的运作方式以及得出的结论：
- **训练过程的阶段性**：图中清晰地显示，模型的“Pass@1024”性能在训练初期（大约从0步到800步）迅速提升。这表明在训练的早期阶段，模型正在“发现”新的推理模式或策略。
- **性能饱和**：在大约800步之后，曲线趋于平缓，性能几乎不再提升，达到了一个饱和点。这说明在训练的后期，模型主要是在“磨练”或“优化”其已经发现的推理能力，而不是继续学习全新的推理方式。
- **结论**：这一现象证明了零强化学习的训练过程通常会经历两个阶段：一个初始的“发现阶段”（discovery phase），模型在此阶段探索并掌握新的推理技巧；以及一个后续的“锐化阶段”（sharpening phase），模型在此阶段专注于改进和优化已有的能力。

具体来说，从图中可以看到：
- 在训练步骤接近0时，“Pass@1024”的值大约在86-87左右。
- 随着训练进行到约400步时，该值迅速上升到约93-94。
- 到约800步时，性能进一步提升到约96-97。
- 之后，在800步、1200步、1600步和2000步时，性能保持在约96-97的水平，几乎没有变化。

因此，这张图直观地展示了“Pass@1024”指标在早期训练中扩展（提升），但很快达到饱和（不再显著提升）的过程，从而验证了论文中提出的“训练过程首先发现新的推理模式，然后转向主要磨练现有能力”的观点。

---

![(a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10](fig9_3.webp)

> (a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10 : Comprehensive analysis of zero RL dynamics. (a) Model scale effect. Ring-2.5-1T-Zero consistently outperforms Ring-2.5-flash-Zero. A larger model capacity unlocks a higher performance ceiling and accelerates capability acquisition. (b) Reasoning boundary. Pass@1024 expands during early training but soon saturates. This proves that RL first discovers novel reasoning patterns and then shifts to primarily sharpening its existing capabilities. (c) Length inertia. We track the sequence length of simple questions that the model answers perfectly on the first attempt within a batch. As training progresses, the model inflates its token usage for these already-solved problems. It learns a lazy shortcut to accumulate rewards rather than maintaining conciseness. (d) Data distribution mismatch. By using the sequence length required to correctly solve a problem as a proxy for its difficulty, we observe that real-world mathematical data forms a massive long-tail difficulty distribution skewed toward simple problems ( e.g., 67.6% of problems can be solved within just 4k tokens). However, zero RL does not benefit from mimicking this natural frequency. Over-training on this long tail simply wastes computational budget and stalls the learning process.

这张图（对应原始caption中的子图(d)，即“Long Tail Distribution”）展示了零强化学习（zero RL）训练过程中，**问题难度（以正确解决问题所需的序列长度衡量）的分布**与**实际训练数据分布**之间的不匹配现象。我们可以通过以下几个层面来理解这张图：

1.  **图表结构与组件**：
    *   **X轴（Step）**：代表训练的步骤或迭代次数，从左到右依次为0、1600、3200、4800。这表示训练过程的时间推进。
    *   **Y轴（Token Distribution）**：代表正确解决问题所需的序列长度（即token数量）的分布情况。数值越大，表示问题越难（需要更多的token来描述或解决）。
    *   **箱线图（Box Plot）**：每个Step（0、1600、3200、4800）对应一个箱线图。箱线图展示了在该训练阶段，模型遇到的或解决的问题的序列长度的统计分布：
        *   **箱体的上下边缘**：分别代表该阶段序列长度的上四分位数（Q3）和下四分位数（Q1），箱体中间的线（中位数线）代表该阶段序列长度的中位数。
        *   **须（Whiskers）**：从箱体延伸出的线，通常表示数据的范围（例如，1.5倍的四分位距内的最大值和最小值）。
        *   **离群点（Outliers）**：图中未明确标出离群点，但须的末端可能代表了极端值的范围。

2.  **数据或信息的流动与解读**：
    *   随着训练步骤（Step）的增加（从0到4800），箱线图的位置整体向上移动。这意味着，在训练的早期阶段（如Step 0），模型遇到的问题序列长度较短（中位数较低），即问题相对简单。随着训练的进行，模型接触到的问题序列长度逐渐增加（中位数上升），表明模型开始处理更难的问题，或者对同一类问题的解决方式变得更加复杂。
    *   箱体的高度（即四分位距IQR）也随着Step的增加而增大，特别是在Step 3200和4800时，箱体更高，须也更长。这表明随着训练的深入，问题序列长度的分布范围变得更广，即模型面临的难度差异更大的问题。

3.  **方法运作的揭示（结合原始caption）**：
    *   这张图的核心是揭示**“数据分布不匹配”**问题。根据原始caption，研究者将“正确解决问题所需的序列长度”作为问题难度的代理。他们发现，现实世界中的数学数据集呈现出一种**“长尾难度分布”**，即大部分问题（例如67.6%）可以在相对较少的token（如4k以内）内解决，而少数问题则需要非常长的序列。
    *   然而，零RL方法并没有从模仿这种自然的长尾频率中受益。换句话说，如果训练数据过度偏向于这种长尾分布中的简单问题（因为它们数量多），或者模型过度专注于解决这些简单问题，那么训练过程可能会浪费计算资源，并且阻碍学习过程的有效推进。
    *   从图中可以看出，随着训练的进行，模型似乎在处理越来越长的序列（问题难度增加）。这可能意味着模型在尝试解决更难的问题，但也可能反映了模型在学习过程中出现了“长度惯性”（如原始caption中的子图(c)所述），即模型为了积累奖励而采取了“懒惰的捷径”，通过增加token使用量来解决已经能够完美解决的问题，而不是保持简洁性。这种行为可能与数据分布不匹配有关，模型可能没有有效地利用数据集中的简单问题来快速学习基本技能，然后再挑战更难的问题。

4.  **结论**：
    *   这张图清晰地展示了在零RL训练过程中，问题难度（以序列长度衡量）的分布随着训练步骤的增加而发生变化，总体趋势是难度增加。
    *   结合原始caption的分析，这种变化揭示了零RL面临的一个关键挑战：**训练数据的长尾难度分布与模型的学习行为不匹配**。这种不匹配可能导致计算资源的浪费和学习效率的降低，因为模型可能过度关注于解决大量简单问题，而没有有效地提升解决难题的能力，或者在学习过程中形成了不良的“长度惯性”。

---

![(a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10](fig9_4.webp)

> (a) Pass@1 (b) Pass@1024 (c) Length Inertia (d) Long Tail Distribution Figure 10 : Comprehensive analysis of zero RL dynamics. (a) Model scale effect. Ring-2.5-1T-Zero consistently outperforms Ring-2.5-flash-Zero. A larger model capacity unlocks a higher performance ceiling and accelerates capability acquisition. (b) Reasoning boundary. Pass@1024 expands during early training but soon saturates. This proves that RL first discovers novel reasoning patterns and then shifts to primarily sharpening its existing capabilities. (c) Length inertia. We track the sequence length of simple questions that the model answers perfectly on the first attempt within a batch. As training progresses, the model inflates its token usage for these already-solved problems. It learns a lazy shortcut to accumulate rewards rather than maintaining conciseness. (d) Data distribution mismatch. By using the sequence length required to correctly solve a problem as a proxy for its difficulty, we observe that real-world mathematical data forms a massive long-tail difficulty distribution skewed toward simple problems ( e.g., 67.6% of problems can be solved within just 4k tokens). However, zero RL does not benefit from mimicking this natural frequency. Over-training on this long tail simply wastes computational budget and stalls the learning process.

这张图（图10的子图d）展示了**零强化学习（zero RL）训练数据与模型实际需求之间的难度分布不匹配问题**，属于对零RL动态的全面分析的一部分。我们先看图表的结构：

- **横轴（X轴）**：标记为“Sequence Length”（序列长度），单位从左到右依次是4k、16k、32k、48k、64k，表示解决问题所需的token数量（可以理解为问题的复杂程度或描述的长度）。横轴从左到右，序列长度增加，意味着问题难度可能上升（因为更长的序列通常对应更复杂的问题）。
- **纵轴（Y轴）**：标记为“Proportion (%)”（比例，百分比），从下到上是0%、5%、10%、15%、20%，表示具有对应序列长度的问题在数据集中的占比（即有多少比例的问题需要这么长的序列来解决）。

接下来看数据的分布形态：这是一个**直方图（或频率分布图）**，蓝色的柱形（或填充区域）展示了不同序列长度的问题在数据集中的比例。从图中可以清晰看到：
- 大部分问题（约67.6%，根据caption说明）的序列长度在4k及以内（尤其是更短的序列，比如接近0到几k的范围），这形成了一个**长尾分布**——大部分问题很简单（短序列），只有少数问题需要很长的序列（难度高）。
- 具体来说，序列长度较短时（比如0到16k之间），比例迅速下降；而序列长度较长时（比如16k以上），比例非常低，几乎趋近于0。

然后结合caption的解释，理解这张图揭示的方法问题和结论：
- **数据分布的本质**：现实世界的数学数据（作为zero RL的训练数据）的难度分布是“长尾”的，即**绝大多数问题都很简单（短序列即可解决），只有极少数问题难度高（长序列）**。例如，67.6%的问题可以在4k token以内解决。
- **零RL的问题**：zero RL如果模仿这种自然的长尾频率（即过多地训练长序列的难题），会**浪费计算资源**，并且**阻碍学习过程**。换句话说，模型不需要通过大量训练长序列的难题来提升，因为数据中大部分是简单问题，过度关注长尾的难题会导致模型在无效的计算上花费时间，而不能有效学习到核心的推理能力。
- **方法的启示**：这张图说明，在设计zero RL的训练策略时，不能简单地模仿数据的自然难度分布（长尾），而需要考虑如何更高效地利用计算资源，比如可能需要在简单问题上快速学习基础能力，然后在合适的时候挑战更难的问题，而不是被长尾的难题“拖累”。

总结来说，这张图通过展示训练数据的序列长度（难度）分布，揭示了**数据分布与零RL训练需求的不匹配**：数据中简单问题占绝大多数（长尾），但过度训练这些长尾难题会浪费计算资源并阻碍学习。因此，zero RL的训练策略需要避免盲目模仿这种自然的长尾分布，以提高训练效率和效果。
