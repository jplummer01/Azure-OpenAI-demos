# Image Anomaly Detection with Cohere Embed 4 on Microsoft Foundry

This demo shows how to perform **image anomaly detection** using **Cohere Embed 4** (multimodal embeddings) hosted on **Microsoft Foundry**. The core idea is:

1. Generate **embeddings** for a set of *reference/normal* images.
2. Generate embeddings for *new/inspection* images.
3. Detect anomalies by comparing embedding distances (e.g., nearest-neighbor distance / similarity) and flagging images that are “far” from the normal distribution.

Notebook:  
`anomaly_detection_cohere_embed4/Image Anomaly Detection with Cohere Embed 4 on Azure AI Foundry.ipynb`

---

## What you’ll build

- A small pipeline to:
  - Load images
  - Call **Cohere Embed 4** through an **Azure AI Foundry endpoint**
  - Compute similarity / distance metrics in embedding space
  - Identify and visualize potential anomalies

Typical use cases:
- Visual quality inspection
- Detecting unusual items on a production line
- Spotting out-of-family images in a dataset

---

## Prerequisites

### Azure
- An **Azure subscription**
- Access to **Microsoft Foundry**
- A deployed **Cohere Embed 4** model endpoint (or a compatible endpoint exposed through Foundry)

### Local environment
- Python 3.9+ recommended
- Jupyter (JupyterLab or VS Code notebooks)

---

## How anomaly detection works (high level)

1. **Embedding extraction**  
   Each image is converted into a fixed-length vector using Cohere Embed 4.

2. **Reference set (“normal”)**  
   A set of known-good images defines the normal embedding distribution.

3. **Distance-based anomaly score**  
   For a new image, compute distance to nearest neighbors among the normal set (or compute centroid distance). Larger distance ⇒ more likely anomaly.

4. **Thresholding**  
   Choose a threshold to flag anomalies. You can tune it based on desired false-positive/false-negative tradeoffs.

---

## Notes / Tips

- Use a **representative** set of normal images (lighting, angle, background variation).
- Start with a small validation set and adjust the **threshold**.
- If you have multiple product families, consider building **separate baselines** per family.

## Author

| Field | Details |
| --- | --- |
| Name | Serge Retkowsky |
| Created | 06 Feb 2026 |
| Email | serge.retkowsky@microsoft.com |
| LinkedIn | https://www.linkedin.com/in/serger/ |
| Medium publications | https://medium.com/@sergems18/ |
