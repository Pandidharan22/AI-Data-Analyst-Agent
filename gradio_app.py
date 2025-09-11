# Entry point for the Gradio UI
import gradio as gr
import httpx

API_URL = "http://127.0.0.1:8000/ping"

def check_api():
    try:
        resp = httpx.get(API_URL)
        if resp.status_code == 200:
            return resp.json()["message"]
        else:
            return f"API error: {resp.status_code}"
    except Exception as e:
        return f"Connection failed: {e}"

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Data Storyteller & Cleaner\nTest FastAPI backend connectivity.")
        btn = gr.Button("Check API Status")
        out = gr.Textbox(label="API Response")
        btn.click(fn=check_api, outputs=out)
    demo.launch()

if __name__ == "__main__":
    main()
