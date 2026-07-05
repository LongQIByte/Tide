# Dockerless: Environment-Free Program Verifier for Coding Agents

[arXiv](https://arxiv.org/abs/2606.28436) · [HuggingFace](https://huggingface.co/papers/2606.28436) · ▲103

## 摘要（原文）

> Program verifiers play a central role in training coding agents, including selecting trajectories for supervised fine-tuning (SFT) and providing rewards for reinforcement learning (RL). Standard execution-based verification requires running unit tests inside per-repository environments such as Docker images, incurring substantial environment setup costs. We propose Dockerless, an environment-free agentic patch verifier that evaluates generated code patches without executing them. Rather than simply matching candidate patches to references, Dockerless judges patch correctness using evidence gathered through agentic repository exploration. On a verifier evaluation benchmark, Dockerless outperforms the strongest open-source verifier by 14.3 AUC points. Using Dockerless as both the SFT trajectory filter and the RL reward enables a fully environment-free post-training pipeline. The resulting model reaches 62.0%, 50.0%, and 35.2% resolve rate on SWE-bench Verified, Multilingual, and Pro, respectively. It surpasses the Qwen3.5-9B baseline by 2.4, 8.7, and 2.9 points, matching environment-based post-training.

## 摘要（中译）

程序验证器在训练编码代理中起着核心作用，包括为监督微调（supervised fine - tuning，SFT）选择轨迹以及为强化学习（reinforcement learning，RL）提供奖励。标准的基于执行的验证需要在每个存储库环境（如Docker镜像）中运行单元测试，这会带来大量的环境设置成本。我们提出了Dockerless，一种无环境的代理补丁验证器，它可以在不执行生成代码补丁的情况下评估这些补丁。Dockerless不是简单地将候选补丁与参考进行匹配，而是通过代理存储库探索收集的证据来判断补丁的正确性。在一个验证器评估基准上，Dockerless比最强的开源验证器高出14.3个AUC点。将Dockerless同时作为SFT轨迹过滤器和RL奖励，可以实现一个完全无环境的训练后管道。由此产生的模型在SWE - bench Verified、Multilingual和Pro上的解决率分别达到62.0%、50.0%和35.2%。它比Qwen3.5 - 9B基线高出2.4、8.7和2.9个点，与基于环境的训练后效果相当。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
程序验证器（program verifiers）是训练自动化编码代理（如解决软件工程问题的AI模型）的核心工具。它们的作用是判断代码修改是否正确解决了问题，从而指导模型学习（例如筛选高质量训练数据或提供强化学习奖励）。传统上，验证需要在一个隔离的运行环境中执行测试用例（比如为每个代码仓库单独配置Docker容器），这在实际应用中至关重要——无论是开源项目还是企业内部代码库，都需要确保AI生成的修复方案真正有效。  

**2. 先前方法的局限性**  
然而，现有的执行式验证方法存在显著缺陷。首先，环境搭建成本高昂：每个代码仓库可能需要定制化的依赖配置和测试脚本，而许多真实场景（如私有代码库或遗留系统）甚至无法提供可复现的环境。其次，浅层验证方法（如仅比较代码文本差异）无法理解代码库的深层逻辑，导致复杂问题判断错误。即使是先进的共享环境方案（如统一Docker镜像），也因缺乏针对性分析而成为性能瓶颈。这些限制使得训练高效的编码代理变得困难且昂贵。  

**3. 本文的解决方案**  
论文提出了Dockerless，一种无需运行环境的程序验证器。其核心思路是让验证器主动“探索”代码库：通过生成验证问题、派遣子代理收集上下文证据（例如函数调用关系或模块依赖），最终综合判断代码修改的正确性。这种方法不依赖执行测试，而是利用代码库本身的信息进行推理，从而解决了环境依赖和浅层分析的问题。  

**4. 与前人的关键差异**  
Dockerless的创新在于将验证从“被动匹配文本”转变为“主动探索上下文”。与依赖Docker环境的传统方法不同，它不需要任何运行时环境；与仅比较代码差异的浅层方法相比，它通过多代理协作深入理解代码逻辑。实验表明，这种环境无关的验证不仅效率更高，还能在真实任务中达到与执行式验证相当的性能，为大规模训练编码代理提供了可行的路径。

## 方法图解

![Figure 2 : Architecture of Dockerless. The verifier takes the issue x x , refere](fig2_1.webp)

> Figure 2 : Architecture of Dockerless. The verifier takes the issue x x , reference patch y ref y_{\text{ref}} , and candidate patch y y , and proceeds in two stages. (1) Question generation and exploration: the verifier first generates K K verification questions and dispatches parallel sub-agents to collect evidence-backed answers from the codebase. (2) Judgment: the verifier conditions on the issue, the patches, and the collected ( Q k , A k ) (Q_{k},A_{k}) pairs to produce a binary verdict token, whose logits define the continuous score r ϕ ​ ( x , y ) r_{\phi}(x,y) .

这张图展示了Dockerless方法的整体架构，它是一个无环境的代理补丁验证器，用于评估生成的代码补丁是否正确，而无需实际执行代码。整个流程分为两个主要阶段：问题生成与探索，以及判断。

首先，在最左边的“Input”（输入）部分，有三个关键输入：
1.  **Issue (x)**：表示需要解决的问题或任务描述，通常是一个编程问题或bug报告。
2.  **Ref Patch (y_ref)**：参考补丁，即被认为是正确的解决方案。
3.  **Candidate Patch (y)**：待验证的候选补丁，即由编码代理生成的解决方案。

接下来是第一个主要阶段：“Question Generation”（问题生成）。
*   这个阶段的输入是上述三个输入（Issue, Ref Patch, Candidate Patch）。
*   首先进行“Generate Question”（生成问题）。这个模块会针对输入的补丁和问题，生成多个验证问题。图中显示了几个示例问题 Q₁, Q₂, Q₃, ..., Qₖ，每个问题都有不同的图标，可能代表不同类型的问题（例如，Q₁可能是关于位置的，Q₂可能是关于功能的，Q₃可能是关于逻辑的）。
*   这个过程被称为“Multi-dimensional Evidence Probing”（多维证据探查），意味着从多个角度对补丁进行提问，以收集全面的证据。

然后是第二个主要阶段：“Exploration”（探索）。
*   这个阶段接收从“Question Generation”阶段产生的多个问题（Q₁, Q₂, ..., Qₖ）。
*   这些问题被分发给多个“Parallel Sub-agent”（并行子代理），图中有 Sub-agent 1 到 Sub-agent k。这些子代理并行工作，提高效率。
*   每个子代理会访问“Static CodeBase”（静态代码库）并使用“Read Tools”（读取工具）来收集信息。它们从代码库中检索与问题相关的证据，并生成“Evidence-Backed Answer”（有证据支持的答案），如图中的 A₁, A₂, ..., Aₖ。每个答案旁边都有一个绿色的对勾，表示这些答案是经过验证或有依据的。

最后是第三个主要阶段：“Judgment”（判断）。
*   这个阶段的输入包括原始的 Issue (x)、Candidate Patch (y)、以及从“Exploration”阶段收集到的所有 (Qₖ, Aₖ) 对。
*   这些信息被输入到“Judge”（判断器）模块。判断器基于这些证据来判断候选补丁是否正确。
*   判断的结果是一个二进制判决令牌（binary verdict token），其逻辑值（logits）定义了一个连续的分数 r_φ(x,y)，这个分数通常在0到1之间，表示候选补丁正确的概率或置信度。

总结来说，Dockerless的工作流程是：
1.  接收问题、参考补丁和候选补丁作为输入。
2.  针对这些输入生成多个验证问题。
3.  使用并行子代理从静态代码库中探索并收集每个问题的答案作为证据。
4.  基于这些问题、答案以及原始输入，由判断器给出一个分数，表示候选补丁的正确性。

这种方法的关键在于，它通过代理对代码库的探索来收集证据，而不是通过执行代码来进行验证，从而实现了无环境的验证。这使得训练编码代理的流程可以在没有Docker等环境的情况下进行，降低了环境设置的成本。

图中的箭头表示数据和信息的流动方向，从输入开始，经过问题生成、探索，最终到达判断阶段并输出一个分数。

---

![Figure 3 : Training pipeline for Dockerless: teacher-generated question-answer-j](fig3_1.webp)

> Figure 3 : Training pipeline for Dockerless: teacher-generated question-answer-judge trajectories are rejection-sampled by matching the predicted verdict against the ground-truth, and used to fine-tune a base model.

这张图展示了Dockerless方法的训练流程，分为**数据生成**和**拒绝采样**两个主要阶段，清晰呈现了从候选路径到最终过滤数据的完整过程：

### 1. 数据生成阶段（左侧）
- **Candidate Paths（候选路径）**：这是初始的输入，代表可能的代码补丁或程序执行路径，作为后续处理的原材料。
- **Tuple \((x, y_{\text{ref}}, y, r^*)\)**：候选路径经过处理后，生成一个元组。其中：
  - \(x\) 可能是输入上下文（如问题描述、代码仓库信息等）；
  - \(y_{\text{ref}}\) 是参考输出（或预期输出）；
  - \(y\) 是生成的输出（如代码补丁的结果）；
  - \(r^*\) 是真实标签（即该补丁是否正确的“ ground - truth 判决”）。
- **Teacher Model（教师模型）**：这个元组被输入到教师模型中。教师模型的作用是生成**Question - Answer - Judge Trajectories \(\tau\)**（问答 - 判断轨迹）和**Verdict \(\hat{r}\)**（预测的判决，即模型判断该补丁是否正确）。简单来说，教师模型会基于输入的元组，模拟“提问（关于补丁的问题）、回答（模型对问题的回应）、判断（对补丁正确性的判决）”的过程，同时输出对补丁正确性的预测。

### 2. 拒绝采样阶段（中间及右侧）
- **Rejection Sampling（拒绝采样）**：教师模型输出的\(\hat{r}\)（预测判决）会与真实的\(r^*\)（真实判决）进行比较。只有当\(\hat{r} = r^*\)（即预测正确）时，对应的数据才会被保留（图中“Keep if \(\hat{r}=r^*\)”的漏斗表示这个过滤过程）。
- **Filtered Data \(\mathcal{D}_{\text{rej}}\)**：被保留的数据会形成过滤后的数据集，其结构包括：
  - **Input Context \((x, y_{\text{ref}}, y)\)**：输入上下文，包含问题、参考输出和生成输出等信息；
  - **Target Sequence \(z\)**：目标序列（可能是用于训练的特定序列）；
  - **Trajectories \(\tau\) followed by \(r^*\)**：问答 - 判断轨迹以及对应的真实判决。

### 方法运作逻辑
整个流程的核心是**利用教师模型生成轨迹并过滤**：首先从候选路径生成包含输入、参考、生成结果和真实判决的元组，输入教师模型得到轨迹和预测判决；然后通过拒绝采样（仅保留预测判决与真实判决一致的数据），得到高质量的过滤数据。这些过滤数据可用于微调基础模型（如作为监督微调SFT的轨迹或强化学习RL的奖励信号），从而实现无环境的代码验证器训练。

### 数据流动顺序
候选路径 → 生成元组\((x, y_{\text{ref}}, y, r^*)\) → 输入教师模型 → 生成轨迹\(\tau\)和预测判决\(\hat{r}\) → 拒绝采样（\(\hat{r}=r^*\)则保留）→ 过滤后的数据\(\mathcal{D}_{\text{rej}}\)。

这张图清晰地展示了Dockerless如何通过“教师模型 + 拒绝采样”的方式，从原始候选路径中筛选出高质量数据，用于训练无环境的代码验证器，避免了传统执行式验证的环境设置成本。

---

![Figure 4 : Env-free post-training pipeline for Dockerless. (A) Environment-free ](fig4_1.webp)

> Figure 4 : Env-free post-training pipeline for Dockerless. (A) Environment-free RFT: candidate rollouts are scored by Dockerless, and the top- K K are kept to fine-tune the base model, yielding the SFT model. (B) Environment-free RL: starting from the SFT model, GRPO uses Dockerless as the per-rollout reward source, yielding the RL model.

这张图展示了Dockerless方法的无环境后训练流程，分为两个主要部分：(A) 无环境监督微调（RFT，这里可能是SFT的笔误或特定术语）和(B) 无环境强化学习（RL）。

首先看(A)部分：
- 最左边的“Issues & Agent”模块代表问题（如编程任务或错误报告）和生成代码的代理（Agent）。这个模块输出候选的代码实现（“Candidates Rollouts”），即代理针对问题生成的多个代码尝试。
- 接下来是“Dockerless”模块，这是一个无环境的程序验证器。它的作用是对这些候选的代码实现进行评分（图中显示了不同的分数，如r=0.98、0.85等），而不需要运行单元测试或使用Docker等环境。这里的评分是基于代理对代码仓库的探索证据来判断补丁的正确性。
- 然后是“Top-K Filtering”（图中用漏斗图标表示），它会根据Dockerless给出的分数，选择得分最高的前K个候选（图中显示了筛选后的分数，如保留了r=0.98、0.85、0.62等，而过滤掉了r=0.31、0.12等较低的分数）。
- 最后，这些筛选后的候选会被用于“SFT”（监督微调），得到一个SFT模型。这个过程是无环境的，因为不需要实际运行代码的环境，只需要Dockerless的评分来选择好的候选进行微调。

然后看(B)部分：
- 最左边的“SFT Model”是(A)部分得到的监督微调模型，作为强化学习的起点。
- 接下来是“Group of Rollouts {y₁, y₂, …, y_G}”，这里G是滚动的数量，即从SFT模型出发，生成的一组代码实现（滚动），每个实现标记为y₁到y_G。
- 中间的“Dockerless”模块再次发挥作用，为每个滚动（y₁到y_G）提供奖励（图中显示了r₁到r_G，这些奖励是Dockerless根据代码的正确性等证据给出的）。
- 然后是“GRPO Algorithm”（一种强化学习算法，可能是Proximal Policy Optimization的变体），它使用Dockerless提供的奖励来优化模型。图中显示了“Reward”和“Policy”的循环，说明RL算法通过不断调整策略（模型）来最大化奖励。
- 最后，经过GRPO训练后得到“RL Model”，这个模型是无环境的，因为它使用Dockerless作为奖励源，而不需要实际运行代码的环境。

整体流程是：首先通过无环境的Dockerless筛选候选代码进行SFT，得到SFT模型；然后以SFT模型为基础，使用Dockerless提供的无环境奖励进行RL训练，得到最终的RL模型。这种方法避免了使用Docker等环境的高成本，同时通过代理的仓库探索来评估代码的正确性，从而实现无环境的后训练。

从结果来看（结合论文摘要），使用这种无环境管道训练的模型在SWE-bench Verified、Multilingual和Pro上的解决率分别达到了62.0%、50.0%和35.2%，超过了Qwen3.5-9B基线，并且匹配了基于环境的后训练的性能。

---

![Figure 5 : Verifier AUC vs. number of verification questions K K on SWE-bench Ve](fig5_1.webp)

> Figure 5 : Verifier AUC vs. number of verification questions K K on SWE-bench Verified verifier evaluation benchmark.

这张图（图5）展示了在不同数量的验证问题（# Verification Questions，横轴）下，验证器的AUC（Area Under the Curve，纵轴）表现，具体是在SWE-bench Verified验证器评估基准上的结果。

首先看横轴，它表示验证问题的数量K，从0到8不等。这代表了在进行代码补丁验证时，所提出的问题或查询的数量。随着K的增加，我们可以观察到验证器性能的变化趋势。

纵轴是AUC值，范围从75.0到85.0，用于衡量验证器的性能。AUC值越高，通常表示验证器的区分能力越强，即能更准确地区分正确和错误的代码补丁。

图中的曲线展示了随着验证问题数量K的增加，AUC值的变化情况：
- 当K=0时，AUC值为78.2。
- 随着K增加到1，AUC值上升到80.1。
- 当K=2时，AUC值进一步增加到80.8。
- 在K=4时，AUC值达到了一个较高的点，为81.0，这个区域被标记为“sweet spot”（最佳点），表明在这个验证问题数量下，验证器的性能表现最佳。
- 当K继续增加到6时，AUC值下降到79.6。
- 最后，当K=8时，AUC值又回升到80.3。

从这张图中，我们可以看出，随着验证问题数量的增加，验证器的AUC值先上升，在K=4时达到峰值，然后有所下降，之后又略有回升。这表明存在一个最佳的验证问题数量（K=4左右），在这个数量下，验证器能够达到最佳的AUC性能。这种方法（Dockerless）通过调整验证问题的数量来优化验证器的性能，从而在不依赖环境（如Docker）的情况下，有效地评估代码补丁的正确性。通过这种方式，Dockerless能够在SWE-bench Verified基准上取得较好的验证效果，进而支持后续的模型训练（如监督微调SFT和强化学习RL）。

---

![Figure 8 : Frontier-model resolve rate (%) on SWE-bench Verified, Multilingual, ](fig8_1.webp)

> Figure 8 : Frontier-model resolve rate (%) on SWE-bench Verified, Multilingual, and Pro under env-based and env-free settings. Solid bars are env-free; hatched extensions show the additional gain from per-repository environments, so the full bar height equals the env-based score.

这张图（图8）展示了在不同设置下（基于环境vs无环境），前沿模型在SWE-bench基准测试的三个子任务（Verified、Multilingual、Pro）上的问题解决率（以百分比表示）。我们可以通过以下几个部分来理解这张图：

首先，图的Y轴列出了四个不同的模型：DS-V3.2、Kimi-K2.5、GLM-5 和 GPT-5.4。X轴则表示“Resolved (%)”，即问题解决率，范围从0%到80%。

图中的每条水平条代表一个模型在特定任务上的表现。这些条被分为几个部分，每个部分用不同的颜色和图案表示，并且对应于图例中的一个类别：
*   **青色实心条（图例中标记为“Verified”）**：这部分代表了在**无环境**设置下，模型通过论文中提出的“Dockerless”方法（一种无需执行代码的环境无关验证器）成功解决的问题比例。这是图中主要的、完整的条形部分。
*   **红色实心条（图例中标记为“Multi.”）**：这部分代表了在**无环境**设置下，模型解决的“Multilingual”（多语言）子任务的问题比例。
*   **黄色实心条（图例中标记为“Pro”）**：这部分代表了在**无环境**设置下，模型解决的“Pro”子任务的问题比例。
*   **浅绿色斜线填充的延伸部分（图例中标记为“w/o Env”）**：这部分是附加在青色“Verified”条末端的斜线区域。它显示了如果使用**基于环境**的设置（例如，使用Docker容器等）所能获得的额外解决率提升。因此，整个条的总高度（青色部分加上斜线部分）等于该模型在**基于环境**设置下的解决率。

数据的流动和组织方式如下：对于每个模型，我们从左到右读取其解决率。青色部分是无环境下的“Verified”解决率，红色和黄色部分分别显示了在同一无环境设置下，“Multilingual”和“Pro”子任务的解决率。斜线部分则展示了切换到基于环境设置后，“Verified”任务解决率的增加量。

这张图揭示了论文方法的具体运作方式和优势：
1.  **无环境验证**：论文提出的“Dockerless”方法能够在不依赖传统执行环境（如Docker）的情况下，对代码补丁进行验证。图中的青色、红色和黄色部分展示了这种方法在三个不同子任务上的表现。
2.  **环境带来的增益**：通过比较青色部分（无环境）和整个条的高度（无环境+环境增益），我们可以看到基于环境的设置在“Verified”任务上能带来额外的解决率提升。这表明，尽管“Dockerless”方法很有前景，但传统的基于环境的方法在某些情况下仍然能解决更多问题。
3.  **模型性能对比**：我们可以直接比较不同模型在相同条件下的表现。例如，在“无环境”设置下，GPT-5.4在“Verified”任务上的解决率为76.4%，而DS-V3.2为72.6%。同样，我们可以比较它们在“Multilingual”和“Pro”子任务上的表现。
4.  **环境增益的量化**：斜线部分的具体数值（如DS-V3.2的58.3% - 48.0% = 10.3%的增益，或者更准确地看斜线部分的长度）量化了环境对“Verified”任务解决率的贡献。

结论部分可以从图中得出：
*   在无环境设置下，GPT-5.4在“Verified”任务上的表现最佳，达到了76.4%。
*   对于所有展示的模型，“Verified”任务在切换到基于环境设置后，解决率都有所提高（通过斜线部分体现）。
*   这张图有效地展示了论文方法（无环境验证）的性能，并将其与基于环境的验证方法进行了对比，突出了无环境方法的潜力和与传统方法相比的差距或优势。

总结来说，这张图通过清晰的视觉元素（不同颜色的条和图例）展示了不同模型在不同任务和不同设置下的问题解决率，使我们能够直观地理解论文中提出的“Dockerless”方法的效果以及环境设置对性能的影响。
