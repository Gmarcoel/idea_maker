import argparse
import subprocess
import os
from duckduckgo_search import DDGS
from swarm import Swarm, Agent
from markdown_pdf import MarkdownPdf, Section
import re
from collections import Counter

required_env_vars = ["OPENAI_API_KEY", "OPENAI_MODEL_NAME", "OPENAI_BASE_URL"]
missing_env_vars = [var for var in required_env_vars if var not in os.environ]

if missing_env_vars:
    print(f"Error: Missing environment variables: {', '.join(missing_env_vars)}")
    print("Please run the program from run.sh or set the environment variables.")
    exit(1)

try:
    import duckduckgo_search
    import swarm
    import markdown_pdf
except ImportError:
    print("Error: Required dependencies are not installed. Please run 'poetry install' to install dependencies.")
    exit(1)

client = Swarm()
ddgs = DDGS()

def check_ollama_installed() -> bool:
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_model_installed(model: str) -> bool:
    try:
        result = subprocess.run(["ollama", "list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        installed_models = result.stdout.decode().splitlines()
        return any(model in line for line in installed_models)
    except subprocess.CalledProcessError:
        return False

def extract_key_terms(text: str) -> list[str]:
    stop_words = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 
        'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was', 
        'will', 'with'
    ])
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    key_terms = [word for word, count in word_counts.most_common(5)]
    return key_terms

def search_internet(key_terms: list[str]) -> str:
    key_terms = [str(term) for term in key_terms]
    concatenated_string = ''.join(key_terms)
    query = concatenated_string.split(' ')
    query = ' '.join(query)
    print(f"Searching the internet for: {query}")    
    search_results = ddgs.text(query, max_results=5)
    return "\n".join([result['body'] for result in search_results])

def create_agents(model: str) -> dict:
    return {
        "idea_agent": Agent(
            name="Idea Assistant",
            instructions="Generate a new interesting software project idea.",
            model=model,
        ),
        "research_agent": Agent(
            name="Research Assistant",
            instructions="Investigate the advantages and disadvantages of the possible tools to use for developing the project, with recommendations and other similar projects and ideas.",
            functions=[search_internet],
            model=model
        ),
        "design_agent": Agent(
            name="Design Assistant",
            instructions="Design a schema of how the project will be built.",
            model=model
        ),
        "testing_agent": Agent(
            name="Testing Assistant",
            instructions="Generate unit tests for the project's codebase.",
            model=model
        ),
        "deployment_agent": Agent(
            name="Deployment Assistant",
            instructions="Provide deployment strategies for the project, including CI/CD pipelines and best practices.",
            model=model
        ),
        "documentation_agent": Agent(
            name="Documentation Assistant",
            instructions="Write a PDF document with all the information about the project idea, research, design, testing, and deployment.",
            model=model
        )
    }

def run_project_workflow(theme: str | None = None, output_file: str = "project_documentation.pdf", model: str = "llama3.2") -> None:
    if not check_ollama_installed():
        print("Error: 'ollama' is not installed. Please install it and try again.")
        return

    if not check_model_installed(model):
        print(f"Error: Model '{model}' is not installed. Please run 'ollama build {model}' to install it.")
        return

    agents = create_agents(model)

    try:
        print("Running project workflow...")

        idea_prompt = f"Generate a new interesting software project idea (only one) about {theme}." if theme else "Generate a new interesting software project idea (only one)."
        idea_response = client.run(
            agent=agents["idea_agent"],
            messages=[{"role": "user", "content": idea_prompt}],
        )
        project_idea = idea_response.messages[-1]["content"]

        key_terms = extract_key_terms(project_idea)

        research_response = client.run(
            agent=agents["research_agent"],
            messages=[{"role": "user", "content": f"Search the internet for: {key_terms}"}],
        )
        research_info = research_response.messages[-1]["content"]

        design_response = client.run(
            agent=agents["design_agent"],
            messages=[{"role": "user", "content": f"Design a schema for the project: {project_idea}. Talk about the tools, technologies, and architecture. Be very organized."}],
        )
        project_schema = design_response.messages[-1]["content"]

        testing_response = client.run(
            agent=agents["testing_agent"],
            messages=[{"role": "user", "content": f"Generate unit tests for the project based on the design: {project_schema}"}],
        )
        testing_info = testing_response.messages[-1]["content"]

        deployment_response = client.run(
            agent=agents["deployment_agent"],
            messages=[{"role": "user", "content": f"Provide deployment strategies for the project: {project_idea}. Include CI/CD pipelines and best practices."}],
        )
        deployment_info = deployment_response.messages[-1]["content"]

        markdown_content = f"""
# Project Idea
{project_idea}

# Research Information
{research_info}

# Project Schema
{project_schema}

# Testing Information
{testing_info}

# Deployment Strategies
{deployment_info}
"""
        with open("project_documentation.md", "w") as md_file:
            md_file.write(markdown_content)

        pdf = MarkdownPdf()
        pdf.meta["title"] = 'Project Documentation'
        pdf.add_section(Section(markdown_content, toc=False))
        pdf.save(output_file)

        print(f"Project workflow completed and documentation generated: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Run a project workflow to generate, research, design, test, deploy, and document a software project idea.")
    parser.add_argument("--theme", type=str, help="Specific theme for the project idea.")
    parser.add_argument("--output", type=str, default="project_documentation.pdf", help="Name of the output PDF file.")
    parser.add_argument("--model", type=str, default="llama3.2", help="Model to use for the agents.")
    args = parser.parse_args()

    run_project_workflow(theme=args.theme, output_file=args.output, model=args.model)

if __name__ == "__main__":
    main()