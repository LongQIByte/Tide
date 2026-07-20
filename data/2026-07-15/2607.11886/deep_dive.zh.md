# Read It Back: Pretrained MLLMs Are Zero-Shot Reward Models for Text-to-Image Generation

[arXiv](https://arxiv.org/abs/2607.11886) · [HuggingFace](https://huggingface.co/papers/2607.11886) · ▲82

## 摘要（原文）

> In this paper, we propose SpectraReward, a training-free reward function that turns pretrained MLLMs into off-the-shelf reward models for image-generation reinforcement learning. Instead of asking the MLLM to judge a generated image or answer decomposed verification questions, SpectraReward measures how well the original prompt can be recovered from the generated image through a single image-conditioned, teacher-forced forward pass. We use the average image-conditioned prompt log-likelihood as the reward, directly reusing the MLLM's pretrained image-text alignment ability without preference labels, reward-model fine-tuning. We further introduce Self-SpectraReward, a special case for unified multimodal models where the policy's own understanding branch serves as the reward model for its generation branch, forming a closed-loop self-improving framework without external reward models or external knowledge. Extensive experiments validate SpectraReward through a broad image-generation RL study covering two diffusion models, three RL algorithms, nine reward MLLM backbones from four MLLM families spanning 4B to 235B parameters, and five out-of-distribution text-to-image benchmarks. Results show that both SpectraReward and Self-SpectraReward significantly and consistently improve generation performance and outperform prior MLLM-derived reward training methods. Further analysis reveals that larger reward MLLMs are not always better, while Self-SpectraReward can match or surpass much larger external reward models, suggesting that reward-policy alignment is a key factor for effective image-generation RL. Project Page: https://huangrh99.github.io/SpectraReward/

## 摘要（中译）

在本文中，我们提出了SpectraReward，这是一种无需训练的奖励函数，它将预训练的多模态大模型（MLLMs）转化为即用型的奖励模型，用于图像生成强化学习。SpectraReward并非要求多模态大模型（MLLM）对生成的图像进行判断或回答分解后的验证问题，而是通过单次图像条件下的教师强制前向传播来衡量从生成图像中恢复原始提示的效果。我们使用平均图像条件提示对数似然作为奖励，直接复用多模态大模型（MLLM）预训练的图像 - 文本对齐能力，无需偏好标签和奖励模型微调。我们进一步引入了Self - SpectraReward，这是统一多模态模型的一种特殊情况，在这种情况下，策略自身的理解分支充当其生成分支的奖励模型，形成一个无需外部奖励模型或外部知识的闭环自我改进框架。大量实验通过广泛的图像生成强化学习研究验证了SpectraReward，该研究涵盖了两种扩散模型、三种强化学习算法、来自四个多模态大模型（MLLM）家族（参数范围从40亿到2350亿）的九个奖励多模态大模型（MLLM）主干以及五个分布外文本到图像基准测试。结果表明，SpectraReward和Self - SpectraReward都显著且一致地提高了生成性能，并且优于之前的多模态大模型（MLLM）派生奖励训练方法。进一步的分析表明，较大的奖励多模态大模型（MLLM）并不总是更好，而Self - SpectraReward可以匹配或超越大得多的外部奖励模型，这表明奖励 - 策略对齐是有效图像生成强化学习的一个关键因素。项目页面：https://huangrh99.github.io/SpectraReward/

## 背景剖析

**背景剖析**

近年来，图像生成技术取得了飞速发展，从专门化的文本到图像模型演进到集成视觉理解和生成的统一多模态模型（UMMs）。强化学习作为有效的后训练阶段，能够持续提升生成结果的组合保真度和指令遵循能力。然而，强化学习流程的成功依赖于两个关键支柱：优化算法和奖励模型。其中，奖励模型决定了训练策略最终能达到的上限，但设计一个既高效又可靠的奖励模型仍然具有挑战性。

先前方法主要分为两类：一类依赖大规模人类偏好标注来对齐视觉-文本表示，但这种方法需要昂贵的数据收集和迭代；另一类尝试复用预训练的多模态大模型（MLLMs）作为零样本奖励来源，虽然无需训练，但对奖励校准和评分噪声敏感，或引入复杂的工程流程。这导致现有方法无法同时满足"无偏好标签"、"训练自由"和"即插即用"的需求。

本文提出SpectraReward，通过重用预训练MLLM的图像-文本对齐能力，将其转化为无需额外训练的图像生成奖励模型。核心思路是测量生成的图像能在多大程度上"读回"原始提示——通过冻结MLLM对图像进行条件化，并计算提示token的平均对数似然作为奖励信号。进一步针对统一多模态模型提出Self-SpectraReward，利用模型自身的理解分支为生成分支提供奖励，形成无需外部依赖的闭环自改进框架。

与前人工作的关键差异在于：1）不同于直接让MLLM判断图像质量或回答分解问题，SpectraReward通过单一前向传播计算提示恢复度；2）Self-SpectraReward利用模型内部的统一架构实现奖励-策略对齐，而此前方法依赖外部模型；3）实验表明奖励模型的分布对齐比单纯扩大规模更重要，这与传统认知不同。这种方法在保持效率的同时，显著提升了生成性能。

## 方法图解

![Figure 1 : Overview of SpectraReward. (a) Pretrained MLLMs naturally induce a se](fig1_1.webp)

> Figure 1 : Overview of SpectraReward. (a) Pretrained MLLMs naturally induce a semantic spectrum that measures how well a generated image aligns with the prompt. SpectraReward aggregates this into a reward for T2I RL. (b) During RL training, SpectraReward steadily increases together with visible improvements in complex scene generation. (c) We study nine reward MLLM backbones from four MLLM families, with external reward MLLMs spanning three families and 4B to 235B parameters. Scaling the reward MLLM backbones brings non-monotonic gains. Qwen3-VL-30B-A3B achieves the best performance among external MLLMs, while Self-SpectraReward, using BAGEL’s own understanding branch as the reward model, outperforms all external MLLMs. (d) Both SpectraReward and Self-SpectraReward bring significant and consistent improvements across all six downstream benchmarks compared to the baselines.

这张图是论文《Read It Back: Pretrained MLLMs Are Zero - Shot Reward Models for Text - to - Image Generation》的核心示意图，分为四个部分（a - d），我们逐个解析：

### 部分(a)：SpectraReward的语义谱来源
- **流程与组件**：首先，T2I（文本到图像）模型接收一个提示（Prompt）\( x \)，这里示例提示是“Two kittens sit in a blue box”，然后生成图像\( y \)（图中是两只小猫在蓝色盒子里的图像）。接着，预训练的多模态大模型（Pretrained MLLM）处理这个生成的图像\( y \)，并输出一个“语义谱（Semantic Spectrum）”。语义谱以不同颜色和数值表示提示中各个语义元素（如“kitten”“cats”“sit”“in”“blue”“box”）的某种对齐分数（例如，这里“kitten”的分数是0.1469，“box”的分数是0.8237等）。最后，通过公式\( \text{SpectraReward} = \frac{1}{T}\sum_{t = 1}^{T - 1}\log P_M(x_{t + 1}|x_{\leq t}, y) \)（这里不需要纠结公式推导，理解是用图像条件下的提示对数似然来计算奖励）将语义谱聚合为T2I强化学习（RL）的奖励。数据/信息的流动顺序是：提示\( x \)→T2I模型生成图像\( y \)→预训练MLLM处理\( y \)得到语义谱→计算SpectraReward作为奖励。

### 部分(b)：训练动态
- **流程与组件**：提示是“A wireless mouse on the bottom of the table is smaller than a crimson scarf basking in sunlight on the top.”（桌子上底部的无线鼠标比顶部阳光下晒着的深红色围巾小）。然后展示了三个训练阶段（Early、Mid、Late）的图像：①Early阶段的图像中，鼠标和围巾的位置关系可能不够准确；②Mid阶段有所改善；③Late阶段更符合提示描述。下方的表格记录了每个阶段对提示中关键元素（“Wireless mouse”“Bottom of table”）的满足情况（X表示不满足，△表示部分满足，√表示满足）。同时，下方的“Train Reward”曲线显示了训练过程中奖励的变化，随着训练步骤（Step）增加，奖励从约 - 3.5逐渐上升到接近0，说明随着训练进行，生成的图像越来越符合提示，奖励模型（SpectraReward）的反馈使得训练朝着正确的方向进行。这部分展示了在RL训练过程中，SpectraReward如何随着训练步骤增加而稳定上升，并且生成的复杂场景（如鼠标和围巾的位置关系）也得到了明显改善。

### 部分(c)：奖励MLLM比较
- **图表类型与内容**：这是一个折线图（或散点图结合折线），横轴可能是不同的奖励MLLM模型（或模型大小、家族等），纵轴是某种性能指标（如奖励分数或任务表现）。图中展示了九个来自四个MLLM家族的奖励MLLM backbone（包括外部奖励MLLM和Self - SpectraReward），其中外部奖励MLLM跨越三个家族，参数从4B到235B不等。从图中可以看到，奖励MLLM的性能提升是非单调的（即不是模型越大性能越好）。例如，Qwen3 - VL - 30B - A3B在外部MLLM中表现最好，而Self - SpectraReward（使用BAGEL自身的理解分支作为奖励模型）的性能超过了所有外部MLLM。这里的对比对象是不同的奖励MLLM（包括外部和Self - SpectraReward），结论是奖励MLLM的性能提升不是随模型大小单调增加的，Self - SpectraReward优于所有外部MLLM。

### 部分(d)：定量比较
- **图表类型与内容**：这是一个雷达图（或蜘蛛图），用于比较SpectraReward和Self - SpectraReward与基线（Baselines）在六个下游基准测试（如WISE、TID2013 Bench Short、TID2013 Bench Long、GenEval2、DPGenBench、GenEval1）上的表现。每个轴代表一个基准测试，轴上的点越靠外表示性能越好。从图中可以看到，SpectraReward和Self - SpectraReward在所有六个下游基准测试中的表现都比基线更靠外，说明它们带来了显著且一致的性能提升。对比对象是SpectraReward、Self - SpectraReward和各种基线，结论是两种方法在所有下游基准测试中都显著且一致地优于基线。

总结这张图的方法运作方式：SpectraReward利用预训练MLLM的图像 - 文本对齐能力，通过计算图像条件下提示的对数似然来生成奖励，用于T2I RL。在训练过程中，这个奖励随着训练步骤增加而上升，使得生成的图像越来越符合提示。通过比较不同的奖励MLLM（包括外部和Self - SpectraReward），发现Self - SpectraReward性能更优，且在多个下游基准测试中都有显著提升。

---

![Figure 2 : Comparison of MLLM-based reward functions. (a) Scalar scoring directl](fig2_1.webp)

> Figure 2 : Comparison of MLLM-based reward functions. (a) Scalar scoring directly asks an MLLM to assign a discrete image-text alignment score, making the reward sensitive to judge calibration and scoring noise. (b) VQA decomposition converts the prompt into atomic questions and aggregates verifier confidence, but introduces a two-stage pipeline and depends on the quality of question decomposition. (c) SpectraReward computes the image-conditioned prompt likelihood through a single teacher-forced forward pass. The resulting token-level likelihoods form a semantic spectrum, whose average is used as the scalar reward. (d) Self-SpectraReward instantiates the same prompt-likelihood reward within a unified multimodal model by using the policy’s own understanding branch, removing the need for an external reward MLLM and improving reward-policy alignment.

这张图（图2）对比了基于多模态大模型（MLLM）的奖励函数，从左到右分为四个子图（a到d），分别介绍不同的方法及其特点：

### 子图(a)：Scalar Scoring（标量评分）
- **组件与流程**：底部有文本（文档图标）和图像（图片图标）作为输入，箭头指向“MLLM”模块，MLLM的输出是“Discrete scalar score”（离散标量分数）。  
- **方法逻辑**：直接让MLLM给图像-文本对齐打一个离散的分数。  
- **缺点**：下方标注了两个红色叉号，说明这种方法的问题：① 奖励对“judge calibration（评分校准）”敏感（即不同评委的评分标准可能不一致）；② 受“scoring noise（评分噪声）”影响（即评分本身可能有随机或不稳定的误差）。  


### 子图(b)：VQA Decomposition（VQA分解）
- **组件与流程**：底部同样有文本和图像输入，先箭头指向“Decomposer”（分解器），分解器的输出“Questions”（问题）箭头指向“Verifier”（验证器）；同时，图像也直接箭头指向“Verifier”。Verifier的输出是“Confidence Scoring”（置信度评分）。  
- **方法逻辑**：将原始prompt（文本）分解为原子问题，然后通过验证器对这些问题的回答（结合图像）进行置信度评分，再聚合这些置信度作为最终奖励。  
- **特点**：下方标注了绿色对勾和灰色圆圈：① 绿色对勾表示奖励是“Continuous（连续的）”；② 灰色圆圈表示是“Two-stage pipeline（两阶段流水线）”（先分解问题，再验证），且存在“Decomposition bottleneck（分解瓶颈）”（即问题分解的质量可能限制整体效果）。  


### 子图(c)：SpectraReward（光谱奖励）
- **组件与流程**：底部有图像和文本输入，箭头指向“MLLM”模块（虚线箭头可能表示图像作为条件输入，文本是目标？或者文本是prompt，图像是生成的图，MLLM计算prompt在图像条件下的似然）。MLLM的输出相关的是“Avg. Prompt Likelihood”（平均prompt似然），箭头从MLLM指向这个输出（或反向？结合文字说明，应该是MLLM计算图像条件下prompt的似然，然后取平均作为奖励）。  
- **方法逻辑**：通过**单次teacher-forced前向传播**（即给定图像，强制MLLM生成或计算prompt的似然），得到token级的似然，这些似然形成一个“语义光谱”，其平均值作为标量奖励。  
- **优点**：下方绿色对勾标注：① “Dense likelihood signal（密集的似然信号）”（即利用MLLM预训练的图像-文本对齐能力，无需偏好标签或奖励模型微调）；② “One forward pass（一次前向传播）”（效率高）；③ “Training-free（无训练需求）”；④ “Support diverse MLLMs（支持多样的MLLM）”。  


### 子图(d)：Self-SpectraReward（自光谱奖励）
- **组件与流程**：底部有文本和图像输入，箭头指向“UMM”（Unified Multimodal Model，统一多模态模型）模块。UMM的输出相关的是“Avg. Prompt Likelihood”，同时有一个虚线箭头从图像指向文本相关的部分（可能表示策略的“理解分支”同时处理图像和文本，作为“生成分支”的奖励模型）。  
- **方法逻辑**：在**统一多模态模型**中实例化同样的“prompt-likelihood奖励”，但使用策略（生成模型）自身的“理解分支”作为奖励模型，形成闭环自改进框架。  
- **优点**：下方绿色对勾标注：① “Reward-policy alignment（奖励-策略对齐）”（因为奖励模型是策略自身的一部分，所以对齐更好）；② “No external reward models or external knowledge（无需外部奖励模型或外部知识）”。  


### 整体逻辑与结论
这张图通过对比四种方法（标量评分、VQA分解、SpectraReward、Self-SpectraReward），展示了SpectraReward和Self-SpectraReward的优势：  
- 标量评分（a）依赖MLLM的离散评分，不稳定；  
- VQA分解（b）是两阶段流程，受分解质量限制；  
- SpectraReward（c）利用MLLM的预训练能力，单次前向传播计算似然平均，高效且无需训练；  
- Self-SpectraReward（d）进一步将奖励模型集成到策略自身的理解分支，实现闭环自改进，对齐更好且无需外部模型。  

实验（论文中）验证了这两种方法在多种扩散模型、RL算法、MLLM骨干和基准测试上的有效性，显著提升生成性能。

---

![Figure 3 : Token-level semantic sensitivity of SpectraReward. Positive and negat](fig3_1.webp)

> Figure 3 : Token-level semantic sensitivity of SpectraReward. Positive and negative images are evaluated using the same positive prompt. For attribute mismatch, instantiated as a counting error, the negative image mainly lowers the likelihood of “Two”; for object identity mismatch, replacing the guitar with a chair sharply lowers the likelihood of “guitar”. Bars show image-conditioned prompt-token log-likelihoods with error bars calculated over four pairs, and dashed lines show the resulting sequence-level reward value, i.e., SpectraReward.

这张图（图3）展示了SpectraReward的**标记级语义敏感性**，核心是解释“为什么SpectraReward能有效衡量图像与文本提示的匹配度”。我们分两部分（属性不匹配、对象身份不匹配）来拆解：  


### 1. 整体逻辑：“文本提示→图像→标记级对数似然→序列级奖励”的流程  
SpectraReward的核心是**用预训练多模态大模型（MLLM）的“图像条件下的文本提示对数似然”作为奖励**——即给定生成的图像，模型预测“原始文本提示中每个标记（token）”的概率，通过对数似然衡量匹配度。图中通过“正例图像（符合提示）”和“负例图像（不符合提示）”的对数似然对比，展示模型如何感知语义差异。  


### 2. 子图(a)：属性不匹配（计数错误）  
- **左侧图像**：  
  - 正例图像（绿色框）：“两只猫坐在沙发上”（Two cats sitting on a sofa），图像内容与提示完全匹配。  
  - 负例图像（红色框）：“五只猫坐在沙发上”（Five cats sitting on a sofa），仅**计数属性**不匹配（猫的数量从2变5）。  

- **右侧图表（标记级对数似然）**：  
  - X轴：文本提示的每个标记（token），依次是“Two”“cats”“sitting”“on”“a”“sofa”。  
  - Y轴：对数似然（log-likelihood），值越高表示模型认为该标记在图像条件下出现的概率越高。  
  - 颜色：绿色（pos）代表正例图像的对数似然，红色（neg）代表负例图像的对数似然。  
  - 关键观察：**负例图像显著降低了“Two”的对数似然**（正例≈-5.66，负例≈-7.44），而其他标记（如“cats”“sitting”等）的对数似然变化很小。这说明SpectraReward能精准捕捉“计数属性”的不匹配——当图像的计数与提示不符时，对应计数的标记（如“Two”）的对数似然会大幅下降。  
  - 虚线与奖励：虚线表示**序列级奖励（SpectraReward）**，计算方式是“正例对数似然的平均值”减去“负例对数似然的平均值”？或直接用正例的平均？图中给出\( r_{\text{pos}} = -1.932 \)、\( r_{\text{neg}} = -2.298 \)，可能是序列级的平均对数似然，负例的奖励更低，因此能区分“正例更匹配提示”。  


### 3. 子图(b)：对象身份不匹配  
- **左侧图像**：  
  - 正例图像（绿色框）：“一把木吉他靠在墙上”（A wooden guitar leaning against the wall），图像内容与提示完全匹配。  
  - 负例图像（红色框）：“一把木椅子靠在墙上”（A wooden chair leaning against the wall），**对象身份**不匹配（吉他被替换为椅子）。  

- **右侧图表（标记级对数似然）**：  
  - X轴：文本提示的每个标记，依次是“A”“wooden”“guitar”“leaning”“against”“the”“wall”。  
  - Y轴：对数似然。  
  - 颜色：绿色（pos）为正例，红色（neg）为负例。  
  - 关键观察：**负例图像显著降低了“guitar”的对数似然**（正例≈-9.61？不，图中绿色“guitar”的对数似然是-1.19？哦，图中绿色“guitar”的对数似然是-1.19？不对，看数值：正例“guitar”的对数似然是-1.19？不，图中绿色“guitar”的柱形上方标了-1.19？红色“guitar”的柱形下方标了-9.61？哦，对：正例（绿色）的“guitar”对数似然是-1.19，负例（红色）的“guitar”对数似然是-9.61，差距极大。而其他标记（如“A”“wooden”“leaning”等）的对数似然变化较小。这说明SpectraReward能精准捕捉“对象身份”的不匹配——当图像的对象与提示不符时，对应对象的标记（如“guitar”）的对数似然会大幅下降。  
  - 虚线与奖励：虚线表示序列级奖励，图中给出\( r_{\text{pos}} = -2.822 \)、\( r_{\text{neg}} = -3.891 \)，负例的奖励更低，因此能区分“正例更匹配提示”。  


### 4. 方法运作的直观解释（读者如何理解SpectraReward？）  
SpectraReward的核心逻辑是：**预训练MLLM已经具备“图像-文本”的对齐能力**——给定一张图像，模型能预测“文本提示中每个标记”的概率（对数似然越高，概率越高）。当图像与文本提示匹配时，所有标记的对数似然都较高；当图像与提示不匹配（如计数错误、对象替换），**对应语义错误的标记的对数似然会显著下降**。通过比较“正例图像”和“负例图像”的标记级对数似然，SpectraReward可以用“序列级奖励”（如正例平均对数似然 - 负例平均对数似然，或直接用正例的平均）来衡量图像与提示的匹配度。  

例如，在“属性不匹配”中，计数错误导致“Two”的对数似然骤降；在“对象身份不匹配”中，对象替换导致“guitar”的对数似然骤降。这种“标记级的敏感度”让SpectraReward能精准识别语义差异，而无需额外的偏好标签或奖励模型微调——直接复用MLLM的预训练对齐能力。  


### 5. 结果的结论（从图中可得出什么？）  
- 标记级敏感度：SpectraReward对**语义相关的标记**（如计数词、对象名）高度敏感——当图像的语义（计数、对象身份）与提示不符时，对应标记的对数似然会显著下降，而其他标记变化不大。  
- 奖励的有效性：序列级奖励（虚线）能区分正例和负例（负例奖励更低），说明SpectraReward能有效衡量图像与提示的匹配度。  
- 方法的合理性：通过“图像条件下的文本提示对数似然”来衡量匹配度，直接复用了MLLM的预训练能力，无需额外训练，逻辑简洁且有效。  


总结：这张图通过“属性不匹配”和“对象身份不匹配”两个案例，直观展示了SpectraReward的核心逻辑——**利用MLLM的图像-文本对齐能力，通过标记级对数似然的变化来衡量图像与文本提示的匹配度**。图中清晰的对比（正例vs负例的标记级对数似然）和奖励计算（虚线），让读者能快速理解SpectraReward如何运作，以及为什么它能成为有效的零样本奖励模型。

---

![Figure 4 : The visual interpretation of SpectraReward. The reward ranking is con](fig4_1.webp)

> Figure 4 : The visual interpretation of SpectraReward. The reward ranking is consistent with the visual quality ranking.

这张图（图4）直观展示了SpectraReward方法的核心逻辑：**通过测量“从生成图像中恢复原始文本提示的能力”来给图像打分（奖励），且奖励排名与视觉质量排名一致**。下面分部分拆解：

### 1. 整体结构与组件含义
- **左侧“Prompt”列**：是文本提示（生成的依据），每个提示对应一行图像，展示不同方法/模型生成的图像。
- **上方“Lower reward → Higher reward”箭头**：表示奖励从低到高的方向（红色到绿色）。奖励数值（如-3.490、-2.887等）越“大”（越接近0或正数），奖励越高，图像质量/与提示的匹配度越好。
- **每行的图像列**：同一行的图像对应同一个文本提示，从左到右奖励逐渐升高（数值从更负变没那么负，或更接近0）。


### 2. 方法的核心逻辑（如何运作）
SpectraReward的核心是**“从图像恢复提示的能力”**：预训练的多模态大模型（MLLM）通过“图像条件下的前向传播”，计算“能多好地从图像中恢复出原始提示”的概率（即图像条件下的提示对数似然的平均值），这个概率作为**奖励**。  

具体到图中：  
- 对于每个文本提示（如第一行：“矩形吧台在三角形茂密圣诞树的右边”），生成多个图像（同一行的四个图像）。  
- MLLM尝试从每个图像中“读回”原始提示，计算恢复的置信度（对数似然）。奖励越高，说明MLLM认为该图像越能准确反映原始提示（即图像与提示的匹配度越好，视觉质量也更高）。  


### 3. 结果与结论（从图中观察）
- **奖励与视觉质量的关联**：从左到右（奖励从低到高），图像的质量/与提示的匹配度提升。例如：  
  - 第一行（圣诞树+吧台）：最左的图像（奖励-3.490）中吧台和树的布局可能不够清晰；最右的图像（奖励-2.887）中吧台、树的位置更符合提示，视觉上更合理。  
  - 第二行（鸢尾花+铜管乐器+布丁碗）：最左的图像（奖励-4.530）中元素（如布丁碗、铜管乐器）的呈现可能偏离提示；最右的图像（奖励-4.089）中元素更符合“azure iris（蓝色鸢尾花）、crimson tuba（深红色铜管）、mustard trifle bowl（芥末色布丁碗）”的描述。  
  - 第三行（乐高海盗）：最左的图像（奖励-3.991）中海盗的姿态、背景可能不够准确；最右的图像（奖励-3.903）中海盗的服装、背景元素（如蓝色乐高人偶）更符合提示。  

- **结论**：奖励排名（从低到高）与视觉质量排名（从差到好）一致。这说明SpectraReward的方法有效——通过“恢复提示的能力”来衡量图像质量是合理的，因为奖励高的图像确实更符合文本提示（视觉上更准确、质量更高）。  


简单来说，这张图用具体的例子展示了：**当MLLM从图像中“读回”提示的能力越强（奖励越高），图像就越符合文本提示，视觉质量也越好**。这验证了SpectraReward作为零样本奖励模型的有效性，即无需额外的偏好标签或奖励模型微调，仅利用MLLM的预训练图像-文本对齐能力，就能判断图像生成的质量。

---

![Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long pr](fig5_1.webp)

> Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long prompts, respectively. For WISE, the second score denotes evaluation with CoT. AlphaGRPO is trained on the reasoning text-to-image generation task. Bold indicates the best performance. The results of BAGEL are reproduced. Table 2 : Effect of different reward MLLM backbones. Unless otherwise specified, reward MLLMs all use Instruct models. Bold indicates the best performance. The second best is underlined . Table 3 : Comparison of different RL algorithms and reward models. When trained with Self-SpectraReward, AWM achieves the best downstream performance. Self-SpectraReward further outperforms prior reward models under comparable RL training. Bold indicates the best performance. Table 4 : Ablation of Reward function. Scalar Scoring asks the MLLM to rate the image from 1 to 5. VQA-Score asks “Does this figure show {caption} ?” and uses P ​ ( yes ) P(\text{yes}) as the reward. Table 5 : Ablation of Reward granularity. Token-level reward does not consistently outperform sequence-level reward, so we use sequence-level reward by default. Figure 5 : Qualitative comparison. Table 6 : The effect of including the EOS token in the reward calculation. Table 7 : Effect of VAE features in Self-SpectraReward reward computation. BAGEL provides two visual inputs to its understanding branch, ViT features from the semantic encoder and VAE features from the generation encoder. Using both inputs improves GenEval and TIIF-Short. Table 8 : Evaluation of text-to-image generation ability on GenEval benchmark. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. † \dagger refers to the methods using the LLM rewriter. Our model’s results and BAGEL all use the LLM rewriter. Table 9 : Performance of proprietary models and state-of-the-art open-source models on TIIF-Bench testmini subset. Evaluated systems are grouped into (i) diffusion-based open-source models, (ii)autoregressive open-source models, and (iii) proprietary models. The results of SpectraReward and BAGEL are evaluated by GPT-4.1. “Inf. SRR” indicates executing the inference-time self-reflective refinement. Table 10: Evaluation of text-to-image generation ability on the DPG-Bench [ dpg ] benchmark. * indicates our reproduced results. Table 11 : Comparison of world knowledge reasoning on WISE. WISE examines the complex semantic understanding and world knowledge for T2I generation. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. Figure 6 : Additional reward-ranking examples. For each prompt, samples are ordered from lower to higher SpectraReward reward. Figure 7 : Additional qualitative comparison. Red text highlights the prompt constraints that are especially sensitive to spatial relation, counting, attribute binding, or long-prompt composition. Self-SpectraReward more consistently satisfies these highlighted constraints than the BAGEL baseline.

这张图属于论文《Read It Back: Pretrained MLLMs Are Zero - Shot Reward Models for Text - to - Image Generation》中的**Figure 7：Additional qualitative comparison**（额外的定性比较），用于直观展示不同方法（BAGEL和Self - SpectraReward）在文本到图像生成任务中对prompt约束的满足情况，核心是对比两种方法生成的图像与原始prompt的匹配度，尤其是对prompt中敏感约束（如空间关系、计数、属性绑定、长prompt组合等）的满足程度。

### 图的组件与信息流动
- **列的含义**：
    - 第一列（Prompt）：展示文本到图像生成的**文本提示（prompt）**，其中**红色文字**标注了prompt中“特别敏感的约束”，比如空间关系（如“A cat is positioned to the right of a table”中的“to the right of a table”）、属性绑定（如“a metallic pyramid - shaped paperweight”中的“metallic”“pyramid - shaped”）、长prompt的组合语义（如关于玫瑰和纸镇的长描述）等。这些红色标注的约束是评估生成图像是否满足关键要求的核心点。
    - 第二列（BAGEL）：展示使用**BAGEL方法**（基线方法）根据对应prompt生成的图像。
    - 第三列（Self - SpectraReward）：展示使用**Self - SpectraReward方法**（本文提出的方法）根据对应prompt生成的图像。
- **行的含义**：图中有四行，每行对应一个不同的prompt，分别从不同角度（如物体属性、空间关系、场景元素、特定领域知识）测试两种方法的生成效果：
    - 第一行（玫瑰相关prompt）：prompt描述了“金属质感的玫瑰，花瓣仍带着盛开的期待……比完全绽放的织物玫瑰更鲜艳，但在完全实现的荣耀中更低沉，但仍鲜艳且编织美丽”，红色标注了“a metallic rose”“a full bloom”“the open flourish of a fabric rose”等敏感约束。通过对比BAGEL和Self - SpectraReward生成的玫瑰图像，观察是否满足“金属质感”“盛开状态”“与织物玫瑰的对比”等约束。
    - 第二行（猫的位置prompt）：prompt要求“一只猫在桌子的右边”，红色标注了“to the right of a table”（空间关系约束）。对比两种方法生成的猫的位置是否符合“在桌子右边”的要求。
    - 第三行（纸镇相关prompt）：prompt描述了“在温暖的金色阳光拥抱中，一个金属金字塔形纸镇，其反射表面投射出耀眼的光芒，闪耀在矮小的绿色灌木旁……”，红色标注了“a metallic pyramid - shaped paperweight”“beside a short, verdant shrub”等约束。对比生成的纸镇的材质、形状以及与灌木的位置关系是否符合prompt。
    - 第四行（工人服装prompt）：prompt要求“早期工业革命工厂中工人穿的典型服装”，红色标注了“garment worn by laborers in the early industrial revolution factories”（特定领域知识和属性约束）。对比生成的服装是否符合“早期工业革命工厂工人服装”的特征。

### 方法的运作方式（从图中理解）
- **BAGEL（基线）**：作为对比方法，它生成的图像在满足prompt的敏感约束上可能存在不足。例如，在“猫的位置”prompt中，BAGEL生成的猫可能在桌子的位置不符合“右边”的要求；在“玫瑰”prompt中，可能没有很好地体现出“金属质感”或“与织物玫瑰的对比”等约束。
- **Self - SpectraReward（本文方法）**：通过“测量从生成图像中恢复原始prompt的能力（利用预训练多模态大模型的图像 - 文本对齐能力，无需偏好标签或奖励模型微调）”来指导图像生成。从图中可以看到，Self - SpectraReward生成的图像更一致地满足prompt的敏感约束：
    - 在“猫的位置”prompt中，Self - SpectraReward生成的猫更准确地在桌子的右边；
    - 在“玫瑰”prompt中，可能更好地体现了“金属质感”和“与织物玫瑰的对比”；
    - 在“纸镇”prompt中，纸镇的材质、形状和与灌木的位置关系更符合prompt；
    - 在“工人服装”prompt中，生成的服装更符合“早期工业革命工厂工人服装”的特征。

### 结论（从图中得出）
这张定性比较图清晰地展示了**Self - SpectraReward比BAGEL更一致地满足prompt中的敏感约束**（如空间关系、属性绑定、特定领域知识等）。通过对比同一prompt下两种方法生成的图像，读者可以直观地看到Self - SpectraReward在文本到图像生成中对prompt要求的满足程度更高，验证了该方法在利用预训练多模态大模型的图像 - 文本对齐能力进行奖励建模时的有效性，即能够更好地引导生成图像与原始prompt的语义约束对齐。

---

![Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long pr](fig5_2.webp)

> Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long prompts, respectively. For WISE, the second score denotes evaluation with CoT. AlphaGRPO is trained on the reasoning text-to-image generation task. Bold indicates the best performance. The results of BAGEL are reproduced. Table 2 : Effect of different reward MLLM backbones. Unless otherwise specified, reward MLLMs all use Instruct models. Bold indicates the best performance. The second best is underlined . Table 3 : Comparison of different RL algorithms and reward models. When trained with Self-SpectraReward, AWM achieves the best downstream performance. Self-SpectraReward further outperforms prior reward models under comparable RL training. Bold indicates the best performance. Table 4 : Ablation of Reward function. Scalar Scoring asks the MLLM to rate the image from 1 to 5. VQA-Score asks “Does this figure show {caption} ?” and uses P ​ ( yes ) P(\text{yes}) as the reward. Table 5 : Ablation of Reward granularity. Token-level reward does not consistently outperform sequence-level reward, so we use sequence-level reward by default. Figure 5 : Qualitative comparison. Table 6 : The effect of including the EOS token in the reward calculation. Table 7 : Effect of VAE features in Self-SpectraReward reward computation. BAGEL provides two visual inputs to its understanding branch, ViT features from the semantic encoder and VAE features from the generation encoder. Using both inputs improves GenEval and TIIF-Short. Table 8 : Evaluation of text-to-image generation ability on GenEval benchmark. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. † \dagger refers to the methods using the LLM rewriter. Our model’s results and BAGEL all use the LLM rewriter. Table 9 : Performance of proprietary models and state-of-the-art open-source models on TIIF-Bench testmini subset. Evaluated systems are grouped into (i) diffusion-based open-source models, (ii)autoregressive open-source models, and (iii) proprietary models. The results of SpectraReward and BAGEL are evaluated by GPT-4.1. “Inf. SRR” indicates executing the inference-time self-reflective refinement. Table 10: Evaluation of text-to-image generation ability on the DPG-Bench [ dpg ] benchmark. * indicates our reproduced results. Table 11 : Comparison of world knowledge reasoning on WISE. WISE examines the complex semantic understanding and world knowledge for T2I generation. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. Figure 6 : Additional reward-ranking examples. For each prompt, samples are ordered from lower to higher SpectraReward reward. Figure 7 : Additional qualitative comparison. Red text highlights the prompt constraints that are especially sensitive to spatial relation, counting, attribute binding, or long-prompt composition. Self-SpectraReward more consistently satisfies these highlighted constraints than the BAGEL baseline.

这张图（图6）属于论文《Read It Back: Pretrained MLLMs Are Zero - Shot Reward Models for Text - to - Image Generation》中的“额外奖励排序示例”（Additional reward - ranking examples），用于直观展示所提出的SpectraReward方法如何对文本到图像生成的结果进行奖励排序。

### 组件与信息流动
- **Prompt（提示词）**：图的左侧列出了四个不同的文本提示词，每个提示词描述了希望生成的图像内容，例如第一个提示是“A spherical clock is in front of a conical clock, partially hiding it. A cubic clock is to the side and fully visible.”（一个球形时钟在圆锥形时钟前面，部分遮挡它。一个立方体时钟在旁边且完全可见），这些提示词是图像生成的目标描述。
- **图像样本**：对于每个提示词，右侧展示了四个图像样本，这些图像是根据该提示词生成的。
- **奖励值（Reward Value）**：每个图像的上方有一个数值，代表该图像根据SpectraReward方法得到的奖励值。奖励值的范围从左到右（或从红色框到绿色框）是从低到高排列的，图中顶部的箭头从“Lower reward”（低奖励）指向“Higher reward”（高奖励），明确了奖励值的递增方向。
- **颜色框**：图像被不同颜色的框（红色、橙色、绿色等）包围，颜色从红色到绿色逐渐变化，对应奖励值从低到高，帮助视觉上区分奖励的高低。

### 方法运作方式
SpectraReward方法的核心是将预训练的多模态大模型（MLLM）作为零样本奖励模型，用于图像生成强化学习。其具体运作方式是：通过测量从生成的图像中恢复原始提示词的程度来评估图像的质量，这里使用的是平均图像条件提示词对数似然作为奖励。在这张图中，对于每个提示词，生成的图像根据它们能够多好地满足提示词的描述（即能够多好地从图像中恢复出原始提示词的信息）被赋予不同的奖励值。奖励值低的图像（红色框）在满足提示词的要求（如物体的形状、位置、数量、属性绑定等）方面表现较差，而奖励值高的图像（绿色框）在这些方面表现更好。例如，对于第一个提示词，最左边的图像（红色框，奖励值-3.490）可能在时钟的形状、位置关系等方面没有很好地符合提示词，而最右边的图像（绿色框，奖励值-2.994）则更接近提示词的描述，因此获得更高的奖励。

### 结果与结论
从图中可以看出，对于每个提示词，图像的奖励值从左到右逐渐增加，这意味着图像在满足提示词要求方面的表现逐渐变好。例如：
- 对于“三个兔子、两顶草帽和四棵松树”的提示，最左边的图像（奖励值-3.362）中兔子和草帽、松树的组合可能不符合提示词的数量或位置要求，而最右边的图像（奖励值-2.664）则更符合，奖励值更高。
- 对于“一个圆柱形笼子是红色的……”的提示，最左边的图像（奖励值-3.314）可能在物体的颜色、形状或位置关系上不符合要求，而最右边的图像（奖励值-2.815）则更符合，奖励值更高。

这表明SpectraReward方法能够有效地对图像生成结果进行排序，奖励值高的图像更符合原始提示词的要求，从而验证了该方法能够将预训练的MLLM作为有效的零样本奖励模型来评估图像生成的质量，帮助图像生成强化学习模型学习生成更符合提示词的图像。

---

![Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long pr](fig5_3.webp)

> Table 1 : Results on Text-to-Image benchmarks . S and L denote Short and Long prompts, respectively. For WISE, the second score denotes evaluation with CoT. AlphaGRPO is trained on the reasoning text-to-image generation task. Bold indicates the best performance. The results of BAGEL are reproduced. Table 2 : Effect of different reward MLLM backbones. Unless otherwise specified, reward MLLMs all use Instruct models. Bold indicates the best performance. The second best is underlined . Table 3 : Comparison of different RL algorithms and reward models. When trained with Self-SpectraReward, AWM achieves the best downstream performance. Self-SpectraReward further outperforms prior reward models under comparable RL training. Bold indicates the best performance. Table 4 : Ablation of Reward function. Scalar Scoring asks the MLLM to rate the image from 1 to 5. VQA-Score asks “Does this figure show {caption} ?” and uses P ​ ( yes ) P(\text{yes}) as the reward. Table 5 : Ablation of Reward granularity. Token-level reward does not consistently outperform sequence-level reward, so we use sequence-level reward by default. Figure 5 : Qualitative comparison. Table 6 : The effect of including the EOS token in the reward calculation. Table 7 : Effect of VAE features in Self-SpectraReward reward computation. BAGEL provides two visual inputs to its understanding branch, ViT features from the semantic encoder and VAE features from the generation encoder. Using both inputs improves GenEval and TIIF-Short. Table 8 : Evaluation of text-to-image generation ability on GenEval benchmark. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. † \dagger refers to the methods using the LLM rewriter. Our model’s results and BAGEL all use the LLM rewriter. Table 9 : Performance of proprietary models and state-of-the-art open-source models on TIIF-Bench testmini subset. Evaluated systems are grouped into (i) diffusion-based open-source models, (ii)autoregressive open-source models, and (iii) proprietary models. The results of SpectraReward and BAGEL are evaluated by GPT-4.1. “Inf. SRR” indicates executing the inference-time self-reflective refinement. Table 10: Evaluation of text-to-image generation ability on the DPG-Bench [ dpg ] benchmark. * indicates our reproduced results. Table 11 : Comparison of world knowledge reasoning on WISE. WISE examines the complex semantic understanding and world knowledge for T2I generation. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. Figure 6 : Additional reward-ranking examples. For each prompt, samples are ordered from lower to higher SpectraReward reward. Figure 7 : Additional qualitative comparison. Red text highlights the prompt constraints that are especially sensitive to spatial relation, counting, attribute binding, or long-prompt composition. Self-SpectraReward more consistently satisfies these highlighted constraints than the BAGEL baseline.

这张图是论文中的**图7：额外的定性比较**，用于直观展示所提出的方法（Self-SpectraReward）与基线方法（BAGEL）在文本到图像生成任务上的表现差异，特别是针对那些对空间关系、计数、属性绑定或长提示组合特别敏感的提示约束。

### 图的结构与组件解释：

这张图被组织成一个表格形式，包含多行，每一行对应一个特定的文本提示（Prompt），以及该提示下两种方法（BAGEL 和 Self-SpectraReward）生成的图像结果。

1.  **Prompt 列**：
    *   位于表格的最左侧，列出了用于生成图像的文本指令。
    *   这些提示涵盖了多种复杂的生成要求，例如：
        *   空间关系："a monkey behind a penguin"（企鹅后面的猴子）、"a bear on top of a purple car to the right of five striped toys"（五个条纹玩具右边的紫色汽车上的熊）。
        *   计数："five striped toys"（五个条纹玩具）。
        *   属性绑定："a black backpack with sturdy leather straps"（带有结实皮革背带的黑色背包）、"The metallic pen is right of the fabric blanket"（金属笔在织物毯子的右边）。
        *   长提示组合："The wooden flowers are taller than the wooden trees."（木制花朵比木制树木高）、"To the left of the vibrant tableaux depicted in the painting..."（画中描绘的生动场景的左边...）。
    *   其中一些提示中的关键约束部分被用**红色字体**标出，这些是论文中特别指出需要方法重点满足的敏感约束。

2.  **BAGEL 列**：
    *   位于 Prompt 列的右侧，展示了使用 BAGEL 方法根据对应 Prompt 生成的图像。
    *   BAGEL 在这里作为基线方法进行比较。

3.  **Self-SpectraReward 列**：
    *   位于 BAGEL 列的右侧，展示了使用 Self-SpectraReward 方法根据对应 Prompt 生成的图像。
    *   Self-SpectraReward 是论文中提出的方法，旨在更好地满足提示中的约束。

### 方法运作的揭示：

这张图通过**定性比较**的方式，展示了方法的具体运作效果：

*   **目标**：验证 Self-SpectraReward 是否能比 BAGEL 更一致地满足文本中提出的复杂生成约束。
*   **比较方式**：对于每一个给定的文本提示，观察并对比 BAGEL 和 Self-SpectraReward 生成的图像。
*   **判断依据**：检查生成的图像是否准确地反映了提示中的所有要求，特别是那些被红色字体标出的敏感约束。
*   **结论展示**：从图中可以看出，Self-SpectraReward 生成的图像通常比 BAGEL 更好地满足了提示中的约束。例如：
    *   对于 "a monkey behind a penguin"，BAGEL 生成的图像中猴子在企鹅前面，而 Self-SpectraReward 生成的图像中猴子在企鹅后面，更符合提示。
    *   对于 "a bear on top of a purple car to the right of five striped toys"，BAGEL 生成的图像中熊在车上，但车的位置和玩具的数量可能不完全准确；Self-SpectraReward 生成的图像中熊在紫色汽车上，且汽车位于五个条纹玩具的右边，更符合提示。
    *   对于 "The wooden flowers are taller than the wooden trees"，BAGEL 生成的图像中花朵和树木的高度关系可能不明显或不符合；Self-SpectraReward 生成的图像中花朵明显高于树木，更符合提示。
    *   对于 "A flat-screen TV is mounted on a plain white wall..."，BAGEL 生成的图像中电视的位置或背景可能不完全准确；Self-SpectraReward 生成的图像中电视安装在白色墙上，旁边有笔记本电脑，更符合提示。

### 坐标、对比对象和结论：

*   **坐标**：图中的每个单元格对应一个特定的 (Prompt, Method) 对。行代表不同的 Prompt，列代表不同的方法（BAGEL 和 Self-SpectraReward）。
*   **对比对象**：主要的对比对象是 BAGEL 方法和 Self-SpectraReward 方法生成的图像。
*   **结论**：
    *   这张定性比较图直观地表明，所提出的 Self-SpectraReward 方法在满足文本提示中的复杂约束方面，表现得比 BAGEL 基线方法更好。
    *   特别是对于那些对空间关系、计数、属性绑定或长提示组合特别敏感的约束，Self-SpectraReward 能够更一致地生成符合要求的图像。
    *   这支持了论文的论点，即利用预训练的多模态语言模型（MLLMs）的能力，通过 SpectraReward 或 Self-SpectraReward 方法，可以有效地提升文本到图像生成的质量，使其更符合原始提示的意图。

总而言之，这张图通过一系列具体的例子，清晰地展示了 Self-SpectraReward 方法在文本到图像生成任务中的优势，特别是在处理复杂和敏感的提示约束方面。
