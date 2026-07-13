# Why Can't I Open My Drawer? Mitigating Object-Driven Shortcuts in Zero-Shot Compositional Action Recognition

[arXiv](https://arxiv.org/abs/2601.16211) · [HuggingFace](https://huggingface.co/papers/2601.16211) · ▲48

## Abstract (verbatim)

> Zero-Shot Compositional Action Recognition (ZS-CAR) requires recognizing novel verb-object combinations composed of previously observed primitives. In this work, we tackle a key failure mode: models predict verbs via object-driven shortcuts (i.e., relying on the labeled object class) rather than temporal evidence. We argue that sparse compositional supervision and verb-object learning asymmetry can promote object-driven shortcut learning. Our analysis with proposed diagnostic metrics shows that existing methods overfit to training co-occurrence patterns and underuse temporal verb cues, resulting in weak generalization to unseen compositions. To address object-driven shortcuts, we propose Robust COmpositional REpresentations (RCORE) with two components. Co-occurrence Prior Regularization (CPR) adds explicit supervision for unseen compositions and regularizes the model against frequent co-occurrence priors by treating them as hard negatives. Temporal Order Regularization for Composition (TORC) enforces temporal-order sensitivity to learn temporally grounded verb representations. Across Sth-com and EK100-com, RCORE reduces shortcut diagnostics and consequently improves compositional generalization.

## Background

### Background Analysis  

**1. Technical Context**  
Video understanding technologies aim to recognize human actions by decomposing them into two core components: **verbs** (e.g., "open") and **objects** (e.g., "drawer"), enabling systems to interpret complex behaviors like "opening a drawer." These technologies are critical for applications such as smart assistants and robot interaction, where AI must execute compound actions (e.g., "pick up a cup and drink water") based on video instructions. However, existing methods struggle with **unseen verb-object combinations** (e.g., trained on "open door" but not "open drawer"), limiting their generalization.  

**2. Previous Limitations**  
Prior approaches fail due to two key issues:  
- **Data sparsity**: Training datasets have extremely low coverage of possible verb-object combinations (e.g., some datasets annotate only 1% of all combinations). This forces models to rely on "object frequency" as a shortcut (e.g., defaulting to "open" when seeing a "drawer") rather than temporal cues.  
- **Learning asymmetry**: Objects are recognizable from single frames (static information), while verbs require multi-frame temporal reasoning (dynamic information). This imbalance encourages models to take shortcuts by predicting verbs based on object labels instead of learning action dynamics.  

**3. Proposed Solution**  
The paper introduces **RCORE**, a framework addressing these issues through:  
- **Composition-aware augmentation**: Generates plausible unseen verb-object combinations (e.g., "close drawer") while preserving temporal structures, pushing models to learn new logic.  
- **Temporal regularization**: Penalizes reliance on static object cues by contrasting original and shuffled videos, forcing models to focus on verb temporal features.  

**4. Key Differences**  
Unlike prior work, this paper:  
- **Explicitly diagnoses the problem**: It is the first to systematically identify "object-driven shortcuts" as a core flaw in ZS-CAR, using metrics like the "compositional gap" to measure true compositional reasoning.  
- **Targets root causes**: Instead of merely increasing data or adjusting models, it directly addresses data sparsity and learning asymmetry through augmentation and temporal constraints.  

This approach demonstrates that the bottleneck lies not in model capacity but in flawed behavior—models take shortcuts due to "laziness." RCORE improves generalization by enforcing temporal awareness, proving that robust compositional understanding requires correcting these behavioral flaws.

## Method, Figure by Figure

![Figure 4 : Overview of RCORE . (a) Overview of our proposed RCORE framework. (b)](fig3_1.webp)

> Figure 4 : Overview of RCORE . (a) Overview of our proposed RCORE framework. (b) VOCAMix synthesizes plausible yet unseen verb–object compositions while preserving the temporal structure of the primary video. (c) TORC penalizes alignment between original and temporally perturbed feature vectors, enforcing explicit temporal order modeling and reducing object-driven shortcuts.

This figure (Figure 4) provides a detailed overview of the **RCORE (Robust COmpositional REpresentations)** framework proposed in the paper, which aims to address the "object-driven shortcut" problem in zero-shot compositional action recognition (ZS-CAR). We can break down the figure into three main parts to understand its workflow:

### Part 1: RCORE Framework Overview (Figure a)
This section illustrates the entire RCORE system pipeline, from input video to final output.

1.  **Input and Initial Processing**:
    *   On the far left is the "Input Video." This video first passes through a yellow module labeled "VOCAM Avg." (likely performing some form of averaging or encoding for objects and actions in the video) and then enters the gray "Video Encoder," which extracts visual features from the video.

2.  **Feature Separation and Encoding**:
    *   The output of the video encoder is split into two paths:
        *   **Verb Encoding Path**: Features are fed into the red "Verb Encoder," generating "Verb Features Fᵛ."
        *   **Object Encoding Path**: Features are fed into the blue "Object Encoder," generating "Object Features Fᵒ."

3.  **Conditioning Module and Text Encoding**:
    *   "Verb Features Fᵛ" and "Object Features Fᵒ" are input into a gray "Conditioning Module," which combines these features and outputs a conditioning vector "y."
    *   There are also two "Text Encoder" modules:
        *   One receives the text description "a photo of lift up spoon" and is constrained by "L_TORC" (Temporal Order Regularization Loss).
        *   The other receives the text description "a photo of spoon."

4.  **Data Synthesis and Augmentation (Part of Figure b)**:
    *   This section demonstrates the "VOCAMix" technique, used to synthesize new, unseen verb-object combinations while preserving the temporal structure of the original video.
    *   Example 1: "Generated by Ours" shows an action "Lift up Spoon," processed through a "Foreground Estimation Algorithm" and "Get Center Frame."
    *   Example 2: The action "Drop Pen" is shown.
    *   Example 3: "Generated by CutMix" shows a mixed action "1 - λ Lift up Spoon λ Drop Pen" (with a probability of 1-λ for lifting up a spoon and λ for dropping a pen).
    *   Example 4: "Generated by Mixup" shows a similar mixed action "1 - λ Lift up Spoon λ Drop Pen."
    *   These synthesized data are used to augment the training set, helping the model learn more generalized compositions.

### Part 2: Temporal Order Regularization (TORC) (Part of Figure c)
This section explains the working principle of "Temporal Order Regularization for Composition (TORC)," which enforces the model to be sensitive to temporal order, thereby reducing the object-driven shortcut.

1.  **Feature Perturbation and Comparison**:
    *   Assume we have an original video feature sequence "Fᵛ" (e.g., feature order [2, 3, 1]).
    *   **Shuffle**: Randomly shuffle this sequence to get "Fᵛ_shuffled" (e.g., [1, 2, 3]).
    *   **Reverse**: Reverse this sequence to get "Fᵛ_rev" (e.g., [3, 2, 1]).

2.  **Encoding and Loss Calculation**:
    *   The original features "Fᵛ," shuffled features "Fᵛ_shuffled," and reversed features "Fᵛ_rev" are each fed into their respective "Verb Encoder."
    *   The encoded features are represented as "Fᵛ_encoded" (or "Fᵛ^shuffled," "Fᵛ^rev").
    *   Then, an average (Avg) operation is performed on these encoded features to obtain "Fᵛ^shuffled_avg," "Fᵛ^rev_avg," etc.
    *   Losses are calculated:
        *   "L_ent" (possibly entropy loss) measures the uncertainty after shuffling features.
        *   "L_cos" (cosine similarity loss) measures the difference between original features and perturbed features.
        *   "L_rev" (reverse loss) may measure the relationship between original features and reversed features.
    *   Through these losses, the model is trained to distinguish between the original temporal order and the perturbed temporal order, thus learning temporally sensitive verb representations and reducing the tendency to rely solely on object information for prediction.

### Method Summary
RCORE mitigates the object-driven shortcut problem through two main components:
1.  **Co-occurrence Prior Regularization (CPR)**: Although not explicitly labeled in the figure, according to the abstract, CPR provides explicit supervision for unseen compositions and regularizes frequent co-occurrence priors as negative examples, preventing the model from overfitting to co-occurrence patterns in the training data.
2.  **Temporal Order Regularization for Composition (TORC)**: As shown in Figure c, TORC perturbs the original video features temporally (e.g., by shuffling and reversing) and forces the model to distinguish between these perturbed features and the original features, thus learning temporally sensitive verb representations. This enables the model to not only rely on object information (i.e., the object-driven shortcut) for action recognition but to utilize temporal information of actions more effectively.

In summary, the RCORE framework, through synthesizing new composition data (VOCAMix) and introducing temporal order regularization (TORC), aims to enable the model to learn more robust and generalizable compositional action representations, thereby improving performance in zero-shot compositional action recognition scenarios.

---

![Figure 6 : RCORE mitigates object-driven shortcuts in verb learning. We visualiz](fig5_1.webp)

> Figure 6 : RCORE mitigates object-driven shortcuts in verb learning. We visualize confusion matrices for six representative verbs to compare the ability of RCORE and C2C to distinguish opposite temporal semantics on unseen compositions of the Sth-com [ 16 ] test set. All values in the confusion matrices are normalized frequencies across the entire verb classes in the dataset.

This figure (Figure 6) from the paper "Why Can't I Open My Drawer? Mitigating Object-Driven Shortcuts in Zero-Shot Compositional Action Recognition" is designed to illustrate how the proposed RCORE method mitigates "object-driven shortcuts" in verb learning.

Let's break down the structure and content of the image:

1.  **Overall Layout**: The figure contains two side-by-side confusion matrices. The left matrix represents a baseline method (according to the caption, C2C), and the right matrix represents the authors' proposed RCORE method. This side-by-side comparison is intended to visually demonstrate the difference in performance between the two methods in distinguishing verbs with similar temporal semantics on unseen compositions.

2.  **Axes and Labels**:
    *   **Y-axis (Vertical Axis)**: Labeled "Ground Truth" (真实标签), this axis represents the actual action categories. From top to bottom, it lists six representative verbs: "Tearing a little bit" (轻微撕裂), "Tearing into two pieces" (撕成两半), "Unfolding" (展开), "Folding" (折叠), "Opening" (打开), and "Closing" (关闭). These verbs are the actions the model needs to recognize.
    *   **X-axis (Horizontal Axis)**: Labeled "Prediction" (预测), this axis represents the action categories predicted by the model. The labels from left to right are the same six verbs as on the Y-axis. This means the rows of the confusion matrix represent the true class, and the columns represent the predicted class.

3.  **Matrix Cells**:
    *   Each cell contains a normalized frequency, representing the proportion of samples in the test set where the true action was of one category and the model predicted it as another. All values are normalized across the entire verb classes in the dataset.
    *   The color intensity typically represents the magnitude of the value; darker colors (e.g., dark brown) indicate a higher value (i.e., the model is more likely to predict the column category when the true category is the row category), while lighter colors (e.g., light orange or beige) indicate a lower value.

4.  **Comparative Analysis (Revealing How the Method Works and Its Effectiveness)**:
    *   **Objective**: The core purpose of this figure is to show how RCORE helps the model better distinguish between verbs that have similar temporal semantics or are easily confused due to object-driven shortcuts. For example, "Tearing a little bit" and "Tearing into two pieces" both involve "tearing" but to different degrees; "Unfolding" and "Folding" are opposite actions; "Opening" and "Closing" are also opposites.
    *   **Performance of the Baseline Method (Left Matrix, assumed to be C2C)**:
        *   Looking at the row for "Tearing a little bit," when the true label is "Tearing a little bit," there is a 0.67 probability of correctly predicting "Tearing a little bit," but a 0.27 probability of incorrectly predicting "Tearing into two pieces." This indicates that the baseline model has difficulty distinguishing between these two similar tearing actions.
        *   Similarly, for "Unfolding," there is a 0.48 probability of correct prediction, but a 0.44 probability of incorrectly predicting "Folding." For "Opening," there is an 0.80 probability of correct prediction, but a 0.07 probability of incorrectly predicting "Closing."
        *   These relatively high error rates suggest that the baseline model might rely on object-driven shortcuts rather than temporal evidence from the actions themselves for prediction.
    *   **Performance of the RCORE Method (Right Matrix)**:
        *   Now, looking at the RCORE method's matrix. For "Tearing a little bit," the probability of correct prediction increases to 0.83, while the probability of incorrectly predicting "Tearing into two pieces" decreases to 0.08.
        *   For "Unfolding," the probability of correct prediction increases to 0.83, and the probability of incorrectly predicting "Folding" decreases to 0.03.
        *   For "Opening," the probability of correct prediction increases to 0.84, and the probability of incorrectly predicting "Closing" decreases slightly to 0.07 (this change is smaller, but other improvements are significant).
        *   More importantly, observe the cross-predictions between similar or opposite actions. For example, in the RCORE matrix, the probability of "Tearing a little bit" being predicted as "Tearing into two pieces" (0.08) is much lower than in the baseline method (0.27). Similarly, the probability of "Unfolding" being predicted as "Folding" (0.03) is much lower than in the baseline method (0.44).
    *   **Revealing How the Method Works**:
        *   RCORE mitigates object-driven shortcuts through two main components:
            *   **Co-occurrence Prior Regularization (CPR)**: Provides explicit supervision for unseen compositions and regularizes the model against frequent co-occurrence priors by treating them as hard negatives. This helps the model learn more generalizable verb representations rather than relying solely on common object-action combinations.
            *   **Temporal Order Regularization for Composition (TORC)**: Enforces temporal-order sensitivity to learn temporally grounded verb representations. This enables the model to focus on the dynamic process of the action rather than just static features of the object or scene.
        *   From the figure, it is clear that RCORE significantly improves the model's ability to distinguish between verbs with similar or opposite temporal semantics. This implies that the model relies more on temporal evidence from the action itself rather than object information for prediction. For instance, the model can now better differentiate between "slight tearing" and "tearing into two halves" because it focuses on the degree of tearing (a temporal change) rather than just seeing an object being torn.

5.  **Conclusion**:
    *   This confusion matrix figure clearly demonstrates the effectiveness of the RCORE method in mitigating object-driven shortcuts. By comparing the prediction results of the baseline method and RCORE, we can see that RCORE performs better in distinguishing verbs with similar temporal semantics or those that are easily confused due to object-driven shortcuts.
    *   Specifically, RCORE reduces the probability of the model incorrectly predicting one verb as another with similar or opposite temporal semantics. This indicates that RCORE successfully makes the model pay more attention to the temporal order evidence of the action itself, thereby improving the accuracy and generalization capability of zero-shot compositional action recognition, especially when dealing with unseen verb-object compositions.

In summary, this figure uses confusion matrix visualization to intuitively compare the performance of the baseline method and RCORE in verb classification tasks, particularly for verbs susceptible to object-driven shortcuts. The results show that RCORE, through its regularization components, effectively helps the model learn verb representations that are more dependent on temporal semantics, thus enhancing classification accuracy and generalization.

---

![Figure 5 : Analysis on the effects of RCORE on the Sth-com [ 16 ] dataset. (a) R](fig4_1.webp)

> Figure 5 : Analysis on the effects of RCORE on the Sth-com [ 16 ] dataset. (a) RCORE prevents the False Co-occurrence Prediction (FCP) ratio from increasing during training, whereas the baseline shows a clear rise in FCP. As a result, RCORE consistently maintains a smaller seen–unseen accuracy gap ( Δ S ​ U \Delta_{SU} ) throughout training. (b) The cosine similarity between the original and reversed verb features becomes strongly negative for RCORE as training progresses, indicating improved temporal discriminative capability. In contrast, the baseline maintains a high similarity (0.91), revealing limited temporal sensitivity. (c) On the Temporal subset, RCORE exhibits a substantially larger performance gap between original and temporally shuffled features compared to the baseline, demonstrating that RCORE learns verb representations that depend on temporal dynamics rather than static object cues. Best viewed with zoom and color.

This figure (Figure 5, likely corresponding to part (a) of the original paper) illustrates the effects of the RCORE method compared to a baseline method (C2C) on several key metrics during training on the Sth-com dataset. It helps us understand how RCORE mitigates object-driven shortcut learning.

First, let's break down the components of the graph:

1.  **X-axis (Epoch)**: Represents the training epochs, ranging from 0 to 30, indicating the progress of model training.
2.  **Y-axes**: There are two y-axes.
    *   **Left Y-axis (Accuracy (%))**: Represents accuracy, ranging from 0% to 50%. It includes two accuracy curves:
        *   **C2C Seen Accuracy (dark blue solid line)**: The accuracy of the baseline C2C method on seen (previously observed) verb-object compositions during training.
        *   **C2C Unseen Accuracy (dark red solid line)**: The accuracy of the baseline C2C method on unseen (novel) verb-object compositions during training.
    *   **Right Y-axis (False Prediction Ratio (%))**: Represents the false prediction ratio, ranging from 0% to 25%. It includes two FCP ratio curves:
        *   **C2C FCP ratio (gray square line)**: The False Co-occurrence Prediction (FCP) ratio for the baseline C2C method. This measures the model's tendency to predict verbs based on incorrect object co-occurrence patterns.
        *   **RCORE FCP ratio (light blue square line)**: The FCP ratio for the proposed RCORE method.
3.  **Data Points and Trends**:
    *   **Accuracy Curves**:
        *   For the C2C method, both its "seen composition accuracy" (dark blue) and "unseen composition accuracy" (dark red) increase with training epochs. However, the "seen accuracy" is consistently higher than the "unseen accuracy," and the gap between them seems to widen or stabilize at certain points (e.g., after epoch 15). For example, at epoch 30, C2C's seen accuracy is approximately 43.1%, while its unseen accuracy is around 25.4%.
    *   **FCP Ratio Curves**:
        *   The FCP ratio for the baseline C2C method (gray square line) is very high at the beginning of training (29.7% at epoch 0), then drops sharply by epoch 5 to around 13.6%, and subsequently decreases slowly, stabilizing at a lower level (around 7.6% at epoch 30).
        *   The FCP ratio for the RCORE method (light blue square line) is also high initially (25.4% at epoch 0) but decreases more rapidly, reaching about 8.6% by epoch 5. It then remains at a relatively low and stable level throughout the rest of the training, even reaching a low of 7.2% at epoch 20. At epoch 30, it slightly increases to 9.5%, but it is still significantly lower than C2C's FCP ratio at later stages (e.g., 7.6% at epoch 30).

**How the method works (as revealed by the figure)**:

*   **RCORE Prevents FCP Ratio Increase**: The figure's title and caption state that RCORE prevents the FCP ratio from increasing during training, whereas the baseline shows a clear rise. Visually, while C2C's FCP ratio also decreases in the early stages, RCORE's FCP ratio is consistently and significantly lower than C2C's throughout the training (especially after epoch 5). This indicates that RCORE effectively suppresses the model's reliance on incorrect object co-occurrence patterns for prediction, i.e., it reduces "object-driven shortcuts."
*   **Maintains a Smaller Seen-Unseen Accuracy Gap (ΔSU)**: The caption mentions that RCORE consistently maintains a smaller seen-unseen accuracy gap (ΔSU) throughout training. From the graph, the gap between C2C's "seen accuracy" and "unseen accuracy" is large at epoch 0 (e.g., ~9.2%), increases to ~15.6% at epoch 5, and continues to grow (e.g., ~19.8% at epoch 15, ~17.7% at epoch 30). While the absolute gap increases, RCORE's lower FCP ratio suggests it generalizes better to unseen compositions. The caption implies that by reducing FCP, RCORE either overfits less to seen compositions or learns unseen compositions more effectively, leading to a relatively smaller or more controlled ΔSU. More directly, a lower FCP ratio for RCORE means it relies less on erroneous co-occurrence patterns, which should improve its performance on unseen compositions, indirectly contributing to a smaller ΔSU.

**Conclusion**:

This figure clearly demonstrates that the RCORE method effectively reduces the False Co-occurrence Prediction (FCP) ratio during training compared to the baseline C2C method. RCORE maintains a significantly lower FCP ratio throughout the training process. This indicates that RCORE successfully mitigates the model's dependence on object-driven shortcuts, thereby improving its generalization ability, particularly for novel (unseen) verb-object compositions. By suppressing the FCP ratio, RCORE encourages the model to rely more on temporal evidence rather than static object category information for prediction.

---

![Figure 9 : Learning curve of the baseline and RCORE on the EK100-com dataset. RC](fig8_1.webp)

> Figure 9 : Learning curve of the baseline and RCORE on the EK100-com dataset. RCORE suppresses the increase of the FCP ratio during training, effectively narrowing the performance gap between seen and unseen composition validation accuracies.

This figure displays learning curves for the baseline method (C2C) and the proposed RCORE method on the EK100-com dataset. It evaluates model performance using three key metrics: compositional action accuracy (for seen and unseen compositions) and the FCP ratio (False Prediction Ratio), which indicates the model's reliance on object-driven shortcuts.

First, let's examine the **axes**:
*   The **X-axis** represents the training "Epoch," ranging from 0 to 30, indicating the progress of model training.
*   The **left Y-axis** represents "Accuracy(%)," ranging from 0 to 50%, used to measure the model's predictive accuracy on seen and unseen compositions.
*   The **right Y-axis** represents the "False Prediction Ratio(%)," ranging from 0 to 25%, used to measure the model's tendency to rely on object-driven shortcuts.

Next, we analyze the **data and curves** in the figure:
There are six curves, each represented by different colors and markers:
1.  **Dark blue solid line with dots**: Represents the accuracy of the baseline C2C method on "seen compositions" (C2C Seen Accuracy). This curve shows that C2C's accuracy on seen compositions rapidly increases from approximately 9.6% initially to around 40% and then plateaus, reaching about 43.1% by epoch 30.
2.  **Dark blue hollow dots**: Represent the accuracy of the RCORE method on "seen compositions" (RCORE Seen Accuracy). Its trend is similar to C2C, but with a slightly lower initial value (around 8.4%), ultimately reaching about 43.1% by epoch 30, comparable or slightly better than C2C.
3.  **Red solid line with dots**: Represents the accuracy of the baseline C2C method on "unseen compositions" (C2C Unseen Accuracy). This curve shows C2C's accuracy on unseen compositions starts near 0% and gradually increases, reaching about 22.0% by epoch 30.
4.  **Red hollow dots**: Represent the accuracy of the RCORE method on "unseen compositions" (RCORE Unseen Accuracy). Its trend is similar to C2C, but with consistently higher accuracy overall. It starts from approximately 0.4% and rises to about 25.4% by epoch 30.
5.  **Gray solid line with squares**: Represents the "FCP ratio" of the baseline C2C method (C2C FCP ratio). This curve shows that the FCP ratio is very high initially (29.7% at Epoch 0), indicating a strong reliance on object-driven shortcuts. As training progresses, this ratio drops rapidly, falling to about 11.9% by epoch 10, and continues to slowly decrease, reaching approximately 9.5% by epoch 30. This suggests C2C reduces shortcut usage to some extent, but the initial value is high and remains significant after decreasing.
6.  **Light blue hollow squares**: Represent the "FCP ratio" of the RCORE method (RCORE FCP ratio). Compared to C2C, RCORE's FCP ratio is significantly lower throughout the training process. It starts at 13.6% (already lower than C2C's initial value) and continues to decrease, reaching about 10.8% by epoch 10, and further reducing to approximately 7.6% by epoch 30. This indicates RCORE more effectively suppresses the use of object-driven shortcuts.

**Revealing how the method works**:
This figure reveals how RCORE operates:
*   **Suppressing FCP ratio growth**: A key goal of RCORE is to reduce the model's reliance on object-driven shortcuts. The figure shows that RCORE's FCP ratio is consistently lower than that of the baseline C2C throughout training. This means RCORE, through its proposed regularization methods (like Co-occurrence Prior Regularization, CPR, and Temporal Order Regularization for Composition, TORC), effectively suppresses the learning of frequent co-occurrence patterns (i.e., object-driven shortcuts).
*   **Narrowing the performance gap between seen and unseen compositions**: Another key goal is to improve the model's generalization to unseen compositions. The figure shows that RCORE's accuracy on "unseen compositions" (red hollow dots) is consistently higher than C2C's accuracy under the same conditions (red solid dots). Simultaneously, RCORE's lower FCP ratio indicates it relies less on shortcuts and more on temporally grounded verb cues. This combination of a lower FCP ratio and higher accuracy on unseen compositions effectively narrows the performance gap between seen and unseen compositions.

**Conclusion**:
This figure clearly demonstrates that the RCORE method, by suppressing the FCP ratio (i.e., reducing reliance on object-driven shortcuts), successfully improves the model's accuracy on unseen compositions. Compared to the baseline C2C, RCORE more effectively learns temporally reasonable verb representations during training, thereby enhancing compositional generalization. Specifically, RCORE achieves higher accuracy on unseen compositions while reducing the model's over-reliance on co-occurrence patterns in the training data, which is crucial for addressing the "object-driven shortcuts" problem highlighted in the paper.

---

![Figure 10 : Performances on Temporal/Static split of Sth-com. We evaluate the mo](fig9_1.webp)

> Figure 10 : Performances on Temporal/Static split of Sth-com. We evaluate the models on Sth-com [ 16 ] using both (a) our reconstructed splits and (b) the splits from Sevilla et al [ 31 ] . We utilize both original and temporally shuffled inputs to assess the model’s temporal modeling capability and its reliance on static cues. A larger performance gap between original and shuffled inputs indicates that the model predicts verbs more based on temporal dynamics rather than on static cues.

This figure (Figure 10) from the paper "Why Can't I Open My Drawer? Mitigating Object-Driven Shortcuts in Zero-Shot Compositional Action Recognition" illustrates the performance of different models under various experimental settings, specifically focusing on their ability to utilize temporal dynamics versus static cues for action recognition. The figure helps us understand how the proposed method (RCORE) works and its effectiveness in improving compositional generalization.

Let's break down the components of the graph:

1.  **X-axis (Horizontal Axis)**: This axis represents different experimental configurations.
    *   **Temporal split / Static split**: These are two types of data splits. "Temporal split" likely refers to data divided based on temporal order or action sequences, while "Static split" might be based on static features (like object categories) without considering temporal order. These splits evaluate model generalization under different data distributions.
    *   **Seen comp. / Unseen comp.**: This indicates the visibility of the verb-object combinations. "Seen comp." refers to combinations present in the training set, while "Unseen comp." refers to those not present, which is a key challenge in zero-shot learning.

2.  **Y-axis (Vertical Axis)**: This axis represents accuracy in percentage (%). Higher accuracy indicates better model performance.

3.  **Bars and Legend**:
    *   **Light Gray Bars (C2C w/ original inputs ↑)**: Represents the accuracy of a baseline model (possibly C2C) when using original input data. The upward arrow (↑) suggests we desire high performance here.
    *   **Dark Gray Bars (C2C w/ shuffled inputs ↓)**: Represents the accuracy of the same baseline model when using time-shuffled input data. The downward arrow (↓) suggests we expect lower performance here, as shuffling time steps disrupts temporal dynamics, and a model relying heavily on static cues would show less degradation.
    *   **Light Pink Bars (RCORE w/ original inputs ↑)**: Represents the accuracy of the proposed method (RCORE) when using original input data. The upward arrow (↑) indicates expected high performance.
    *   **Red Bars (RCORE w/ shuffled inputs ↓)**: Represents the accuracy of RCORE when using time-shuffled input data. The downward arrow (↓) indicates expected low performance.

The method's operation and conclusions revealed by the figure:

*   **Core Idea of the Method**: The paper addresses a key issue in Zero-Shot Compositional Action Recognition (ZS-CAR): models tend to predict verbs using "object-driven shortcuts" (relying on object labels) rather than temporal evidence. To mitigate this, the paper proposes Robust COmpositional REpresentations (RCORE), which includes:
    *   **Co-occurrence Prior Regularization (CPR)**: Provides explicit supervision for unseen compositions and regularizes against frequent co-occurrence priors by treating them as hard negatives.
    *   **Temporal Order Regularization for Composition (TORC)**: Enforces temporal-order sensitivity to learn temporally grounded verb representations.

*   **Evaluating Model Dependence on Temporal vs. Static Cues**: The figure uses "original inputs" and "time-shuffled inputs." If a model relies on temporal dynamics, its accuracy on original inputs should be significantly higher than on shuffled inputs (a larger gap). Conversely, if it relies on static cues, accuracy will not drop much with shuffled inputs.

*   **Conclusions from the Figure**:
    1.  **RCORE's Performance Advantage**: In most cases, RCORE (light pink bars) achieves higher accuracy than the baseline C2C (light gray bars) on original inputs. This suggests RCORE better utilizes temporal dynamics or generalizes better to unseen combinations.
    2.  **Dependence on Temporal Cues**:
        *   For "Temporal split," on "Seen comp.," RCORE's accuracy on original inputs (~70%) is much higher than on shuffled inputs (~32%), indicating it relies on temporal dynamics. A similar trend exists for C2C, but RCORE shows a greater advantage.
        *   For "Unseen comp." (under Temporal split), RCORE's accuracy on original inputs (~62%) is significantly higher than on shuffled inputs (~25%).
        *   For "Static split," on "Seen comp.," RCORE's accuracy on original inputs (~64%) is higher than on shuffled inputs (~44%). For "Unseen comp.," RCORE's accuracy on original inputs (~53%) is also higher than on shuffled inputs (~36%).
    3.  **Generalization Ability**: RCORE generally performs better than C2C on "Unseen comp.," indicating better generalization to novel combinations. For example, under Temporal split for Unseen comp., RCORE (~62%) far outperforms C2C (~30%).
    4.  **Impact of Time-Shuffled Inputs**: For all methods and combination types, shuffling inputs reduces accuracy, validating that models rely, to some extent, on temporal dynamics. However, the drop in accuracy for RCORE is sometimes more pronounced (or shows a greater advantage over C2C) compared to C2C (e.g., under Temporal split for Unseen comp., C2C drops from ~30% to ~28%, while RCORE drops from ~62% to ~25%), suggesting RCORE relies more purely on temporal dynamics or less on static cues.

In summary, this figure clearly demonstrates how RCORE improves zero-shot compositional action recognition by reducing object-driven shortcuts and enhancing temporal sensitivity. Specifically, RCORE achieves higher accuracy on original inputs and often shows a more significant performance drop with shuffled inputs (or a greater advantage over C2C), indicating it learns more effective temporally grounded verb representations and generalizes better to unseen combinations.
