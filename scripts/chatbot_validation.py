## Imports
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# Adjust sys.path to correctly import project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.llm_local_interface import ask_llm
from app.query_executor import execute_query


## Functions
def extract_all_numbers(text):
    """
    Extract all integers from the given text (not necessarily sorted).
    """
    return [int(x.replace(',', '')) for x in re.findall(r'\d[\d,]*', text)]


def contains_all_values(ans, expected, min_overlap=0.6):
    """
    Returns True if all expected numbers and locations are present in the answer, and year (if required).
    This is a robust semantic match for answers with the same factual content, even if phrasing/order changes.
    """
    ans_norm = re.sub(r'[^\w\s]', '', ans.lower())
    expected_norm = re.sub(r'[^\w\s]', '', expected.lower())
    nums_ans = set(extract_all_numbers(ans_norm))
    nums_expected = set(extract_all_numbers(expected_norm))
    locs_expected = set(re.findall(r'community area \d+', expected_norm))
    locs_ans = set(re.findall(r'community area \d+', ans_norm))
    years_expected = set(re.findall(r'\b20\d{2}\b', expected_norm))
    years_ans = set(re.findall(r'\b20\d{2}\b', ans_norm))
    has_all_numbers = nums_expected.issubset(nums_ans)
    has_all_locs = locs_expected.issubset(locs_ans)
    has_year = (not years_expected) or years_expected.issubset(years_ans)
    return has_all_numbers and has_all_locs and has_year


def run_validation(df, prompt_template):
    """
    Runs the chatbot for each question in the validation set.
    Returns a list with each chatbot answer in natural language.
    """
    chatbot_responses = []
    for q in df['question']:
        full_prompt = prompt_template.replace("{question}", q)
        code = ask_llm(full_prompt)
        response = execute_query(code, df_data)
        chatbot_responses.append(response)
    return chatbot_responses


## Loads
# Load the filtered crime data
df_data = pd.read_csv("data/crime_filtered.csv")

# Load the prompt template
with open("app/prompt_template.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read().strip()


## Main
if __name__ == "__main__":
    # Load validation CSV
    validation_file = "data/validation_set.csv"
    df = pd.read_csv(validation_file)

    # Run validation
    print ("\nAnalyzing chatbot responses...\n")
    df['chatbot_answer'] = run_validation(df, prompt_template)
    df['result'] = df.apply(
        lambda row: 'Passed' if contains_all_values(row['chatbot_answer'], row['expected_answer']) else 'Failed',
        axis=1
    )

    # Generate pie chart
    summary = df['result'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(summary, labels=summary.index, autopct='%1.1f%%', startangle=90)
    plt.title("Chatbot Validation Results")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # Print and save the summary report
    report_lines = []
    for i, row in df.iterrows():
        report_lines.append(f"Q{i + 1}: {row['question']}")
        report_lines.append(f"Expected: {row['expected_answer']}")
        report_lines.append(f"Chatbot:  {row['chatbot_answer']}")
        report_lines.append(f"Result:   {row['result']}")
        report_lines.append("-" * 70)
    report_lines.append(f"\nAccuracy: {100 * summary.get('Passed', 0) / len(df):.2f}%")

    report_text = "\n".join(report_lines)
    print(report_text)
    with open("data/validation_results.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
