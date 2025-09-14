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
    Uses Meta-Llama-3-8B-Instruct via huggingface_hub InferenceClient to get cleaning suggestions.
    This version includes a robust parsing mechanism to handle inconsistent and repetitive model output.
    """
    try:
        hf_token = get_hf_token()
        os.environ["HF_TOKEN"] = hf_token
        
        client = InferenceClient(
            provider="novita",
            api_key=hf_token,
        )
        
        system_prompt = (
            "You are an expert data-cleaning assistant. Your output MUST be a numbered manual of issues. "
            "Format each issue EXACTLY as:\n\n"
            "Issue 1: <Concise Title>\n"
            "Why this needs to be fixed:\n<Explanation>\n"
            "Code:\n<Pure, runnable Python code ONLY. No comments, no narrative, no markdown.>\n"
            "Result:\n<Expected outcome>\n\n"
            "Then 'Issue 2:', etc. Do NOT use 'Task' or 'Suggestion'. Do NOT include markdown fences."
        )
        
        user_prompt = (
            f"Dataset Analysis:\nColumns: {columns}\nData Issues Found: {data_issues}\n\n"
            "Produce a numbered manual of data cleaning issues based on the analysis. "
            "Start directly with 'Issue 1:'. Follow the specified format strictly."
        )
        
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2500,
            temperature=0.3,
        )
        
        response_text = completion.choices[0].message.content.strip() if hasattr(completion.choices[0].message, 'content') else str(completion.choices[0].message)
        
        # --- Overhauled Parsing Logic ---
        
        # Split the entire response into blocks based on "Issue X:"
        # This is more robust against malformed content between issues.
        issue_blocks = re.split(r'Issue \d+:', response_text)
        if len(issue_blocks) > 1:
            issue_blocks = issue_blocks[1:] # The first element is usually empty or intro text
        
        final_suggestions = []
        for i, block in enumerate(issue_blocks, 1):
            # Extract all content for each section, case-insensitively, across the entire block
            titles = [t.strip() for t in re.findall(r'^(.*?)(?:\nWhy this needs to be fixed:|\nCode:|\nResult:|$)', block, re.IGNORECASE | re.MULTILINE)]
            whys = [w.strip() for w in re.findall(r'Why this needs to be fixed:(.*?)(?:\nCode:|\nResult:|$)', block, re.IGNORECASE | re.DOTALL)]
            codes = [c.strip() for c in re.findall(r'Code:(.*?)(?:\nResult:|$)', block, re.IGNORECASE | re.DOTALL)]
            results = [r.strip() for r in re.findall(r'Result:(.*?)$', block, re.IGNORECASE | re.DOTALL)]

            # --- Deduplicate and Clean Each Section ---
            
            # 1. Title: Find the first non-empty, meaningful title
            final_title = f"Untitled Issue {i}"
            for title in titles:
                if title:
                    clean_title = re.sub(r'(?i)^Data\s*Cleaning\s*Suggestion\s*\d*:\s*', '', title).strip()
                    if not re.fullmatch(r'(?i)Data\s*Cleaning\s*Suggestions?', clean_title, re.IGNORECASE):
                        final_title = clean_title
                        break

            # 2. Why: Join all unique 'why' explanations
            unique_whys = list(dict.fromkeys(w for w in whys if w))
            final_why = "\n".join(unique_whys).strip()

            # 3. Code: Join unique code blocks and strip out any narrative or comments
            unique_codes = list(dict.fromkeys(c for c in codes if c))
            code_lines = []
            for code_block in unique_codes:
                for line in code_block.split('\n'):
                    stripped_line = line.strip()
                    # A line is considered code if it contains common Python keywords/patterns.
                    # This filters out narrative text that sometimes gets mixed in.
                    is_code = (
                        stripped_line and not stripped_line.startswith('#') and 
                        any(kw in stripped_line for kw in ['import ', 'pd.', 'np.', '=', 'df[', 'print('])
                    )
                    if is_code:
                        code_lines.append(line)
            final_code = "\n".join(code_lines).strip()

            # 4. Result: Join all unique, non-empty 'result' explanations
            unique_results = list(dict.fromkeys(r for r in results if r and r.upper() != 'RESULT:'))
            final_result = "\n".join(unique_results).strip()

            # --- Assemble Final Output for the Issue ---
            
            # Only add the issue if it has some content besides a title
            if final_why or final_code:
                parts = [f"Issue {i}: {final_title}"]
                if final_why:
                    parts.append(f"Why this needs to be fixed:\n{final_why}")
                if final_code:
                    parts.append(f"Code:\n{final_code}")
                if final_result:
                    parts.append(f"Result:\n{final_result}")
                
                final_suggestions.append("\n\n".join(parts))

        return final_suggestions if final_suggestions else get_default_suggestions()

    except Exception as e:
        print(f"An error occurred in get_cleaning_suggestions_hf: {e}")
        return get_default_suggestions()

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
