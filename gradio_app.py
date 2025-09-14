API_SUGGEST_URL = "http://127.0.0.1:8000/suggest-cleaning"
API_CHAT_URL = "http://127.0.0.1:8000/chat"
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
            # Backend now returns a single Markdown string
            suggestions_md = resp.json().get("suggestions", "")
            return suggestions_md or "No suggestions generated."
        else:
            return f"API error: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"
# Entry point for the Gradio UI
import gradio as gr
import httpx
import pandas as pd
import ast

API_ANALYZE_URL = "http://127.0.0.1:8000/analyze-csv"


if __name__ == "__main__":
    # Force wrapping and remove horizontal scrolling for suggestions
    css = """
    .sugg { white-space: pre-wrap; word-break: break-word; overflow-x: hidden; }
    .scroll-story { height: 24rem; overflow-y: auto; padding: 1rem; border: 1px solid #E5E7EB; border-radius: 4px; }
    .scroll-suggestions { height: 24rem; overflow-y: auto; padding: 1rem; border: 1px solid #E5E7EB; border-radius: 4px; }
    """
    with gr.Blocks(css=css, title="AI Data Analyst Agent") as demo:
        # Add a hidden state component to store the uploaded file path
        filepath_state = gr.Textbox(visible=False)
        
        gr.Markdown("# AI Data Analyst Agent\nUpload a CSV to detect issues, get AI cleaning code, generate stories, visualizations, and chat with an analyst.")
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
        # Render markdown with scrollable container for better readability
        suggestions_out = gr.Markdown(label="AI Cleaning Suggestions", elem_classes=["scroll-suggestions"])
        suggest_btn.click(fn=get_ai_suggestions, inputs=[issues_hidden, columns_hidden], outputs=suggestions_out, show_progress=True)

        gr.Markdown("---")
        gr.Markdown("## AI Data Storytelling")
        story_btn = gr.Button("Generate Data Story")
        story_out = gr.Markdown(label="Data Story", elem_classes=["scroll-story"])

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
        gr.Markdown("## AI Visualization Suggestion")
        with gr.Row():
            viz_btn = gr.Button("Suggest a Visualization")
        with gr.Row():
            viz_plot = gr.Plot(label="Suggested Visualization")
            viz_code = gr.Code(label="Visualization Code", language="python")

        def get_ai_visualization(filepath, columns_str):
            if not filepath:
                return None, "Please analyze a file first."
            
            try:
                # Read dataframe to get head
                df = pd.read_csv(filepath)
                df_head = df.head().to_string()
                columns = ast.literal_eval(columns_str)

                # Call the new backend endpoint
                with httpx.Client(timeout=None) as client:
                    resp = client.post(
                        "http://127.0.0.1:8000/suggest-visualization",
                        json={"columns": columns, "df_head": df_head}
                    )
                
                if resp.status_code == 200:
                    code = resp.json().get("visualization_code")
                    
                    # Execute the code to generate the plot
                    # The code should define a 'fig' variable or just show the plot
                    # We need to capture the plot object. A simple way is to exec
                    # and assume it creates a figure.
                    
                    # Create a space for the code to execute in
                    local_scope = {}
                    # The code expects a dataframe 'df'
                    local_scope['df'] = df
                    
                    # Redirect stdout to capture any prints if needed
                    from io import StringIO
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = captured_output = StringIO()
                    
                    exec(code, globals(), local_scope)
                    
                    sys.stdout = old_stdout # Restore stdout
                    
                    # Gradio's gr.Plot can take a matplotlib figure object
                    # We assume the executed code creates a figure on plt
                    import matplotlib.pyplot as plt
                    fig = plt.gcf()
                    
                    # If the figure is empty, it might be a seaborn plot that needs drawing
                    if not fig.axes:
                        # This is a bit of a hack, but seaborn plots often just need plt.show()
                        # to be drawn onto the current figure.
                        plt.tight_layout()

                    return fig, code
                else:
                    return None, f"API error: {resp.status_code}"

            except Exception as e:
                return None, f"Error generating visualization: {e}"

        viz_btn.click(
            fn=get_ai_visualization,
            inputs=[filepath_state, columns_hidden],
            outputs=[viz_plot, viz_code],
            show_progress=True
        )

        gr.Markdown("---")
        gr.Markdown("## Data Analyst Chatbot")
        chatbot = gr.Chatbot(label="Chat with your Data Analyst")
        msg = gr.Textbox(label="Ask a question about your data...")
        clear = gr.Button("Clear Chat")

        def user_chat(user_message, history):
            return "", history + [[user_message, None]]

        def bot_response(history, filepath, columns_str):
            if not filepath:
                history[-1][1] = "Please upload and analyze a file before starting a chat."
                return history

            user_message = history[-1][0]
            
            try:
                df = pd.read_csv(filepath)
                df_head = df.head().to_string()
                columns = ast.literal_eval(columns_str)

                with httpx.Client(timeout=None) as client:
                    resp = client.post(
                        API_CHAT_URL,
                        json={
                            "message": user_message,
                            "history": history[:-1], # Send history without the current question
                            "columns": columns,
                            "df_head": df_head,
                        }
                    )
                
                if resp.status_code == 200:
                    bot_message = resp.json().get("response", "Sorry, I didn't get a response.")
                else:
                    bot_message = f"API Error: {resp.status_code}"

            except Exception as e:
                bot_message = f"An error occurred: {e}"

            history[-1][1] = bot_message
            return history

        msg.submit(user_chat, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot_response, [chatbot, filepath_state, columns_hidden], chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
    demo.launch()
