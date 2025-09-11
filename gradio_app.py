
def analyze_csv(file):
    if file is None:
        return "No file uploaded.", None
    try:
        with open(file.name, "rb") as f:
            files = {"file": (file.name, f, "text/csv")}
            resp = httpx.post(API_ANALYZE_URL, files=files)
        if resp.status_code == 200:
            issues = resp.json()["issues"]
            columns = resp.json().get("columns", [])
            summary = ""
            for k, v in issues.items():
                summary += f"**{k.replace('_', ' ').title()}**: {v if v else 'None'}\n\n"
            return summary, columns
        else:
            return f"API error: {resp.status_code}", None
    except Exception as e:
        return f"Error: {e}", None
# Entry point for the Gradio UI
import gradio as gr
import httpx

API_PING_URL = "http://127.0.0.1:8000/ping"
API_ANALYZE_URL = "http://127.0.0.1:8000/analyze-csv"


def check_api():
    try:
        resp = httpx.get(API_PING_URL)
        if resp.status_code == 200:
            return resp.json()["message"]
        else:
            return f"API error: {resp.status_code}"
    except Exception as e:
        return f"Connection failed: {e}"



    with gr.Blocks() as demo:
        gr.Markdown("# AI Data Storyteller & Cleaner\nUpload a CSV to detect data issues.")
        with gr.Row():
            file = gr.File(label="Upload CSV", file_types=[".csv"])
            analyze_btn = gr.Button("Analyze Data Issues")
        issues_out = gr.Markdown(label="Detected Issues")
        columns_out = gr.Textbox(label="Columns", visible=False)
        analyze_btn.click(fn=analyze_csv, inputs=file, outputs=[issues_out, columns_out])
        gr.Markdown("---")
        gr.Markdown("## Backend Connectivity Test")
        btn = gr.Button("Check API Status")
        out = gr.Textbox(label="API Response")
        btn.click(fn=check_api, outputs=out)
    demo.launch()


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("# AI Data Storyteller & Cleaner\nUpload a CSV to detect data issues.")
        with gr.Row():
            file = gr.File(label="Upload CSV", file_types=[".csv"])
            analyze_btn = gr.Button("Analyze Data Issues")
        issues_out = gr.Markdown(label="Detected Issues")
        columns_out = gr.Textbox(label="Columns", visible=False)
        analyze_btn.click(fn=analyze_csv, inputs=file, outputs=[issues_out, columns_out])
        gr.Markdown("---")
        gr.Markdown("## Backend Connectivity Test")
        btn = gr.Button("Check API Status")
        out = gr.Textbox(label="API Response")
        btn.click(fn=check_api, outputs=out)
    demo.launch()
