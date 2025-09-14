import ollama

def get_cleaning_suggestions_ollama(data_issues, columns, model="llama3"):
    """
    Calls the local Ollama LLM to get cleaning suggestions for the given data issues and columns.
    """
    prompt = f"""
    You are a data cleaning assistant. Given the following data issues and columns, suggest a list of specific, actionable data cleaning steps (in plain English, and if possible, as Python/pandas code snippets). Be concise and practical.

    Columns: {columns}
    Data Issues: {data_issues}
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        text = response.get("message", {}).get("content", "")
        suggestions = [s.strip('- ').strip() for s in text.split('\n') if s.strip()]
        return suggestions
    except Exception as e:
        return [f"Error calling Ollama: {e}"]
