# PixWorld: Unifying 3D Scene Generation and Reconstruction in Pixel Space

[arXiv](https://arxiv.org/abs/2607.05373) · [HuggingFace](https://huggingface.co/papers/2607.05373) · ▲61

## Abstract (verbatim)

> 3D reconstruction and generation are commonly tackled by separate paradigms: pixel-based regression for reconstruction, and latent diffusion for generation. Recent works attempt to unify them in latent space, but with notable drawbacks: the diffusion objective is defined on latent features rather than the underlying 3D representation, and both branches suffer from information loss introduced by latent encoding, while requiring a pretrained Variational Autoencoder (VAE) or Representation Autoencoder (RAE). In this paper, we reformulate these two tasks under a unified pixel-space diffusion paradigm and introduce PixWorld, a single model that jointly addresses 3D reconstruction and generation. By supervising diffusion directly on rendered images, PixWorld removes the above limitations and aligns optimization with 3D scene fidelity. Beyond photometric and perceptual supervision that operates at the 2D image level and lacks 3D geometric awareness, we further introduce a geometry perception loss that aligns rendered views with their ground truth in the geometry-aware feature space of a pretrained 3D foundation model, providing 3D structural supervision. PixWorld consistently outperforms prior latent-space generation methods and matches state-of-the-art reconstruction methods, demonstrating the superiority of a unified pixel-space approach.

## Background

### Background Analysis  

**1. Technical Context**  
3D scene construction is a core goal in computer vision, with applications in gaming, robotics, VR/AR, and more. For instance, metaverse platforms require realistic virtual environments, while autonomous driving needs scene reconstruction from sensor data. Current research splits into two tasks: **3D reconstruction** (recovering scenes from real images) and **3D generation** (synthesizing new scenes from conditions). Both are critical for building future digital worlds but have historically developed separately.  

**2. Previous Limitations**  
Traditional methods face key challenges:  
- **Information Loss and Pretraining Dependency**: Existing generation approaches often operate in latent spaces (e.g., VAE/RAE-encoded features), leading to information loss in 3D outputs and requiring additional pretraining costs.  
- **Misaligned Optimization Objectives**: Diffusion-based generation targets latent features rather than direct 3D optimization, while reconstruction relies on pixel-wise supervision (e.g., photometric loss) that fails to ensure geometric accuracy.  
- **Lack of Unified Frameworks**: Attempts like Gen3R to unify tasks still depend on latent spaces, failing to align 3D scene fidelity directly.  

**3. Proposed Solution**  
PixWorld introduces a **pixel-space diffusion paradigm** that supervises a 3D Gaussian representation through differentiable rendering, avoiding latent space trade-offs. Specifically:  
- **Unified Framework**: Combines reconstruction and generation into a single model by partitioning multi-view inputs into "clean" (for reconstruction) and "noisy" (for generation) subsets, optimizing a pixel-aligned 3D Gaussian representation jointly.  
- **Geometry-Aware Loss**: Adds a loss in a pretrained 3D foundation model’s feature space to enforce geometric alignment between rendered views and ground truth, complementing pixel-wise supervision.  

**4. Key Differences**  
Compared to prior work, PixWorld’s innovations include:  
- **Direct Pixel-Space Supervision**: Bypasses latent spaces to optimize 3D representations directly, eliminating information loss and pretraining costs.  
- **Geometric Structure Alignment**: Uses a geometry-aware loss to ensure 3D structural fidelity, not just 2D appearance.  
- **End-to-End Unification**: Handles both tasks in a single forward pass without task switching, improving efficiency and performance.  

This design enables PixWorld to outperform state-of-the-art methods in both generation and reconstruction, demonstrating the effectiveness of a pixel-space diffusion paradigm.

## Method, Figure by Figure

![Figure 2: Overview of PixWorld. (a) PixWorld adopts a unified DiT-based framewor](fig2_1.webp)

> Figure 2: Overview of PixWorld. (a) PixWorld adopts a unified DiT-based framework that takes noisy and clean multi-view inputs, with optional text conditioning, and jointly predicts depth and 3DGS through shared transformer blocks. (b) A pixel-space flow matching loss is imposed on rendered multi-view images to directly optimize the underlying 3D representation. (c) A geometry perception loss further enforces structural consistency by aligning rendered views with ground-truth observations through a 3D foundation model.

This figure is Figure 2 from the paper "PixWorld: Unifying 3D Scene Generation and Reconstruction in Pixel Space," which details the architecture and workflow of the PixWorld model. We can understand it by dividing it into three main parts: Model Overview (a), Flow Matching Loss (b), and Geometry Perception Loss (c).

First, let's look at **Figure (a) Model Overview**:
This part shows the core framework of PixWorld. It is a unified model based on DiT (Diffusion Transformer).
1.  **Input Part**:
    *   **Noisy Views**: These are input multi-view images with noise. They are fed into the "Patchify" module, which splits the images into small patches (patches), a common input processing method for Transformer-like models.
    *   **Clean Views**: These are the target multi-view images without noise. They also go through the "Patchify" module.
    *   **Text Prompt**: This is an optional conditional input for text-guided generation. The text prompt is first sent to the "Text Encoder" for encoding.
2.  **Shared Feature Processing Part**:
    *   The patch data from the noisy views and clean views are processed by their respective "Projector" (projector) to convert the patches into feature vectors suitable for Transformer processing.
    *   These feature vectors then enter a series of "Shared DIT Block × L" (shared DiT blocks, where L represents the number of layers). Each DiT block internally contains "Self-Attention" (self-attention) and "Cross-Attention" (cross-attention) mechanisms to capture dependencies between features. There is also a final "FFN" (feed-forward network).
    *   The output of the text encoder is connected to these DiT blocks via a dashed arrow, indicating that the text condition is injected into the feature processing.
3.  **Output Prediction Part**:
    *   After processing by the shared DiT blocks, the model outputs multiple predictions:
        *   **Depth Head**: Predicts the depth map of the scene. There are two depth heads in the figure, possibly corresponding to different inputs or stages.
        *   **3DGS Head**: Predicts the parameters of the 3D Gaussian Splatting model. The outputs of the two 3DGS heads (which may represent different geometric or appearance attributes) are combined by "Merged 3DGS" (merged 3D Gaussian Splatting) to form the final 3D scene representation.
    *   Data flow order: Input (noisy/clean views, text) → Patchify → Projector → Shared DiT blocks → Various prediction heads (depth, 3DGS) → Final 3D scene.

Next is **Figure (b) Flow Matching Loss**:
This part explains how the model optimizes its learned 3D representation using a pixel-space flow matching loss.
1.  **Input**: "Noisy Views" are fed into the "Model" (i.e., the PixWorld model in Figure (a)).
2.  **Model Output**: The model predicts "Predicted Flow Velocity v^p".
3.  **Ground Truth**: "GT" (Ground Truth) provides "Ground-truth Clean Views" and calculates "Ground-truth Velocity v^n" from them.
4.  **Rendering Process**: "Rendered Clean Views" likely refers to views rendered using the model's predicted 3D representation (e.g., 3DGS).
5.  **Loss Calculation**:
    *   "LPIPS" (Learned Perceptual Image Patch Similarity) is a perceptual loss used to compare the differences between the rendered clean views and the real clean views.
    *   The calculation formula for "Flow Matching L_FFM" is L_FFM = (1/|η_T|) Σ_{n∈η_T} ||v^n - v^p||, where v^n is the real flow velocity and v^p is the predicted flow velocity. This loss directly optimizes the flow related to the underlying 3D representation, ensuring that the 3D structure learned by the model can produce correct motion or view changes.

Finally, **Figure (c) Geometry Perception Loss**:
This part explains how the model enhances the geometric consistency of its predicted 3D structure using a geometry perception loss.
1.  **Input and Rendering**:
    *   "Rendered" views are rendered using the model's predicted 3D scene (e.g., 3DGS).
    *   "GT" views are the original clean views.
2.  **3D Foundation Model**: Both the rendered views and real views are input into a "3D Foundation Model" (e.g., a pre-trained NeRF or point cloud model).
3.  **Feature Extraction**: The 3D foundation model extracts "Geometry-aware Features (Rendered)" and "Geometry-aware Features (GT)" from the rendered views and real views, respectively.
4.  **Loss Calculation**: "Features Matching L_geo" aims to align these geometry-aware features extracted from the rendered views and real views, thereby ensuring that the rendered views are geometrically consistent with the real views. This is a higher-level structural supervision that complements pixel-level losses.

**Summary of the Method Revealed by This Figure**:
The PixWorld model works as follows:
1.  **Unified Input Processing**: It accepts noisy multi-view images, clear reference multi-view images (optional), and text prompts as inputs simultaneously.
2.  **Shared Feature Learning**: All inputs are patchified and then undergo feature extraction and fusion through shared DiT blocks, which use self-attention and cross-attention mechanisms to learn a joint representation of multi-view images and text.
3.  **Multi-task Prediction**: The model jointly predicts the depth map of the scene and the parameters of the 3D Gaussian Splatting, which together define a 3D scene representation.
4.  **Pixel-space Optimization**: It directly optimizes the flow related to the 3D representation using a flow matching loss, ensuring that the 3D structure learned by the model can produce realistic view changes.
5.  **Geometric Structure Supervision**: Through a geometry perception loss, it uses features extracted by a pre-trained 3D foundation model to align the geometric structures of the rendered views and real views, thereby enhancing the geometric consistency of the 3D scene.
This method unifies 3D reconstruction and generation within a pixel-space diffusion paradigm, directly supervising on rendered images to avoid the limitations of potential space methods, and improves the accuracy of the 3D structure through additional geometry perception loss.

---

![Figure 1: PixWorld unifies 3D scene reconstruction and generation within a singl](fig1_1.webp)

> Figure 1: PixWorld unifies 3D scene reconstruction and generation within a single model. Unlike prior approaches that compute losses in the latent space of a VAE (Kingma and Welling, 2013 ) or RAE (Zheng et al. , 2025 ) , PixWorld applies a flow matching objective directly in pixel space over multi-view renderings, enabling end-to-end optimization of the underlying 3D representation. This design avoids the information loss inherent to latent representations and eliminates the cost of pretraining a VAE or RAE.

This diagram clearly illustrates the core ideas and methodological flow of the paper "PixWorld: Unifying 3D Scene Generation and Reconstruction in Pixel Space." We can understand the diagram by dividing it into three main sections: the application examples at the top, the comparison with existing methods in the middle, and the PixWorld (our method) flow at the bottom.

First, let's look at the **application examples at the top**:
*   The **top-left** shows "Reconstruction Input (Lake Scene)." This displays several photos of the same lake scene taken from different angles, serving as input data. An arrow points to the "3D Reconstruction" module in the middle, indicating that these input images will be used for the 3D reconstruction task.
*   The **top-right** shows "3D Reconstruction Result (Lake Scene)." This displays the three-dimensional model of the lake scene obtained after processing, which appears as a point cloud or voxel-based representation.
*   The **middle-left** shows "Generation Input (Living Room Scene)." This displays some initial images, possibly noisy or low-quality, along with some camera position illustrations, serving as input for generating a new scene. An arrow points to the "3D Generation" module in the middle.
*   The **middle-right** shows "3D Generation Result (Living Room Scene)." This displays the three-dimensional model of the living room scene generated after processing, also presented as a point cloud or voxel-based form.
*   The core module in the middle is "PixWorld," which includes two main functions: "3D Reconstruction" and "3D Generation." This indicates that PixWorld is a unified model capable of handling both 3D scene reconstruction and generation.

Next, let's examine the **"Existing Methods" section in the middle**, which shows the workflow of traditional methods for comparison with PixWorld:
*   The process starts with "Input Images," such as several indoor scene images from different perspectives.
*   These input images are first fed into the "VAE/RAE Encoder." This step encodes the images into a latent space, a process that may lead to information loss.
*   The encoded latent features are then sent to the "DiT (Latent Space)" (Diffusion Transformer in latent space). Here, the DiT is trained in the latent space.
*   A red dashed arrow labeled "Training Objective (latent space)" indicates that the training process occurs in the latent space rather than directly targeting the 3D representation.
*   After processing by the DiT, the features are sent to the "3D Decoder," which ultimately generates "3DGS" (possibly referring to a 3D representation like 3D Gaussian Splatting).
*   The problem with this workflow is that the diffusion objective is defined on latent features rather than the underlying 3D representation, and the encoding process introduces information loss. Additionally, it requires pre-trained VAE or RAE.

Finally, let's look at the **"PixWorld (Ours)" section at the bottom**, which details the workflow of PixWorld:
*   The process also starts with "Input Images," such as several indoor scene images from different perspectives.
*   Unlike existing methods, PixWorld directly feeds these input images into the "DiT (Pixel Space)" (Diffusion Transformer in pixel space). This means the diffusion model's training and operation occur in pixel space rather than latent space.
*   The output of the DiT is directly "3DGS" (3D Gaussian Splatting or another 3D representation). This indicates that PixWorld can generate a 3D representation directly from the diffusion process in pixel space.
*   Then, this generated "3DGS" is rendered into "Rendered Images," which are 2D images obtained by observing the 3D representation from different perspectives.
*   The key training objective is "Training Objective (3D Representation)." A green dashed arrow from the "Rendered Images" points to this training objective, indicating that the training is based on comparing the rendered images with real images (or target images), but optimizing the underlying 3D representation.
*   Additionally, the diagram mentions "Beyond photometric and perceptual supervision... we further introduce a geometry perception loss..." This means that, in addition to supervising the rendered images in pixel space, a loss function considering the 3D geometric structure is introduced to improve the quality of generation or reconstruction.

In summary, this diagram reveals the core idea of the PixWorld method: by directly applying a flow matching objective to multi-view rendered images in pixel space, PixWorld unifies 3D scene reconstruction and generation into a single model. This approach avoids the information loss and the need for pre-trained VAE/RAE present in latent space methods. By directly optimizing the 3D representation, the optimization objective is more consistent with the fidelity of the 3D scene. Compared to existing methods, PixWorld can match state-of-the-art reconstruction methods while maintaining or improving generation quality.

---

![Table 2: Quantitative comparison on single-image 3D scene generation, averaged. ](fig3_1.webp)

> Table 2: Quantitative comparison on single-image 3D scene generation, averaged. Results on RealEstate10K (Zhou et al. , 2018 ) and DL3DV-10K (Ling et al. , 2024 ) under the 1-view setting, averaged over First Frame and Bidirectional configurations. Best in bold ; second best underlined . Table 3: Quantitative comparison on two-view 3D scene generation, averaged. Results on RealEstate10K (Zhou et al. , 2018 ) and DL3DV-10K (Ling et al. , 2024 ) under the 2-view setting, averaged over Interpolation and Extrapolation configurations. Best in bold ; second best underlined . Table 4: Quantitative comparison on the WorldScore benchmark (Duan et al. , 2025 ) . We report all seven official metrics together with their average. Bold and underline indicate the best and the second-best results, respectively. Figure 3: Visualization of PixWorld under different settings. PixWorld flexibly handles both 3D reconstruction and generation: when all input views are clean, it performs reconstruction; when clean and noisy views are arbitrarily mixed, it performs generation. We visualize the camera trajectory, where blue and red frustums denote clean input views and generated views, respectively. Table 5: Ablation study on geometry perception loss. We report results on RealEstate10K (Zhou et al. , 2018 ) under the 1-view setting. Figure 4: Visualization of comparisons with baselines. The large view on top denotes the input view, while the two smaller views below show novel views generated by each method. Table 6: Architecture of the two-stream DiT denoiser f θ f_{\theta} . Each block follows an MMDiT-style design: the clean and noise streams maintain independent pre-LayerNorm, QKV / output projections, SwiGLU MLP, and adaLN-Zero weights, while a single full attention is computed jointly over the concatenated [ Ω c ; Ω n ] [\,\Omega_{\mathrm{c}};\,\Omega_{\mathrm{n}}\,] tokens with shared q , k q,k -RMSNorm. The cross-attention to text and the timestep embedder are also shared across streams, and output heads are duplicated per stream so that both clean and noisy tokens are decoded into depth and 3D-Gaussian attributes at every patch. Table 7: Quantitative comparison on single-image 3D scene generation, per configuration. We evaluate on RealEstate10K (Zhou et al. , 2018 ) and DL3DV-10K (Ling et al. , 2024 ) under 1-view First Frame and 1-view Bidirectional. Best in bold ; second best underlined . Table 8: Quantitative comparison on two-view 3D scene generation, per configuration. We evaluate on RealEstate10K (Zhou et al. , 2018 ) and DL3DV-10K (Ling et al. , 2024 ) under 2-view Interpolation and 2-view Extrapolation. Best in bold ; second best underlined . Figure 5: Ablation study on the Geometry Perception loss in PixWorld. Given a single input image, our model generates the subsequent 7 frames (8 frames in total); we visualize 4 representative frames here for clarity. Pose accuracy is quantitatively evaluated by comparing the estimated camera poses against the ground-truth poses. Compared to the variant without Geometry Perception ( w/o Geom. ), the full model achieves more precise camera pose control and substantially mitigates the blurriness in later-view predictions, demonstrating that the global 3D perception loss is essential for maintaining both geometric consistency and visual fidelity over long generation horizons. Table 9: Inference speed comparison on a single NVIDIA A100-SXM4-80G GPU. We report the wall-clock time to generate one scene, the number of key frames per scene, and the number of function evaluations (NFE). Figure 6: More visualizations of reconstruction and generation under varying view selections, including camera trajectories with input and generated views marked, and the corresponding depth maps predicted by PixWorld. Figure 7: More visualizations of generated scenes. The first view is the input, and we show both RGB renderings and predicted depth maps.

This figure (Figure 3) visualizes the PixWorld model's performance under different settings, focusing on how it simultaneously handles **3D reconstruction** and **3D generation** tasks, as well as the relationships between camera trajectories, input views (clean/noisy), and generated views. We can break down the understanding into the following parts:  

### 1. Structure and Component Meanings of the Figure  
- **Camera frustums on the left**: Each frustum represents a camera’s viewpoint. The blue frustum (labeled “Clean view (input)”) denotes a **clean input view** (a known view used for reconstruction or as a basis for generation); the red frustum (labeled “Generated view (noise)”) denotes a **generated view** (output by the model when the input contains noise or new perspectives are needed). The position and direction of the frustums correspond to the camera’s position and orientation, illustrating the spatial distribution of the camera trajectory.  
- **Legend at the top**: Clarifies color meanings: blue = clean input view, red = generated (noisy) view, gray = camera trajectory (though the trajectory is implicitly shown via frustum arrangement; gray may refer to lines connecting frustums, but color primarily distinguishes input from generation).  
- **Image grid**: Each row represents a different scene or task setting, while each column corresponds to a **timestep (or viewpoint sequence)**. For example:  
  - **Top row**: All frustums are blue (clean inputs), and the images show different perspectives of the same building. This demonstrates **3D reconstruction** (reconstructing the same scene from multiple angles) when all inputs are clean views.  
  - **Second row**: The first frustum is blue (clean input), and subsequent ones are red (generated). The images show viewpoint changes in an indoor scene, illustrating **3D generation** (generating new viewpoints from a known perspective) when inputs include one clean view and subsequent generated views.  
  - Other rows follow a similar pattern: some mix blue (input) and red (generated) frustums, showcasing the model’s ability to generate under “arbitrary mixing of clean and noisy views” (i.e., unified handling of reconstruction + generation).  


### 2. How the Method Works (Operational Logic)  
PixWorld’s core is a **unified pixel-space diffusion paradigm** combining 3D reconstruction and generation:  
- **Reconstruction mode**: When all input views are “clean” (blue frustums), the model reconstructs the entire 3D scene from these inputs and renders images from different viewpoints (e.g., the top row, where all views are input-driven reconstructions, demonstrating multi-view consistency in the scene).  
- **Generation mode**: When inputs include both “clean” and “noisy” views (blue + red frustums), the model generates new viewpoints (images corresponding to red frustums) based on known clean views. For example, in the second row, the first is an input (clean), and subsequent ones are generated viewpoints, showing how the model expands from a single viewpoint to a continuous sequence.  
- **Camera trajectory and viewpoint sequence**: The camera trajectory is shown via frustum arrangement (changes in frustum positions in the same row), indicating the model generates **continuous viewpoint sequences** (e.g., timesteps or sequences of rotational/positional changes). For instance, in the third row’s outdoor scene, frustums move from left to right, and images show the scene rendered from different distances/angles, verifying the model’s consistent 3D space modeling.  


### 3. Interpreting the Results (Conclusions)  
From the figure, we can intuitively observe:  
- **Reconstruction consistency**: When all inputs are clean views (e.g., the top row), the reconstructed (generated) views are highly consistent in scene content, lighting, and object positions, proving the model accurately reconstructs multi-view 3D scenes.  
- **Generation coherence**: When inputs include both clean and generated views (e.g., the second, fourth, and fifth rows), the generated views (red) remain coherent with the input views (blue) in scene structure and object appearance, with no obvious breaks or mismatches. This shows the model generates **geometrically consistent and visually realistic** new viewpoints.  
- **Handling mixed inputs**: Multiple rows mix blue (input) and red (generated) frustums, demonstrating the model’s flexibility in handling “arbitrary mixing of clean and noisy views”—that is, performing reconstruction (using clean inputs) and generation (supplementing new viewpoints) simultaneously. This reflects the method’s **unified nature** (no need to separate reconstruction and generation; instead, the same model and paradigm handle both).  


In summary, this figure clearly demonstrates how PixWorld **unifies 3D reconstruction and generation** through visualized camera trajectories and mixed input/generated views: clean views serve as inputs (for reconstruction), while noisy/missing views are generated by the model, ultimately outputting continuous, consistent 3D scene viewpoint sequences. Each row corresponds to a task setting (pure reconstruction, pure generation, mixed inputs), columns correspond to temporal/spatial viewpoint sequences, and colors distinguish inputs from generations—intuitively verifying the model’s reconstruction consistency and generation coherence.
