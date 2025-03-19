# Sentiment-Based Customer Review Response System

## Overview
This project is a Flask-based web application that processes customer reviews, determines their sentiment, and generates appropriate responses using an AI model powered by LangChain and Groq's Llama3.

## Features
- Accepts customer reviews as input.
- Analyzes the sentiment of the review (positive, negative, or neutral).
- Generates an appropriate response based on sentiment.
- Uses LangChain's structured output capabilities.
- Implements a state graph with LangGraph for workflow automation.
- Flask web interface to submit reviews and display AI-generated responses.

## Technologies Used
- **Python**: Core programming language
- **Flask**: Web framework for handling requests and rendering templates
- **LangChain**: AI framework for LLM-based applications
- **LangGraph**: Workflow state management for AI processing
- **Groq**: Model provider for Llama3
- **HTML**: Frontend for displaying responses

## Installation and Setup
### Prerequisites
Ensure you have Python installed (recommended version: 3.8+). Install required dependencies using:
```bash
pip install flask langchain-core langchain chat_models langgraph
```

### Set Environment Variables
Set up the Groq API key before running the application:
```bash
export GROQ_API_KEY='your_groq_api_key'
```
(Replace `your_groq_api_key` with your actual API key.)

### Running the Application
1. Clone this repository:
```bash
git clone <repository_url>
cd <project_directory>
```
2. Run the Flask application:
```bash
python app.py
```
3. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## Project Structure
```
|-- app.py               # Main Flask application and AI workflow
|-- templates/
    |-- home.html       # Review submission page
    |-- response.html   # Display AI-generated response
```

## How It Works
1. **User submits a review** via the home page.
2. **Sentiment analysis** determines if the review is positive, negative, or neutral.
3. **Response generation** selects an appropriate AI response template.
4. **Response is displayed** on the response page.

## Future Enhancements
- Improve sentiment classification with fine-tuned models.
- Store reviews and responses in a database.
- Add a frontend using ReactJS for a better user experience.
