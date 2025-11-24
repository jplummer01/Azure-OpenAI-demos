# AI Podcast Generation with Azure AI

This project demonstrates how to generate audio and video podcasts using Azure AI services. It is based on the Python notebook [`Audio and video podcast generation with Azure AI.ipynb`](https://github.com/retkowsky/Azure-AIGEN-demos/blob/main/AI%20podcast%20generation/Audio%20and%20video%20podcast%20generation%20with%20Azure%20AI.ipynb), which walks through the process of creating and synthesizing podcast episodes with both textual and multimedia output.

![Podcast Demo](podcast.jpg)

## Features

- **Podcast Generation**: Automates the creation of podcast scripts using Azure AI.
- **Audio and Video Output**: Generates both audio and video versions of the podcasts.
- **Multimodal AI Services**: Integrates Azure AI for speech synthesis and content creation.
- **Environment Configuration**: Uses an `azure.env` example file for managing Azure keys and endpoints.
- **Outputs**: Stores generated podcasts in the `outputs` folder and sources in the `documents` folder.

## Folder Structure

- `Audio and video podcast generation with Azure AI.ipynb`: Main Jupyter notebook containing the code and workflow.
- `azure.env`: Environment file for Azure credentials (fill with your own).
- `documents/`: Folder to store podcast scripts or documents as input.
- `outputs/`: Folder where generated podcast files will be saved.
- `podcast.jpg`: Example image representing the podcast demo.

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/retkowsky/Azure-AIGEN-demos.git
   cd Azure-AIGEN-demos/AI podcast generation
   ```

2. **Set up Azure Credentials**

   - Copy `azure.env` and enter your Azure OpenAI keys and endpoints.

3. **Run the Notebook**

   - Open `Audio and video podcast generation with Azure AI.ipynb` with Jupyter or VSCode.
   - Follow the steps in the notebook to generate podcasts.

## Requirements

- Python 3.x
- Azure OpenAI API access
- Jupyter Notebook

See the notebook for specific package requirements.

## Usage

- Use your own scripts or text documents in the `documents` folder.
- Generated podcasts (audio/video) will be saved in the `outputs` folder.

## License

This project is for educational demo purposes.

---

For more information and demos, visit the [Azure-AIGEN-demos repository](https://github.com/retkowsky/Azure-AIGEN-demos/tree/main/AI%20podcast%20generation).