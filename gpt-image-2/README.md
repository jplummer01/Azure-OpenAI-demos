# GPT-Image-2 demos using Microsoft Foundry

![GPT-Image-2 banner](https://techcommunity.microsoft.com/t5/s/gxcuf89792/images/bS00NTAwNTcxLTZ4WmdLeQ?revision=9&image-dimensions=2000x2000&constrain-image=true)

## Model: `gpt-image-2` (overview)

`gpt-image-2` is an image generation model that can create and transform images from natural-language prompts. In these notebooks, it’s used from **Azure AI Foundry / Azure OpenAI** to demonstrate practical workflows such as:
- **Text-to-image generation** (prompt → image)
- **Prompt iteration for style/composition control**
- **Image variation / editing-style flows** (where supported by your deployment and the notebook code)
- **Working with provided input images** and saving generated results

> Note: Available features and parameters can vary depending on your Azure deployment, API version, and any policy/safety settings applied to your resource.

---

This folder contains **Python/Jupyter notebooks** showcasing **`gpt-image-2`** capabilities using **Azure AI Foundry / Azure OpenAI**.

> Notebooks are split into 3 parts:
- **Part 1**: first steps + core image generation
- **Part 2**: more scenarios / prompt patterns
- **Part 3**: advanced scenarios and end-to-end examples

---

## Contents

### Notebooks
- [`gpt image 2 with Microsoft Foundry - Part 1.ipynb`](./gpt%20image%202%20with%20Microsoft%20Foundry%20-%20Part%201.ipynb)
- [`gpt image 2 with Microsoft Foundry - Part 2.ipynb`](./gpt%20image%202%20with%20Microsoft%20Foundry%20-%20Part%202.ipynb)
- [`gpt image 2 with Microsoft Foundry - Part 3.ipynb`](./gpt%20image%202%20with%20Microsoft%20Foundry%20-%20Part%203.ipynb)

### Configuration
- [`azure.env`](./azure.env) – environment variable template (copy/rename it to `.env` or load it in your notebook environment)

### Assets
- [`animation.gif`](./animation.gif)
- [`input/`](./input) – sample input images used by some notebook cells:
  - `cat.jpg`
  - `clothes.jpg`
  - `nyc.jpg`
  - `plot.png`
- [`images/`](./images) – generated outputs and illustrations saved by the notebooks (many PNG/JPEG examples)

---

## What these notebooks demonstrate

Depending on the part, you will find examples for:
- **Text-to-image generation** (prompt → image)
- **Iterating on prompts** to control style, composition, typography-like content, etc.
- **Image transformation / editing workflows** (when supported by your deployment and code path)
- **Working with input images** (see `./input`)
- **Saving outputs** to disk (see `./images`)
- **Building small “story” / multi-step generations** (see storyboard-like outputs in `./images`)

---

## Prerequisites

1. **Azure subscription**
2. Access to **Azure AI Foundry / Azure OpenAI**
3. A deployed model endpoint for **`gpt-image-2`**
4. Python environment capable of running Jupyter notebooks (local, VS Code, or hosted)

---

## Setup

### 1) Create your environment variables

Use `azure.env` as a starting point.

Typical values you’ll need (names may vary depending on your code):
- Azure OpenAI / Foundry endpoint
- API key (or Entra ID auth, if you use it)
- API version
- Deployment name (your `gpt-image-2` deployment)

Example (illustrative):
```bash
AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-key>"
AZURE_OPENAI_API_VERSION="2024-xx-xx"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-image-2"
```

> If your notebooks use a different variable naming convention, keep the notebook’s variable names and update your `.env` accordingly.

### 2) Install dependencies

Install common notebook dependencies (adjust if your notebooks specify others):
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -U pip
pip install notebook ipykernel python-dotenv requests pillow matplotlib
```

### 3) Run the notebooks

From the repository root:
```bash
jupyter notebook
```

Open the notebooks in order:
1. **Part 1**
2. **Part 2**
3. **Part 3**

---

## Tips

- Some generations can be **slow** and/or **rate-limited** depending on your quota.
- If you re-run cells multiple times, consider saving outputs with unique names (the notebooks already appear to do this—see `./images` filenames with timestamps).
- Keep your keys out of Git history: prefer `.env` and add it to `.gitignore` (do not commit secrets).

---

## Gallery (examples)

- Animation example: [`animation.gif`](./animation.gif)
- Example outputs live in [`./images`](./images)

---

## Microsoft / Azure resources

- Introducing OpenAI's GPT-image-2 in Microsoft Foundry: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openais-gpt-image-2-in-microsoft-foundry/4500571
- Microsoft Foundry model catalog: https://ai.azure.com/catalog/models
- Azure AI Foundry documentation (image generation tool): https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/foundry/agents/how-to/tools/image-generation.md

---

## License / Responsible AI

Use these demos in accordance with:
- your organization’s policies,
- Azure OpenAI / Azure AI Foundry terms,
- and any applicable Responsible AI guidelines (content, safety, and data handling).

---

## Author

| Field | Details |
| --- | --- |
| Name | Serge Retkowsky |
| Email | serge.retkowsky@microsoft.com |
| LinkedIn | https://www.linkedin.com/in/serger/ |
| Medium publications | https://medium.com/@sergems18/ |
