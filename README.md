# CrimeBot - Crime Insights Chatbot for Chicago

A terminal-based chatbot powered by LLM and pandas, enabling users to ask natural language questions about crime data in Chicago between 2020 and 2022. The bot interprets questions, generates Python code via an LLM, executes queries on a filtered dataset, and returns clear, human-readable answers.

---

## Features

- Natural language Q&A about Chicago crimes (2020–2022).
- Handles questions involving crime types, years, locations (district, ward, community area), arrests, and domestic cases.
- Automatically generates and runs code using an open-source LLM (Ollama local inference, e.g. Mistral, Gemma).
- Returns well-formatted English answers, not raw code or numbers.
- Validation set and report for accuracy tracking.

---

## Project Structure

```
LLM-chatbot/
├── app/
│ ├── init.py
│ ├── main.py # Main chatbot script (run here!)
│ ├── llm_local_interface.py # Interface to call LLM locally (Ollama Mistral)
│ ├── query_executor.py # Runs generated code on the DataFrame
│ └── prompt_template.txt # Prompt rules and examples for the LLM
├── data/
│ ├── crime_filtered.csv # Filtered crime dataset (2020–2022)
│ ├── validation_set.csv # Validation questions-answers
│ └── validation_results.txt # Results (generated after validation)
├── scripts/
│ ├── build_clean_dataset.py # Script to load, filter and clean the dataset
│ └── chatbot_validation.py # Script to run automated validation
├── src/
│ ├── cleaner.py # Cleans and standardizes relevant fields
│ └── data_loader.py # Loads and filter complete dataset
├── README.md
└── requirements.txt # Dependencies
```

## Setup Instructions

1. Clone this repository
2. Install Python 3.9 or higher. The project is tested with Python 3.10

3. Install [Ollama](https://ollama.com/)
    - For Windows/Mac: download from [https://ollama.com/](https://ollama.com/)

4. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Pull the LLM model you want to use (e.g. Mistral):
    ```bash
    ollama pull mistral
    ```
    **Note:** Running the Mistral model locally with Ollama requires at least 8GB of RAM.


## Dataset

- The original, unfiltered Chicago crime dataset can be downloaded from the City of Chicago open data portal:

  - [Crimes - 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)


- This project uses a **filtered version** (`data/crime_filtered.csv`) containing only records from 2020 to 2022 and the relevant columns. You may generate your own filtered dataset using the original file and the included data filtering script `scripts/build_clean_dataset.py`:
  - Download the original dataset, named ´crime_raw.csv´, and place it in the ´data/´ folder.

  - Run the filtering and cleaning script: ```scripts/build_clean_dataset.py ```
  - This script will:
    - Load the original CSV from data/crime_raw.csv
    - Filter it for the years 2020–2022
    - Select and clean only the relevant columns for the chatbot
    - Save the result as data/crime_filtered.csv

**Note:**
The filtering logic relies on `src/cleaner.py` and `src/data_loader.py`.
You can modify these scripts to adapt for different columns as needed.

## Running CrimeBot

From the root directory, run:
```bash
    python app/main.py
```

The bot will greet you, ask your name, and prompt you for questions.

Type questions about Chicago crime (e.g., `"How many robberies occurred in 2022 in ward 8?"`).

To exit, type `'exit'` or `'quit'`.

## Validation
To check accuracy against the reference validation set:
```bash
    python scripts/chatbot_validation.py
```
This script will generate a pie chart and save a summary of each question-answer pair and the total accuracy in the `data/validation_results.txt` file.

## Example Questions

- "How many thefts were reported in 2021?"
- "Compare the number of assaults between community area 12 and 14 in 2022."
- "How many crimes involving children resulted in arrest in 2021 in district 1?"
- "How many battery crimes happened in ward 28?"

**Note:** If you do not specify a year in your question, the chatbot will automatically return the total for the entire available period (2020 to 2022).


## Out-of-Scope Questions
Questions that fall outside the chatbot’s scope will be **automatically rejected** with a message: `“Sorry, I cannot answer this question. My scope is limited to crime information that occurred in Chicago between 2020 and 2022.”`

If the user asks about crimes outside the supported date range (e.g., before 2020 or after 2022), the chatbot will reply:
`"Sorry, I am only trained to answer questions about crimes in Chicago between 2020 and 2022."`

If the user asks an in-scope question but the chatbot cannot interpret it, it will respond:
`"I didn't understand that. Could you rephrase your question?"`

### Examples of unsupported or misunderstood questions:

- `"How to reduce crime rates?"`
→ `"Sorry, I cannot answer this question. My scope is limited to crime information that occurred in Chicago between 2020 and 2022."`

- `"How many assaults were reported in 2018?"`
→ `"Sorry, I am only trained to answer questions about crimes in Chicago between 2020 and 2022."`

- `"What is the population of prisoners in Chicago?"`
→ `"I didn't understand that. Could you rephrase your question?"`

## Customization
To switch between LLMs (e.g., Gemma or Mistral), change the DEFAULT_MODEL variable in `app/llm_local_interface.py`.

You can update or tune prompt rules in `app/prompt_template.txt`.




