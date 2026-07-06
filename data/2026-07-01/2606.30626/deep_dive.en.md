# DOPD: Dual On-policy Distillation

[arXiv](https://arxiv.org/abs/2606.30626) · [HuggingFace](https://huggingface.co/papers/2606.30626) · ▲99

## Abstract (verbatim)

> On-policy distillation (OPD) offers superior capacity transfer by supervising student-sampled trajectories with dense token-level signals. To furnish high-quality supervision sources and thereby elevate the performance frontier of distillation, an intuitive direction is to infuse privileged information to either teacher or student itself. However, this additional input induces a potential failure mode we dub privilege illusion: a pattern that conflates the transferable capability gap that students are meant to close, and the information asymmetry gap that can only be mimicked but never replicated. This issue is further amplified by the inherent non-uniformity of token-level supervision, where only a small subset of tokens carries pivotal capability-bearing signals. To this end, we propose DOPD, an advantage-aware dual distillation paradigm that dynamically routes token-level supervision between privileged teacher and privileged student policies based on their advantage gap and relative probabilities. Each token receives supervision of different strength, objective, and strategy from either teacher or student itself, which transfers credible capability while simultaneously receiving auxiliary signals, to alleviate privilege illusion. Extensive experiments on both large language model (LLM) and vision-language model (VLM) settings demonstrate that DOPD consistently outperforms Vanilla OPD and other counterparts. Further results on stability, robustness, continual learning, and out-of-distribution tasks validate its superiority.

## Background

**Background Analysis**

This research focuses on "policy distillation," a technique critical for transferring capabilities from a high-performing model (teacher) to a weaker one (student). Such methods are essential in AI for tasks like enabling large language models (LLMs) or vision-language models (VLMs) to pass complex reasoning or multimodal understanding abilities to smaller models, achieving cost-effective deployment. Real-world needs include improving small models' decision quality, reducing reliance on large-scale data, and maintaining task adaptability.

However, traditional distillation methods face significant limitations. Early "off-policy" approaches suffered from mismatches between data distributions and student behavior, reducing effectiveness. Subsequent "on-policy" distillation (OPD) improved this by having students generate trajectories and using teachers for token-level supervision, but introduced new bottlenecks: when teachers or students access "privileged information" (e.g., extra reasoning hints or structured annotations), students might overfit to these superficial advantages (termed "privilege illusion") rather than learning truly transferable abilities. More critically, existing methods apply uniform supervision to all tokens, ignoring value differences—few tokens carry core capability signals, while most may depend on privileged information, lowering supervision efficiency.

To address these issues, the paper proposes DOPD (Dual On-policy Distillation). Its core idea is dynamically distinguishing token supervision sources: for tokens where teachers show credible capability advantages, stronger teacher supervision transfers high-value abilities; for tokens dominated by privileged information or low capability, lighter supervision maintains stability and encourages exploration. This "advantage-aware" mechanism allocates supervision intensity, objectives, and strategies between teacher and student based on actual token value, reducing privilege illusion.

Compared to prior work, DOPD's key differences are: 1) It does not assume all tokens contribute equally to capability transfer but adjusts supervision based on token value; 2) It shifts privileged information use from "global enhancement" to "selective utilization," preventing over-reliance on untransferable information; 3) It balances capability transfer and exploration stability through dual supervision sources (teacher and student). Experiments show DOPD significantly outperforms traditional OPD in both LLM and VLM tasks, validating its effectiveness and generalizability.

## Method, Figure by Figure

![Figure 5 : Overview of our proposed DOPD.](fig5_1.webp)

> Figure 5 : Overview of our proposed DOPD.

This diagram illustrates the overall framework and workflow of the **Advantage-Aware Dual Distillation (DOPD)** method proposed in the paper *DOPD: Dual On-policy Distillation*, aiming to address the "privilege illusion" problem and enhance distillation performance.  

### Overall Structure and Information Flow:  
The diagram is divided into two parts:  
1. **Upper Part (Policy and Distillation Process):**  
   - **Left: Student Policy:** Starts with "Original Input," generating an output sequence \( y \sim \Pi_S(\cdot|x) \) through **On-policy Sampling**, where the student policy samples output \( y \) based on input \( x \).  
   - **Middle: Privileged Student Policy and Privileged Teacher Policy:** These policies take "Original Input + Privileged Input" as input, producing output probability distributions \( q_S = \Pi_S(y_n|x, p, y_{<n}) \) (privileged student policy) and \( q_T = \Pi_T(y_n|x, p, y_{<n}) \) (privileged teacher policy). The student policy’s output is passed to these privileged policies via arrows, with information exchange between the privileged policies (green and black arrows).  

2. **Lower Part (Privilege Advantage Gap and Conditional Distillation):**  
   - **Left: Predicted Probability:** Displays the predicted probability distributions (via bar charts) for different tokens from the student policy (blue) and privileged teacher policy (green). The **Privilege Advantage Gap** \( \mathcal{A} = |\ell_S - \ell_T| \) is then calculated, where \( \ell_S = \log \Pi_S(y_n|x, p, y_{<n}) \) (student policy’s log probability) and \( \ell_T = \log \Pi_T(y_n|x, p, y_{<n}) \) (privileged teacher policy’s log probability). This gap measures the token-level capability difference between the student and privileged teacher.  
   - **Right: Condition and Distillation:** Based on changes in \( \mathcal{A} \) (rising or falling) and the relative strengths of the student policy \( \Pi_S \) and teacher policy \( \Pi_T \) (e.g., Light, Weak, Deep), different distillation strategies (e.g., \( q_S \uparrow q_T \uparrow \), \( q_S \downarrow q_T \downarrow \)) are determined. For example, when \( \mathcal{A} \) falls and \( q_S \) and \( q_T \) rise, it corresponds to "Light \( \Pi_T \)"; when \( \mathcal{A} \) rises and \( q_S \) rises while \( q_T \) falls, it corresponds to "Light \( \Pi_S \)."  

### Method Operation:  
The core of DOPD is **advantage-aware dual distillation**, detailed as follows:  
1. **On-policy Sampling:** The student policy generates an output sequence via on-policy sampling based on the original input, serving as the source of supervision signals.  
2. **Privileged Policies Introduction:** Privileged student and teacher policies are introduced, with inputs containing privileged information to generate more accurate output probability distributions using additional data.  
3. **Privilege Advantage Gap Calculation:** The privilege advantage gap \( \mathcal{A} \) is computed by comparing the log probabilities of each token from the student and privileged teacher policies, reflecting their token-level capability differences.  
4. **Dynamic Distillation Strategy Selection:** Distillation strategies are dynamically chosen based on changes in \( \mathcal{A} \) and the relative strengths of the student and teacher policies. For different tokens, supervision signals of varying intensities, targets, and strategies are received from the privileged teacher, privileged student, or self, based on their \( \mathcal{A} \) and policy strength. This transfers credible capabilities while receiving auxiliary signals, mitigating the "privilege illusion"—avoiding confusion between the transferable capability gap students need to narrow and the information asymmetry gap that can only be imitated, not replicated.  

### Implicit Results:  
Although experimental results are not directly shown, the paper’s abstract indicates DOPD consistently outperforms Vanilla OPD and other baselines in large language model (LLM) and vision-language model (VLM) settings, with further positive results in stability, robustness, and continual learning. This shows DOPD effectively enhances distillation performance and resolves the privilege illusion.  

In summary, DOPD uses an advantage-aware dual distillation mechanism to dynamically leverage information from privileged student and teacher policies, adjusting distillation strategies based on token-level advantages and policy strengths. This transfers capabilities while mitigating the privilege illusion, improving distillation effectiveness.

---

![Figure 2 : Comparison of existing (a) standard distillation, (b) self distillati](fig2_1.webp)

> Figure 2 : Comparison of existing (a) standard distillation, (b) self distillation, and (c) adaptive distillation paradigms with our proposed (d) dual distillation paradigm.

This figure (Figure 2) clearly compares several existing knowledge distillation paradigms with our proposed Dual On-policy Distillation (DOPD) paradigm. Let's analyze each subplot:

*   **(a) Standard Distillation**:
    *   **Components & Flow**: At the top is the "Student Policy," with four circles below it representing outputs or states generated by the student policy. At the bottom is the "Teacher Policy," also with four circles. Green arrows point from the Teacher Policy to the circles of the Student Policy, indicating that information or supervision signals flow from the teacher to the student. This represents traditional knowledge distillation, where the student imitates the teacher's behavior or output.

*   **(b) Self Distillation**:
    *   **Components & Flow**: At the top is the "Student Policy." At the bottom is the "Privileged Student Policy." Blue arrows point from the Privileged Student Policy to the circles of the Student Policy, indicating that supervision signals originate from a "privileged" version of the student itself. The term "privileged" here might imply that this student policy possesses more or better information.

*   **(c) Adaptive Distillation**:
    *   **Components & Flow**: At the top is the "Student Policy," and at the bottom is the "Teacher Policy." The arrows are a mix of green and light green, pointing from the Teacher Policy to the circles of the Student Policy. This suggests a more flexible supervision method, possibly adjusting the teacher's influence on the student dynamically based on certain conditions or signal strengths.

*   **(d) Dual Distillation (Ours)**:
    *   **Components & Flow**: This is our proposed method. At the top is the "Student Policy." At the bottom left is the "Privileged Student Policy," and at the bottom right is the "Privileged Teacher Policy." There are two types of arrows:
        *   Blue arrows point from the "Privileged Student Policy" to certain circles of the "Student Policy."
        *   Green arrows point from the "Privileged Teacher Policy" to other circles of the "Student Policy."
        *   Additionally, there is a bidirectional arrow connecting the "Privileged Student Policy" and the "Privileged Teacher Policy," indicating some form of interaction or information exchange between them.
    *   **Method Operation**: This figure reveals the core idea of the DOPD method. It does not solely rely on supervision signals from the teacher or the student itself. Instead, it dynamically allocates token-level supervision between the "Privileged Teacher Policy" and the "Privileged Student Policy." Specifically, each token (or state) will receive supervision of different strength, objective, and strategy from either the teacher or the student, based on their "advantage gap" and "relative probabilities." This means that for some critical tokens, the student might rely more on the teacher's guidance; for others, it might use its own privileged information, or a combination of both. This dynamic routing mechanism aims to mitigate the "privilege illusion" problem, which is the confusion between the actual capability gap that students need to close and the information asymmetry gap that can only be mimicked but not truly replicated.

In summary, this figure effectively contrasts four different distillation paradigms, highlighting the dual and dynamic nature of our proposed DOPD method. It shows how more effective capability transfer and improved distillation performance can be achieved by simultaneously leveraging both privileged teacher and student policies and dynamically adjusting the supervision source based on specific circumstances.

---

![(a) Performance Gain vs. Teacher-student Size Ratio (b) Gap Reduction vs. Teache](fig6_1.webp)

> (a) Performance Gain vs. Teacher-student Size Ratio (b) Gap Reduction vs. Teacher-student Size Ratio Figure 6 : Scalability comparison of proposed DOPD and Vanilla OPD on (a) performance gain and (b) teacher-student gap reduction ratio. Here, the solid and dashed lines represent the 0.6B and 1.7B student policy, respectively.

This figure (Figure 6a) from the paper "DOPD: Dual On-policy Distillation" illustrates the scalability comparison between the proposed DOPD method and Vanilla OPD in terms of "Performance Gain" across different "Teacher-student Size Ratios."

Let's break down the components of the graph:

1.  **Axes**:
    *   **X-axis (Horizontal)**: Labeled "Size Ratio," this represents the "Teacher-student Model Size Ratio." The ticks (e.g., 4B, 5, 8B, 10, 15) likely refer to the parameter scale of the models (e.g., a 4B-parameter teacher model compared to a 1.7B or 0.6B-parameter student model). This ratio indicates the relative size of the student model compared to the teacher model.
    *   **Y-axis (Vertical)**: Labeled "Performance Gain," this measures the improvement in performance achieved by the student model through the distillation process. Higher values indicate greater performance enhancement.

2.  **Data Series and Legend**:
    *   **Gray dots and solid line**: Represent "Vanilla OPD" (the original, unmodified On-policy Distillation method).
    *   **Green dots and dashed line**: Represent "DOPD (Ours)" (the new method proposed in the paper).
    *   Annotations like "4B ↓ 1.7B" and "8B ↓ 0.6B" next to the data points clarify the "Size Ratio." For instance, "4B ↓ 1.7B" means the teacher model has 4B parameters and the student model has 1.7B parameters; "8B ↓ 0.6B" means the teacher has 8B parameters and the student has 0.6B parameters. These annotations help interpret the performance under different teacher-student size combinations.

3.  **Data Points and Trends**:
    *   **For Vanilla OPD (gray series)**:
        *   When the teacher is 4B and the student is 1.7B, the performance gain is approximately +4.9.
        *   When the teacher is 4B and the student is 0.6B, the performance gain is approximately +5.5.
        *   As the teacher-student ratio increases (e.g., teacher 8B, student 0.6B with +4.7; teacher 8B, student 0.6B with +3.5), the performance gain of Vanilla OPD shows a decreasing trend. This suggests that the original OPD method becomes less effective at transferring knowledge when the student model is significantly smaller than the teacher.

    *   **For DOPD (Ours) (green series)**:
        *   When the teacher is 4B and the student is 1.7B, the performance gain is approximately +11.1.
        *   When the teacher is 1.7B and the student is 0.6B (interpreting the flow), the performance gain is approximately +11.9.
        *   When the teacher is 8B and the student is 1.7B, the performance gain is approximately +12.3.
        *   When the teacher is 4B and the student is 0.6B, the performance gain is approximately +13.7.
        *   When the teacher is 8B and the student is 0.6B, the performance gain reaches +14.1.
        *   The performance gain of DOPD is consistently much higher than that of Vanilla OPD across all tested size ratios. Moreover, its performance gain appears relatively stable or even slightly increases with larger size ratios, indicating that DOPD is more effective at leveraging the teacher's knowledge, even when the student model is small.

4.  **Revealing Method Operation**:
    *   The graph demonstrates how DOPD outperforms Vanilla OPD in terms of performance gain. By comparing the two methods across different teacher-student size ratios, it's evident that DOPD achieves more effective knowledge transfer from the teacher to the student.
    *   The paper states that DOPD is an "advantage-aware dual distillation paradigm" that dynamically routes token-level supervision between a privileged teacher and a privileged student policy based on their "advantage gap" and "relative probabilities."
    *   Specifically, each token receives supervision of different strength, objective, and strategy from either the teacher or the student itself. This approach ensures credible capability transfer while providing auxiliary signals, thereby alleviating the "privilege illusion" problem. Privilege illusion refers to the conflation of the capability gap students need to close with the information asymmetry gap that can only be mimicked but not truly replicated.
    *   Therefore, DOPD's dynamic routing mechanism ensures more effective knowledge transfer, especially for resource-constrained student models, leading to higher performance gains.

5.  **Conclusion**:
    *   The figure clearly shows that DOPD's performance gain is significantly higher than Vanilla OPD across various teacher-student size ratios.
    *   This indicates that DOPD is more effective at model distillation, particularly when the student model is much smaller than the teacher.
    *   The graph supports the paper's argument that DOPD, through its unique dual distillation and dynamic routing mechanisms, overcomes the limitations of Vanilla OPD and advances the performance frontier.

In summary, this figure visually compares the performance of DOPD and Vanilla OPD under different teacher-student size ratios, clearly demonstrating the superiority of DOPD in model distillation tasks. It shows that DOPD can more effectively utilize the teacher model's knowledge, achieving significant performance improvements even when the student model has limited resources.

---

![(a) Performance vs. Training Step (b) Entropy vs. Training Step Figure 3 : Compa](fig3_1.webp)

> (a) Performance vs. Training Step (b) Entropy vs. Training Step Figure 3 : Comparison of (a) performance and (b) entropy on OPD variants with privileged information. Here, T., S., and Priv. denote teacher policy, student policy and with privileged information, respectively.

This figure (Figure 3a) illustrates the relationship between training steps (Step) and performance for different policy-based distillation methods, used to compare OPD variants with privileged information.  

First, let’s examine the axes:  
- The **x-axis** ("Step") ranges from 0 to 200, representing the progress of the training process.  
- The **y-axis** ("Performance") ranges from 35 to 45, measuring the model’s performance on a specific task.  

Next, the figure contains four curves, each representing a different method, distinguished by the legend:  
- **Black curve (T. → S.)**: Represents the "teacher policy to student policy" distillation method, where a teacher guides the student in a traditional manner.  
- **Blue curve (Priv. S. → S.)**: Represents the "privileged student policy to student policy" method, where the student learns independently with additional privileged information.  
- **Green curve (Priv. T. → S.)**: Represents the "privileged teacher policy to student policy" method, where the teacher guides the student while possessing privileged information.  
- **Gray curve (Priv. T. → Priv. S.)**: Represents the "privileged teacher policy to privileged student policy" method, where both the teacher and student have privileged information during distillation.  

Each point on the curves indicates the performance value at a specific training step, while the shaded areas around the curves likely represent the variance or confidence interval of the performance, showing the stability of different methods across steps.  

From the figure:  
- The **black curve (T. → S.)** shows a gradual increase in performance during training and maintains a high level in the later stages, indicating that the traditional teacher-guided student learning method performs well in terms of performance.  
- The **green curve (Priv. T. → S.)** also shows an increase in performance with more training steps but slightly decreases in the later stages, possibly due to instability introduced by privileged information.  
- The **blue curve (Priv. S. → S.)** initially rises in performance but gradually declines in the later stages, suggesting that learning solely with the student’s own privileged information may not be effective.  
- The **gray curve (Priv. T. → Priv. S.)** remains relatively flat throughout the training process, with no significant upward or downward trend, possibly because the presence of privileged information for both the teacher and student limits performance improvement.  

This figure reveals how the performance of different methods changes during training, helping us understand how privileged information-based distillation methods operate and their advantages and disadvantages. By comparing these curves, we can conclude that the traditional teacher-guided student learning method (T. → S.) performs best in terms of performance, while methods with privileged information require further optimization to improve both performance and stability.

---

![(a) Performance vs. Training Step (b) Entropy vs. Training Step Figure 8 : Train](fig8_1.webp)

> (a) Performance vs. Training Step (b) Entropy vs. Training Step Figure 8 : Training stability comparison of proposed DOPD and representative baselines, reporting the (a) performance and (b) entropy trends over training steps on LiveBench.

This figure (Figure 8a) illustrates a **training stability comparison** of different methods on the LiveBench benchmark, specifically by showing the **performance trends over training steps**.  

### Key Components of the Figure:  
1. **Axes**:  
   - **X-axis (Horizontal)**: Represents "Step" (training steps), ranging from 0 to 200. This indicates the progress of training.  
   - **Y-axis (Vertical)**: Represents "Performance," with values ranging approximately from 35 to over 50. This measures the model’s performance on LiveBench tasks.  

2. **Curves and Legend**:  
   The figure includes four main curves, each representing a different method, distinguished by color and markers. The legend clearly identifies each curve:  
   - **Gray curve (a) Standard**: Represents the "standard" or baseline method.  
   - **Red curve (b) Self**: Represents the "self" or baseline method.  
   - **Blue curve (c) Adaptive**: Represents the "adaptive" or baseline method.  
   - **Green curve (d) Dual (Ours)**: Represents the proposed method, "Dual (Our method)."  

3. **Data Points and Trends**:  
   Each curve is formed by connecting data points that represent the average performance measured at specific training steps (e.g., 0, 40, 80, 120, 160, 200). The overall trend of each curve shows how performance changes as training progresses. A semi-transparent shaded area around each curve typically indicates the variance or confidence interval of the performance, reflecting the volatility of the results.  

4. **Information Flow and Interpretation**:  
   The core message of this figure is to display the learning curves of different methods during training. Readers can compare these methods by observing the speed of performance improvement, the final performance level achieved, and the stability of the performance (i.e., the width of the shaded area).  

### Analysis of Method Performance and Behavior:  
- **Purpose of Comparison**: The figure aims to compare the proposed "Dual (Ours)" method with three baseline methods (Standard, Self, Adaptive) in terms of training stability. Training stability can be judged by the speed of performance improvement, the level of final performance, and the magnitude of performance fluctuations.  

- **How Methods Work (Inferred from Results)**:  
  Although the figure does not directly show the mechanisms of the methods, we can infer from the paper’s abstract and the results:  
  - **Dual (Ours) Method** (green curve): Performs the best among all methods. Its performance increases rapidly in the early training stages and continues to maintain a high level, eventually approaching a performance value of 50. The shaded area is relatively narrow, indicating low performance volatility and a stable training process. This suggests that the Dual method effectively utilizes its proposed "advantage-aware dual distillation paradigm," dynamically allocating token-level supervision between privileged teacher and student strategies, thereby mitigating the "privileged hallucination" problem and achieving more stable and higher performance.  
  - **Adaptive Method** (blue curve): Performs second-best, with final performance slightly lower than the Dual method but still showing good stability and high final performance.  
  - **Standard Method** (gray curve): Shows a more gradual performance increase, with final performance lower than both Dual and Adaptive methods.  
  - **Self Method** (red curve): Performs the worst, with the lowest final performance and significant performance fluctuations (wider shaded area), indicating poor training stability.  

- **Conclusion**:  
  The figure clearly concludes that on the LiveBench benchmark, the proposed **Dual (Ours) method significantly outperforms other representative baseline methods (including Standard, Self, Adaptive) in both training stability and final performance**. Its performance curve is higher and smoother, indicating that this method trains more effectively and achieves a higher performance level. This aligns with the conclusion in the paper’s abstract that "DOPD consistently outperforms Vanilla OPD and other counterparts," although this figure specifically focuses on training stability comparison on LiveBench.  

In summary, this figure intuitively compares the training stability and final performance of different methods by showing their performance changes over training steps, strongly supporting the superiority of the proposed Dual method.
