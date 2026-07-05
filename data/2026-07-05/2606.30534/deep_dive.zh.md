# Orca: The World is in Your Mind

[arXiv](https://arxiv.org/abs/2606.30534) · [HuggingFace](https://huggingface.co/papers/2606.30534) · ▲230

## 摘要（原文）

> We introduce Orca, an initial instantiation of a general world foundation model. Orca learns a unified world latent space from multimodal world signals and exposes it through multimodal readout interfaces. Rather than optimizing isolated next-token, next-frame, or next-action prediction, we are centered on Next-State-Prediction modeling, offering a unified state-transition modeling route toward understanding, predicting, and acting upon the world. Orca learns through two complementary paradigms: unconscious learning captures dense natural state transitions from continuous videos, and conscious learning models sparse meaningful state transitions by language-described events and VQA supervision. For pre-training, we construct a large-scale world-learning inventory data, including 125K hours of video data and 160M event annotations. After pre-training, Orca learns a unified world latent space. To examine whether the learned latent supports downstream, we evaluate it by three representative downstream readouts: text generation, image prediction, and embodied action generation. Orca's backbone is frozen, and only the lightweight modality-specific decoders are trainable. Experiments show the scalability of the proposed paradigm and verify that stronger world latent enables stronger downstream readouts. Orca outperforms similar-sized specialized baselines. These results show that Orca, as a general world foundation model, presents a promising approach to understanding, predicting, and acting upon the world. Finally, we discuss the current limitations, aiming to provide useful insights and inspiration for the community.

## 摘要（中译）

我们介绍了Orca，这是一个通用世界基础模型的初步实例化。Orca从多模态世界信号中学习统一的世界潜在空间，并通过多模态读出接口将其暴露出来。我们没有优化孤立的下一token、下一帧或下一动作预测，而是专注于Next-State-Prediction建模，提供了一种统一的状态转换建模路径，以理解、预测和对世界采取行动。Orca通过两种互补的范式学习：无意识学习从连续视频中捕获密集的自然状态转换，而有意识学习通过语言描述的事件和VQA监督来建模稀疏的有意义的状态转换。对于预训练，我们构建了一个大规模的世界学习库存数据，包括125K小时的视频数据和160M的事件注释。预训练后，Orca学习了一个统一的世界潜在空间。为了检查学习到的潜在空间是否支持下游任务，我们通过三个代表性的下游读出进行评估：文本生成、图像预测和具身动作生成。Orca的骨干网络被冻结，只有轻量级的特定于模态的解码器是可训练的。实验证明了所提范式的可扩展性，并验证了更强的世界潜在空间能够实现更强的下游读出。Orca优于类似大小的专门基线。这些结果表明，作为通用世界基础模型的Orca，为理解、预测和对世界采取行动提供了一种有前景的方法。最后，我们讨论了当前的局限性，旨在为社区提供有用的见解和灵感。

## 背景剖析

### 背景剖析  

#### 1. 技术背景与真实需求  
当前人工智能的应用场景正从单一任务（如文本生成或图像识别）向更复杂的“理解并互动于真实世界”扩展。例如，机器人需要根据视觉观察和语言指令完成操作，自动驾驶系统需整合摄像头、雷达和环境描述来决策，而虚拟助手则需结合用户行为和语义理解提供个性化服务。这些场景的核心需求是：**让AI具备像人类一样的世界认知能力**——能够从多模态信号（视觉、语言、动作等）中学习世界的运行规律，并基于这些规律预测未来状态、规划行动。然而，现有方法往往局限于特定任务（如下一个词预测、下一帧生成），缺乏对世界本质的统一建模。  

#### 2. 之前的问题与局限  
传统AI模型（如Next-Token-Prediction或Next-Frame-Prediction）的缺陷在于：  
- **碎片化学习**：它们针对单一模态或任务优化（如仅处理文本或图像），无法捕捉不同信号间的关联（例如，视频中的动作与语言指令的关系）。  
- **缺乏动态建模**：多数模型依赖静态数据或人工标注，难以从连续、无标签的真实世界数据（如长时间视频）中学习自然的状态变化规律。  
- **任务导向而非世界导向**：它们的目标是完成任务（如生成图像）而非理解世界本身，因此无法迁移到未见过的场景或任务。  

这些问题导致模型在复杂、开放的环境中表现受限，例如机器人无法应对意外情况，或助手无法理解隐含的用户意图。  

#### 3. 本文的解法：Orca的设计思路  
Orca通过**“世界潜在空间”**（World Latent Space）的概念解决上述问题。其核心思想是：  
- **统一多模态学习**：从视频、图像、语言等多模态数据中学习一个共享的潜在表示，这个表示能编码世界的状态（如物体的位置、动作的后果）。  
- **两种互补学习范式**：  
  - **无监督学习**：从连续视频中学习“自然状态转移”，例如一个人开门后拿起钥匙的动作序列，模型通过预测下一帧来内化这种动态规律。  
  - **有监督学习**：通过语言描述的稀疏事件（如“机器人捡起杯子”）学习“有意义的状态转移”，将语言逻辑与视觉观察关联。  
- **下游任务验证**：通过冻结主干模型、仅训练轻量级解码器（如文本生成、图像预测），验证潜在空间的通用性。实验表明，潜在空间越强，下游任务表现越好。  

#### 4. 与前人工作的关键差异  
Orca的创新在于：  
- **从“任务导向”到“世界导向”**：不同于专注于单一任务的模型（如GPT-54仅优化文本生成），Orca的目标是建模世界的潜在规律，从而支持多种下游任务。  
- **双范式结合**：将无监督的自然动态学习与有监督的语言条件学习结合，既捕捉真实世界的连续性，又利用人类的逻辑指导。  
- **可扩展性验证**：通过大规模数据（125K小时视频+1.6亿事件标注）证明，模型性能随数据量和规模提升而增强，而非依赖任务特定的优化。  

总之，Orca的提出标志着向“通用世界基础模型”迈出第一步，其核心是通过统一的状态转移建模，让AI真正理解并互动于复杂世界。

## 方法图解

![Figure 1 : The Orca’s overall framework. Orca follows an Encoder-Decoder archite](fig1_1.webp)

> Figure 1 : The Orca’s overall framework. Orca follows an Encoder-Decoder architecture. Given multimodal world signals, the Encoder learns a world latent through two complementary paradigms: unconscious learning and conscious learning . Unconscious learning captures dense natural state transitions, while conscious learning captures sparse meaningful state transitions. To prove that the learned latent is effective, the Encoder is frozen after pre-training, and only the lightweight modality-specific decoders are trainable separately. The Decoder reads out the latent into text, images, actions, and other modalities.

我们来详细解读这张图，它展示了Orca模型的整体框架，遵循**编码器-解码器（Encoder-Decoder）**架构，清晰呈现了从多模态世界信号输入到多模态输出（文本、图像、动作等）的完整流程：

### 编码器（Encoder）部分：
- **输入**：最左侧的“Multimodal world signal”（多模态世界信号）是整个流程的起点，代表来自现实世界的多种类型数据（如视频、语言描述的事件等）。
- **核心组件：Orca**：绿色的“Orca”模块是编码器的核心，负责学习**统一的世界潜在表示（World Latent Representation）**。它通过两种互补的学习范式来实现这一点：
  - **Unconscious learning（无意识学习）**：虚线框标注的“无意识学习”，其作用是**捕捉密集的自然状态转移**——比如从连续视频中学习现实中连续发生的状态变化（如物体移动、场景切换等自然发生的动态过程）。
  - **Conscious learning（有意识学习）**：另一个虚线框“有意识学习”，负责**捕捉稀疏的有意义状态转移**——例如通过语言描述的事件（如“猫跳上桌子”）或视觉问答（VQA）监督来学习具有明确语义的状态变化。
- **输出到潜在表示**：Orca处理多模态信号后，输出“World Latent Representation”（世界潜在表示），这是对世界的统一抽象表示，包含了从输入中学习到的状态转移规律。

### 解码器（Decoder）部分：
- **冻结编码器**：根据图注，在预训练后，“Orca”的 backbone（核心结构）被**冻结**（即参数不再更新），这确保了学习到的世界潜在表示的稳定性。
- **轻量解码器**：只有“lightweight modality - specific decoders”（轻量级的模态特定解码器）是可训练的，它们负责从世界潜在表示中“读取”出不同模态的输出：
  - **文本输出路径**：“LM head”（语言模型头）将潜在表示转换为文本（如回答问题、生成描述等）；然后“Action expert”（动作专家）模块可以将文本进一步转换为动作（如果需要的话，比如基于文本指令生成机器人动作）。
  - **图像输出路径**：“Image decoder”（图像解码器）将潜在表示转换为图像（如生成与潜在状态对应的图像、预测下一帧图像等）。
  - **其他模态输出**：“Other modal decoder”（其他模态解码器）可以扩展到更多模态（如音频、触觉等），输出“More outputs”（更多输出），体现了模型的多模态泛化能力。

### 数据/信息流动顺序：
1. 多模态世界信号输入到Orca（编码器）。
2. Orca通过无意识学习和有意识学习，从输入中学习世界潜在表示。
3. 预训练后，编码器冻结，潜在表示被传递到解码器。
4. 解码器的不同模块（LM头、图像解码器、动作专家等）将潜在表示转换为文本、图像、动作等不同模态的输出，以完成下游任务（如文本生成、图像预测、具身动作生成等）。

### 方法运作逻辑：
Orca的目标是学习一个统一的“世界潜在空间”，这个空间能够捕捉现实世界的状态转移规律。通过**无意识学习**处理连续的、密集的自然状态转移（如视频中的动态），**有意识学习**处理稀疏的、有语义的状态转移（如语言事件），Orca能够全面理解世界的运作方式。预训练后冻结编码器，只训练轻量解码器，这样的设计既保证了潜在表示的稳定性，又能灵活适配不同的下游任务（文本、图像、动作等）。通过评估下游任务的性能（如文本生成质量、图像预测准确性、动作生成合理性），可以验证学习到的世界潜在空间的有效性——实验表明，更强大的世界潜在空间会带来更好的下游任务表现，Orca在同类规模的专用基线模型上表现出优势。

这张图清晰地展示了Orca从“理解世界（编码器学习潜在表示）”到“作用于世界（解码器生成多模态输出）”的完整流程，体现了其作为“通用世界基础模型”的设计理念：通过统一的世界潜在空间，支持多种下游任务的优秀表现。

---

![Figure 2 : Overview of Encoder. Orca learns a world latent representation throug](fig2_1.webp)

> Figure 2 : Overview of Encoder. Orca learns a world latent representation through two learning paradigms. Unconscious learning uses video data to capture dense and natural state transitions. Conscious learning uses language instructions as explicit semantic conditions to capture sparse and meaningful state transitions.

这张图展示了Orca模型学习世界潜在表示的**整体架构**，核心是通过两种学习范式（无意识学习和有意识学习）从多模态信号中学习统一的世界潜在空间，并最终输出到“World Latent Representation”（世界潜在表示）。以下分模块和流程详细讲解：

### 输入与整体流程
- **左侧输入**：有两个信号源——`Visual Signal`（视觉信号，带眼睛图标）和`Language Signal`（语言信号，带文档图标）。这些是Orca学习的外部输入，分别提供视觉和语言层面的世界信息。
- **中间模块**：分为两个虚线框，分别是`Unconscious learning`（无意识学习）和`Conscious learning`（有意识学习），每个框内有不同的子任务（状态转移或响应生成），最终所有学习结果流向右侧的`World Latent Representation`（世界潜在表示），这是模型学习到的统一世界表征。

### 1. 无意识学习（Unconscious learning）
- **子任务**：`Observation-only state transition`（仅观测的状态转移）。
- **组件与流程**：
  - 输入：`v_t`（时间步t的视觉信号，带眼睛图标），以及潜在变量`z`（虚线箭头输入，可能表示先验或隐状态）。
  - 模型：`Orca`（绿色方框，核心模型）。
  - 输出：`\hat{v}_{t+1}^l`（时间步t+1的预测视觉信号，带眼睛图标）。
- **逻辑**：无意识学习通过**连续视频数据**捕捉**密集且自然的状态转移**（比如视频中帧与帧之间的连续变化）。它只基于当前视觉观测（`v_t`）和潜在变量`z`，预测下一个时间步的视觉状态（`\hat{v}_{t+1}^l`），模拟人类无意识中对外部世界连续变化的感知与预测。

### 2. 有意识学习（Conscious learning）
有意识学习包含两个子任务，通过**语言描述的稀疏事件**和**VQA监督**捕捉**稀疏但有意义的状态转移**（比如根据语言指令或问题理解世界状态的变化）：

#### 子任务2：Event-conditioned state transition（事件条件下的状态转移）
- **输入**：
  - `v_t`（时间步t的视觉信号，带眼睛图标）。
  - `e_{t+Δ}`（时间步t+Δ的事件信号，带文档图标，可能是语言描述的事件，比如“球被抛出”）。
  - 潜在变量`z`（虚线箭头输入）。
- **模型**：`Orca`（绿色方框）。
- **输出**：`\hat{v}_{t+Δ}^l`（时间步t+Δ的预测视觉信号，带眼睛图标）。
- **逻辑**：有意识学习的第一部分，利用**语言描述的事件**（`e_{t+Δ}`）作为条件，结合当前视觉（`v_t`）和潜在变量`z`，预测未来时间步（t+Δ）的视觉状态。这模拟了人类根据语言指令或事件描述，有意识地预测世界状态变化的能力（比如根据“扔球”的指令，预测球后续的位置）。

#### 子任务3：VQA response generation（VQA响应生成）
- **输入**：
  - `V`（视觉信号，带眼睛图标，可能是问题相关的图像）。
  - `ℓ_q`（语言问题信号，带文档图标，比如“球在哪里？”）。
  - 潜在变量`z`（虚线箭头输入）。
- **模型**：`Orca`（绿色方框）。
- **输出**：`ℓ_a`（语言回答信号，带文档图标，比如“球在桌子上”）。
- **逻辑**：有意识学习的第二部分，利用**视觉问题**（`V`）和**语言问题**（`ℓ_q`）作为输入，结合潜在变量`z`，生成**语言回答**（`ℓ_a`）。这模拟了人类回答关于世界状态的问题（视觉问答）的能力，通过语言交互理解并输出世界状态。

### 整体运作逻辑
Orca的核心是学习**统一的世界潜在空间**：
- 无意识学习从**连续视频**中学习**密集的自然状态转移**（如帧间的连续变化），捕捉世界的基础动态。
- 有意识学习从**语言描述的事件**（事件条件状态转移）和**VQA任务**（响应生成）中学习**稀疏但有意义的状态转移**（如根据指令或问题理解特定状态变化）。
- 所有学习过程都围绕`Orca`模型，通过预测下一个状态（视觉或语言）来建模**Next-State-Prediction**（下一个状态预测），最终输出到“World Latent Representation”，这个潜在表示可以被用于下游任务（如图中提到的文本生成、图像预测、具身动作生成）。

### 方法核心
Orca通过**两种互补的学习范式**（无意识的密集连续学习 + 有意识的稀疏语义学习），从多模态信号（视觉、语言）中学习统一的世界潜在空间，而不是优化孤立的next-token、next-frame等预测。这种方法的目标是让模型能够**理解、预测和作用于世界**，通过学习到的潜在表示支持下游任务，并验证“更强的世界潜在表示会带来更强的下游任务表现”。

总结来说，这张图清晰展示了Orca如何从视觉和语言信号中，通过无意识和有意识的学习范式，学习统一的世界潜在表示，核心是**Next-State-Prediction**建模，以实现对世界的统一理解、预测和交互。

---

![Figure 3 : Overview of pre-training data. Orca’s pre-training data includes vide](fig3_1.webp)

> Figure 3 : Overview of pre-training data. Orca’s pre-training data includes video, event, and VQA data. A. Video Data supports 1) Observation-only state transition , A. Video Data and B. Event Data support 2) Event-conditioned state transition , and C. VQA Data supports 3) VQA response generation .

这张图是论文《Orca: The World is in Your Mind》中关于Orca模型预训练数据的概述图，展示了Orca预训练数据的组成、数据流向以及不同数据类型与预训练目标、学习范式的关系，帮助理解Orca模型的预训练机制：

### 数据来源与类型
- **视觉信号（Visual Signal）** 是数据的起始输入，分为两类数据：
    - **视频数据（A. Video Data）**：包含四种类型，分别是“Ego - Centric Interaction（以自我为中心的交互）”、“Exo - Centric Manipulation（以外部为中心的操作）”、“Action - Free Robot Execution（无动作机器人执行）”和“Natural Dynamics（自然动态）”。这些视频数据通过“Event Segmentation（事件分割）”处理后，会流向后续的事件数据和VQA数据相关流程，同时也直接支持预训练目标中的“1) Observation - only state transition（仅观察的状态转换）”。
    - **语言信号（Language Signal）** 是另一类输入，与视频数据经过事件分割后的结果结合，生成两类数据：
        - **事件数据（B. Event Data）**：包含“Fine & Coarse Caption（精细和粗略的描述）”，它和视频数据一起支持预训练目标中的“2) Event - conditioned state transition（事件条件下的状态转换）”。
        - **VQA数据（C. VQA Data）**：包含“General VQA（通用视觉问答）”，它支持预训练目标中的“3) VQA response generation（VQA响应生成）”。

### 预训练目标（Pre - Training Objectives）
Orca的预训练目标有三个，分别对应不同的数据和学习范式：
- **1) Observation - only state transition**：仅由视频数据（A. Video Data）支持，属于“Unconscious learning（无意识学习）”范式。这种学习范式捕捉连续视频中的密集自然状态转换，不需要语言描述的监督，是从视频的视觉信息中直接学习状态的变化。
- **2) Event - conditioned state transition**：由视频数据（A. Video Data）和事件数据（B. Event Data）共同支持，属于“Conscious learning（有意识学习）”范式。这里的状态转换是在事件（由语言描述的）的条件下进行的，结合了视觉的事件分割结果和语言的事件描述，学习有条件的状态变化。
- **3) VQA response generation**：由VQA数据（C. VQA Data）支持，也属于“Conscious learning（有意识学习）”范式。通过视觉问答的监督，学习如何根据视觉和语言信息生成响应，进一步建模状态相关的知识。

### 学习范式与世界潜在表示（Learning Paradigms & World Latent Representation）
- **Unconscious learning（无意识学习）**：基于“Observation - only state transition”的预训练目标，从视频数据中学习密集的自然状态转换，这是一种无语言监督的学习方式，主要捕捉世界的基本动态。
- **Conscious learning（有意识学习）**：基于“Event - conditioned state transition”和“VQA response generation”的预训练目标，结合事件数据（语言描述的 event）和VQA数据，学习有意义的、由语言引导的状态转换和响应生成，这种方式利用语言来丰富对世界的理解。
- 这两种学习范式最终都指向“World Latent Representation（世界潜在表示）”，即Orca通过这两种互补的学习范式，学习到一个统一的世界潜在空间，这个潜在空间可以支持下游的任务（如文本生成、图像预测、具身动作生成等）。

### 数据流动顺序
1. 视觉信号输入到视频数据（A. Video Data），视频数据经过事件分割后，一部分用于支持“Observation - only state transition”（无意识学习），另一部分与语言信号结合生成事件数据（B. Event Data）和VQA数据（C. VQA Data）。
2. 事件数据（B. Event Data）和视频数据（A. Video Data）共同支持“Event - conditioned state transition”（有意识学习）；VQA数据（C. VQA Data）支持“VQA response generation”（有意识学习）。
3. 无意识学习和有意识学习这两种范式的学习结果最终汇聚到世界潜在表示，为下游任务提供支持。

这张图清晰地展示了Orca模型如何通过多模态数据（视频、事件、VQA数据）、不同的预训练目标和两种互补的学习范式（无意识和有意识学习）来构建世界潜在表示，从而实现对世界的理解、预测和行动的基础能力。

---

![Figure A1 : Conceptual illustration of Orca . Existing models are often organize](fig9_1.webp)

> Figure A1 : Conceptual illustration of Orca . Existing models are often organized around passive task-driven prediction, including next-token, next-frame, and next-action prediction. Orca shifts the modeling target toward next-state prediction, where multimodal world signals are used to learn a unified world latent. Unconscious learning captures dense natural dynamics from continuous observation, while conscious learning captures meaningful state transitions guided by language, events, and intentions. The learned world latent supports downstream readouts to language, vision, and action.

这张图是论文《Orca: The World is in Your Mind》中的概念插图，用于直观展示Orca模型的核心思想和运作机制。我们可以从左到右、从上到下逐步解析图中的各个部分：

首先，图的顶部有一个水平轴，从左到右展示了从“被动任务驱动”（Passive Task Driven）到“主动世界学习者”（Active World Learner）的范式转变。这个轴代表了模型学习的演进方向。

在“被动任务驱动”部分，从左到右依次列出了几种传统的预测任务：
1.  **Next Token Prediction (Semantic Understanding)**：这是最基础的预测任务，通常与语言处理相关，比如预测文本中的下一个词或标记，代表语义理解。
2.  **Next Frame Prediction (Visual Dynamics Prediction)**：这是计算机视觉中的任务，预测序列中的下一帧图像，关注视觉动态。
3.  **Next Action Prediction (Action Affordance Reasoning)**：这是决策或机器人学中的任务，预测下一步应该采取的行动，涉及行动可能性推理。
这些任务都是“被动”的，因为它们通常针对特定的、孤立的预测目标。

然后，箭头指向“Next State Prediction (World Modeling)”，这代表了Orca模型的核心创新点。它不再局限于单一类型的预测，而是专注于预测“下一个状态”，这涉及到对整个世界的统一建模（World Modeling）。这个转变是从一系列孤立的任务预测转向一个更统一、更全面的世界状态理解。

图的下半部分通过两个主要路径展示了Orca的学习过程：
1.  **无意识学习（Unconscious learning）**：这条路径由上方的文本“Unconscious learning”和例子“Natural physical laws (e.g. Wind blows leaves fall)”（自然物理规律，如风吹叶落）来标识。它对应于从连续的视频数据中捕获密集的自然动态。在图中，这通过一列连续的、逐渐变化的房间场景来表示，这些场景从一个婴儿（标记为“A World Learner”）开始，通过观看一系列视频帧（用胶片条表示）来学习世界的自然规律。这些视频帧展示了场景的连续变化，婴儿通过观察这些变化来学习。
2.  **有意识学习（Conscious learning）**：这条路径由下方的文本“Conscious learning”和例子“Meaningful causal events (e.g. Ice cream melts when heated)”（有意义的因果事件，如冰淇淋受热融化）来标识。它通过语言描述的事件和视觉问答（VQA）监督来建模稀疏但有意义的状态转换。在图中，这通过一个被突出显示的人物（可能代表一个思考者或学习者）和一个特定的场景（例如，一个人在房间里，旁边可能有某种事件发生）来表示。这个路径关注的是由语言和意图引导的、更具目的性和因果关系的学习。

这两个学习路径共同作用于“一个世界学习者”（A World Learner），最终目标是学习一个“统一的世界潜在空间”（unified world latent space）。这个潜在空间是Orca模型内部对世界的表示。

图的左侧展示了传统的模型组织方式，即围绕被动任务驱动的预测。而Orca则将建模目标转向“下一个状态预测”，利用多模态世界信号来学习这个统一的潜在空间。

总结来说，这张图揭示了Orca方法的具体运作方式：
*   **范式转变**：从孤立的被动任务预测（如下一个词、下一帧、下一个动作）转向统一的主动世界状态预测。
*   **双轨学习**：
    *   **无意识学习**：从连续视频中学习自然的、密集的动态规律。
    *   **有意识学习**：从语言描述的事件和VQA中学习有意义的、稀疏的因果关系。
*   **统一表征**：通过这两种学习方式，Orca构建了一个统一的世界潜在空间，这个空间支持下游的语言生成、图像预测和行动生成等任务。

图中的信息流动顺序是：从传统的被动任务驱动预测开始，逐渐演进到Orca的核心——下一个状态预测，然后通过无意识学习和有意识学习这两种互补范式来构建统一的世界潜在空间，最终支持各种下游应用。
