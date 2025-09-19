import gradio as gr
from query_bot import query_chroma, ask_llm

def full_pipeline(user_question):
    context_docs = query_chroma(user_question)
    context_text = "\n".join(context_docs)
    
    if not context_text.strip() or context_text.strip() == "(No relevant context found)":
        context_text = "Sorry, I couldn't find any relevant information in my database."
    
    answer = ask_llm(user_question, context_text)
    return answer

iface = gr.Interface(
    fn = full_pipeline,
    inputs = gr.Textbox(
        label = "Ask a question about PGA Tour players. Be specific! This is a work in progress so it may struggle with vague questions.",
        placeholder = "eg. Which player has the highest sand save percentage?"
    ),
    outputs = gr.Textbox(
        label = "Answer"
    ),
    title = "PGA Tour Player Stats Chatbot",
    description = "Ask questions about PGA Tour players' stats. Powered by ChromaDB and Mistral LLM.",
)

iface.launch(share=True)