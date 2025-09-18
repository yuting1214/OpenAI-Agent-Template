"""
Gradio UI Application

Gradio Blocks UI for the AI agent interface.
"""
import gradio as gr

def build_product_catalog_ui():

    def greet(name, intensity):
        return "Hello, " + name + "!" * int(intensity)

    demo = gr.Interface(
        fn=greet,
        inputs=["text", "slider"],
        outputs=["text"],
    )

    return demo
