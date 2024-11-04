# Idea Maker

Idea Maker is a Python application that automates the process of generating software project ideas, researching them, designing schemas, generating unit tests, suggesting deployment strategies, and compiling everything into a PDF document.

## Features

- Generates new and interesting software project ideas.
- Researches project ideas using DuckDuckGo Search.
- Designs project schemas with detailed tools, technologies, and architecture.
- Generates unit tests for the project's codebase.
- Provides deployment strategies, including CI/CD pipelines and best practices.
- Compiles all information into a neatly formatted PDF document.

## Requirements

- Python 3.x
- [Poetry](https://python-poetry.org/) for dependency management.
- [ollama](https://ollama.ai/) installed and configured.
- OpenAI API Key, Model Name, and Base URL set in environment variables.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd idea_maker
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   ```

3. **Set required environment variables:**

   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export OPENAI_MODEL_NAME='your-openai-model-name'
   export OPENAI_BASE_URL='your-openai-base-url'
   ```

   Alternatively, you can run the provided 

run.sh

 script:

   ```bash
   ./run.sh
   ```

4. **Ensure `ollama` is installed and the required model is built:**

   ```bash
   ollama build llama3.2
   ```

## Usage

Run the application with optional arguments for theme, output file, and model:

```bash
python idea_maker/app.py --theme "Your Theme" --output "output.pdf" --model "model_name"
```

- `--theme`: (Optional) Specify a theme for the project idea.
- `--output`: (Optional) Specify the name of the output PDF file. Defaults to 

project_documentation.pdf

.
- `--model`: (Optional) Specify the model to use for the agents. Defaults to `llama3.2`.

**Example:**

```bash
python idea_maker/app.py --theme "Artificial Intelligence" --output ai_project.pdf --model llama3.2
```

## How It Works

1. **Idea Generation:** Uses the `Idea Assistant` agent to generate a new software project idea based on the provided theme.

2. **Key Term Extraction:** Extracts key terms from the project idea using the `extract_key_terms` function in 

app.py

.

3. **Research:** Employs the `Research Assistant` agent to search the internet for information related to the key terms.

4. **Design:** Utilizes the `Design Assistant` agent to create a detailed project schema.

5. **Testing:** Calls upon the `Testing Assistant` agent to generate unit tests based on the project design.

6. **Deployment:** Engages the `Deployment Assistant` agent to suggest deployment strategies and best practices.

7. **Documentation:** Compiles all the information into a markdown file and converts it into a PDF using `markdown_pdf`.


## License

This project is licensed under the MIT License.