import os
import re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

def get_hf_token():
    # Prefer environment variable for cloud deployment
    token = os.environ.get("HF_TOKEN") or os.environ.get("HF_API_KEY")
    if not token:
        raise RuntimeError("Hugging Face token not found in environment variable 'HF_TOKEN' or 'HF_API_KEY'. Please set it in your deployment secrets or environment.")
    return token

def get_cleaning_suggestions_hf(data_issues, columns, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
    """
    Use Meta-Llama-3-8B-Instruct via Hugging Face InferenceClient to get cleaning suggestions.
    Returns a single Markdown-formatted string with clear headings and fenced Python code blocks.
    """
    try:
        hf_token = get_hf_token()
        os.environ["HF_TOKEN"] = hf_token

        client = InferenceClient(provider="novita", api_key=hf_token)

        system_prompt = (
            "You are an expert data-cleaning assistant. Return a clean, readable Markdown manual of issues.\n"
            "For each issue, follow EXACTLY this structure and formatting (use headings, bold labels, and fenced code):\n\n"
            "### Issue 1: <Concise Title>\n\n"
            "**Why this needs to be fixed:**\n<Short, direct explanation in 1-3 sentences>\n\n"
            "**Code:**\n"
            "```python\n<Pure, runnable Python code only. No comments outside code.>\n```\n\n"
            "**Result:**\n<Expected outcome in 1-2 sentences>\n\n"
            "Then continue with '### Issue 2:', etc. Do not include extra sections or raw prose."
        )

        user_prompt = (
            "Dataset Analysis Context:\n"
            f"Columns: {columns}\n"
            f"Data Issues Found: {data_issues}\n\n"
            "Produce the Markdown manual now. Start directly with '### Issue 1:'."
        )

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2500,
            temperature=0.2,
        )

        md = (
            completion.choices[0].message.content.strip()
            if hasattr(completion.choices[0].message, "content")
            else str(completion.choices[0].message)
        )

        # Light cleanup: ensure python fences aren't duplicated and strip stray triple backticks
        md = re.sub(r"```python\s*```", "", md)
        return md

    except Exception as e:
        print(f"An error occurred in get_cleaning_suggestions_hf: {e}")
        # Fallback to a minimal Markdown example
        return (
            "### Issue 1: Handling Missing Values\n\n"
            "**Why this needs to be fixed:**\nMissing values can affect model accuracy and create bias.\n\n"
            "**Code:**\n```python\nimport pandas as pd\ndf['Age'].fillna(df['Age'].median(), inplace=True)\nprint('Missing values:', df['Age'].isnull().sum())\n```\n\n"
            "**Result:**\nAge column will have no missing values."
        )

def get_default_suggestions():
    """Returns a list of default fallback suggestions in the correct format."""
    return [
        "Issue 1: Handling Missing Values\n\nWhy this needs to be fixed:\nMissing values can affect model accuracy and create bias.\n\nCode:\nimport pandas as pd\ndf['Age'].fillna(df['Age'].median(), inplace=True)\nprint('Missing values:', df['Age'].isnull().sum())\n\nResult:\nAge column will have no missing values.",
        "Issue 2: Remove Duplicate Rows\n\nWhy this needs to be fixed:\nDuplicate entries can skew analysis and model training.\n\nCode:\nimport pandas as pd\nprint('Duplicates found:', df.duplicated().sum())\ndf.drop_duplicates(inplace=True)\nprint('Dataset shape after removal:', df.shape)\n\nResult:\nClean dataset without duplicate entries.",
    ]

def get_data_story_hf(df_head: str, df_describe: str, columns: list, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
    """
    Generates a data story using a Hugging Face model.
    """
    try:
        hf_token = get_hf_token()
        client = InferenceClient(provider="novita", api_key=hf_token)

        system_prompt = (
            "You are a senior data analyst and an expert storyteller. Your task is to analyze the provided dataset summary "
            "and write a compelling, easy-to-understand narrative for a non-technical audience. "
            "Focus on the key insights, trends, potential outliers, and interesting relationships between variables. "
            "Structure your story logically. Start with a high-level overview, then dive into specific, noteworthy findings. "
            "Conclude with a summary of the most important takeaways or potential next steps for analysis. "
            "Do NOT produce Python code. Generate a narrative story only."
        )

        user_prompt = (
            "Here is a summary of the dataset I am analyzing:\n\n"
            f"First 5 rows:\n{df_head}\n\n"
            f"Descriptive Statistics:\n{df_describe}\n\n"
            f"Columns: {columns}\n\n"
            "Please generate a data story based on this information."
        )

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1500,
            temperature=0.5, # Slightly higher temperature for more creative storytelling
        )
        
        story = completion.choices[0].message.content.strip() if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
        return story

    except Exception as e:
        print(f"An error occurred in get_data_story_hf: {e}")
        return "Error: Could not generate the data story. Please check the logs."

def get_visualization_suggestion_hf(columns: list, df_head: str, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
    """
    Generates a data visualization suggestion using a Hugging Face model.
    """
    try:
        hf_token = get_hf_token()
        client = InferenceClient(provider="novita", api_key=hf_token)

        system_prompt = (
            "You are a data visualization expert. Your task is to suggest a relevant and insightful "
            "data visualization based on the provided dataset columns and head. "
            "Your output must be a single, clean block of executable Python code using seaborn or matplotlib. "
            "The code should be complete and ready to run, assuming a pandas DataFrame named `df` already exists. "
            "It must include all necessary imports. "
            "Do not add any explanation, narrative, or markdown fences. Do NOT include `pd.read_csv()`. Just the plotting code."
        )

        user_prompt = (
            "Based on the following dataset information, please provide the Python code for a single, meaningful visualization. "
            "Assume the data is already loaded into a pandas DataFrame called `df`.\n\n"
            f"Columns: {columns}\n\n"
            f"First 5 rows:\n{df_head}\n\n"
            "Provide only the runnable Python code for the plot. Do not include `pd.read_csv()`."
        )

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.2,
        )
        
        code = completion.choices[0].message.content.strip()
        
        # Clean the output to ensure it's just code
        code = re.sub(r"```python", "", code)
        code = re.sub(r"```", "", code)
        
        return code.strip()

    except Exception as e:
        print(f"An error occurred in get_visualization_suggestion_hf: {e}")
        return "import matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Error generating suggestion. Please check logs.\nplt.figure()\nplt.title('Error Generating Plot')\nplt.show()"

def get_chat_response_hf(message: str, history: list, columns: list, df_head: str, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
    """
    Generates a conversational response using a Hugging Face model, maintaining context.
    """
    try:
        hf_token = get_hf_token()
        client = InferenceClient(provider="novita", api_key=hf_token)

        system_prompt = (
            "You are a friendly and helpful data analyst chatbot. Your role is to assist users in understanding and exploring their dataset. "
            "You have access to the dataset's column names and the first few rows. "
            "When a user asks for a visualization, provide the Python code (using seaborn or matplotlib) in a clean, executable block. "
            "Assume the data is in a pandas DataFrame named `df`. Do NOT include `pd.read_csv()` in your code. "
            "For other questions, provide clear, concise answers based on the provided data context."
        )

        # Format the history for the prompt
        formatted_history = "\n".join([f"User: {h[0]}\nAssistant: {h[1]}" for h in history])

        user_prompt = (
            "Here is the context for our conversation:\n\n"
            f"Dataset Columns: {columns}\n"
            f"First 5 rows of data:\n{df_head}\n\n"
            "--- Conversation History ---\n"
            f"{formatted_history}\n\n"
            "--- Current Question ---\n"
            f"User: {message}\n"
            "Assistant:"
        )

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1500,
            temperature=0.4,
        )
        
        response = completion.choices[0].message.content.strip() if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
        return response

    except Exception as e:
        print(f"An error occurred in get_chat_response_hf: {e}")
        return "Error: I'm having trouble connecting to my brain right now. Please try again in a moment."
