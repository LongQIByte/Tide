# The Mirage of Optimizing Training Policies: Monotonic Inference Policies as the Real Objective for LLM Reinforcement Learning

[arXiv](https://arxiv.org/abs/2606.29526) · [HuggingFace](https://huggingface.co/papers/2606.29526) · ▲6

## 摘要（原文）

> Reinforcement learning (RL) has gained growing attention in large language model (LLM) post-training, yet RL training remains fragile and can suffer from instability or collapse. One vital cause is training-inference mismatch: LLM adopts separate inference and training engines for generation efficiency and training precision, which in practice exhibits inconsistent probabilities for the same trajectories on training and inference sides, even with synchronized model parameters. This naturally induces a special type of off-policyness ever existing and poisoning the training. Prior works have made various efforts in addressing the off-policyness to stabilize the training policies under the mismatch. In this paper, we point out the objective misalignment neglected by existing works that an effective update to the policy in the training engine not necessarily ensures the improvement of the inference policy, i.e., the one used in deployment. To this end, we propose a new policy optimization objective for LLM RL, named Monotonic Inference Policy Improvement (MIPI). Following this principle, we introduce Monotonic Inference Policy Update (MIPU), a two-step LLM RL framework that constructs sampler-referenced candidate updates and selectively accepts synchronized candidates using an inference-side gap proxy. Experiments conducted on two model scales under high mismatch show that MIPU improves average reasoning performance and training stability.

## 摘要（中译）

强化学习（Reinforcement learning, RL）在大语言模型（large language model, LLM）后训练中越来越受到关注，然而RL训练仍然很脆弱，可能会出现不稳定或崩溃的情况。一个关键原因是训练-推理不匹配：LLM为了生成效率和训练精度采用了独立的推理和训练引擎，即使在模型参数同步的情况下，实际上在训练和推理两侧对相同轨迹的概率表现并不一致。这自然会引发一种特殊类型的偏离策略（off-policyness），这种策略一直存在并影响着训练。先前的工作已经在解决偏离策略问题上做出了各种努力，以在匹配不匹配的情况下稳定训练策略。在本文中，我们指出了现有工作忽略的目标不对齐问题，即在训练引擎中对策略的有效更新并不一定确保推理策略的改进，即在部署中使用的策略。为此，我们提出了一种新的LLM RL策略优化目标，名为单调推理策略改进（Monotonic Inference Policy Improvement, MIPI）。遵循这一原则，我们引入了单调推理策略更新（Monotonic Inference Policy Update, MIPU），这是一个两步LLM RL框架，它构建了基于采样器的候选更新，并使用推理侧的差距代理选择性地接受同步候选。在高匹配的情况下，对两个模型规模进行的实验表明，MIPU提高了平均推理性能和训练稳定性。

## 背景剖析

随着推理导向模型（如DeepSeek-R1）的出现，强化学习（RL）已成为大语言模型（LLM）后训练的重要范式，主要用于提升指令遵循、对齐和推理能力。由于LLM规模庞大，现代RL流程通常将生成（由推理引擎完成）与梯度计算（由训练引擎完成）分离。这种分离导致训练策略和推理策略在相同轨迹上可能分配不同概率，即使参数同步也是如此，从而引发训练-推理不匹配问题。  

先前方法主要通过修正采样比例、过滤不稳定样本或缩小系统差异来缓解这一问题，但这些努力仅关注训练侧稳定性，未解决核心矛盾：训练策略的改进未必能提升实际部署的推理策略。例如，即使训练策略在优化目标下表现更好，推理端可能因量化或解码差异而性能下降。  

本文提出“单调推理策略改进（MIPI）”原则，强调优化应直接针对推理策略的性能提升。基于此，设计了“单调推理策略更新（MIPU）”框架，分两步解决问题：第一步通过采样参考更新生成候选模型，确保部分单调性；第二步通过推理端差距代理选择性接受更新，保证剩余单调性。实验表明，在高不匹配场景（如FP8量化推理）下，MIPU显著提升了推理性能和训练稳定性。  

与前人工作相比，本文的关键差异在于：1）重新定义优化目标，从“改进训练策略”转向“改进推理策略”；2）提出两阶段框架，明确分离候选生成与接受步骤；3）首次通过推理端差距代理实现选择性更新，而非单纯减少不匹配。这种方法更贴近实际部署需求，为RL在LLM中的稳定应用提供了新方向。

## 方法图解

![Figure 1: Monotonic Inference Policy Update (MIPU) resolves the Objective Misali](fig1_1.webp)

> Figure 1: Monotonic Inference Policy Update (MIPU) resolves the Objective Misalignment issue of LLM RL. Canonical LLM RL accepts synchronized updates by a training-side objective, which does not necessarily imply improvement of the inference policy. Here, π {\color[rgb]{0,0,1}\definecolor[named]{pgfstrokecolor}{rgb}{0,0,1}\pi} and μ {\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\mu} denote the training policy and inference policy respectively, c c is a tolerance parameter accounting for proxy noise. To address this mismatch, we propose a new principle as monotonic improvement on the inference-policy trajectory (the MIPI principle). MIPU realizes this principle with two steps: Step 1 optimizes Terms ②+③, while Step 2 estimates and validates Term ①, jointly covering all three terms in the MIPI decomposition.

这张图展示了**单调推理策略更新（MIPU）**如何解决大模型强化学习（LLM RL）中的**目标不对齐**问题，我们可以分板块拆解其逻辑和流程：  

### 1. 传统RL的问题（最上方“Canonical RL”板块）  
- **流程顺序**：首先进行“Training - side update（训练侧更新）”，目标是优化训练策略的性能提升（即 \( J(\pi_{k + 1}) - J(\pi_k) \)，这里 \( J \) 是性能指标，\( \pi \) 是训练策略）；然后执行“Sync（同步）”，将训练策略 \( \pi_{k + 1} \) 同步为推理策略 \( \mu_{k + 1} \)。  
- **关键问题**：这个同步更新**没有推理侧的验证**（“No inference - side validation”），直接进行同步。而同步后的结果有两种可能：  
  - 绿色框“Beneficial Synchronized outcome”：推理策略的性能提升（\( \Delta J(\mu) > 0 \)，即 \( J(\mu_{k + 1}) - J(\mu_k) > 0 \)）；  
  - 红色框“Risky Synchronized outcome”：推理策略的性能下降（\( \Delta J(\mu) < 0 \)，即 \( J(\mu_{k + 1}) - J(\mu_k) < 0 \)）。  
- **核心矛盾（Objective misalignment）**：训练侧的性能提升（\( J(\pi_{k + 1}) - J(\pi_k) \geq 0 \)）**并不必然**带来推理侧的性能提升（\( J(\mu_{k + 1}) - J(\mu_k) \geq 0 \)）——这就是“目标不对齐”，也是传统LLM RL脆弱、易不稳定/崩溃的重要原因。  


### 2. 解决思路：单调推理策略改进（MIPI）  
- **定义**：MIPI是“基于推理策略的单调改进原则”，它将推理策略的性能变化 \( J(\mu_{k + 1}) - J(\mu_k) \) 分解为三个部分（对应图中的三个项）：  
  1. \( J(\mu_{k + 1}) - J(\pi_{k + 1}) \)：**更新后推理侧与训练侧的差距**（Post - update inference gap）；  
  2. \( J(\pi_{k + 1}) - J(\pi_k) \)：**训练侧的性能提升**（Training - side update）；  
  3. \( J(\pi_k) - J(\mu_k) \)：**更新前推理侧与训练侧的差距**（Pre - update inference gap）。  
- **作用**：MIPI要求这三个部分的组合变化是“单调改进”的，即确保推理策略的性能随更新单调提升，解决“训练侧优化不代表推理侧优化”的问题。  


### 3. 具体实现：MIPU的两步流程  
MIPU是MIPI的“两步实现”，流程如下：  

#### Step 1：Sampler - Referenced Update（采样器参考更新）  
- **操作**：优化MIPI分解中的“Term ② + ③”（即 \( J(\pi_{k + 1}) - J(\pi_k) + J(\pi_k) - J(\mu_k) \)）。具体实现用了“TRUNC(\( \frac{\pi_k}{\mu_k} \))·CLIP(\( \frac{\pi_\theta}{\pi_k} \))”（这部分是技术细节，核心是针对训练侧和推理侧的差距优化）。  
- **输出**：得到更新后的训练策略 \( \pi_{k + 1} \)，然后执行“Sync”，将 \( \pi_{k + 1} \) 同步为 \( \mu_{k + 1} \)（这一步和传统RL的同步类似，但后续有验证）。  


#### Step 2：Inference - Gap - Aware Acceptance（推理差距感知的接受机制）  
- **验证环节**：估计并验证“Term ①”（即 \( J(\mu_{k + 1}) - J(\pi_{k + 1}) \)，更新后推理侧与训练侧的差距）。这里用 \( \hat{T}_{\text{post}} \approx J(\mu_{k + 1}) - J(\pi_{k + 1}) \) 来近似这个差距（\( \hat{T}_{\text{post}} \) 是“推理后差距的代理”）。  
- **接受/回滚决策**：  
  - 如果 \( \hat{T}_{\text{post}} \geq -c \)（\( c \) 是容忍参数，用于处理代理噪声）：通过“接受准则”，**接受**这次同步（即使用 \( (\pi_{k + 1}, \mu_{k + 1}) \) 作为新的策略对）；  
  - 如果 \( \hat{T}_{\text{post}} < -c \)：**回滚**到之前的策略对 \( (\pi_k, \mu_k) \)，不进行这次更新。  


### 整体逻辑总结  
传统LLM RL直接同步训练侧更新到推理侧，忽略了“训练侧优化≠推理侧优化”的目标不对齐问题。MIPU通过**两步**解决：第一步优化训练侧和推理侧的“历史差距 + 训练侧提升”，第二步验证“更新后推理侧与训练侧的差距”是否满足容忍条件，从而确保推理策略的性能单调提升，解决训练-推理不匹配导致的训练不稳定问题。实验（论文中）表明，MIPU在高不匹配场景下能提升平均推理性能和训练稳定性。

---

![Figure 3: Training curves for ablation studies under FP8-quantized rollout. We s](fig3_1.webp)

> Figure 3: Training curves for ablation studies under FP8-quantized rollout. We show the training score, the inference-training K3-KL, T ^ post \widehat{T}_{\mathrm{post}} (i.e., inference gap) and the rollback rate computed over a 100-step moving window. Step 1 improves the candidate update direction, while Step 2 introduces inference-gap-aware acceptance to filter unreliable synchronized candidates. The full method obtains stronger performance with a more controlled inference-policy trajectory.

这张图展示了在FP8量化回滚设置下的消融实验训练曲线，用于验证论文中提出的方法的有效性。我们可以从四个子图来理解整个实验的设计和方法的运作方式：

首先，最左边的子图是“Reward”（奖励），它展示了不同方法在训练过程中的奖励变化情况。横轴是“Training Step”（训练步数），纵轴是“pass@1”（可以理解为一次通过率或成功解决问题的比例）。图中有四条曲线，分别代表不同的方法：红色是“baseline”（基线方法），橙色是“+ step 1”（基线方法加上第一步改进），浅橙色是“+ step 2”（基线方法加上第二步改进），黄色是“ours”（我们的完整方法）。从图中可以看到，随着训练步数的增加，奖励逐渐上升并趋于稳定。其中，“ours”方法的奖励最高且最稳定，说明我们的方法在提高训练性能方面更有效。

接下来是第二个子图“Mismatch-K3”，它展示了训练和推理之间的不匹配情况，具体是K3-KL散度。横轴同样是“Training Step”，纵轴是“Mismatch-K3”的值。这个值越大，说明训练和推理之间的不匹配越严重。从图中可以看到，不同方法的曲线走势不同。“baseline”方法的曲线波动较大且整体较高，而“+ step 1”、“+ step 2”和“ours”方法的曲线相对更平稳且数值更低，尤其是“ours”方法，说明我们的方法能够有效减少训练和推理之间的不匹配。

第三个子图是“Inference Gap”（推理差距），它展示了推理端的差距代理。横轴是“Training Step”，纵轴是“Inference Gap”的值。这个值反映了推理端的不确定性或误差。从图中可以看到，不同方法的曲线波动情况不同。“baseline”方法的曲线波动较大，而“+ step 1”、“+ step 2”和“ours”方法的曲线相对更平稳，尤其是“ours”方法，说明我们的方法能够更好地控制推理端的差距。

最后是第四个子图“Rollback Rate”（回滚率），它展示了在100步移动窗口内计算的回滚率。横轴是“Training Step”，纵轴是“Rollback Rate”的值。回滚率越高，说明需要回滚的次数越多，训练的稳定性可能越差。从图中可以看到，“baseline”方法的回滚率较高且波动较大，而“+ step 1”、“+ step 2”和“ours”方法的回滚率相对较低且更平稳，尤其是“ours”方法，说明我们的方法能够提高训练的稳定性。

现在我们来理解论文中的方法是如何运作的。论文提出了一个名为Monotonic Inference Policy Improvement (MIPI)的新策略优化目标，以及一个名为Monotonic Inference Policy Update (MIPU)的两步LLM RL框架。MIPU的第一步是改进候选更新的方向，第二步是引入推理差距感知的接受机制来过滤不可靠的同步候选。从图中的曲线可以看出，“+ step 1”方法在第一歩改进后，性能有所提升，而不匹配和回滚率有所降低。然后，“+ step 2”方法在第二步改进后，性能进一步提升，不匹配和回滚率进一步降低。最终的“ours”方法（即完整的方法）在奖励、不匹配、推理差距和回滚率方面都表现最好，说明我们的方法能够有效地提高训练性能和稳定性。

总结一下，这张图通过四个子图展示了不同方法在训练过程中的奖励、训练推理不匹配、推理差距和回滚率的变化情况。结果表明，我们的方法（ours）在所有指标上都优于基线方法和仅使用第一步或第二步改进的方法，说明我们的方法能够有效地解决训练推理不匹配问题，提高训练的稳定性和性能。

---

![(a) Inference-training K3-KL and inference gap. (b) Step 2 vs. random rollback. ](fig4_1.webp)

> (a) Inference-training K3-KL and inference gap. (b) Step 2 vs. random rollback. Figure 4: (a) Inference-training K3-KL and T ^ post \widehat{T}_{\mathrm{post}} (i.e., inference gap) under FP8-quantized rollout. Qwen3-1.7B exhibits larger mismatch and a more volatile T ^ post \widehat{T}_{\mathrm{post}} than Qwen3-4B. (b) Comparison between inference-gap-aware Step 2 acceptance and a random rollback control. Random rollback rejects more updates, applying fewer effective policy changes, but still collapses.

这张图（图4a）展示了在FP8量化回滚设置下，两个不同规模的Qwen模型（Qwen3-4B和Qwen3-1.7B）在训练过程中出现的“训练-推理不匹配”现象及其导致的“推理差距”。

图的左侧子图标题为“Mismatch-K3”，横轴是“Training Step”（训练步数），从0到750。纵轴表示某种与K3相关的KL散度或不匹配度量，数值范围从0到0.020。图中有两条曲线：
*   橙色曲线代表“Qwen3-4B FP8”模型。
*   红色曲线代表“Qwen3-1.7B FP8”模型。
这两条曲线展示了随着训练步数的增加，模型在训练引擎上的输出与推理引擎上的输出之间的不匹配程度。我们可以看到，两条曲线都呈现出上升趋势，表明随着训练的进行，这种不匹配在增大。同时，红色曲线（Qwen3-1.7B）的整体不匹配度高于橙色曲线（Qwen3-4B），这说明规模较小的模型（Qwen3-1.7B）表现出更大的训练-推理不匹配。

图的右侧子图标题为“Inference Gap”，横轴同样是“Training Step”（训练步数），从0到750。纵轴表示“推理差距”（T^post或\widehat{T}_{\mathrm{post}}），数值范围从-0.0008到0.0008。这里同样有两条曲线：
*   橙色曲线代表“Qwen3-4B FP8”模型。
*   红色曲线代表“Qwen3-1.7B FP8”模型。
这条曲线展示了训练过程中，基于推理引擎的差距代理（inference-side gap proxy）的变化情况。我们可以观察到，红色曲线（Qwen3-1.7B）的波动性更大，且其平均值似乎更远离零点，这表明规模较小的模型（Qwen3-1.7B）不仅不匹配度更高，其推理差距也更加不稳定和显著。

这张图揭示了现有方法忽视的一个目标不对齐问题：训练引擎中策略的有效更新并不一定能保证推理引擎（部署时使用的）策略的改进。图中清晰地展示了，即使模型参数同步，由于训练和推理引擎的分离，它们对相同轨迹的概率评估仍然存在不一致，这种不一致会随着训练的进行而增大，并且在不同规模的模型上表现不同（小模型更严重）。这为论文提出的“单调推理策略改进”（MIPI）目标和“单调推理策略更新”（MIPU）框架提供了动机：需要关注推理侧的差距，以确保训练过程能够真正提升部署时的模型性能。

总结来说，这张图通过对比两个不同规模的模型在训练过程中的训练-推理不匹配度和推理差距，直观地展示了训练-推理不匹配问题的存在及其严重性，特别是对于规模较小的模型。这支持了论文的核心观点，即需要一种新的优化目标和方法来处理这种不匹配，以提高训练稳定性和推理性能。

---

![Figure 5: Step 1 implementation analysis under the Qwen3-4B FP8-quantized rollou](fig5_1.webp)

> Figure 5: Step 1 implementation analysis under the Qwen3-4B FP8-quantized rollout. Comparison of PPO-IS, Vanilla-IS, and TIS in terms of performance, gradient norm, inference-training K3-KL, and clip ratio.

这张图（图5）来自论文《The Mirage of Optimizing Training Policies: Monotonic Inference Policies as the Real Objective for LLM Reinforcement Learning》，展示了在Qwen3-4B FP8量化rollout环境下，对PPO-IS、Vanilla-IS和TIS这三种方法的**第一步实现分析**。它通过四个子图，从不同维度对比了这些方法的性能、梯度范数、推理-训练K3-KL散度以及clip比率，旨在揭示这些方法的具体运作方式及其效果。

我们来逐一解析每个子图：

1.  **第一个子图（左侧）：Reward (性能)**
    *   **横轴 (X-axis)**：`Training Step`（训练步数），表示训练过程中的迭代次数，范围从0到约800。
    *   **纵轴 (Y-axis)**：`pass@1`，这是一个性能指标，通常表示在一次尝试中成功解决问题的概率（例如，模型生成的答案被判断为正确的概率）。值越接近1.0表示性能越好。
    *   **曲线与图例**：
        *   蓝色曲线代表 `Baseline`（基线）。
        *   红色曲线代表 `PPO-IS`（Proximal Policy Optimization with Importance Sampling）。
        *   橙色曲线代表 `Vanilla-IS`（Vanilla Importance Sampling）。
        *   黄色曲线代表 `TIS`（论文中提出的方法，可能是Targeted Importance Sampling或类似概念）。
    *   **信息解读**：这个子图展示了随着训练步数的增加，不同方法的性能变化。可以看到，`TIS`（黄色）的性能最高且最稳定，接近1.0。`Vanilla-IS`（橙色）次之，而`PPO-IS`（红色）的性能较低且波动较大。`Baseline`（蓝色）在早期有波动，但最终性能介于`PPO-IS`和`Vanilla-IS`之间。这表明`TIS`在提升推理性能方面表现更优。

2.  **第二个子图（左二）：Mismatch-K3 (推理-训练不匹配)**
    *   **横轴 (X-axis)**：`Training Step`（训练步数），与第一个子图相同。
    *   **纵轴 (Y-axis)**：`Mismatch-K3`，这通常表示推理引擎和训练引擎在生成相同轨迹时概率分布的差异，这里用K3-KL散度来衡量。值越小表示不匹配程度越低。
    *   **曲线与图例**：与第一个子图相同。
    *   **信息解读**：这个子图展示了训练过程中推理-训练不匹配的程度。`TIS`（黄色）和`Vanilla-IS`（橙色）的不匹配程度较低且相对稳定。`PPO-IS`（红色）的不匹配程度在早期较高，随后有所下降但仍高于前两者。`Baseline`（蓝色）的不匹配程度在早期也较高。这表明`TIS`和`Vanilla-IS`能更好地减少训练与推理之间的不匹配。

3.  **第三个子图（右二）：Grad Norm (梯度范数)**
    *   **横轴 (X-axis)**：`Training Step`（训练步数），与第一个子图相同。
    *   **纵轴 (Y-axis)**：`Grad Norm`（梯度范数），通常表示策略更新梯度的大小，以对数尺度（10^-2 到 10^1）展示。梯度范数过大可能导致训练不稳定。
    *   **曲线与图例**：与第一个子图相同。
    *   **信息解读**：这个子图展示了训练过程中梯度范数的变化。`TIS`（黄色）和`Vanilla-IS`（橙色）的梯度范数相对较小且稳定。`PPO-IS`（红色）的梯度范数在某些步骤上非常大（峰值高），表明其训练过程可能更不稳定。`Baseline`（蓝色）的梯度范数也有较大波动。这表明`TIS`和`Vanilla-IS`的训练过程更稳定。

4.  **第四个子图（右侧）：Clip Ratio (裁剪比率)**
    *   **横轴 (X-axis)**：没有明确的刻度，但有四个柱状图，分别对应四种方法（从左到右：Baseline, PPO-IS, Vanilla-IS, TIS）。
    *   **纵轴 (Y-axis)**：`Clip Ratio`，这是PPO算法中的一个关键参数，表示策略更新时梯度被裁剪的比例。较高的clip ratio可能意味着策略更新幅度受到更多限制，以防止大的更新导致不稳定。
    *   **柱状图与图例**：每个柱状图的高度代表对应方法的平均clip ratio。
        *   `Baseline`（蓝色）：约1.80e-04。
        *   `PPO-IS`（黄色）：约2.10e-04。
        *   `Vanilla-IS`（橙色）：约2.00e-04。
        *   `TIS`（红色）：约7.18e-03（明显高于其他方法）。
    *   **信息解读**：这个子图显示了不同方法的平均clip ratio。`TIS`的clip ratio远高于其他三种方法，这可能意味着TIS在策略更新时允许更大的变化（或者说其更新更激进），但结合前几个子图来看，这种更大的clip ratio并没有导致性能下降或不匹配增加，反而可能有助于其获得更好的性能和稳定性。这也可能反映了TIS在处理推理-训练不匹配时的不同策略。

**方法运作揭示**：
这张图通过对比实验揭示了所提出的TIS方法如何运作：
*   **目标对齐**：TIS似乎更好地将对训练引擎的策略更新与推理引擎的实际需求对齐，从而减少了推理-训练不匹配（Mismatch-K3较低）。
*   **性能提升**：TIS在推理性能（Reward）上取得了显著提升，这表明其对训练引擎的优化确实带来了推理引擎性能的改善。
*   **训练稳定性**：TIS的梯度范数（Grad Norm）相对稳定，尽管其clip ratio较高，但并未导致训练不稳定，反而可能通过更有效的更新实现了更好的性能。
*   **与现有方法对比**：与PPO-IS和Vanilla-IS相比，TIS在性能、不匹配程度和训练稳定性方面都表现出优势。这支持了论文的核心观点：传统的优化训练策略的方法可能忽略了训练与推理之间的目标错位，而TIS通过关注推理策略的单调改进（Monotonic Inference Policy Improvement, MIPI）来解决这个问题。

**结论**：
从图中可以清楚地看到，在Qwen3-4B FP8量化rollout环境下，TIS方法在性能、推理-训练不匹配程度和训练稳定性方面均优于PPO-IS、Vanilla-IS和基线方法。这表明TIS能够更有效地处理LLM强化学习中的训练-推理不匹配问题，并实现更稳定和更优的推理性能。

---

![Figure 6: Sensitivity to the acceptance tolerance c c under the Qwen3-4B FP8-qua](fig6_1.webp)

> Figure 6: Sensitivity to the acceptance tolerance c c under the Qwen3-4B FP8-quantized rollout in terms of inference-training K3-KL, training score, and T ^ post \widehat{T}_{\mathrm{post}} .

这张图（图6）来自论文《The Mirage of Optimizing Training Policies: Monotonic Inference Policies as the Real Objective for LLM Reinforcement Learning》，它展示了在不同接受容忍度参数 `c` 下，Qwen3-4B模型在FP8量化rollout中的表现，具体从三个维度进行评估：推理-训练K3-KL散度（Mismatch-K3）、训练得分（Score）和后验推断差距（Inference Gap）。

### 图的组成部分和信息流动：

1. **三个子图**：
   - **左图（Mismatch-K3）**：横轴是训练步骤（Training Step），范围从0到800；纵轴是K3-KL散度的值，范围大约从0.003到0.015。这个图展示了不同`c`值下，推理和训练之间的K3-KL散度随训练步骤的变化。K3-KL散度衡量的是推理和训练引擎在生成轨迹上的概率分布差异，差异越小说明匹配度越高。
   - **中图（Score）**：横轴同样是训练步骤（0到800）；纵轴是得分（Score），范围从0.4到1.0。这个图展示了不同`c`值下，训练过程中得分随训练步骤的变化。得分可能代表了模型在训练任务上的性能表现，得分越高说明性能越好。
   - **右图（Inference Gap）**：横轴是训练步骤（0到800）；纵轴是后验推断差距（$\widehat{T}_{\mathrm{post}}$），范围大约从-0.00025到0.00050。这个图展示了不同`c`值下，后验推断差距随训练步骤的变化。后验推断差距可能衡量了推理和训练在后验概率上的差异，差距越小说明一致性越好。

2. **图例（Legend）**：
   - 不同的颜色代表不同的`c`值：
     - 蓝色（`c=0`）：基准情况，接受容忍度为0。
     - 红色（`c=0.0001`）：接受容忍度为正的小值。
     - 橙色（`c=-0.0001`）：接受容忍度为负的小值。
     - 黄色（`Ours`）：论文提出的方法（Monotonic Inference Policy Update, MIPU）对应的`c`设置。

### 方法的运作方式（从图中理解）：

论文指出，现有的强化学习（RL）训练在大型语言模型（LLM）中存在训练-推理不匹配的问题，即训练引擎和推理引擎对相同轨迹的概率估计不一致，这会导致训练不稳定。为了应对这个问题，论文提出了**单调推断策略改进（MIPI）**目标和**单调推断策略更新（MIPU）**框架。MIPU的核心是：
1. **采样参考的候选更新**：首先，从训练过程中采样一些候选策略更新。
2. **选择性接受同步候选**：然后，使用一个推断侧的差距代理（即图中的“Inference Gap”）来选择性地接受那些在推断侧表现良好的候选更新，以确保训练的更新能够真正改善推理时的策略。

从图中可以看到，不同的`c`值（接受容忍度）会影响这三个指标的变化：
- 对于**Mismatch-K3**（左图），黄色的“Ours”（MIPU方法）的K3-KL散度在训练过程中相对较低且稳定，说明MIPU方法能够有效减少训练和推理之间的不匹配。
- 对于**Score**（中图），黄色的“Ours”的得分在训练过程中上升得更快且最终更高，说明MIPU方法能够提升模型的训练性能。
- 对于**Inference Gap**（右图），黄色的“Ours”的后验推断差距在训练过程中相对较小且稳定，说明MIPU方法能够减少推断侧的差距，提高一致性。

### 结果分析（坐标、对比对象和结论）：

- **坐标**：
  - 横轴：训练步骤（0到800），表示训练的进度。
  - 纵轴：
    - 左图：K3-KL散度（0.003到0.015），衡量训练和推理的概率分布差异。
    - 中图：得分（0.4到1.0），衡量模型的训练性能。
    - 右图：后验推断差距（-0.00025到0.00050），衡量推断侧的差距。

- **对比对象**：
  - 不同的`c`值（`c=0`、`c=0.0001`、`c=-0.0001`和`Ours`）在三个指标上的表现对比。

- **结论**：
  - 论文提出的MIPU方法（黄色曲线）在三个指标上都表现更好：
    - 在Mismatch-K3（左图）中，K3-KL散度更低且更稳定，说明训练和推理的不匹配更小。
    - 在Score（中图）中，得分更高且上升更快，说明模型的训练性能更好。
    - 在Inference Gap（右图）中，后验推断差距更小且更稳定，说明推断侧的一致性更好。
  - 这表明MIPU方法能够有效解决训练-推理不匹配的问题，提高训练的稳定性和模型的推理性能。
