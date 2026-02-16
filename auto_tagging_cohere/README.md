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

## Prerequisites

- Python **3.10+**
- An **Azure AI Foundry** endpoint with **Cohere Embed v4** deployed
- Packages:
  - `azure-ai-inference`
  - `azure-identity`
  - `azure-core`
  - `python-dotenv`
  - plus common scientific packages (`numpy`, `pandas`, `matplotlib`, `Pillow`, `requests`)

## Setup

### 1) Create an `azure.env` file

The notebook loads environment variables from `azure.env`:

- `endpoint`: your Azure AI Foundry endpoint URL (the notebook expects `os.getenv("endpoint")`)

Create a file named `azure.env` next to the notebook (or ensure the path matches the `load_dotenv("azure.env")` call):

```bash
endpoint="https://<your-foundry-endpoint>"
```

### 2) Authenticate to Azure

The notebook uses:

- `DefaultAzureCredential()` to obtain an Azure AD token
- Then passes that token into `AzureKeyCredential(tok.token)` for the inference client

Make sure you are authenticated in a way that `DefaultAzureCredential` can pick up, for example:
- `az login` (local development)
- Managed Identity (Azure-hosted environment)
- VS Code Azure Account extension login, etc.

## Running the notebook

1. Open `auto_tagging_cohere_embed4_azure.ipynb`
2. Install missing dependencies (if needed)
3. Ensure `azure.env` is present and points to your deployed model endpoint
4. Run cells top-to-bottom

The notebook also downloads a few public sample images (URLs embedded in the notebook) for demo purposes.

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

## Extending this demo

Ideas to productionize/extend:
- Use a curated tag taxonomy per category (fashion, electronics, etc.)
- Add multi-tag selection with diversity constraints (MMR)
- Persist embeddings in a vector database for reuse
- Evaluate with a labeled dataset and tune thresholds per facet
- Add batching + retry logic + robust HTTP handling for image downloads

## License / content note

The notebook uses public image URLs for demonstration. For production usage, you should use images you have rights to process and store.

---
If you want, I can also generate:
- a repo-root README section that links to this notebook
- an `azure.env.example`
- a `requirements.txt` specific to this notebook
