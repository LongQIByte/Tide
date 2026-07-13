# Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling

[arXiv](https://arxiv.org/abs/2607.02980) · [HuggingFace](https://huggingface.co/papers/2607.02980) · ▲68

## 摘要（原文）

> Scaling modern large language models (LLMs) to long contexts is limited by the quadratic computation cost, and poor length extrapolation of dense attention. Chunk-wise sparse attention offers a promising alternative, but all existing methods fall short of full attention because of their inaccurate chunk selection. We propose Hierarchical Landmark Sparse (HiLS) Attention, a chunk-wise sparse attention mechanism that learns chunk selection end-to-end under the language-modeling (LM) loss. HiLS factorizes attention hierarchically: each query performs attention independently with each retrieved chunk to extract chunk-specific information, and the resulting outputs are fused according to chunk retrieval scores. By incorporating retrieval scores into the forward attention computation, HiLS optimizes them directly with the LM loss, enabling end-to-end retrieval learning and native sparse training. Experimental results show that HiLS-Attention achieves performance comparable to, and in some cases better than, full attention at in-domain context lengths. Meanwhile, HiLS-Attention extrapolates more than 64times the training context length with 90% retrieval accuracy, far beyond full attention. Moreover, existing full-attention models can be converted to HiLS-Attention with lightweight continued pretraining, preserving in-domain performance while acquiring ultra-long-context extrapolation. Together with its sparse KV access and computation, HiLS-Attention breaks the usual efficiency-performance trade-off, enabling long-context LLMs that are both more efficient and more effective on general long-context tasks than their full-attention counterparts.

## 摘要（中译）

将现代大型语言模型（LLMs）扩展到长上下文受到二次计算成本和密集注意力的长度外推能力差的限制。分块稀疏注意力提供了一种有前途的替代方案，但所有现有方法由于不准确的分块选择而无法达到完全注意力。我们提出了分层地标稀疏（HiLS）注意力，这是一种分块稀疏注意力机制，它在语言建模（LM）损失下端到端地学习分块选择。HiLS分层分解注意力：每个查询独立地与每个检索到的分块进行注意力以提取分块特定信息，并且根据分块检索分数融合得到的输出。通过将检索分数纳入前向注意力计算，HiLS直接使用LM损失优化它们，实现端到端检索学习和原生稀疏训练。实验结果表明，HiLS-Attention在领域内上下文长度上实现了与完全注意力相当的性能，在某些情况下甚至更好。同时，HiLS-Attention可以外推超过训练上下文长度的64倍，检索准确率为90%，远远超过完全注意力。此外，现有的完全注意力模型可以通过轻量级的继续预训练转换为HiLS-Attention，保留领域内性能，同时获得超长上下文外推。结合其稀疏KV访问和计算，HiLS-Attention打破了通常的效率-性能权衡，使得长上下文LLMs在一般长上下文任务上比其完全注意力对应物更高效且更有效。

## 背景剖析

### 背景剖析  

**1. 技术背景**  
现代大语言模型（LLMs）需要处理越来越长的文本上下文，例如长文档理解、多轮对话或复杂推理任务。然而，传统“全注意力”机制的计算成本随文本长度平方增长，导致长文本处理效率低下，且难以准确预测超出训练长度的内容（即“长度外推”问题）。为此，研究者提出“分块稀疏注意力”，通过选择性关注相关文本块来降低计算量，但现有方法在性能上仍无法媲美全注意力。  

**2. 之前的问题**  
现有分块方法的核心缺陷在于“块选择不准确”。例如，简单的均值池化等非参数方法无法充分表达文本块的重要性，而参数化方法虽然更灵活，但其选择的块信息在训练中未被直接优化，导致模型难以区分相关与无关内容。此外，这些方法通常需要额外的计算步骤（如硬阈值筛选），无法与全注意力一样高效学习。  

**3. 本文的解法**  
本文提出“分层地标稀疏注意力”（HiLS-Attention），通过两步解决上述问题：首先，为每个文本块添加一个“地标标记”，生成更具表达力的块摘要；其次，将块选择过程与语言模型的训练目标（如预测下一个词）直接关联，使模型能自动学习哪些块更重要。这种方法避免了全注意力的高计算成本，同时通过端到端优化提高了块选择的准确性。  

**4. 切入角度**  
与传统方法不同，HiLS-Attention的关键创新在于将“块选择”转化为可学习的注意力权重，并利用全注意力的数学特性（如泰勒展开近似）来指导块摘要的设计。实验表明，这种方法不仅在常规长度任务中表现优异，还能将上下文长度扩展至训练长度的64倍以上，远超现有方法。

## 方法图解

![Figure 3 : An overview of HiLS-Attention. We omit the scaling factor 1 d \frac{1](fig3_1.webp)

> Figure 3 : An overview of HiLS-Attention. We omit the scaling factor 1 d \frac{1}{\sqrt{d}} for simplicity. Naive block sparse attention selects the top- K K chunks by their exact mass Z c Z_{c} , e.g., chunks 1 and 3 when K = 2 K=2 , but computing all Z c Z_{c} requires a full QK computation. HiLS-Attention instead uses compressed chunk keys k c ′ k^{\prime}_{c} to efficiently estimate a chunk-mass surrogate Z c ′ ∝ exp ⁡ ( q ⊤ ​ k c ′ ) Z^{\prime}_{c}\propto\exp(q^{\top}k^{\prime}_{c}) . It factorizes attention into two stages: an inter-chunk softmax , which specifies the total attention mass assigned to each chunk, and an intra-chunk softmax , which distributes each chunk’s attention mass among its tokens. Since Z c ′ Z^{\prime}_{c} parameterizes the forward attention weights, gradients from the next-token prediction loss can be directly backpropagated to the compressed key k c ′ k^{\prime}_{c} , enabling end-to-end learning.

这张图（图3）概述了**HiLS-Attention**（分层地标稀疏注意力）的核心机制，并将其与“朴素块稀疏注意力”进行了对比，以展示HiLS-Attention的优势和工作流程。我们按从上到下、从左到右的顺序来解析图中的各个部分：

首先，图的顶部展示了一个序列的抽象表示，被分成了多个“块”（chunk），如T₁, T₂, T₃, ..., T_c。每个块包含若干“令牌”（token）。图例解释了不同颜色和样式的方块代表的含义：
*   **浅蓝色方块**：远距离令牌（Distant token）
*   **浅绿色方块**：相邻令牌（Adjacent token）
*   **深蓝色虚线方块**：地标令牌（Landmark token）
*   **深绿色方块**：当前令牌（Current token）
*   **T_c**：表示第c个块中的令牌。
*   **c(j)**：表示令牌j所属的块的索引。

1.  **朴素块稀疏注意力 (Naïve Block Sparse Attention)**：
    *   这部分展示了传统方法如何选择块。它选择了“质量”（mass）最高的K个块（图中示例K=2，选择了块1和块3，用对勾标记）。这里的“质量”Z_c是通过计算查询q与块c中所有地标令牌k'_j的点积的softmax得到的，即 Z_c = Σ_{j∈T_c} exp(q^⊤ k'_j)。然后，注意力权重w_j是根据这些Z_c进行归一化的。
    *   数据流：查询q与每个块的地标令牌k'_j进行交互，计算出每个块的总质量Z_c。然后，对于某个当前令牌x_j（图中为浅蓝色方块），其注意力权重w_j是基于其所在块的质量Z_c(j)以及所有选中块的总质量（如图中的Z₁ + Z₃ + Z_swa）进行归一化的。
    *   这种方法的缺点是计算所有Z_c需要完整的QK（查询-键）计算，这在计算上可能很昂贵。

2.  **HiLS-注意力 (HiLS-Attention)**：
    *   这部分展示了HiLS-Attention的核心思想，它通过两步softmax来分解注意力：
        *   **块间softmax (inter-chunk softmax)**：这一步决定了分配给每个块的总注意力“质量”。它使用压缩的块键k'_c来高效估计块质量代理Z'_c，其中Z'_c ∝ exp(q^⊤ k'_c)。这意味着不需要计算完整的QK来得到Z_c，而是通过一个更高效的估计Z'_c来代替。图中显示查询q与每个块的地标令牌k'_c进行交互（例如，与块1的地标令牌K₁和块3的地标令牌k'_3交互），并通过某种方式（如图中的饼图所示）计算出每个块的相对重要性。
        *   **块内softmax (intra-chunk softmax)**：对于每个被选中的块，这一步将分配给该块的注意力质量在其内部令牌之间进行分配。图中显示，对于块1（浅蓝色令牌），查询q与该块内的所有令牌（通过q^⊤ K₁表示）进行交互，然后通过一个softmax（如图中的橙色条形图所示）来计算块内各个令牌的注意力权重。
    *   数据流：首先，查询q与每个块的地标令牌k'_c进行交互，估计每个块的注意力质量代理Z'_c。然后，根据这些Z'_c进行块间softmax，确定每个块应获得的注意力份额。接着，对于每个块，查询q与该块内的所有令牌进行交互，并通过块内softmax在该块内部分配注意力。最终的注意力权重w_j是块间注意力份额（Z'_{c(j)} / (Z'₁ + Z'₃ + Z_swa)）与块内注意力权重（exp(q^⊤ k_j) / Z_{c(j)}）的乘积。
    *   关键创新点：Z'_c参数化了前向注意力权重，因此来自下一个令牌预测损失的梯度可以直接反向传播到压缩键k'_c，从而实现端到端的学习。

3.  **等价条件 (Equivalent when:)**：
    *   图的右侧指出，当Z'_c = Z_c时，HiLS-Attention的计算与朴素块稀疏注意力的计算是等价的。这意味着HiLS-Attention在理论上可以恢复到传统方法，但其优势在于Z'_c是一个高效的估计，不需要完整的QK计算。

总结来说，这张图展示了HiLS-Attention如何通过分层的方式（先在块之间分配注意力，再在块内部分配注意力）来实现稀疏注意力。它通过使用压缩的块键来高效估计块质量，从而避免了传统方法中计算完整QK的高昂成本，并且能够实现端到端的优化。这种方法使得HiLS-Attention能够在保持性能的同时，处理更长的上下文。

这张图揭示了HiLS-Attention的具体运作方式：
*   它首先将输入序列分成多个块。
*   对于每个块，它使用一个或多个地标令牌来生成一个压缩的键k'_c。
*   查询q与这些压缩键k'_c进行交互，以估计每个块的注意力质量代理Z'_c。
*   通过块间softmax，根据这些Z'_c确定每个块应获得的注意力份额。
*   对于每个块，查询q与该块内的所有令牌进行交互，并通过块内softmax在该块内部分配注意力。
*   最终的注意力权重是块间和块内注意力的乘积。
*   由于Z'_c直接参与注意力权重的计算，因此可以端到端地学习这些压缩键k'_c。

---

![(a) NSA kernel (b) HiLS-Attention kernel Figure 4 : Kernel design of NSA and HiL](fig4_1.webp)

> (a) NSA kernel (b) HiLS-Attention kernel Figure 4 : Kernel design of NSA and HiLS-Attention. Kernel design of NSA and HiLS-Attention. (a) NSA handles one query token per tile and computes attention over its selected chunks. Each Tensor Core operation has shape ( G , d ) × ( d , S ) (G,d)\times(d,S) , where G G is the GQA group size and S S is the chunk size. (b) HiLS-Attention packs M M adjacent query tokens, attends to the union of their selected chunks, and enlarges the Tensor Core operation to ( M × G , d ) × ( d , S ) (M\times G,d)\times(d,S) . This packing reuses overlapping K/V chunks across adjacent tokens.

这张图展示了HiLS - Attention的核设计，我们按数据流动和组件功能来拆解：

### 组件与数据流动
1. **输入部分**：
    - 左侧的\( Q \)（形状为\( L \times h \times d \)）是查询（Query）张量，这里通过“Grid Loop”（网格循环）处理不同的查询组（图中蓝色的多层结构可能代表不同的查询块或组）。\( L \)是序列长度，\( h \)是注意力头数，\( d \)是特征维度。
    - 上方的“selected K”（选择的键，形状为\( L \times d \)）是经过选择后的键（Key）张量，“Inner Loop”（内循环）处理这些键的选择逻辑，绿色块代表被选中的键部分。
    - 右侧的\( V \)（形状为\( L \times d \)）是值（Value）张量，“Inner Loop”也处理值的选择，绿色块代表被选中的值部分。
2. **计算核心（Tensor Core操作）**：
    - 图中绿色的菱形（形状为\( G \times d \)，\( G \)是GQA组大小）代表查询的分组处理，它会被送到Tensor Core进行计算。Tensor Core的操作形状是\( (G, d) \times (d, S) \)，其中\( S \)是块大小（chunk size）。这里的矩阵乘法（用\( \odot \)或矩阵乘符号表示）是注意力计算的核心：查询分组（\( G \times d \)）与键的选中部分（\( d \times S \)）相乘，然后和值的选中部分（\( d \times S \)）进行加权求和（注意力机制的分数加权）。
    - 箭头展示了数据的流向：查询分组从\( Q \)经过处理后进入Tensor Core，键和值的选中部分也从各自的张量中被选取后进入Tensor Core，计算结果（蓝色块）最终输出到\( O \)（输出张量，形状为\( L \times h \times d \)）。
3. **输出部分**：
    - 下方的\( O \)是输出张量，接收Tensor Core的计算结果，完成注意力机制的输出，之后会继续处理下一个查询组（通过“Grid Loop”）。

### 方法运作方式
HiLS - Attention的核心是**分块稀疏注意力**，结合了查询分组和块选择：
- 首先，对查询（\( Q \)）进行分组（图中\( G \)大小的组），每个查询组独立处理。
- 然后，从键（\( K \)）和值（\( V \)）中选择特定的块（“selected K”和“selected V”中的绿色块），这些块是根据学习到的策略选择的（论文中提到是端到端学习块选择）。
- 接着，在Tensor Core上进行矩阵乘法操作：查询分组（\( G \times d \)）与键的选中块（\( d \times S \)）相乘，得到注意力分数相关的中间结果，再与值的选中块（\( d \times S \)）相乘，得到每个查询组的输出。
- 最后，这些输出被融合（根据块检索分数，论文中提到将检索分数融入前向注意力计算），得到最终的输出张量\( O \)。

这种方法的优势在于：
- 利用分块稀疏性减少计算量（避免全注意力的二次方复杂度）。
- 端到端学习块选择，使得检索分数（块选择的结果）可以直接通过语言模型损失（LM loss）优化，从而实现更准确的块选择和更好的长上下文建模能力。

### 结果相关（结合论文）
虽然这张图主要是核设计（方法原理），但论文中的实验结果表明：
- HiLS - Attention在域内上下文长度上性能可与全注意力媲美，甚至在某些情况下更好。
- 它能外推超过训练上下文长度64倍的情况，且检索准确率达到90%，远超全注意力。
- 现有的全注意力模型可以通过轻量的继续预训练转换为HiLS - Attention，保留域内性能的同时获得超长上下文外推能力。

总结来说，这张图清晰地展示了HiLS - Attention如何通过分块、查询分组和Tensor Core优化计算，实现高效的稀疏注意力，解决长上下文建模的效率和长度外推问题。

---

![Figure 5 : Perplexity (a) and RULER accuracy (b) of the 1.4B model at different ](fig5_1.webp)

> Figure 5 : Perplexity (a) and RULER accuracy (b) of the 1.4B model at different training steps. Left: Full-Attention with RoPE; right: HiLS-Attention with HoPE. The annotated values on the curves correspond to the final checkpoint (143k steps), which is highlighted with star markers and thicker lines. The detailed per-step results are deferred to Appendix H (Tab. 15 & Tab. 16 ).

这张图（图5）来自论文《Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling》，它通过两个子图（a和b）展示了两种不同注意力机制（Full-Attention with RoPE 和 HiLS-Attention with HoPE）在1.4B参数模型上的性能表现，具体是困惑度（Perplexity）和RULER平均精确匹配率（RULER average exact match %），并且是在不同的训练步骤下进行的比较。

首先看子图（a），它展示了**困惑度（Perplexity）**随**上下文长度（Context Length，以对数刻度表示，单位为K，即千）**的变化情况，并且针对不同的**训练步骤（Steps，如20k、40k、…、143k步）**有不同的曲线。图中有左右两个子图（a的左和右），分别对应两种注意力机制：

- **左侧（Full-Attention RoPE）**：这是传统的完全注意力机制，结合了RoPE（Rotary Position Embedding）位置编码。横轴是上下文长度（从64到512K），纵轴是困惑度（数值越低表示模型在该上下文长度下的表现越好，因为困惑度衡量的是模型预测下一个token的不确定性，越低说明预测越准确）。不同的颜色/线型代表不同的训练步骤（图例中从20k到143k步，143k步的曲线用星号标记且线更粗，是最终的检查点）。我们可以看到，随着训练步骤的增加（从20k到143k），在训练长度（8K）附近，困惑度先降低后升高？不，仔细看，在8K之前，随着上下文长度增加（从64到8K），困惑度下降（比如20k步时，64的困惑度是26.17，8K时是4.02）；但在8K之后，当上下文长度超过训练长度（8K），比如到32K、128K、512K时，困惑度又上升了（比如20k步时，32K的困惑度是8.69，128K是37.07？不对，图中左侧的红色曲线，在8K之后，当上下文长度到32K时，困惑度是8.69？然后到128K时是37.07？而143k步的曲线（星号）在8K之后，比如32K时是4.08？哦，可能我看错了，重新看：左侧的图，横轴是64、128、512、8K、32K、128K、512K。纵轴是困惑度。不同的步骤，比如20k步（浅橙色），在64时是26.17，128时是20.05，512时是13.56，8K时是4.02，32K时是8.69，128K时是37.07，512K时是？而143k步（深红色，星号）在8K时是4.02？不，图中左侧的红色曲线，在8K之后，当上下文长度到32K时，困惑度是8.69？然后到128K时是37.07？而右侧的HiLS-Attention HoPE的图，横轴同样的长度，纵轴困惑度。比如20k步（浅蓝色）在64时是26.21，128时是20.03，512时是13.55，8K时是4.02，32K时是4.08，128K时是5.54，512K时是8.58。而143k步（深蓝色，星号）在8K时是4.08？不，图中右侧的曲线，在8K之后，困惑度上升的幅度比左侧小很多。这说明，传统的Full-Attention RoPE在上下文长度超过训练长度（8K）时，困惑度会显著上升，而HiLS-Attention HoPE的困惑度上升幅度小很多，说明HiLS在长上下文（超出训练长度）时的表现更好。

然后看子图（b），它展示了**RULER平均精确匹配率（%）**随**上下文长度（对数刻度，从8K到512K）**的变化情况，同样针对不同的训练步骤。RULER准确率衡量的是模型在给定上下文下精确匹配目标的能力，数值越高越好。

- **左侧（Full-Attention RoPE）**：横轴是上下文长度（8K、16K、32K、512K），纵轴是RULER准确率（%）。不同的训练步骤，比如20k步（浅红色），在8K时是96.7%，16K时是1.7%，32K时是1.0%，512K时是0.0%。而143k步（深红色，星号）在8K时是96.7%？不，图中左侧的曲线，在8K时，所有步骤的准确率都很高（接近96.7%），但当上下文长度超过训练长度（8K），比如16K、32K、512K时，准确率急剧下降，甚至到0%。这说明传统的Full-Attention RoPE在超出训练长度的上下文下，精确匹配能力几乎丧失。

- **右侧（HiLS-Attention HoPE）**：横轴同样的上下文长度，纵轴准确率。比如20k步（浅蓝色）在8K时是96.3%，16K时是91.7%，32K时是90.7%，128K时是88.7%，512K时是83.7%。而143k步（深蓝色，星号）在8K时是96.3%？不，图中右侧的曲线，在8K时准确率很高（接近96.3%），当上下文长度增加到16K、32K、128K、512K时，准确率缓慢下降，但仍然保持在80%以上（512K时是83.7%）。这说明HiLS-Attention HoPE在超出训练长度的上下文下，仍然能保持较高的精确匹配率，远优于传统的Full-Attention RoPE。

现在总结这张图的**方法和结果**：

- **方法**：论文提出了HiLS-Attention（Hierarchical Landmark Sparse Attention），这是一种分层的块稀疏注意力机制，通过端到端学习块选择（利用语言模型的损失直接优化检索分数），解决了传统密集注意力的二次计算成本和长上下文外推差的问题，以及现有稀疏注意力的不准确块选择问题。HiLS将注意力分层：每个查询独立地与每个检索到的块进行注意力计算以提取块特定信息，然后根据块检索分数融合这些输出。通过将检索分数纳入前向注意力计算，HiLS能够直接用语言模型损失优化它们，实现端到端的检索学习和原生稀疏训练。

- **结果（从图中得出）**：
  - **困惑度（图a）**：在训练长度（8K）内，两种方法的困惑度都随着训练步骤的增加而降低（模型收敛）。但当上下文长度超过训练长度（8K）时，Full-Attention RoPE的困惑度显著上升（比如在32K、128K、512K时，困惑度远高于HiLS-Attention HoPE），而HiLS-Attention HoPE的困惑度上升幅度很小，说明HiLS在长上下文（超出训练长度）时的困惑度更低，表现更好。
  - **RULER准确率（图b）**：在训练长度（8K）内，两种方法的准确率都很高（接近100%）。但当上下文长度超过训练长度（8K）时，Full-Attention RoPE的准确率急剧下降（甚至在32K、512K时接近0%），而HiLS-Attention HoPE的准确率虽然也下降，但下降幅度小得多（在512K时仍有83.7%的准确率），说明HiLS在长上下文外推时的精确匹配能力远优于传统的Full-Attention。

此外，图的原始caption提到，详细的每步结果在附录H的表15和表16中。图中看不到或不确定的地方按caption处理，比如具体的数值细节可以参考附录。

这张图清晰地展示了HiLS-Attention相对于传统Full-Attention在长上下文（尤其是超出训练长度的上下文）下的优势：更低的困惑度和更高的精确匹配率，验证了HiLS在解决长上下文建模问题上的有效性。

---

![(a) (b) (c) (d) Figure 1 : After only 50B continued-training tokens, HiLS-Attent](fig1_1.webp)

> (a) (b) (c) (d) Figure 1 : After only 50B continued-training tokens, HiLS-Attention inherits the capability of full attention while bringing two key advantages: strong ultra-long context extrapolation beyond the YaRN-extended 4 × \times length (Fig. 1(a) ) and faster inference (Fig. 1(b) ) . Meanwhile, it preserves comparable performance for short- and medium-context tasks, within both the original training length and the YaRN-extrapolated range (Fig. 1(c) & 1(d) ).

这张图（图1(a)）展示了两种模型在不同上下文长度下的RULER平均精确匹配率（即模型输出与参考答案完全匹配的比例），以此对比它们在长上下文外推任务中的表现。

首先，我们来看图的各个组成部分：

1.  **X轴（横轴）**：表示“Context length”（上下文长度），单位是token。从左到右，上下文长度从8K（8千个token）逐渐增加到1M（1百万个token）。这代表了模型需要处理的输入序列的长度。
2.  **Y轴（纵轴）**：表示“RULER average exact match (%)”（RULER平均精确匹配率，百分比）。这个指标衡量了模型输出与真实答案完全一致的样本比例，数值越高表示模型性能越好。从下到上，百分比从0%增加到100%。
3.  **两条曲线**：
    *   **蓝色实线（带圆点标记）**：代表“Olmo3-HiLS-Attn”模型，即应用了论文提出的Hierarchical Landmark Sparse (HiLS) Attention方法的模型。
    *   **灰色虚线（带方形标记）**：代表“Olmo3-CPT (YaRN)”模型，这可能是一个基线模型，例如使用了YaRN方法进行长上下文扩展的模型。
4.  **数据点和数值**：每条曲线上都有具体的数值标注，表示在特定上下文长度下的精确匹配率。例如，在8K的训练长度时，Olmo3-HiLS-Attn的匹配率为99.0%，而Olmo3-CPT (YaRN)也为99.0%（或接近，因为灰色虚线在8K处开始）。
5.  **阴影区域和标注**：在X轴的8K位置，有一个灰色的垂直阴影区域，并标注了“8K training length”（8K训练长度）。这表明模型可能在8K长度的上下文上进行了主要训练。
6.  **图例**：位于图的右侧，解释了两条曲线分别代表的模型。

接下来，我们分析这张图揭示的信息和方法的运作效果：

*   **训练长度内的表现**：在8K到32K的上下文长度范围内（即训练长度或其附近），两种模型的表现都非常好，精确匹配率都在95%以上，HiLS-Attn甚至接近100%。这说明HiLS-Attn模型在训练过的上下文长度范围内能够很好地继承全注意力模型的性能。
*   **长上下文外推能力**：当上下文长度超过32K，特别是远超训练长度（如64K、128K、256K、512K直至1M）时，两种模型的表现开始出现显著差异。
    *   **Olmo3-HiLS-Attn（蓝色曲线）**：尽管精确匹配率随着上下文长度的增加而逐渐下降（从32K的95.3%下降到1M的81.7%），但其下降趋势相对平缓。即使在1M（1百万）的极长上下文长度下，其精确匹配率仍然保持在81.7%，这表明HiLS-Attn具有很强的长上下文外推能力。
    *   **Olmo3-CPT (YaRN)（灰色虚线）**：在32K之后，其性能急剧下降。在64K时，匹配率已经降至约25%左右，随后在更长的上下文长度下几乎趋近于0%。这表明基线模型在长上下文外推方面表现不佳。
*   **方法的运作方式（从结果推断）**：
    *   HiLS-Attention通过分层稀疏注意力的方式解决了传统密集注意力在长上下文下的二次计算成本和较差的外推能力问题。
    *   图中的结果表明，HiLS-Attn能够在保持与全注意力模型相当的短/中长度任务性能的同时，实现远超训练长度的长上下文外推。具体来说，它能够外推超过64倍于训练长度（8K x 64 = 512K，而图中甚至达到了1M）的上下文，并且在1M长度时仍保持81.7%的匹配率，这远优于基线模型。
    *   这验证了HiLS-Attn的设计理念：通过端到端学习块选择（利用检索分数），并分层地进行注意力计算（查询独立地与每个检索到的块进行注意力交互，然后根据检索分数融合输出），从而优化了稀疏注意力的性能。

**结论**：
这张图清晰地展示了HiLS-Attention在长上下文建模方面的优势。它表明，经过少量的继续训练（如caption中提到的50B tokens），HiLS-Attention不仅能够继承全注意力模型的性能，还能在超长上下文外推方面取得显著优于基线模型的结果。具体来说，在训练长度（8K）到32K的范围内，两种模型表现相当；但在更长的上下文（如64K及以上）中，HiLS-Attn的精确匹配率远高于YaRN基线，证明了其强大的长上下文外推能力。例如，在1M的上下文长度下，HiLS-Attn的匹配率为81.7%，而基线模型几乎无法处理。这说明HiLS-Attention有效地解决了长上下文建模的挑战，实现了高效的超长上下文理解。

---

![Figure 7 : Chunk-id overlap among adjacent query tokens. Left: loaded union size](fig7_1.webp)

> Figure 7 : Chunk-id overlap among adjacent query tokens. Left: loaded union size for the final M = 16 M=16 queries versus the visible historical chunks; percentages denote loaded fractions. Right: normalized overlap as group size M M increases, with the dashed line showing inter-block reuse at M = 16 M=16 . Error bars show standard deviation across HiLS layers and heads, and shaded regions show the layer-wise min–max range.

这张图包含两个子图，分别从不同角度展示了HiLS-Attention中chunk-id的重叠情况，帮助我们理解其工作原理和性能。

首先看左边的子图(a)，标题为“Final-block KV loading”。这个子图的横轴是“Context length”（上下文长度），从4K到64K不等，表示输入序列的长度。纵轴是“Chunk ids (log scale)”（chunk的ID数量，对数刻度），表示加载的chunk的数量。图中有两条曲线：
- 灰色的虚线代表“Visible history chunks”（可见的历史chunk），它随着上下文长度的增加而线性增长，这表明随着输入序列变长，模型能“看到”的历史chunk数量也在增加。
- 蓝色的实线代表“Loaded union chunks”（加载的并集chunk），它的增长速度比灰色虚线慢很多。图中还标注了不同上下文长度下的“loaded fractions”（加载比例），例如在8K时是48.0%，16K时是31.9%，32K时是15.1%，64K时是9.9%。这说明随着上下文长度的增加，实际加载的chunk数量占可见历史chunk数量的比例在下降，也就是说，模型并没有加载所有的可见历史chunk，而是选择了一部分，这体现了稀疏注意力的特点，即只关注部分相关的chunk。

接下来看右边的子图(b)，标题为“Chunk-id overlap”。这个子图的横轴是“Grouped query tokens M”（分组查询token的数量），从2到64不等，表示将查询token分成的组大小。纵轴是“Overlap / reuse (%)”（重叠/重用比例），表示chunk-id的重叠比例。图中有两条曲线：
- 蓝色的实线代表“Chunk overlap”（chunk重叠），它随着M的增加而上升，从M=2时的约90%上升到M=64时的接近98%。图中还标注了M=16时的重叠比例为97.0%。
- 红色的虚线代表“M=16 block reuse (92.8%)”，这是当M=16时的块重用比例，作为对比。此外，图中还有误差线和阴影区域，误差线表示HiLS层和头之间的标准差，阴影区域表示层级的最小-最大范围，这说明不同层和头之间的重叠比例有一定的变化，但整体趋势是随着M的增加而上升。

从这两个子图中，我们可以看出HiLS-Attention的工作方式：
- 在图(a)中，随着上下文长度的增加，模型加载的chunk数量远小于可见的历史chunk数量，这说明HiLS-Attention通过选择部分相关的chunk来进行稀疏注意力计算，从而减少了计算量。
- 在图(b)中，随着分组查询token的数量M的增加，chunk-id的重叠比例也增加，这说明当查询token被分成更大的组时，它们所关注的chunk有更多的重叠，这有助于提高注意力的效率和效果。

总的来说，这张图展示了HiLS-Attention在chunk选择和重叠方面的性能，说明它能够通过稀疏选择chunk来减少计算量，同时保持较高的chunk重叠比例，从而实现高效的长期上下文建模。
