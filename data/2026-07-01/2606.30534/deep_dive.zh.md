# Orca: The World is in Your Mind

[arXiv](https://arxiv.org/abs/2606.30534) · [HuggingFace](https://huggingface.co/papers/2606.30534) · ▲234

## 摘要（原文）

> We introduce Orca, an initial instantiation of a general world foundation model. Orca learns a unified world latent space from multimodal world signals and exposes it through multimodal readout interfaces. Rather than optimizing isolated next-token, next-frame, or next-action prediction, we are centered on Next-State-Prediction modeling, offering a unified state-transition modeling route toward understanding, predicting, and acting upon the world. Orca learns through two complementary paradigms: unconscious learning captures dense natural state transitions from continuous videos, and conscious learning models sparse meaningful state transitions by language-described events and VQA supervision. For pre-training, we construct a large-scale world-learning inventory data, including 125K hours of video data and 160M event annotations. After pre-training, Orca learns a unified world latent space. To examine whether the learned latent supports downstream, we evaluate it by three representative downstream readouts: text generation, image prediction, and embodied action generation. Orca's backbone is frozen, and only the lightweight modality-specific decoders are trainable. Experiments show the scalability of the proposed paradigm and verify that stronger world latent enables stronger downstream readouts. Orca outperforms similar-sized specialized baselines. These results show that Orca, as a general world foundation model, presents a promising approach to understanding, predicting, and acting upon the world. Finally, we discuss the current limitations, aiming to provide useful insights and inspiration for the community.

## 摘要（中译）

我们介绍了Orca，这是一个通用世界基础模型的初步实例化。Orca从多模态世界信号中学习统一的世界潜在空间，并通过多模态读出接口将其暴露出来。我们没有优化孤立的下一token、下一帧或下一动作预测，而是专注于Next-State-Prediction建模，提供了一种统一的状态转换建模路径，以理解、预测和对世界采取行动。Orca通过两种互补的范式学习：无意识学习从连续视频中捕获密集的自然状态转换，而有意识学习通过语言描述的事件和VQA监督来建模稀疏的有意义的状态转换。对于预训练，我们构建了一个大规模的世界学习库存数据，包括125K小时的视频数据和160M的事件注释。预训练后，Orca学习了一个统一的世界潜在空间。为了检查学习到的潜在空间是否支持下游任务，我们通过三个代表性的下游读出进行评估：文本生成、图像预测和具身动作生成。Orca的骨干网络被冻结，只有轻量级的特定于模态的解码器是可训练的。实验证明了所提范式的可扩展性，并验证了更强的世界潜在空间能够实现更强的下游读出。Orca优于类似大小的专门基线。这些结果表明，作为通用世界基础模型的Orca，为理解、预测和对世界采取行动提供了一种有前景的方法。最后，我们讨论了当前的局限性，旨在为社区提供有用的见解和灵感。

## 背景剖析

### 背景剖析  

#### 1. 技术背景  
通用人工智能（AGI）的核心挑战之一是让模型像人类一样持续学习并理解世界。现实中，我们需要一种系统能从视觉、语言、动作等多模态信号中构建对世界的统一认知，并基于这种认知进行预测和决策。例如，机器人需要理解物理规律（如物体运动）、因果关系（如“开灯会导致房间变亮”），甚至跨领域知识（如科学原理或社会规则）。这类技术旨在打造一个能自主进化、适应复杂环境的智能体，最终超越人类在特定任务上的认知局限。  

#### 2. 之前的问题  
传统方法（如仅优化“下一个词预测”“下一帧生成”或“下一步动作预测”）存在明显不足：它们孤立地处理单一任务，缺乏对世界动态的统一建模。例如，语言模型擅长生成文本，但难以理解图像中的物理交互；视频预测模型能生成画面，却无法关联语义意图。此外，这些方法依赖大量标注数据，而真实世界中许多关键信号（如无监督的视频流或稀疏的事件描述）未被充分利用。因此，现有模型无法泛化到未见过的新场景或跨领域任务。  

#### 3. 本文的解法  
Orca 提出通过“状态转移建模”解决这一问题。它从两类信号中学习世界的潜在状态：  
- **无监督学习**：从连续视频中捕捉自然、密集的状态变化（如物体移动或场景转换），无需人工标注。  
- **有监督学习**：通过语言描述的事件（如“人打开门”）和视觉问答（VQA）监督，学习与决策相关的稀疏但有意义的状态转移。  
这种方法让 Orca 构建一个统一的潜在空间，支持文本生成、图像预测和机器人动作生成等下游任务。实验表明，随着模型规模和数据量增加，其性能持续提升，且优于同类专用模型。  

#### 4. 切入角度  
与以往工作不同，Orca 不追求单一任务的“最优性能”，而是聚焦于“世界建模的通用性”。其关键创新在于：  
- **双学习范式**：结合无监督的自然动态学习和有监督的任务导向学习，平衡数据效率与认知深度。  
- **冻结主干网络**：仅训练轻量级的模态特定解码器，避免过拟合，确保潜在空间的泛化能力。  
- **大规模多模态数据**：构建包含 125K 小时视频和 1.6 亿事件标注的数据集，覆盖多样化场景。  
这种设计使 Orca 成为迈向通用世界基础模型的第一步，为未来 AGI 的发展提供了新方向。

## 方法图解

![Figure 1 : The Orca’s overall framework. Orca follows an Encoder-Decoder archite](fig1_1.webp)

> Figure 1 : The Orca’s overall framework. Orca follows an Encoder-Decoder architecture. Given multimodal world signals, the Encoder learns a world latent through two complementary paradigms: unconscious learning and conscious learning . Unconscious learning captures dense natural state transitions, while conscious learning captures sparse meaningful state transitions. To prove that the learned latent is effective, the Encoder is frozen after pre-training, and only the lightweight modality-specific decoders are trainable separately. The Decoder reads out the latent into text, images, actions, and other modalities.

这张图展示了Orca的整体框架，采用**编码器-解码器（Encoder - Decoder）**架构，清晰呈现了从多模态世界信号输入到多模态输出的工作流程：

### 编码器（Encoder）部分：
- **输入**：最左侧的“Multimodal world signal”（多模态世界信号）是整个流程的起点，代表来自现实世界的多模态输入（如视频、文本描述的事件等）。
- **核心组件：Orca**：绿色的“Orca”模块是编码器的核心，负责学习**统一的世界潜在空间（World Latent Representation）**。它通过两种互补的学习范式实现这一目标：
  - **Unconscious learning（无意识学习）**：虚线框标注，作用是“捕捉密集的自然状态转移”——即从连续视频等连续数据中学习大量的、自然发生的状态变化（比如视频中物体的运动、场景的连续变化等）。
  - **Conscious learning（有意识学习）**：另一个虚线框，作用是“捕捉稀疏的有意义状态转移”——通过语言描述的事件（如“猫跳上桌子”）和视觉问答（VQA）监督，学习那些虽然出现频率低但语义重要的状态变化（比如特定事件的触发、物体间的语义关联等）。
- **输出到潜在空间**：Orca的输出是“World Latent Representation”（世界潜在表示），这是经过两种学习范式处理后得到的统一潜在空间，它编码了世界的关键状态信息。

### 解码器（Decoder）部分：
- **冻结编码器**：图中隐含的信息是，预训练后Orca的编码器（即学习潜在空间的部分）被**冻结**（不再训练），只有轻量级的、特定于模态的解码器是可训练的——这保证了潜在空间的稳定性，同时让下游任务能灵活适配。
- **解码器的目标**：右侧的“Decoder”部分目标是“做好所有下游任务（Do all downstream tasks well）”，即从潜在空间中读取信息并转换为不同的模态输出：
  - **文本生成**：路径为“LM head（语言模型头）”→“Text（文本）”，通过语言模型头将潜在空间的信息解码为文本（比如回答问题、生成描述等）。
  - **图像预测**：路径为“Image decoder（图像解码器）”→“Image（图像）”，通过图像解码器将潜在空间信息转换为图像（比如预测下一帧视频、生成与描述匹配的图像等）。
  - **动作生成（具身智能）**：路径为“Action expert（动作专家）”→“Action（动作）”，通过动作专家模块将潜在空间信息转换为动作（比如机器人的运动控制、游戏中的角色动作等）。
  - **其他模态输出**：“Other modal decoder（其他模态解码器）”→“More outputs（更多输出）”，表示还可以扩展到其他模态（如音频、触觉等）的输出，体现了方法的通用性。

### 数据/信息流动顺序：
1. 多模态世界信号输入到Orca（编码器）。
2. Orca通过无意识学习和有意识学习，将输入转换为统一的世界潜在表示。
3. 冻结的编码器将潜在表示传递给解码器。
4. 解码器的不同模块（LM头、图像解码器、动作专家、其他模态解码器）将潜在表示解码为文本、图像、动作或其他模态的输出，完成下游任务。

### 方法运作逻辑：
Orca的核心是**学习统一的世界潜在空间**，而不是优化孤立的“下一个token/帧/动作”预测。它通过两种互补的学习范式（无意识学习处理密集的自然状态转移，有意识学习处理稀疏的有意义状态转移）从多模态世界信号中学习。预训练后，编码器冻结以保证潜在空间的稳定性，下游任务通过轻量级的模态特定解码器来实现，这样既利用了统一的潜在空间理解世界，又能灵活适配不同的下游任务（文本、图像、动作等）。实验表明，更强的世界潜在空间能带来更好的下游任务表现，Orca在同类规模的专用基线模型上表现出优势，验证了其作为通用世界基础模型的有效性。

---

![Figure 2 : Overview of Encoder. Orca learns a world latent representation throug](fig2_1.webp)

> Figure 2 : Overview of Encoder. Orca learns a world latent representation through two learning paradigms. Unconscious learning uses video data to capture dense and natural state transitions. Conscious learning uses language instructions as explicit semantic conditions to capture sparse and meaningful state transitions.

这张图展示了Orca模型学习世界潜在表示的核心流程，分为**无意识学习**和**有意识学习**两个互补范式，最终输出统一的“世界潜在表示（World Latent Representation）”。以下是各组件的详细解释和信息流动逻辑：

### 输入与整体流程
- **左侧输入**：包含两种信号源——`Visual Signal`（视觉信号，如图标所示）和`Language Signal`（语言信号，如图标所示）。这些信号是Orca学习的原始数据输入。
- **核心组件：Orca**：图中有三个Orca模块，分别对应三种学习/推理任务，它们共享底层架构（backbone冻结，仅轻量模态特定解码器可训练），目标是学习统一的世界潜在空间。
- **输出**：所有学习任务的最终目标是生成`World Latent Representation`（世界潜在表示），这是对世界的统一抽象，支持下游任务（如文本生成、图像预测、具身动作生成）。


### 1. 无意识学习（Unconscious Learning）
- **任务类型**：`Observation-only state transition`（仅观测的状态转移）。
- **输入**：`v_t`（时间步t的视觉信号，如图标所示），以及潜在变量`z`（虚线箭头表示，可能是先验或上下文信息）。
- **处理与输出**：Orca模块接收`v_t`和`z`，输出`$\hat{v}_{t+1}^l$`（时间步t+1的预测视觉信号）。这个过程模拟了从连续视频中捕捉**密集且自然的状态转移**（比如视频中物体的运动、场景的变化等，无需显式语言指导，仅通过视觉观测序列学习状态变化规律）。
- **数据流动**：视觉信号`v_t` → Orca（结合`z`）→ 预测的下一视觉状态`$\hat{v}_{t+1}^l$`，这一过程反复进行以学习状态的连续转移模式。


### 2. 有意识学习（Conscious Learning）
有意识学习又分为两个子任务，利用语言提供的**稀疏但语义明确的状态转移条件**来学习：

#### 子任务2：事件条件下的状态转移（Event-conditioned state transition）
- **输入**：`v_t`（时间步t的视觉信号）、`e_{t+Δ}`（时间步t+Δ的事件注释/语言描述，如图标所示），以及潜在变量`z`。
- **处理与输出**：Orca模块接收`v_t`、`e_{t+Δ}`和`z`，输出`$\hat{v}_{t+Δ}^l$`（时间步t+Δ的预测视觉信号）。这个任务模拟了**基于语言描述的事件（如“球被抛出”）来预测未来状态**，捕捉稀疏但有语义意义的状态转移（因为语言事件是稀疏的，但能明确状态变化的原因和结果）。
- **数据流动**：视觉信号`v_t` + 事件语言`e_{t+Δ}` + `z` → Orca → 预测的未来视觉状态`$\hat{v}_{t+Δ}^l$`，通过这种方式学习“语言事件→状态转移”的映射。

#### 子任务3：VQA响应生成（VQA response generation）
- **输入**：`V`（视觉信号，如图标所示）、`ℓ_q`（语言问题，如图标所示），以及潜在变量`z`。
- **处理与输出**：Orca模块接收`V`、`ℓ_q`和`z`，输出`ℓ_a`（语言答案，如图标所示）。这个任务模拟了**基于视觉和语言问题的问答**，进一步验证模型对世界状态的理解（比如“图中的球是什么颜色？”需要模型理解视觉状态并生成语言响应）。
- **数据流动**：视觉信号`V` + 语言问题`ℓ_q` + `z` → Orca → 语言答案`ℓ_a`，通过问答任务强化模型对世界状态的表示能力。


### 方法的核心逻辑
Orca通过**两种互补的学习范式**构建世界潜在表示：
- **无意识学习**：从连续视频中学习**密集的自然状态转移**（如物体的连续运动），捕捉世界的“连续性”和“自然性”。
- **有意识学习**：从语言描述的事件（子任务2）和VQA（子任务3）中学习**稀疏但语义明确的状态转移**，捕捉世界的“因果性”和“语义性”。

这两种范式共同作用，让Orca学习到一个统一的`World Latent Representation`，该表示能够支持下游的多模态任务（文本生成、图像预测、具身动作生成）。模型的backbone冻结，仅训练轻量的模态特定解码器，确保学习的效率和通用性。


### 结论（从图中逻辑推导）
这张图展示了Orca如何通过“无意识（连续视频）+ 有意识（语言事件/VQA）”的双范式学习，构建统一的世界潜在表示。这种设计让模型既能捕捉世界的连续动态（无意识学习），又能理解语义明确的事件和问答（有意识学习），最终生成的潜在表示能够支持多种下游任务，体现了“通用世界基础模型”的核心思想。

---

![Figure 3 : Overview of pre-training data. Orca’s pre-training data includes vide](fig3_1.webp)

> Figure 3 : Overview of pre-training data. Orca’s pre-training data includes video, event, and VQA data. A. Video Data supports 1) Observation-only state transition , A. Video Data and B. Event Data support 2) Event-conditioned state transition , and C. VQA Data supports 3) VQA response generation .

这张图展示了Orca模型预训练数据的构成、预训练目标以及学习范式，清晰地呈现了Orca如何从多模态信号中学习世界潜在表示的过程。

首先看**预训练数据和注释（Pre - Training Data and Annotations）**部分：
- **视觉信号（Visual Signal）**作为输入，分为三类数据：
    - **A. 视频数据（Video Data）**：包含四种类型，分别是“Ego - Centric Interaction（以自我为中心的交互）”、“Exo - Centric Manipulation（以他人为中心的操作）”、“Action - Free Robot Execution（无动作机器人执行）”和“Natural Dynamics（自然动态）”。这些视频数据会经过“Event Segmentation（事件分割）”处理，之后为后续的目标提供支持。
    - **B. 事件数据（Event Data）**：由“Fine & Coarse Caption（精细和粗略的描述）”组成，它的输入来源是“Language Signal（语言信号）”以及经过事件分割后的视频数据相关内容。
    - **C. VQA数据（VQA Data）**：包含“General VQA（通用视觉问答）”，输入同样来自“Language Signal”。

然后是**预训练目标（Pre - Training Objectives）**部分，它有三个目标，分别对应不同的数据支持：
- 目标1：“Observation - only state transition（仅观察的状态转换）”，仅由**视频数据（A）**支持。
- 目标2：“Event - conditioned state transition（事件条件下的状态转换）”，由**视频数据（A）和事件数据（B）**共同支持。
- 目标3：“VQA response generation（VQA响应生成）”，由**VQA数据（C）**支持。

接下来是**学习范式（Learning Paradigms）**部分，分为两种学习方式，它们最终都指向“World Latent Representation（世界潜在表示）”：
- **无意识学习（Unconscious learning）**：与目标1（仅观察的状态转换）相关联，它从连续的视频中捕捉密集的自然状态转换。
- **有意识学习（Conscious learning）**：与目标2（事件条件下的状态转换）和目标3（VQA响应生成）相关联，它通过语言描述的事件和VQA监督来建模稀疏的有意义的状态转换。

数据的流动顺序是：视觉信号先进入视频数据、事件数据（经过事件分割）和VQA数据的构建；然后这些数据分别支持不同的预训练目标；最后，通过无意识学习和有意识学习这两种范式，学习得到世界潜在表示。

从方法运作的角度来看，Orca的预训练过程是：首先收集大规模的多模态数据，包括125K小时的视频数据、160M的事件注释等。然后，针对不同的预训练目标，利用对应的视频、事件或VQA数据进行学习。无意识学习专注于从连续视频中学习密集的状态转换，而有意识学习则通过语言相关的事件和VQA任务学习稀疏但有意义的状态转换。最终，这两种学习范式共同作用，让Orca学习到一个统一的世界潜在空间，这个潜在空间可以用于下游的任务，如图文生成、图像预测和具身动作生成等。

---

![Figure A1 : Conceptual illustration of Orca . Existing models are often organize](fig9_1.webp)

> Figure A1 : Conceptual illustration of Orca . Existing models are often organized around passive task-driven prediction, including next-token, next-frame, and next-action prediction. Orca shifts the modeling target toward next-state prediction, where multimodal world signals are used to learn a unified world latent. Unconscious learning captures dense natural dynamics from continuous observation, while conscious learning captures meaningful state transitions guided by language, events, and intentions. The learned world latent supports downstream readouts to language, vision, and action.

这张图是论文《Orca: The World is in Your Mind》中用于概念性说明Orca模型核心思想的示意图，我们可以从左到右、从上到下逐步解析图中的各个组件、信息流动以及方法的核心逻辑：

### 整体框架与任务演进
图的上方有一个从“Passive Task Driven（被动任务驱动）”到“Active World Learner（主动世界学习者）”的渐变箭头，代表了模型从传统任务驱动的预测范式向更主动的世界学习范式的转变。在被动任务驱动阶段，模型主要关注**Next Token Prediction（下一个token预测，语义理解）**、**Next Frame Prediction（下一个帧预测，视觉动态预测）**、**Next Action Prediction（下一个动作预测，动作可供性推理）**；而在主动世界学习阶段，模型的核心是**Next State Prediction（下一个状态预测，世界建模）**。信息（或任务的焦点）沿着这个箭头的方向演进，从局部的、任务特定的预测转向全局的、统一的状态转移预测。

### 左侧：传统被动任务驱动的模型（“A World Learner”的早期/传统方式）
- **“A World Learner”的初始状态**：图中左下角有一个婴儿形象，旁边是电影胶片样式的图像序列（带紫色虚线），这代表了传统的“世界学习者”可能从连续的视觉观察（如视频帧）中学习，但这种学习是碎片化、任务驱动的（比如只关注下一个帧或下一个动作）。
- **传统任务的流程**：从左到右，绿色的框（标注“This is a fridge”）代表**语义理解**（Next Token Prediction），即识别物体（如冰箱）的语义；蓝色的框代表**视觉动态预测**（Next Frame Prediction），即预测下一个视觉帧的内容（如图中人物或物体的移动）；再往右的蓝色框代表**动作可供性推理**（Next Action Prediction），即预测可以执行的动作（如在某个位置拿取物品）。这些任务都是“被动”的，因为它们围绕特定的任务目标（如token、帧、动作）展开，而不是对整个世界的状态进行统一建模。

### 中间到右侧：Orca的核心——统一世界潜变量学习（“Active World Learner”）
- **“Active World Learner”的核心目标**：图的中间到右侧是Orca的目标——**Next State Prediction（下一个状态预测，世界建模）**。这里的“状态”是多模态的（包含视觉、语言、动作等世界的不同方面），模型试图学习一个统一的“世界潜变量空间”，来表示世界的状态及其转移。
- **两种学习范式**：
  - **无意识学习（Unconscious learning）**：由箭头和文字说明“Natural physical laws (e.g. Wind blows leaves fall)”表示。这部分对应从连续视频中捕获**密集的自然状态转移**（如物理规律驱动的事件，风导致树叶落下）。图中右侧的树木和落叶（或类似的自然场景）是这种学习的视觉体现——模型从连续的视觉观察（如长时间视频）中学习自然发生的状态变化，不需要显式的语言指导，是“无意识”的（类似人类通过观察世界自动学习物理规律）。
  - **有意识学习（Conscious learning）**：由箭头和文字说明“Meaningful causal events (e.g. Ice cream melts when heated)”表示。这部分对应通过**语言描述的事件和VQA（视觉问答）监督**来建模**稀疏但有意义的状态转移**（如加热导致冰淇淋融化这类因果事件）。图中被圈出的人物（或特定场景）可能代表语言或事件驱动的学习目标——模型通过语言指令、事件描述（如“加热冰淇淋”）来学习有意义的因果关系，这是“有意识”的（类似人类通过语言和意图理解世界的因果）。

### 数据流动与模型运作方式
1. **输入数据**：模型接收多模态的世界信号，包括连续的视频（用于无意识学习）和语言描述的事件、VQA注释（用于有意识学习）。图中左侧的电影胶片（视频帧序列）代表视频输入，右侧的语言相关描述（如“加热冰淇淋”“风与树叶”）代表语言/事件输入。
2. **学习过程**：
   - 无意识学习：从连续视频中提取密集的状态转移（如物体位置、外观的变化，物理规律的体现），并将这些信息编码到统一的世界潜变量空间中。
   - 有意识学习：从语言描述的事件中提取稀疏但有意义的因果状态转移（如“加热”导致“融化”的状态变化），并将这些信息也编码到同一个世界潜变量空间中。
3. **输出（下游读出）**：学习到的世界潜变量空间支持**下游读出（downstream readouts）**，包括文本生成（语言模态）、图像预测（视觉模态）、具身动作生成（动作模态）。图中没有直接画出下游任务，但根据论文摘要，这些读出是通过轻量级的模态特定解码器实现的（骨干网络冻结，只训练解码器），验证了统一世界潜变量的有效性。

### 方法的核心逻辑总结
Orca的核心是**从被动任务驱动的预测（关注token、帧、动作）转向主动的世界状态预测**，通过**无意识学习（从连续视频学自然动态）**和**有意识学习（从语言/事件学因果动态）**两种互补范式，学习一个**统一的多模态世界潜变量空间**。这个潜变量空间能够支持下游的语言生成、图像预测、动作生成等任务，从而实现对世界的理解、预测和交互。与传统的碎片化任务驱动模型不同，Orca试图构建一个“世界在心中”的统一模型，让模型像人类一样，从多模态的观察中学习世界的整体规律，而不是仅仅优化单个任务的预测性能。

这张图清晰地展示了Orca相对于传统模型的优势：它不是围绕单个任务（如下一个token、下一个帧）设计，而是围绕“下一个状态”的统一预测，通过两种学习范式捕获世界的密集和稀疏动态，最终支持多模态的下游任务。

---

![Figure 5 : Loss of model and data scaling.](fig5_1.webp)

> Figure 5 : Loss of model and data scaling.

这张图（图5）的标题是“Loss of model and data scaling”，它清晰地展示了模型规模与预训练数据量对总损失（Total Loss）的影响。我们可以通过以下几个部分来详细理解这张图：

### 图的组成部分：
1. **横轴（X轴）**：标记为“Pre-Training Data (Hours)”，表示预训练数据的时长，单位是小时。数据从0小时开始，一直延伸到8000小时，代表随着预训练数据量的增加，模型的学习过程。
2. **纵轴（Y轴）**：标记为“Total Loss”，表示模型在预训练过程中的总损失值。损失值越低，通常意味着模型的性能越好，因为它在预测或学习任务上的误差更小。
3. **两条曲线**：
    - **绿色曲线**：代表模型规模为0.8B（8亿参数）的情况。这条曲线显示了在预训练数据量增加时，0.8B模型的总损失变化情况。
    - **紫色曲线**：代表模型规模为4B（40亿参数）的情况。这条曲线显示了在相同预训练数据量下，4B模型的总损失变化情况。
4. **图例**：位于图的右上角，用不同颜色的点和线区分了两条曲线所代表的模型规模。

### 数据或信息的流动顺序：
- 随着横轴上预训练数据时长的增加（从左到右），我们观察到两条曲线的总损失值都在逐渐下降。这表明，无论是0.8B还是4B的模型，在更多的预训练数据支持下，其性能都在提升，即损失值降低。
- 对比两条曲线，我们可以看到，在相同的预训练数据量下，4B模型的总损失值始终低于0.8B模型。这说明模型规模的增大有助于提高模型的性能，即使在相同的预训练数据量下，更大的模型也能取得更低的损失值。

### 方法的运作方式：
这张图揭示了Orca模型在预训练阶段的运作方式。Orca通过两种互补的学习范式进行预训练：
1. **无意识学习**：从连续视频中捕获密集的自然状态转换。
2. **有意识学习**：通过语言描述的事件和VQA（视觉问答）监督来建模稀疏的有意义状态转换。

在这张图中，我们看到随着预训练数据量的增加，模型的总损失值逐渐降低，这表明Orca的预训练方法是有效的。模型规模的增大也有助于提高性能，因为更大的模型能够处理更复杂的状态转换和学习任务。

### 结论：
从图中可以看出，随着预训练数据量的增加，无论是0.8B还是4B的模型，其总损失值都在逐渐降低。此外，在相同的预训练数据量下，4B模型的总损失值始终低于0.8B模型。这表明，模型规模的增大和预训练数据量的增加都有助于提高Orca模型的性能。这些结果验证了Orca作为一般世界基础模型的有效性，以及其在理解和预测世界方面的潜力。
