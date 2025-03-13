from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from flask import Flask, render_template, request,redirect
from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict
import os

# Set up the environment variables with the GROQ API key
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

# Initialize the Llama3 model with GROQ as provider
llm = init_chat_model("llama3-8b-8192",model_provider="groq")

# Define the schema for sentiment analysis
class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="The sentiment of the text")

# Create a sentiment analysis model using with_structured_output
sentiment_analyzer = llm.with_structured_output(SentimentAnalysis)

# Define chat templates for different responses
thankful_template = ChatPromptTemplate.from_template(
    "You are a customer service agent responding to a positive review. "
    "Write ONLY the main body paragraph of a thankful and appreciative response "
    "to the customer's feedback. Do NOT include any greeting, salutation, "
    "closing remarks, or signature: {review}"
)

regretful_template = ChatPromptTemplate.from_template(
    "You are a customer service agent responding to a negative review. "
    "Write ONLY the main body paragraph of an empathetic and regretful response "
    "to address the customer's concerns. Do NOT include any greeting, salutation, "
    "closing remarks, or signature: {review}"
)

# Create chains for generating responses
thankful_chain = thankful_template | llm | StrOutputParser()
regretful_chain = regretful_template | llm | StrOutputParser()

# Define state for the graph
class State(TypedDict):
    review: str
    sentiment: str
    response: str

# Define graph functions
def analyze_sentiment(state: State) -> State:
    prompt = f"""Analyze the sentiment of the following review. 
    Classify it as either 'positive', 'negative', or 'neutral':
    Review: {state["review"]}
    """
    result = sentiment_analyzer.invoke(prompt)
    return {"sentiment": result.sentiment}

# Generate a response based on the sentiment of the review.
def generate_response(state: State) -> State:
    if state["sentiment"] == "negative":
        response = regretful_chain.invoke({"review": state["review"]})
    else:
        response = thankful_chain.invoke({"review": state["review"]})
    return {"response": response}

# Router function to determine next steps based on sentiment
def route_by_sentiment(state: State) -> str:
    return "end"

# Create the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("generate_response", generate_response)

# Define the edges - fixed to use proper END node
workflow.add_edge(START, "analyze_sentiment")
workflow.add_edge("analyze_sentiment", "generate_response")
workflow.add_edge("generate_response", END)

# Compile the graph
langchain = workflow.compile()

# Function to process the review text and generate a response
def process_review(review_text):
    result = langchain.invoke({"review": review_text})
    return result.get("response","No response generated")

app=Flask(__name__)

# Retrieve the home.html when user starts the server. 
@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=="POST":
        review=request.form['review']
        response=process_review(review)
        return render_template("response.html",response=response)
    return redirect('/')

# Run the program
if __name__=='__main__':
    app.run(debug=True)
