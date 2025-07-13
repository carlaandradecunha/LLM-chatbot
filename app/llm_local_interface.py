## Imports
import subprocess
import re

# Default model for local inference via Ollama
DEFAULT_MODEL = "mistral"  # To switch between LLMs (e.g. gemma:2b), change here


## Functions
def ask_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Sends a prompt to the local LLM via Ollama and returns the generated code.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output = result.stdout.strip()

        # Extract code block
        match = re.search(r"```(?:python)?\n(.*?)```", output, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return output  # fallback: return full output
    except subprocess.CalledProcessError as e:
        return f"[ERROR] LLM execution failed:\n{e.stderr}"
