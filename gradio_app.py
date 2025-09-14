API_SUGGEST_URL = "http://127.0.0.1:8000/suggest-cleaning"
def analyze_csv(file):
    if file is None:
        return "No file uploaded.", None, None, None, None
    try:
        # The file object has a .name attribute with the temp path
        filepath = file.name
        with open(filepath, "rb") as f:
            files = {"file": (filepath, f, "text/csv")}
            with httpx.Client(timeout=None) as client:
                resp = client.post(API_ANALYZE_URL, files=files)
        if resp.status_code == 200:
            response_data = resp.json()
            issues = response_data.get("issues", {})
            columns = response_data.get("columns", [])
            
            # Prepare summary for display
            summary = ""
            for k, v in issues.items():
                summary += f"**{k.replace('_', ' ').title()}**: {v if v else 'None'}\n\n"
            
            # Return the filepath to be stored in state
            return summary, columns, str(issues), str(columns), filepath
        else:
            return f"API error: {resp.status_code}", None, None, None, None
    except Exception as e:
        return f"Error: {e}", None, None, None, None

def get_ai_suggestions(issues_str, columns_str):
    import ast
    try:
        issues = ast.literal_eval(issues_str)
        columns = ast.literal_eval(columns_str)
    except Exception:
        return "Could not parse issues/columns for AI suggestions."
    try:
        with httpx.Client(timeout=None) as client:
            resp = client.post(API_SUGGEST_URL, json={"issues": issues, "columns": columns})
        if resp.status_code == 200:
            suggestions = resp.json().get("suggestions", [])
            # Join suggestions into a single wrapped block of text (no markdown code blocks)
            if isinstance(suggestions, list):
                return "\n\n".join(suggestions)
            return str(suggestions)
        else:
            return f"API error: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"
# Entry point for the Gradio UI
import gradio as gr
import httpx
import pandas as pd
import ast

API_PING_URL = "http://127.0.0.1:8000/ping"
API_ANALYZE_URL = "http://127.0.0.1:8000/analyze-csv"


def check_api():
    try:
        with httpx.Client(timeout=None) as client:
            resp = client.get(API_PING_URL)
        if resp.status_code == 200:
            return resp.json()["message"]
        else:
            return f"API error: {resp.status_code}"
    except Exception as e:
        return f"Connection failed: {e}"


if __name__ == "__main__":
    # Force wrapping and remove horizontal scrolling for suggestions
    css = ".sugg { white-space: pre-wrap; word-break: break-word; overflow-x: hidden; }"
    with gr.Blocks(css=css) as demo:
        # Add a hidden state component to store the uploaded file path
        filepath_state = gr.Textbox(visible=False)
        
        gr.Markdown("# AI Data Storyteller & Cleaner\nUpload a CSV to detect data issues and get AI-powered cleaning suggestions.")
        with gr.Row():
            file_input = gr.File(label="Upload CSV", file_types=[".csv"])
            analyze_btn = gr.Button("Analyze Data Issues")
        issues_out = gr.Markdown(label="Detected Issues")
        columns_out = gr.Textbox(label="Columns", visible=False)
        issues_hidden = gr.Textbox(visible=False)
        columns_hidden = gr.Textbox(visible=False)
        
        analyze_btn.click(
            fn=analyze_csv, 
            inputs=file_input, 
            outputs=[issues_out, columns_out, issues_hidden, columns_hidden, filepath_state]
        )

        with gr.Row():
            suggest_btn = gr.Button("Get AI Cleaning Suggestions (Meta Llama 3)")
        # Use a multiline Textbox to avoid horizontal scrolling and keep code readable
        suggestions_out = gr.Textbox(label="AI Cleaning Suggestions", lines=28, show_copy_button=True, elem_classes=["sugg"], interactive=False)
        suggest_btn.click(fn=get_ai_suggestions, inputs=[issues_hidden, columns_hidden], outputs=suggestions_out, show_progress=True)

        gr.Markdown("---")
        gr.Markdown("## AI Data Storytelling")
        story_btn = gr.Button("Generate Data Story")
        story_out = gr.Markdown(label="Data Story")

        def get_ai_story(filepath, columns_str):
            if not filepath:
                return "Please analyze a file first."
            
            try:
                # Use the stored filepath to read the dataframe
                temp_df = pd.read_csv(filepath)
                df_head = temp_df.head().to_string()
                df_describe = temp_df.describe().to_string()
                
                with httpx.Client(timeout=None) as client:
                    resp = client.post(
                        "http://127.0.0.1:8000/generate-story", 
                        json={
                            "df_head": df_head,
                            "df_describe": df_describe,
                            "columns": ast.literal_eval(columns_str)
                        }
                    )
                if resp.status_code == 200:
                    return resp.json().get("story", "No story generated.")
                else:
                    return f"API error: {resp.status_code}"
            except Exception as e:
                return f"Error generating story: {e}"

        story_btn.click(fn=get_ai_story, inputs=[filepath_state, columns_hidden], outputs=story_out, show_progress=True)

        gr.Markdown("---")
        gr.Markdown("## Backend Connectivity Test")
        btn = gr.Button("Check API Status")
        out = gr.Textbox(label="API Response")
        btn.click(fn=check_api, outputs=out)
    demo.launch()
