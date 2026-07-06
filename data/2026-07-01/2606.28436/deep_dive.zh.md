# Dockerless: Environment-Free Program Verifier for Coding Agents

[arXiv](https://arxiv.org/abs/2606.28436) · [HuggingFace](https://huggingface.co/papers/2606.28436) · ▲105

## 摘要（原文）

> Program verifiers play a central role in training coding agents, including selecting trajectories for supervised fine-tuning (SFT) and providing rewards for reinforcement learning (RL). Standard execution-based verification requires running unit tests inside per-repository environments such as Docker images, incurring substantial environment setup costs. We propose Dockerless, an environment-free agentic patch verifier that evaluates generated code patches without executing them. Rather than simply matching candidate patches to references, Dockerless judges patch correctness using evidence gathered through agentic repository exploration. On a verifier evaluation benchmark, Dockerless outperforms the strongest open-source verifier by 14.3 AUC points. Using Dockerless as both the SFT trajectory filter and the RL reward enables a fully environment-free post-training pipeline. The resulting model reaches 62.0%, 50.0%, and 35.2% resolve rate on SWE-bench Verified, Multilingual, and Pro, respectively. It surpasses the Qwen3.5-9B baseline by 2.4, 8.7, and 2.9 points, matching environment-based post-training.

## 摘要（中译）

程序验证器在训练编码代理中起着核心作用，包括为监督微调（supervised fine-tuning，SFT）选择轨迹和为强化学习（reinforcement learning，RL）提供奖励。标准的基于执行的验证需要在每个存储库环境（如Docker镜像）中运行单元测试，这会带来大量的环境设置成本。我们提出了Dockerless，一种无环境的代理补丁验证器，它可以在不执行生成代码补丁的情况下评估这些补丁。Dockerless不是简单地将候选补丁与参考进行匹配，而是通过代理存储库探索收集的证据来判断补丁的正确性。在一个验证器评估基准上，Dockerless比最强的开源验证器高出14.3个AUC点。使用Dockerless作为SFT轨迹过滤器和RL奖励，可以实现完全无环境的训练后管道。由此产生的模型在SWE-bench Verified、Multilingual和Pro上的解决率分别达到了62.0%、50.0%和35.2%。它比Qwen3.5-9B基线高出2.4、8.7和2.9个点，与基于环境的训练后结果相匹配。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
程序验证器（program verifiers）是训练自动化编码代理（如解决软件工程问题的AI模型）的核心工具。它们的作用是判断代码修改是否能正确解决问题，从而指导模型学习（例如筛选高质量训练数据或提供强化学习奖励）。传统上，验证需要在一个隔离的环境中运行测试用例（比如为每个代码仓库单独配置Docker容器），确保代码在特定依赖和配置下能正确执行。这种需求源于现实场景：企业或开源项目中，代码的正确性必须结合实际运行环境来验证，否则训练出的模型可能无法应对真实世界的复杂情况。  

**2. 之前的问题与瓶颈**  
然而，传统方法存在显著缺陷。首先，环境搭建成本高昂：为每个代码仓库配置独立的Docker容器需要解决依赖冲突、编写测试脚本等工程工作，且许多企业或遗留系统无法提供可复现的环境。其次，现有“无环境”验证器（不依赖Docker）仅通过表面文本匹配判断代码正确性，缺乏对代码库上下文的理解。例如，它们无法判断一个修改的函数是否被实际调用，或是否与周围模块兼容。这导致验证结果不可靠，尤其是在处理复杂问题时（如SWE-bench这类需要深度理解代码逻辑的基准测试）。  

**3. 本文的解决方案**  
论文提出了Dockerless，一种无需环境的“智能验证器”。它的核心思路是让验证器主动探索代码库上下文，而非简单匹配文本。具体来说，Dockerless会生成几个关键问题（如“修改的函数是否解决了目标问题？”），然后派遣子代理（sub-agents）从代码库中收集证据（如函数调用关系、模块依赖等），最后综合这些信息判断代码正确性。这种方法结合了代码理解与逻辑推理，能够处理更复杂的场景。  

**4. 与前人工作的关键差异**  
与依赖Docker的传统方法相比，Dockerless避免了环境搭建成本；与无环境的浅层验证器相比，它通过主动探索代码库上下文提高了准确性。此外，Dockerless还支持完全无环境的训练流程：从数据收集到模型优化，均无需为每个代码仓库配置特定环境。实验表明，其性能优于最强的开源验证器，并使训练出的模型在多个基准测试中达到与环境依赖方法相当的水平。  

这种方法的关键创新在于将“环境依赖”从验证环节中移除，同时通过智能探索弥补了浅层方法的不足，为大规模训练编码代理提供了可行的技术方案。

## 方法图解

![Figure 2 : Architecture of Dockerless. The verifier takes the issue x x , refere](fig2_1.webp)

> Figure 2 : Architecture of Dockerless. The verifier takes the issue x x , reference patch y ref y_{\text{ref}} , and candidate patch y y , and proceeds in two stages. (1) Question generation and exploration: the verifier first generates K K verification questions and dispatches parallel sub-agents to collect evidence-backed answers from the codebase. (2) Judgment: the verifier conditions on the issue, the patches, and the collected ( Q k , A k ) (Q_{k},A_{k}) pairs to produce a binary verdict token, whose logits define the continuous score r ϕ ​ ( x , y ) r_{\phi}(x,y) .

这张图展示了论文《Dockerless: Environment-Free Program Verifier for Coding Agents》中提出的Dockerless方法的核心架构，它是一个无需环境的程序验证器，用于评估生成的代码补丁是否正确。整个流程分为两个主要阶段：问题生成与探索（Question Generation & Exploration），以及判断（Judgment）。数据或信息的流动顺序如下：

1.  **输入阶段（Input）**：
    *   最左侧的“Input”板块提供了方法的输入数据，包括：
        *   `Issue (x)`：代表需要修复的软件问题或缺陷描述，通常以文档或文本形式呈现。
        *   `Ref Patch (y_ref)`：参考补丁，即被认为是正确或标准的解决方案。
        *   `Candidate Patch (y)`：待验证的候选补丁，即由编码代理生成的解决方案。

2.  **问题生成与探索阶段（Question Generation & Exploration）**：
    *   这个阶段是方法的核心，旨在通过多维度的问题提出和对代码库的探索来收集证据。
    *   **多维证据探查（Multi-dimensional Evidence Probing）**：
        *   首先，系统会“Generate Question”（生成问题）。这个过程会针对输入的`Issue`、`Ref Patch`和`Candidate Patch`，生成多个（K个）验证问题（`Q₁`, `Q₂`, ..., `Qₖ`）。这些问题从不同维度探查补丁的正确性。例如，`Q₁`可能用定位图标表示，关注代码位置或影响范围；`Q₂`可能用电源图标表示，关注功能或性能；`Q₃`可能用烧瓶图标表示，关注逻辑或算法；`Qₖ`则代表其他类型的问题。
    *   **并行子代理（Parallel Sub-agent）**：
        *   生成的每个问题（`Q₁`到`Qₖ`）都会被分配给一个“Parallel Sub-agent”（并行子代理）。图中显示了`Sub-agent 1`到`Sub-agent k`，它们并行工作以提高效率。
    *   **代码库探索与证据收集**：
        *   这些子代理会与“Static CodeBase”（静态代码库）进行交互，并可能使用工具（`Read Tools`，如图中的扳手图标所示）来读取和分析代码。
        *   探索的结果是为每个问题收集到一个“Evidence-Backed Answer”（有证据支持的答案），即`A₁`, `A₂`, ..., `Aₖ`。这些答案是基于对代码库的分析而得出的，而不是通过执行代码。

3.  **判断阶段（Judgment）**：
    *   在收集到所有问题-答案对（`(Q₁, A₁)`, `(Q₂, A₂)`, ..., `(Qₖ, Aₖ)`）之后，进入判断阶段。
    *   系统会结合原始的`Issue (x)`、`Ref Patch (y_ref)`、`Candidate Patch (y)`以及收集到的问题-答案对来进行“Judge”（判断）。
    *   判断的结果是一个二进制判决令牌（binary verdict token），其逻辑斯蒂（logits）定义了一个连续的分数`r_φ(x, y)`。这个分数`r_φ(x, y) ∈ [0,1]`代表了候选补丁`y`相对于问题`x`的正确性概率或评分。

总结来说，Dockerless方法通过以下步骤运作：
*   首先，根据给定的问题、参考补丁和候选补丁，生成多个验证问题。
*   然后，使用并行子代理对这些问题的答案进行探索，通过对静态代码库和工具的分析来获取证据支持的答案。
*   最后，结合所有这些信息和原始输入，对候选补丁的正确性做出判断，并给出一个连续的评分。

这种方法的关键在于它不需要执行代码，而是通过代码分析和证据收集来判断补丁的正确性，从而实现了一个无需环境的程序验证器。

---

![Figure 3 : Training pipeline for Dockerless: teacher-generated question-answer-j](fig3_1.webp)

> Figure 3 : Training pipeline for Dockerless: teacher-generated question-answer-judge trajectories are rejection-sampled by matching the predicted verdict against the ground-truth, and used to fine-tune a base model.

这张图（图3）展示了Dockerless方法的训练流程，分为两个主要阶段：数据生成和拒绝采样。

首先看**数据生成**阶段（左侧，虚线左侧）：
- 最上方的“Candidate Paths”（候选路径）模块，用数据库图标表示，代表初始的候选代码路径或补丁。
- 这些候选路径被转换为一个元组（Tuple）`(x, y_ref, y, r*)`，其中`x`可能是输入上下文，`y_ref`是参考输出，`y`是生成的输出，`r*`是真实的裁决（即该补丁是否正确的真实标签）。这个元组生成后，输入到“Teacher Model”（教师模型）中。
- 教师模型的作用是生成“Question-Answer-Judge Trajectories τ & Verdict r̂”，即问题-答案-判断轨迹τ和对补丁的预测裁决r̂。这里的轨迹可能包含了教师模型对补丁的推理过程，而r̂是教师模型预测的该补丁是否正确的结果。

然后进入**拒绝采样**阶段（右侧，虚线右侧）：
- 教师模型输出的轨迹τ和预测裁决r̂被送入“Rejection Sampling”（拒绝采样）模块。
- 拒绝采样的逻辑是“Keep if r̂ = r*”，即只有当预测裁决r̂与真实裁决r*匹配时，才保留这个样本。
- 被保留的样本会被整理成“Filtered Data D_rej”（过滤后的数据），其结构包括“Input Context (x, y_ref, y)”（输入上下文）和“Target Sequence z Trajectories τ followed by r*”（目标序列z，包含轨迹τ和真实裁决r*）。这些过滤后的数据将用于微调基础模型。

整体流程的数据流动顺序是：候选路径→生成元组→教师模型生成轨迹和预测裁决→拒绝采样（匹配真实裁决则保留）→过滤后的数据用于微调。

这张图揭示了Dockerless方法的核心训练逻辑：通过教师模型生成包含推理轨迹和预测裁决的数据，然后通过拒绝采样筛选出预测裁决与真实裁决一致的样本，这些样本包含了推理过程（轨迹）和正确标签，用于微调模型，从而实现无环境的程序验证训练。这种方法利用教师模型的推理能力来生成训练数据，避免了传统执行式验证对环境的需求，同时通过拒绝采样确保训练数据的准确性（预测裁决与真实裁决一致）。

---

![Figure 4 : Env-free post-training pipeline for Dockerless. (A) Environment-free ](fig4_1.webp)

> Figure 4 : Env-free post-training pipeline for Dockerless. (A) Environment-free RFT: candidate rollouts are scored by Dockerless, and the top- K K are kept to fine-tune the base model, yielding the SFT model. (B) Environment-free RL: starting from the SFT model, GRPO uses Dockerless as the per-rollout reward source, yielding the RL model.

这张图展示了Dockerless方法的无环境后训练流程，分为两个主要部分：(A) 无环境监督微调（RFT，这里可能是SFT的笔误或特定术语）和(B) 无环境强化学习（RL）。

首先看(A)部分：
- 最左边的“Issues & Agent”模块代表问题（如编程任务或错误报告）和生成代码的代理（Agent）。这个模块输出候选的代码实现（Candidate Rollouts），即代理针对问题生成的多组代码尝试。
- 接下来是“Dockerless”模块，这是一个无环境的程序验证器。它的作用是对这些候选的代码实现进行评分（score），但不是通过执行代码（如在Docker环境中运行单元测试），而是通过代理对代码仓库的探索来收集证据，判断代码补丁的正确性。
- 然后是“Top-K Filtering”（图中显示为筛选出r值较高的，如r=0.98、0.85等，r可能代表评分或正确性分数），这个步骤会从所有候选中选择得分最高的前K个代码实现。
- 最后，这些选中的前K个代码实现被用于“SFT”（监督微调），训练出一个SFT模型。这个过程是无环境的，因为不需要为每个代码实现设置单独的执行环境（如Docker）。

接下来看(B)部分：
- 最左边的“SFT Model”是(A)部分训练得到的监督微调模型，作为强化学习的起点。
- 中间的“Group of Rollouts {y₁, y₂, …, y_G}”代表从SFT模型生成的多个代码实现（rollouts），每个y_i是一个代码尝试。
- 同样，“Dockerless”模块对这些生成的代码实现进行评分，得到每个实现的奖励（r₁, r₂, …, r_G），这里的奖励是基于代码的正确性判断。
- 然后，“GRPO Algorithm”（一种强化学习算法）使用这些奖励来优化模型。GRPO会根据每个rollout的奖励来调整模型参数，以最大化累积奖励。
- 最终，经过GRPO优化的模型成为“RL Model”，这个模型也是无环境训练的，因为奖励的计算不依赖于执行环境。

整个流程的核心是Dockerless作为一个无环境的验证器，在监督微调阶段筛选高质量的代码实现，在强化学习阶段提供基于正确性的奖励，从而实现完全无环境的后训练。这种方法避免了传统执行环境（如Docker）的高昂设置成本，同时通过代理的仓库探索来有效判断代码的正确性。

从结果来看（结合论文摘要），使用Dockerless的无环境后训练流程得到的模型在SWE-bench的三个子任务（Verified、Multilingual、Pro）上的解决率分别达到了62.0%、50.0%和35.2%，超过了Qwen3.5-9B基线模型，并且接近基于环境的后训练模型的性能。

---

![Figure 5 : Verifier AUC vs. number of verification questions K K on SWE-bench Ve](fig5_1.webp)

> Figure 5 : Verifier AUC vs. number of verification questions K K on SWE-bench Verified verifier evaluation benchmark.

这张图（图5）展示了在不同数量的验证问题（# Verification Questions）下，验证器的AUC（Area Under the Curve）性能变化，具体是在SWE-bench Verified验证基准上的表现。

首先，我们来看图的各个组成部分：
- **X轴**：表示验证问题的数量（# Verification Questions），从0到8。这可以理解为在验证过程中提出的疑问或检查点的数量。
- **Y轴**：表示验证器的AUC值（AUC on SWE-bench Verified），范围大约从75.0到85.0。AUC值越高，通常意味着验证器的性能越好，能够更准确地区分正确和错误的代码补丁。
- **数据点**：图中有几个数据点，分别对应不同的验证问题数量，例如：
  - 当验证问题数量为0时，AUC值为78.2。
  - 当验证问题数量为1时，AUC值为80.1。
  - 当验证问题数量为2时，AUC值为80.8。
  - 当验证问题数量为4时，AUC值为81.0，这是图中的一个高点，并且被标记为“sweet spot”（最佳点）。
  - 当验证问题数量为6时，AUC值为79.6。
  - 当验证问题数量为8时，AUC值为80.3。
- **趋势线**：数据点之间用一条线连接，显示了AUC值随验证问题数量变化的趋势。可以看到，随着验证问题数量的增加，AUC值先上升，达到一个峰值（在验证问题数量为4时），然后略有下降，之后又有所回升。
- **“sweet spot”区域**：在验证问题数量为2到4之间，有一个浅蓝色的背景区域，标记为“sweet spot”，表示这个范围内的验证问题数量可能是最佳的，因为在这个范围内AUC值较高且相对稳定。

这张图揭示了方法的具体运作方式：
- 方法（Dockerless）通过提出不同数量的验证问题来评估代码补丁的正确性。随着验证问题数量的增加，验证器的性能（AUC值）会发生变化。
- 从图中可以看出，当验证问题数量从0增加到4时，AUC值逐渐上升，达到一个峰值（81.0），这表明在这个阶段，增加验证问题数量有助于提高验证器的性能。
- 当验证问题数量超过4（例如增加到6）时，AUC值开始下降，这可能是因为过多的验证问题引入了不必要的复杂性或噪声，导致验证器的性能下降。
- 当验证问题数量进一步增加到8时，AUC值又有所回升，但仍然低于峰值（81.0）。这可能是因为在某些情况下，更多的验证问题可以提供更全面的信息，从而提高验证器的性能，但这种提升是有限的。

结论：
- 图中显示，在SWE-bench Verified验证基准上，Dockerless验证器的AUC值随着验证问题数量的变化而变化。最佳的验证问题数量（“sweet spot”）大约在2到4之间，此时AUC值达到最高（81.0）。
- 这表明，在使用Dockerless进行代码补丁验证时，选择适当数量的验证问题可以优化验证器的性能。过多的验证问题并不一定能带来更好的性能，甚至可能导致性能下降。
- 这张图的结果支持了Dockerless方法的有效性，因为它能够在不同的验证问题数量下表现出较好的性能，并且存在一个最佳的验证问题数量范围，使得验证器的性能达到最优。

---

![Figure 8 : Frontier-model resolve rate (%) on SWE-bench Verified, Multilingual, ](fig8_1.webp)

> Figure 8 : Frontier-model resolve rate (%) on SWE-bench Verified, Multilingual, and Pro under env-based and env-free settings. Solid bars are env-free; hatched extensions show the additional gain from per-repository environments, so the full bar height equals the env-based score.

这张图（图8）展示了不同模型在SWE-bench基准测试的三个任务（Verified、Multilingual、Pro）上，在有环境（env-based）和无环境（env-free）设置下的问题解决率（以百分比表示）。我们可以通过以下几个部分来理解这张图：

1.  **坐标轴与任务**：
    *   纵轴列出了四个不同的模型：DS-V3.2、Kimi-K2.5、GLM-5 和 GPT-5.4。这些是用于评估的编码代理模型。
    *   横轴表示“Resolved (%)”，即问题解决率，范围从0%到80%。
    *   图例解释了不同颜色和图案的条形代表的含义：
        *   **青色实心条 (Verified)**：代表“无环境”设置下的解决率。这是使用论文中提出的Dockerless方法（环境无关的代理补丁验证器）获得的结果。
        *   **红色实心条 (Multi.)**：代表“多语言”（Multilingual）任务在“无环境”设置下的解决率。
        *   **黄色实心条 (Pro)**：代表“专业”（Pro）任务在“无环境”设置下的解决率。
        *   **灰色斜线条 (w/o Env)**：这些是附加在青色、红色或黄色实心条末端的斜线部分。它们表示在有环境设置下获得的额外解决率增益。因此，整个条的高度（实心部分+斜线部分）等于该模型在“有环境”设置下的解决率。

2.  **数据的解读与方法的揭示**：
    *   这张图的核心是比较了“无环境”方法（Dockerless）与“有环境”方法在解决编程问题上的表现。
    *   对于每个模型，青色、红色和黄色实心条的长度展示了该方法在不依赖特定执行环境的情况下，能够解决多少百分比的问题。
    *   灰色斜线条的长度则显示了如果使用传统的、需要为每个代码仓库设置特定执行环境（如Docker镜像）的方法，能够额外解决多少问题。
    *   论文的方法（Dockerless）旨在通过代理对代码仓库的探索来收集证据判断补丁的正确性，而不是简单地执行单元测试。这张图通过比较“无环境”和“有环境”的解决率，直观地展示了Dockerless方法的有效性。

3.  **对比对象和结论**：
    *   **对比对象**：主要对比的是同一模型在“无环境”设置下的表现（青色、红色、黄色实心条）与其在“有环境”设置下的潜在表现（整个条的高度，包括斜线部分）。
    *   **具体数据示例**：
        *   对于模型 **GPT-5.4**：
            *   在“无环境”设置下，其在“Verified”任务上的解决率为76.4%（青色条）。
            *   在“无环境”设置下，其在“Multilingual”任务上的解决率为72.7%（红色条）。
            *   在“无环境”设置下，其在“Pro”任务上的解决率为54.7%（黄色条）。
            *   灰色斜线条非常短，表明GPT-5.4在“有环境”设置下的额外增益很小，或者说Dockerless方法已经非常接近有环境的表现。
        *   对于模型 **DS-V3.2**：
            *   “无环境”下的“Verified”解决率为72.6%。
            *   “无环境”下的“Multilingual”解决率为58.3%。
            *   “无环境”下的“Pro”解决率为48.0%。
            *   灰色斜线条相对较长，表明在有环境下有较大的增益空间。
    *   **结论**：这张图表明，尽管“有环境”方法通常能获得更高的解决率（因为可以实际执行代码），但论文提出的“无环境”方法（Dockerless）已经取得了非常接近甚至在某些情况下（如GPT-5.4的Verified任务）可能相当或更好的结果。这证明了环境无关的程序验证是可行的，并且可以用于构建完全环境无关的训练后管道（post-training pipeline），如论文摘要所述。

总而言之，这张图通过比较不同模型在不同任务和不同环境设置下的问题解决率，清晰地展示了Dockerless方法的有效性和性能。它说明了在不依赖特定执行环境的情况下，仍然可以实现较高的问题解决率，这对于降低训练编码代理的环境设置成本具有重要意义。
