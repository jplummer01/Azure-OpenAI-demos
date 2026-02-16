# Image Anomaly Detection with Cohere Embed 4 on Azure AI Foundry

This demo shows how to perform **image anomaly detection** using **Cohere Embed 4** (multimodal embeddings) hosted on **Azure AI Foundry**. The core idea is:

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
- Access to **Azure AI Foundry**
- A deployed **Cohere Embed 4** model endpoint (or a compatible endpoint exposed through Foundry)

### Local environment
- Python 3.9+ recommended
- Jupyter (JupyterLab or VS Code notebooks)

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/retkowsky/Azure-AIGEN-demos.git
   cd Azure-AIGEN-demos
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   Install the libraries required by the notebook (Jupyter + Azure/Cohere client libs + image tooling + scientific stack). If the repo already includes a `requirements.txt`, prefer that. Otherwise, install the typical set:
   ```bash
   pip install -U pip
   pip install jupyter numpy pandas matplotlib pillow scikit-learn
   ```

   If the notebook uses Azure AI Foundry / Azure OpenAI style clients, you may also need:
   ```bash
   pip install azure-identity
   ```

---

## Configuration

You will need to provide your **endpoint** and **credentials** for the model hosted in Azure AI Foundry.

Common approaches:
- Environment variables
- A `.env` file loaded inside the notebook
- Direct configuration in a notebook cell (not recommended for secrets)

Create environment variables (example names — adapt to what the notebook expects):

```bash
# Endpoint for your deployed Cohere Embed 4 in Azure AI Foundry
export AZURE_AI_FOUNDRY_ENDPOINT="https://<your-endpoint>"

# API key or token (depending on your deployment/auth model)
export AZURE_AI_FOUNDRY_API_KEY="<your-key>"
```

On Windows PowerShell:
```powershell
$env:AZURE_AI_FOUNDRY_ENDPOINT="https://<your-endpoint>"
$env:AZURE_AI_FOUNDRY_API_KEY="<your-key>"
```

---

## Running the notebook

1. Start Jupyter:
   ```bash
   jupyter lab
   ```

2. Open:
   ```
   anomaly_detection_cohere_embed4/
     Image Anomaly Detection with Cohere Embed 4 on Azure AI Foundry.ipynb
   ```

3. Run cells top-to-bottom:
   - Data/image loading
   - Embedding generation
   - Similarity/distance computation
   - Anomaly scoring + visualization

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

---

## Repo structure (relevant)

- `anomaly_detection_cohere_embed4/`
  - `Image Anomaly Detection with Cohere Embed 4 on Azure AI Foundry.ipynb` — main demo notebook

---

## Security

Do not hardcode keys in the notebook. Prefer environment variables or managed identity where possible.

---

## License

See repository license (if provided).