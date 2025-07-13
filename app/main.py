## Imports
from llm_local_interface import ask_llm
from query_executor import execute_query
import pandas as pd
import re


## Functions
def load_prompt_template() -> str:
    """
    Loads and returns the full prompt template from the file.
    """
    with open("app/prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, question: str) -> str:
    """
    Builds the prompt by inserting the question into the template.
    """
    return template.replace("{question}", question)


def format_natural_response(question: str, result) -> str:
    """
    Converts the code execution result into a natural language response for the user.
    """
    if isinstance(result, str):
        if result.startswith("[ERROR"):
            return "I didn't understand that. Could you rephrase your question?"
        if result.lower().startswith("outside_scope"):
            return ("Sorry, I cannot answer this question. "
                    "My scope is limited to crime information that occurred in Chicago between 2020 and 2022.")
        return result  # Already a natural language answer
    elif isinstance(result, int):
        return f"There were {result:,} crimes reported."
    else:
        return "I didn't understand that. Could you rephrase your question?"


def is_question_in_scope(question: str, crime_types: set) -> bool:
    """
    Checks if the user's question is within the supported crime types and year range.
    """
    # Extract words from question
    words = re.findall(r'\b\w+\b', question.lower())

    # Check if any crime type appears in the question (whole phrase match)
    crime_mentioned = any(crime in question.lower() for crime in crime_types)

    # Check if year mentioned or user said "chicago"
    year_match = re.search(r"\b(2020|2021|2022)\b", question)

    return crime_mentioned or year_match is not None or "chicago" in question.lower()


## Main
if __name__ == "__main__":
    """
    Runs the main chatbot loop, interacting with the user via the terminal.
    """
    df = pd.read_csv("data/crime_filtered.csv")
    crime_types = set(df['primary_type'].dropna().str.lower().unique())

    print("\nChatbot: Hello, I am CrimeBot, your assistant for crime information in Chicago.")
    print("Chatbot: My scope is limited to crimes that occurred in Chicago between the years 2020 and 2022.")
    print("Chatbot: What is your name?")

    user_name = ""
    while True:
        user_name = input("\nYou: ").strip()
        if 0 < len(user_name) <= 20:
            break
        print("\nChatbot: Please enter a valid name (max 20 characters).")

    print(f"\nChatbot: Hello {user_name}, what would you like to know today?\n")

    template = load_prompt_template()

    while True:
        print("\nEnter your question below or 'exit' to quit. (press Enter to send)")
        question = input(f"{user_name}: ").strip()
        if question.strip().lower() in {"exit", "quit"}:
            print(f"\nChatbot: Goodbye {user_name}!")
            break

        if not is_question_in_scope(question, crime_types):
            print("Chatbot: Sorry, I cannot answer this question. My scope is limited to crime information that occurred in Chicago between 2020 and 2022.\n")
            continue

        prompt = build_prompt(template, question)
        print("\nChatbot: Let me check that...")

        code = ask_llm(prompt)
        result = execute_query(code, df)
        response = format_natural_response(question, result)
        print(f"\nChatbot: {response}\n")
