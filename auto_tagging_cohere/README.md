# Auto-Tagging Images with Cohere Embed 4 on Microsoft Foundry (Azure AI Foundry)

This folder contains a Jupyter notebook that demonstrates **automatic image tagging** using **Cohere Embed v4** (multimodal embeddings) deployed through **Azure AI Foundry / Microsoft Foundry**.

Notebook:
- [`auto_tagging_cohere_embed4_azure.ipynb`](./auto_tagging_cohere_embed4_azure.ipynb)

## What this notebook does

It implements a simple, practical pipeline for tagging product-style images:

1. Define a set of candidate tags as text (e.g., *“red”*, *“dress”*, *“sneakers”*, *“leather bag”*, etc.)
2. Compute **text embeddings** for those tags using **Cohere Embed v4**
3. Compute **image embeddings** for input images using the same model (multimodal embedding space)
4. Compute **cosine similarity** between the image embedding and each tag embedding
5. Assign the best tag(s), optionally grouped by **facet** (e.g., `color`, `category`, `material`, …) with thresholds

This is a lightweight baseline that can be extended into production workflows (catalog enrichment, DAM tagging, e-commerce search filters, moderation pipelines, etc.).

## Key implementation notes

- **Image loading & preprocessing**
  - Images are downloaded with `requests`
  - Converted to RGB with Pillow
  - Resized (thumbnail) and encoded to base64 JPEG to reduce payload/token usage

- **Similarity**
  - A cosine similarity matrix is computed between the image embedding and all tag embeddings
  - Tag selection supports:
    - `top_per_facet` (pick top-N tags per facet)
    - `threshold` (minimum similarity score)

- **Model settings**
  - `MODEL_NAME = "embed-v-4-0"`
  - `output_dimension` is set to **1536** (the notebook notes other allowed sizes)

## Author

| Field | Details |
| --- | --- |
| Name | Serge Retkowsky |
| Created | 06 Feb 2026 |
| Email | serge.retkowsky@microsoft.com |
| LinkedIn | https://www.linkedin.com/in/serger/ |
| Medium publications | https://medium.com/@sergems18/ |
