import os
from flask import Flask, render_template, request
import openai
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import constants

app = Flask(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY
openai.api_key = constants.APIKEY

def reformat_text(input_text, style):
    """
    Uses the LLM to reformat the provided text according to the selected style.
    """
    templates = {
        "Professional": (
            "You are a professional editor. Please reformat the following text, "
            "ensuring that it has proper punctuation, capitalization, and spacing, proper grammar, "
            "and add some slight paraphrasing to make it more professional to meet book editorial standards, "
            "without altering its original meaning significantly. "
            "Return only the reformatted text.\n\n"
            "Text: {text}\n\n"
            "Reformatted text:"
        ),
        "Casual": (
            "You are a friendly editor. Please reformat the following text in a casual tone, "
            "making it easy to read and understand while preserving its original meaning. "
            "Return only the reformatted text.\n\n"
            "Text: {text}\n\n"
            "Reformatted text:"
        ),
        "Academic": (
            "You are an academic editor. Please reformat the following text in a formal academic style, "
            "ensuring proper punctuation, grammar, and a scholarly tone without significantly altering its original meaning. "
            "Return only the reformatted text.\n\n"
            "Text: {text}\n\n"
            "Reformatted text:"
        ),
        "Nigerian": (
            "You are a creative editor who converts text into Nigerian Pidgin English with popular slangs. "
            "Please reformat the following text into lively, informal Nigerian Pidgin English, using well-known local expressions and slangs, "
            "while preserving the original meaning. "
            "Return only the reformatted text.\n\n"
            "Text: {text}\n\n"
            "Reformatted text:"
        )
        
    }
    
    prompt_template = PromptTemplate(
        template=templates.get(style, templates["professional"]),
        input_variables=["text"]
    )
    
    # Set temperature low for deterministic editing output
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
    
    # Use the new RunnableSequence syntax: prompt_template | llm
    result = (prompt_template | llm).invoke({"text": input_text})
    return result.content

@app.route("/", methods=["GET", "POST"])
def index():
    reformatted_text = None
    input_text = ""
    selected_style = "professional"  # default style

    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        selected_style = request.form.get("style", "professional")
        if input_text:
            reformatted_text = reformat_text(input_text, selected_style)
    
    return render_template("index.html", input_text=input_text, 
                           reformatted_text=reformatted_text, 
                           selected_style=selected_style)

if __name__ == "__main__":
    app.run(debug=True)
