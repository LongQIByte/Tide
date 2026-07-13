# Dual Latent Memory in Vision-Language-Action Models for Robotic Manipulation

[arXiv](https://arxiv.org/abs/2607.07608) · [HuggingFace](https://huggingface.co/papers/2607.07608) · ▲51

## 摘要（原文）

> Mainstream Vision-Language-Action (VLA) models predict actions primarily from the current observation under a Markovian assumption, thus struggling with long-horizon, temporally dependent tasks. Existing memory-augmented VLAs either expand the observation window or retrieve history from the memory bank as auxiliary policy-side context. However, they leave memory outside the native latent embedding space of VLA reasoning, preventing historical experience from being fluidly interleaved with multimodal reasoning and action formation. To this end, we introduce LaMem-VLA, a latent-memory-native framework that reconstructs historical experience into latent memory tokens and directly interweaves them with VLA reasoning. At its core, LaMem-VLA introduces four coordinated components: (i) a curator that organizes historical experience into two complementary short-term and long-term memory vaults; (ii) a seeker that queries both vaults using the multimodal cognition to retrieve context-relevant evidence; (iii) a condenser that reconstructs the retrieved evidence into compact short-term and long-term latent memory tokens; and (iv) a weaver that injects these memory tokens with the current observation and instruction into one continuous embedding sequence. By representing, retrieving, and consuming historical experience entirely in the same continuous latent space, LaMem-VLA enables memory to directly participate in VLA reasoning and guide action generation under a bounded context. Extensive experiments on SimplerEnv and LIBERO demonstrate the superiority of our LaMem-VLA.

## 摘要（中译）

主流视觉-语言-动作（Vision-Language-Action, VLA）模型主要在马尔可夫假设下从当前观测中预测动作，因此在长期规划、时间依赖型任务中表现不佳。现有的增强记忆的VLA模型要么扩展观测窗口，要么从记忆库中检索历史作为辅助策略上下文。然而，它们将记忆置于VLA推理的原生潜在嵌入空间之外，导致历史经验无法与多模态推理和动作生成流畅地交织在一起。为此，我们提出了LaMem-VLA，一种原生潜在记忆框架，它将历史经验重构为潜在记忆令牌，并直接将它们与VLA推理交织在一起。其核心是四个协调组件：（i）一个管理者，将历史经验组织成两个互补的短期和长期记忆库；（ii）一个搜索器，使用多模态认知查询两个库以检索与上下文相关的证据；（iii）一个压缩器，将检索到的证据重构为紧凑的短期和长期潜在记忆令牌；（iv）一个编织器，将这些记忆令牌与当前观测和指令一起注入到一个连续的嵌入序列中。通过在相同的连续潜在空间中表示、检索和使用历史经验，LaMem-VLA使记忆能够直接参与VLA推理并在有限上下文中指导动作生成。在SimplerEnv和LIBERO上的大量实验证明了我们的LaMem-VLA的优越性。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
视觉-语言-动作（VLA）模型是机器人操作领域的核心技术，旨在让机器人通过理解视觉场景和语言指令来执行复杂任务（如组装、搬运）。这类技术的核心需求是让机器人具备**长时程任务能力**——例如，在“将桌子上的苹果放入冰箱”的任务中，机器人需要记住已完成的步骤（如“拿起苹果”）、当前状态（如“冰箱门是否打开”），并规划后续动作。然而，现有VLA模型大多假设“当前观察足以预测动作”（即马尔可夫性），导致它们在需要**历史依赖的复杂任务**中表现不佳，例如多步骤装配或动态环境中的适应性操作。  

**2. 之前的问题与局限**  
早期改进尝试通过两种方式引入记忆机制：  
- **短期窗口扩展**：将历史帧拼接或延长输入序列，但计算成本随时间窗口增长，且无法处理超出窗口的长时依赖。  
- **外部记忆库**：从外部存储中检索历史轨迹或token，但这些记忆与模型内部推理分离，导致历史信息无法与当前感知、语言理解直接交互。  
这两种方法的核心缺陷是**记忆与推理的脱节**：历史经验未被整合到模型的原生嵌入空间中，无法自然参与视觉-语言-动作的联合推理过程。  

**3. 本文的解决思路**  
论文提出LaMem-VLA框架，通过**原生潜伏记忆**（latent memory）将历史经验直接融入模型推理。其核心设计包括：  
- **双尺度记忆库**：短期记忆存储当前任务的视觉细节（如物体位置），长期记忆保存语义信息（如任务进度）。  
- **统一嵌入空间**：历史记忆被压缩为与模型原生嵌入兼容的token，与当前观察、语言指令共同参与推理。  
- **动态检索与编织**：模型根据当前状态动态查询相关历史，并将记忆token“编织”到推理序列中，使历史信息直接影响动作生成。  

**4. 与前人工作的关键差异**  
与以往方法不同，LaMem-VLA的关键创新在于**记忆的内生性**：  
- 历史记忆不再作为外部辅助上下文，而是与视觉-语言推理共享同一嵌入空间，实现“感知-理解-记忆-动作”的端到端融合。  
- 双尺度记忆设计同时支持视觉主导的短期细节和语义主导的长期上下文，解决了单一记忆机制的局限性。  
这一设计使机器人能够像人类一样，通过“回忆相关经验”来指导复杂任务的执行，而非仅依赖当前观察做出反应。

## 方法图解

![Figure 2: The Framework of LaMem-VLA . Given an instruction and the current obse](fig2_1.webp)

> Figure 2: The Framework of LaMem-VLA . Given an instruction and the current observation, the vision–language encoder first encodes the inputs into a multimodal representation. The memory curator (§ 3.3 ) organizes historical experience into dual memory vaults, and the memory seeker (§ 3.4 ) then retrieves task-relevant evidence from dual memory vaults based on this multimodal representation. This retrieved evidence is compressed into fixed-length latent memory tokens by the memory condenser (§ 3.4 ). Finally, the memory weaver (§ 3.5 ) injects these latent memory tokens into the reasoning sequence, producing memory-grounded action tokens that guide the action expert to generate future action chunks.

这张图展示了LaMem - VLA（一种用于机器人操作的视觉 - 语言 - 动作模型）的框架，我们可以从左到右、按数据流动的顺序来理解每个组件的作用和方法的运作流程：

首先看最左侧的“Robotic manipulation Task”部分：这里有一个指令\( I \)（比如“pick up the black bowl and place it on the plant”），还有一系列的观测 - 动作对\( <o_1,a_1>, <o_2,a_2>, \dots, <o_t,a_t> \)，这些构成了机器人操作任务的历史经验和当前任务的输入。然后这些输入会被处理成“Hidden States”中的三种token：视觉token（蓝色方块）、指令token（绿色方块）和动作token（紫色方块），其中视觉token对应短期记忆库的键（Short - Term Vault Key，带斜线的蓝色方块），动作token等对应短期记忆库的值（Short - Term Vault Value，实心蓝色方块）。

接下来是中间的“Dual - scale Latent Memory Synthesis”部分，它包含三个子组件：
1. **Memory Curator（记忆管理者）**：它的作用是组织历史经验到两个互补的记忆库中。一个是“Short - term vault (visual evidence)”（短期库，视觉证据），这里存储的是键 - 值对（Key - value pairs），键是带斜线的蓝色方块（对应视觉token），值是实心蓝色方块；另一个是“Long - term vault (semantic evidence)”（长期库，语义证据），这里存储的是动作token（\( a_1, a_2, \dots, a_t \)），还有一些辅助的符号如milestones（里程碑）、progress（进度）、goals（目标）、semantics（语义）来表示长期记忆的语义信息。
2. **Memory Seeker（记忆检索者）**：它根据当前的“Multimodal Cognition (visual + instruction)”（多模态认知，即视觉和指令的结合）来检索相关证据。首先，它会生成“Query tokens”（查询token，由眼睛、绿色方块等组成，代表当前的视觉和指令信息），然后用这个查询token分别从短期库和长期库中检索。从短期库检索时，会得到“Top - k”的相关键 - 值对（带斜线的蓝色方块和实心蓝色方块）；从长期库检索时，会得到“Top - k”的相关动作token（\( a_1, a_2, \dots, a_t \)中的部分）。
3. **Memory Condensor（记忆压缩器）**：它将检索到的证据压缩成固定长度的潜在记忆token。对于检索到的短期记忆，通过“Short - term Memory Condensor”（短期记忆压缩器，函数为\( \mathbb{R}^{KN\times C} \to \mathbb{R}^{L\times C} \)）将其压缩；对于检索到的长期记忆，通过“Long - term Memory Condensor”（长期记忆压缩器，同样的函数）将其压缩，得到压缩后的短期和长期潜在记忆token（带斜线的方块和实心方块）。

然后看最右侧的“Latent Memory Weaver（潜在记忆编织者）”部分：这里的“Large Language Model”（大语言模型）会接收来自记忆压缩器的潜在记忆token（短期和长期的，分别用橙色和紫色框表示）、当前的multimodal tokens（多模态token，包括视觉、指令、认知等，用不同颜色方块表示）和action tokens（动作token，紫色方块），然后将这些token交织成一个连续的嵌入序列。这个序列会被“Action Expert”（动作专家）处理，最终生成“Future action chunk”（未来的动作块，即一系列的观测 - 动作对，如\( <o_1,a_1>, \dots > \)）。

整个方法的运作流程是：首先，机器人操作任务的指令和历史观测 - 动作对被编码成多模态表示（视觉、指令、动作token）；然后，记忆管理者将这些历史经验组织到短期（视觉证据）和长期（语义证据）记忆库中；接着，记忆检索者根据当前的多模态认知从这两个库中检索相关证据；之后，记忆压缩器将检索到的证据压缩成固定长度的潜在记忆token；最后，记忆编织者将这些潜在记忆token与当前的多模态token和动作token交织，输入到动作专家中，生成未来的动作块。这样，历史经验就被完全整合到VLA推理的连续潜在空间中，使得记忆能够直接参与推理并指导动作生成，解决了现有模型在长 horizon、时间依赖任务中的不足。

总结来说，LaMem - VLA通过四个协调的组件（管理者、检索者、压缩者、编织者），将历史经验重构为潜在记忆token，并直接将其与VLA推理交织，从而在有限的上下文下实现基于记忆的动作生成。

---

![Figure 1: Paradigm comparison of memory-augmented VLA Models. (a) Unlike previou](fig1_1.webp)

> Figure 1: Paradigm comparison of memory-augmented VLA Models. (a) Unlike previous VLA models that store historical experience in an auxiliary memory bank and consume retrieved memory as external policy-side context, (b) LaMem-VLA treats historical experience as context-native latent memory, which is stored, retrieved, and consumed in the model embedding space.

这张图（图1）对比了两种视觉-语言-动作（VLA）模型的范式：(a) 之前的检索记忆型VLA模型，以及(b) 本文提出的LaMem-VLA模型。它清晰地展示了两种方法在处理历史经验（记忆）与当前任务推理和动作生成方面的根本区别。

首先看(a)部分，标题为“Previous retrieved-memory VLA”（之前的检索记忆型VLA）：
- 数据流从左到右。最左边是两个输入源：“Instruction”（指令，如图标所示，可能是一段文本或任务描述）和“Observation”（观察，如图标所示，可能是图像或传感器数据）。这两个输入共同进入“VLA Backbone (Reasoning)”模块（VLA主干网络，负责推理）。
- 此外，还有一个独立的“Retrieved Experience”（检索到的经验）模块，它通过一个橙色的箭头指向“Action Head”（动作头）。这个橙色箭头上有一个红色的“X”标记，并且旁边有一个警告标志，文字说明是“Historical Memory is separated from native VLA reasoning”（历史记忆与原生VLA推理是分离的）。这意味着，在这种方法中，历史经验并不是直接整合到VLA的推理过程中，而是作为一个外部辅助信息，在推理之后或并行地提供给动作生成模块。
- “VLA Backbone (Reasoning)”的输出流向“Action Head”，最终产生一个动作（由右侧困惑表情的机器人图标表示，暗示这种方法可能效果不佳或存在问题）。
- 总结来说，这种方法将历史经验存储在外部记忆库中，检索后作为外部策略上下文使用，与VLA的核心推理过程是分离的。

接下来看(b)部分，标题为“LaMem-VLA (Ours)”（我们的LaMem-VLA模型）：
- 数据流同样从左到右。最左边的输入源也是“Instruction”和“Observation”，它们进入“VLA Backbone (Reasoning)”模块。
- 关键的区别在于历史经验的处理方式。这里有两个新的模块：“Short-term visual memory”（短期视觉记忆，如图标所示，可能代表近期感知）和“Long-term visual memory”（长期视觉记忆，如图标所示，可能代表过往经验）。这两个记忆模块的输出流向一个“Latent memory tokens”（潜在记忆令牌）模块。
- “Latent memory tokens”模块的输出，通过一个标注为“Latent injection”（潜在注入）的绿色箭头，直接注入到“VLA Backbone (Reasoning)”模块中。图中还展示了一个示例，其中几个潜在令牌（z^(1), z^(2), ..., z^(n)）被注入到一个连续的嵌入序列中（由浅棕色区域和绿色点表示）。
- “VLA Backbone (Reasoning)”的输出流向“Action Head”，最终产生一个动作（由右侧带灯泡的开心表情机器人图标表示，暗示这种方法更有效或更智能）。
- 右侧的文字说明是“Historical memory is represented as context-native robotic memory.”（历史记忆被表示为上下文原生的机器人记忆）。这意味着，在LaMem-VLA中，历史经验被重构为潜在记忆令牌，并直接交织在VLA的推理过程中，共享同一个连续的潜在空间。
- 总结来说，LaMem-VLA的方法是：将历史经验组织成短期和长期视觉记忆，然后将这些记忆重构为紧凑的潜在记忆令牌，并将这些令牌与当前的观察和指令一起注入到VLA的主干网络中，使得历史经验能够直接参与VLA的推理和动作生成。

这张图揭示了LaMem-VLA方法的具体运作方式：
1.  **记忆组织**：使用“curator”（管理者）将历史经验组织成互补的短期和长期视觉记忆库。
2.  **记忆检索**：使用“seeker”（查询器）根据多模态认知（当前指令和观察）查询这两个记忆库，以检索与上下文相关的证据。
3.  **记忆压缩**：使用“condenser”（压缩器）将检索到的证据重构为紧凑的短期和长期潜在记忆令牌。
4.  **记忆注入**：使用“weaver”（编织器）将这些潜在记忆令牌与当前的观察和指令一起注入到一个连续的嵌入序列中，供VLA主干网络进行推理。
通过这种方式，LaMem-VLA使得历史经验能够在同一个连续的潜在空间中被表示、检索和使用，从而允许记忆直接参与VLA推理，并在有限的上下文内指导动作生成。

图中的箭头表示数据和信息的流动方向。例如，在(a)中，指令和观察流向VLA主干，而检索到的经验则独立地流向动作头。在(b)中，指令和观察流向VLA主干，同时短期和长期视觉记忆生成的潜在记忆令牌也注入到VLA主干中。
