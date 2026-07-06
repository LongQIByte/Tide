# ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving

[arXiv](https://arxiv.org/abs/2607.00466) · [HuggingFace](https://huggingface.co/papers/2607.00466) · ▲24

## 摘要（原文）

> In prefill-decode (PD) disaggregated LLM serving, each request is assigned to a decode worker after prefill. Existing decode routers balance only load; for mixture-of-experts (MoE) models this is incomplete: equally loaded workers can differ in latency, since each decode step loads the weights of every distinct expert its batch activates. We present ELDR, an expert-locality-aware decode router for PD-disaggregated MoE serving. From a request's prefill expert activations, ELDR builds an expert signature predicting the experts it will activate during generation. Offline, balanced K-means partitions signature space across decode workers; online, locality-band routing sends each request to the least-loaded worker among those best matching its signature. A signature cache, co-indexed with the KV cache at KV-block granularity, keeps signatures exact under prefix caching. Implemented in vLLM and evaluated on deployments of up to 40 GPUs, ELDR reduces median TPOT by 5.9-13.9% over the strongest of four load-balancing baselines across three MoE models and two workloads, with model outputs unchanged.

## 摘要（中译）

在预填充 - 解码（prefill - decode，PD）分解式大型语言模型（LLM）服务中，每个请求在预填充后会被分配给一个解码工作器。现有的解码路由器仅平衡负载；对于混合专家（mixture - of - experts，MoE）模型来说，这是不完整的：负载相同的工作器在延迟上可能不同，因为每个解码步骤会加载其批次激活的每个不同专家的权重。我们提出了ELDR，一种用于PD - 分解式MoE服务的专家局部性感知解码路由器。从请求的预填充专家激活中，ELDR构建一个专家签名，以预测其在生成过程中将激活的专家。在离线状态下，平衡的K - 均值算法将签名空间划分到各个解码工作器上；在线状态下，局部性带路由将每个请求发送到与其签名最匹配且负载最轻的工作器。一个签名缓存，与键值（KV）缓存在KV块粒度上共同索引，在前缀缓存下保持签名的准确性。ELDR在vLLM中实现，并在最多40个GPU的部署上进行评估，在三个MoE模型和两种工作负载中，与四个负载平衡基线中最强的那个相比，ELDR将中位数TPOT（可能是某种性能指标，保留英文）降低了5.9 - 13.9%，且模型输出不变。

## 背景剖析

### 背景剖析  

#### 1. 技术背景与需求  
大型语言模型（LLM）的部署正转向**预填充-解码（PD）解聚架构**，即将“提示处理”（预填充）和“令牌生成”（解码）分离到不同的工作节点池中。这种架构的挑战在于：预填充是并行计算密集型任务，而解码是串行且延迟敏感的任务。若将两者共置，长预填充会阻塞解码，导致“首令牌时间”（TTFT）和“每输出令牌时间”（TPOT）变长。因此，PD解聚需要高效的**路由机制**——预填充完成后，请求需被分配到合适的解码节点以生成后续令牌。  

对于**混合专家（MoE）模型**，传统负载均衡方法存在缺陷。MoE的解码是内存带宽瓶颈，其延迟由每个批次激活的**专家集合的大小**决定（而非令牌数量）。例如，若两个请求共享解码节点，但激活的专家不同，延迟可能差异显著。然而，现有方法仅关注负载均衡，忽略了专家激活的**局部性**（即相关请求倾向于激活相似的专家区域，如代码、医学等任务）。  

#### 2. 之前的问题  
传统路由方法的局限性在于：  
- **负载均衡不足**：仅平衡计算负载，但MoE的延迟由专家集合决定，负载相同的节点可能因专家集合不同而有显著延迟差异。  
- **忽视专家局部性**：未利用MoE专家激活的结构性（如同一领域的请求激活相似专家），导致专家集合碎片化，增加内存访问开销。  
- **前缀缓存不兼容**：前缀缓存（用于跳过重复提示的预填充）会破坏专家签名，现有方法无法在缓存命中时保持路由准确性。  

#### 3. 本文的解法  
论文提出**ELDR（Expert-Locality-Aware Decode Routing）**，通过以下思路解决问题：  
- **专家签名与局部性感知路由**：从预填充阶段的专家激活生成**专家签名**，离线用平衡K-means将签名空间划分为多个区域（每个区域对应一个解码节点），在线路由时选择与请求签名最相似且负载最低的节点。  
- **前缀缓存兼容性**：维护与KV缓存对齐的**块级专家签名缓存**，在缓存命中时恢复完整签名，确保路由准确性。  
- **双目标优化**：同时满足专家局部性（通过签名聚类）和实时负载均衡（通过在线选择最低负载节点）。  

#### 4. 切入角度的关键差异  
ELDR与前人工作的核心区别在于：  
- **关注专家局部性**：首次将MoE专家激活的结构性（如领域相关性）作为路由依据，而非仅依赖负载。  
- **离线-在线分离设计**：离线通过K-means捕获专家局部性结构，在线通过局部性带（locality band）平衡结构与实时负载。  
- **缓存感知路由**：通过块级签名缓存解决前缀缓存与路由的冲突，而传统方法未考虑这一场景。  

ELDR在vLLM中实现，仅需修改路由层，保持模型输出不变，显著降低了TPOT（最高达13.9%），适用于从几十亿到数百亿参数的MoE模型。

## 方法图解

![Figure 6. ELDR architecture: offline fitting of one centroid per decode worker o](fig6_1.webp)

> Figure 6. ELDR architecture: offline fitting of one centroid per decode worker over expert signatures, then online routing at the prefill?밺ecode handoff by signature similarity, subject to load.

这张图展示了论文《ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving》中提出的ELDR架构。该架构主要分为离线（OFFLINE）和在线（ONLINE）两个阶段，旨在解决预填充-解码（PD）解聚的混合专家（MoE）模型服务中的解码路由问题。

**离线阶段（OFFLINE - once / deployment）：**
这个阶段在系统部署时只执行一次。
*   **Calibration Signatures（校准签名）：** 首先，系统会收集或生成一组“校准签名”。这些签名代表了不同请求在预填充或解码阶段可能激活的专家模式。
*   **balanced K-means（平衡K均值）：** 然后，使用“平衡K均值”算法对这些校准签名进行处理。这个算法的目标是将签名空间划分为K个簇（centroids），并且确保每个簇的负载（例如，专家数量或计算量）尽可能均衡。结果是得到K个“Centroids（质心）”，每个解码worker对应一个质心。这意味着每个解码worker被分配了一组特定的专家，这些专家的激活模式在签名空间中是相似的。

**在线阶段（ONLINE - per request）：**
这个阶段针对每个服务请求都会执行。
*   **Client（客户端）：** 用户请求从客户端发出。
*   **ELDR Router（ELDR路由器）：** 客户端的请求首先到达ELDR路由器。路由器负责决定将请求发送到哪个解码worker。
    *   **请求流程（箭头方向）：**
        1.  客户端发送`request`给ELDR路由器。
        2.  ELDR路由器需要做出路由决策。
    *   **Prefill × x signature cache（预填充签名缓存 × x）：** 这是一个缓存层，存储了之前请求在预填充阶段的专家激活签名。它与KV缓存（Key-Value cache）在KV块粒度上是共索引的，这有助于在Prefix caching（前缀缓存）机制下保持签名的准确性。图中标号1和2指向这个缓存。
    *   **expert signature（专家签名）：** ELDR路由器会根据当前请求的信息（可能结合预填充签名缓存中的信息）构建一个“专家签名”。这个签名预测了该请求在生成阶段（decode）会激活哪些专家。图中标号3表示这个专家签名。
    *   **locality-band routing（局部性带路由）：** 路由器使用“局部性带路由”策略。它会找到与当前请求的专家签名最相似的那些解码worker（即，这些worker对应的质心与请求签名距离最近）。然后，在这些匹配度最高的worker中，选择一个当前负载最轻的worker来处理该请求。图中标号4表示这个路由过程，并且文字说明“one centroid per decoder”（每个解码器一个质心）。
    *   **Decode × y centroid c_k each（解码 × y，每个质心c_k）：** 这代表了多个解码worker，每个worker都关联一个质心（centroid c_k）。请求最终会被发送到其中一个解码worker。图中标号4的箭头指向这些解码worker。
    *   **KV transfer（KV传输）：** 在请求被路由到解码worker后，可能会涉及到KV缓存的传输。图中标号5表示这个KV传输过程，通常是从预填充阶段或之前的处理步骤将KV缓存数据传递给解码worker。

**方法运作方式总结：**
1.  **离线准备：** 系统预先计算并存储K个均衡的专家签名质心，每个解码worker对应一个。
2.  **在线路由：**
    *   当一个新请求到达时，ELDR路由器首先获取或构建该请求的专家签名。
    *   然后，它查找与这个签名最相似的质心（即最可能处理类似专家激活模式的解码worker）。
    *   在这些候选worker中，选择一个当前负载最轻的，以实现更好的负载均衡和潜在的更低延迟。
    *   请求被路由到选定的解码worker进行处理。
    *   预填充签名缓存的存在有助于快速生成准确的专家签名，特别是在有前缀缓存的情况下。

这张图清晰地展示了ELDR如何通过结合专家签名的相似性和负载均衡来实现更智能的解码路由，从而优化PD解聚MoE模型的服务性能。

**图中看不清或不确定的地方：**
*   具体的“balanced K-means”是如何确保负载均衡的细节。
*   “expert signature”的具体构建方法。
*   “KV transfer”的具体内容和时机。
*   图中的“x”和“y”代表什么，虽然可以推测是预填充和解码worker的数量。

---

![Figure 7. Signature quality ρ \rho (Eq. 1 ) for six candidate transformations T ](fig7_1.webp)

> Figure 7. Signature quality ρ \rho (Eq. 1 ) for six candidate transformations T T . Bars are the mean across six cells (3 models × \times 2 workloads); whiskers span the per-cell min/max.

这张图展示了六种候选变换（T）在计算“签名质量ρ”（Signature quality ρ）时的表现。这里的“签名质量ρ”是论文中提出的一个指标（见公式1），用于衡量某种变换在生成专家签名时的有效性。

图中的每个垂直条形代表一种特定的变换，从左到右依次是：`count:idf`、`count`、`√count`、`gate prob`、`gate logit` 和 `binary`。这些是论文中考虑的六种不同的专家激活模式变换方式，用于构建专家签名。

每个条形的高度表示该变换在所有测试场景下的平均签名质量ρ。例如，`count:idf` 变换的平均签名质量最高，约为0.76；而 `binary` 变换的平均签名质量最低，约为0.47。条形上方的数字是该变换的平均值，而条形顶部的误差线（whiskers）则表示该方法在六个不同测试单元（3个模型 × 2个工作负载）中的最小值和最大值范围。例如，`count:idf` 的误差线显示其性能在不同单元间相对稳定，而其他变换如 `gate prob` 的误差线则更长，表明其性能波动较大。

这张图揭示了方法的运作方式：为了实现专家局部性感知的解码路由（expert-locality-aware decode routing），需要从请求的预填充（prefill）专家激活中构建一个专家签名，以预测其在生成阶段将激活哪些专家。图中比较了六种不同的变换方法，这些方法用于处理预填充阶段的专家激活数据，以生成更有效的签名。通过比较这些变换的签名质量ρ，可以评估哪种变换能更好地捕捉专家激活的模式，从而为后续的路由决策提供更准确的信息。结果表明，`count:idf` 变换在生成高质量签名方面表现最佳，这意味着它能更准确地预测专家激活，进而可能帮助ELDR方法更有效地进行解码路由，减少延迟并提高系统性能。

总结来说，这张图通过比较六种不同的变换方法的签名质量，展示了哪种变换在构建专家签名方面更有效。结果是 `count:idf` 变换在所有测试场景下表现最好，而 `binary` 变换表现最差。这为论文中提出的ELDR方法选择合适的变换提供了实证依据。

---

![Figure 10. ELDR stores expert signatures at KV cache block granularity: the sign](fig10_1.webp)

> Figure 10. ELDR stores expert signatures at KV cache block granularity: the signature cache is co-indexed with KV cache.

这张图（图10）清晰地展示了ELDR（Expert-Locality-Aware Decode Routing）方法中专家签名（Expert Signature）如何在KV缓存（KV Cache）的块粒度（block granularity）上进行存储和管理。

首先，我们来看图的结构和各个组件：

1.  **顶部区域**：分为两部分，“Prefix Cache Hit”（前缀缓存命中）和“Computed”（计算得到）。这表示请求中的token可能来自两种来源：一部分是之前计算并缓存的（前缀缓存命中），另一部分是需要当前计算的。

2.  **KV Cache（键值缓存）**：这是LLM推理中常见的组件，用于存储之前计算过的键（key）和值（value）。图中显示了四个KV缓存块，分别对应token “Translate”（块ID 0）、“to French:”（块ID 1）、“Good”（块ID 2）和“morning”（块ID 3）。这些块代表了请求处理过程中不同阶段的缓存内容。

3.  **Block ID（块ID）**：位于KV Cache下方，为每个KV缓存块分配一个唯一的标识符（0, 1, 2, 3）。这使得系统能够索引和管理不同的缓存块。

4.  **Signature Cache（签名缓存）**：位于KV Cache下方，与KV Cache“共索引”（co-indexed）。这意味着对于每个KV缓存块（如块ID 0, 1, 2, 3），都有一个对应的签名缓存条目。图中用柱状图表示这些签名，不同的柱状图颜色（灰色和蓝色）可能区分了不同类型或来源的签名，但核心是每个KV块都有一个与之关联的签名。

5.  **数据流和运作机制**：
    *   **前缀缓存命中（Prefix Cache Hit）**：当处理请求时，如果某个token（如“Translate”和“to French:”）已经在KV缓存中（即前缀缓存命中），那么它的对应签名（块ID 0和1下方的灰色柱状图）也已经存在于签名缓存中。这意味着系统可以直接从缓存中获取这些token的专家签名，而无需重新计算。
    *   **计算得到（Computed）**：对于当前步骤需要计算的token（如“Good”和“morning”），系统会计算它们的专家签名（块ID 2和3下方的蓝色柱状图），并将这些签名存储到签名缓存中，以便后续请求可能重用。
    *   **专家签名的聚合**：图中底部的“Σ₀₋₃”符号表示将所有相关的专家签名（从块ID 0到块ID 3）进行聚合（例如，求和或某种形式的组合），以生成一个最终的“Expert Signature”（专家签名）。这个专家签名代表了当前请求或当前生成步骤所涉及的专家的总体特征。

6.  **方法的核心思想**：
    *   **预测专家激活**：ELDR从请求的预填充（prefill）阶段的专家激活情况开始，构建一个专家签名，用以预测该请求在生成（decode）阶段将激活哪些专家。
    *   **签名缓存的作用**：签名缓存与KV缓存共索引，确保了当KV缓存中的数据被重用时（例如，由于前缀缓存命中），其对应的专家签名也能被快速检索，从而保持签名的准确性。这对于基于前缀缓存的优化至关重要，因为它允许系统在不重新计算的情况下利用之前的专家激活信息。
    *   **路由决策**：虽然图中没有直接展示路由过程，但这个专家签名的构建是ELDR路由策略的基础。在线上，系统会根据这个专家签名（或其预测）以及当前的负载情况，将请求路由到最适合的解码工作节点（decode worker），以实现专家局部性感知的负载均衡。

总结来说，这张图展示了ELDR如何通过在KV缓存块粒度上维护专家签名缓存，来支持其专家局部性感知的解码路由策略。通过将专家签名与KV缓存共索引，ELDR能够在利用前缀缓存的同时，有效地预测和管理专家的激活，从而优化MoE模型的解码性能。

这张图不是传统意义上的结果图，而是一个方法示意图，展示了ELDR中专家签名存储和管理的核心机制。它解释了数据（token及其对应的专家签名）如何在KV缓存和签名缓存之间流动和组织。

---

![Figure 8. Cumulative ρ \rho (Eq. 1 ) versus the number of layers kept under gree](fig8_1.webp)

> Figure 8. Cumulative ρ \rho (Eq. 1 ) versus the number of layers kept under greedy layer selection. One panel per model; task (blue) and language (orange) shown separately. The star marks the peak N ∗ N^{*} chosen by ELDR ’s offline fit.

这张图（图8）展示了在不同MoE模型下，累积ρ值随保留层数变化的曲线，用于说明ELDR方法中专家选择的依据。

首先，我们来看图的各个组成部分：

1.  **子图结构**：图中有三个子图，分别对应三个不同的MoE模型：Qwen3-30B-A3B、GPT-OSS-120B和Gemma-4-26B-A4B。每个子图独立展示了一个模型的结果。
2.  **坐标轴**：
    *   **X轴（横轴）**：标记为“Layers kept”，表示在贪婪层选择策略下保留的层数。这个数值从0开始，向右增加，代表了在选择专家时考虑的层数范围。
    *   **Y轴（纵轴）**：标记为“Cumulative ρ”，表示累积的ρ值（根据公式1定义）。ρ值衡量的是某种性能指标（如专家激活的局部性或相关性），其值范围从大约0.6到1.0。值越高，通常表示性能越好。
3.  **曲线和颜色**：
    *   每个子图中有两条曲线，一条蓝色，一条橙色。
    *   **蓝色曲线（Task）**：代表“任务”类型的工作负载或数据集。
    *   **橙色曲线（Language）**：代表“语言”类型的工作负载或数据集。
    *   这两条曲线展示了在不同保留层数下，任务和语言工作负载的累积ρ值变化趋势。
4.  **星形标记（Star）**：
    *   在每条曲线（蓝色和橙色）上都有一个星形标记。
    *   根据图的原始说明，这个星号标记了由ELDR的离线拟合所选择的峰值N*。这意味着，在所有可能的保留层数中，ELDR方法通过离线分析确定了一个最优的层数N*，在这个层数下，累积ρ值达到或接近最大值，从而可以用来指导专家的选择，以优化性能（如减少TPOT）。
5.  **数据流动和信息解读**：
    *   图的核心信息是展示不同保留层数对累积ρ值的影响。
    *   对于每个模型和每种工作负载类型（任务或语言），随着保留层数的增加，累积ρ值会先上升，达到一个峰值（由星号标记），然后可能趋于平稳或略有下降。
    *   ELDR方法利用这个特性，通过离线分析找到每个模型和工作负载类型的最佳保留层数N*。在在线服务时，ELDR会根据请求的专家签名（由预填充阶段的专家激活构建），选择最匹配该签名且负载最轻的解码工作器，并使用这个最优的N*来进行专家选择，以提高效率。

这张图揭示了ELDR方法的具体运作方式：

*   **离线分析阶段**：ELDR首先对每个模型和不同工作负载类型进行分析。它通过贪婪层选择策略，计算在不同保留层数下的累积ρ值。然后，它找到累积ρ值达到峰值的那个层数N*。这个N*就是图中星号标记的位置。这个过程是为了确定一个最优的层数，使得专家选择能够最大化某种性能指标（如专家激活的局部性）。
*   **在线路由阶段**：当有新的请求到达时，ELDR会基于请求的预填充专家激活构建一个专家签名。然后，它会将这个签名与预先划分好的专家签名空间（通过离线K-means聚类得到）进行匹配，找到最匹配的解码工作器。在这些匹配的工作器中，选择一个当前负载最轻的工作器。最后，使用离线分析得到的最优层数N*来在该工作器上进行专家选择。

结论：

*   图中显示，对于所有三个模型（Qwen3-30B-A3B、GPT-OSS-120B、Gemma-4-26B-A4B）和两种工作负载类型（任务和语言），累积ρ值随着保留层数的增加而变化，并存在一个明显的峰值（由星号标记）。
*   这个峰值对应的层数N*就是ELDR方法选择的最优层数，用于指导专家选择。
*   通过这种方式，ELDR能够利用专家激活的局部性，选择出最优的专家子集，从而提高解码效率，如在论文摘要中提到的减少中位数TPOT。

---

![Figure 2. MoE layer latency scales with active experts, not batch size (single M](fig2_1.webp)

> Figure 2. MoE layer latency scales with active experts, not batch size (single MoE layer, one MI300X).

这张图（图2）的核心信息是**展示Mixture-of-Experts (MoE) 层的延迟如何随“激活的专家数量”而非“批次大小（batch size）”变化**，且实验是在“单个MoE层、单块MI300X GPU”上进行的。我们可以从以下几个角度拆解这张图：

### 1. 坐标轴与子图结构
- **横轴（X轴）**：`Number of active experts`（激活的专家数量），范围从0到100左右，代表每个请求在生成阶段会激活的专家数量。
- **纵轴（Y轴）**：`MoE expert latency (ms)`（MoE专家延迟，单位毫秒），表示处理这些激活专家所需的延迟时间。
- **子图（a）、（b）、（c）**：分别对应三个不同的MoE模型：
  - (a) `Qwen3-30B-A3B`
  - (b) `GPT-OSS-120B`
  - (c) `Gemma-4-26B-A4B`
  每个子图都展示了同一模型下，不同批次大小（`B=32`、`B=64`、`B=128`）对应的延迟随激活专家数量的变化。

### 2. 数据系列（线条与标记）
- 图例中的三种颜色/标记分别代表不同的**批次大小（batch size）**：
  - 浅蓝色（`B=32`）：批次大小为32。
  - 中蓝色（`B=64`）：批次大小为64。
  - 深蓝色（`B=128`）：批次大小为128。
- 每条线上的点表示在特定“激活专家数量”下，对应批次大小的MoE延迟。例如，在子图(a)中，当激活专家数量为100时，`B=128`的延迟约为0.45 ms，而`B=32`的延迟略低（约0.35 ms？需结合具体刻度，但趋势更关键）。

### 3. 核心趋势与结论（从图中可观察到）
- **延迟随“激活专家数量”增加而上升**：在所有子图和所有批次大小下，随着激活专家数量的增加，MoE延迟呈上升趋势。这表明**激活的专家数量是影响MoE延迟的关键因素**。
- **批次大小的影响相对较小**：对比同一子图中不同批次大小的线（如子图(a)中`B=32`、`B=64`、`B=128`的线），它们的斜率（延迟随专家数量的增长速率）和整体趋势相似，只是绝对延迟值有差异。这说明**批次大小对延迟的影响远小于激活专家数量的影响**——即“延迟随激活专家数量变化，而非批次大小”。

### 4. 与论文方法的关联（理解这张图的作用）
这篇论文提出了`ELDR`（Expert-Locality-Aware Decode Router），用于PD-disaggregated MoE服务的解码路由优化。这张图的作用是**验证“激活专家数量是MoE延迟的关键驱动因素”这一假设**，为`ELDR`的设计提供依据：
- `ELDR`的核心思想是通过“专家签名（expert signature）”预测请求会激活哪些专家，从而将请求路由到“专家局部性匹配度高且负载低”的解码worker。
- 这张图的结果（延迟随激活专家数量变化）说明：**优化路由时，应优先考虑“激活专家数量”而非“批次大小”**——因为后者对延迟的影响较小，而前者是主要因素。这也解释了为什么`ELDR`需要关注“专家激活模式”（通过签名预测），而不是单纯的批次大小平衡。

### 5. 实验设置细节
- 实验环境：单个MoE层、单块MI300X GPU（“single MoE layer, one MI300X”）。
- 对比对象：虽然图中没有直接对比其他方法，但通过展示“激活专家数量 vs 延迟”的关系，为后续`ELDR`与其他负载均衡基线的对比提供了基础（论文摘要中提到`ELDR`减少了5.9-13.9%的TPOT）。

总结：这张图清晰地展示了**MoE延迟随“激活专家数量”增加而上升，且批次大小的影响相对次要**的规律。这一发现是`ELDR`方法设计的核心前提——因为`ELDR`需要针对“专家激活模式”进行路由优化，而不是单纯的批次大小平衡。
