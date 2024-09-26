## README for SmartOlive Price Negotiator

### Project Overview

This project is a web-based AI price negotiation system named **SmartOlive Price Negotiator**. It allows users to interact with a custom-built AI agent that assists in negotiating prices for AI-driven home appliances sold by the company 'SmartOlive'. The system is built using **Streamlit** for the frontend and **FastAPI** for the backend. The negotiation logic is handled by the Gemini language model integrated with the LangChain framework.

### Tech Stack

- **Frontend**: Streamlit (for building the user interface)
- **Backend**: FastAPI (for handling API requests)
- **AI Model**: LangChain using Google Gemini (for generating negotiation dialogues)
- **Data Sources**: Google Serper (for retrieving additional product details if needed)
- **Memory**: MemorySaver (to store negotiation progress for each session)
  
### Key Features
- **Product Listing and Description**: Users can see detailed product descriptions and prices.
- **Real-Time Negotiation**: Users can interact with an AI-powered price negotiator.
- **Bulk Order Discounts**: Discounts are provided for bulk or polite customers.
- **Transport Fee Calculation**: Includes transportation costs based on customer location and order quantity.

---

### Setup Instructions

To run the project, follow the steps below:

#### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/smartolive-price-negotiator.git
cd smartolive-price-negotiator
```

#### 2. Install Dependencies
Make sure you have Python 3.10+ installed. Install the required libraries using the following command:
```bash
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables
You need API keys to access Google Gemini and Google Serper. Set these keys in the `credentials.py` file:
```python
GEMINI_KEY = "<your_gemini_key>"
SERP_KEY = "<your_serper_key>"
```

Alternatively, you can set these as environment variables:
```bash
export GEMINI_KEY="<your_gemini_key>"
export SERP_KEY="<your_serper_key>"
```

#### 4. Run FastAPI Backend
Start the FastAPI server for handling negotiation requests:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

#### 5. Run Streamlit Frontend
In a new terminal, start the Streamlit app:
```bash
streamlit run app.py
```

The Streamlit app will be available at `http://localhost:8501`.

---

### Explanation of the Code

#### 1. **Frontend (app.py)**

The **Streamlit** app creates a user interface where customers can interact with the AI negotiator.

- `st.set_page_config()`: Configures the app layout and title.
- `st.title()`: Displays the title of the app.
- **Session Management**: Manages the conversation history and unique thread ID using `st.session_state`.
- **Send Message Function**: The function `send_message()` sends customer input to the FastAPI backend and retrieves the AI-generated response.
- **Sidebar**: The sidebar contains product descriptions, prices, and contact information.
- **Chat Interface**: The main chat interface allows customers to type messages and see responses from the AI agent.

#### 2. **Backend (app.py)**

The **FastAPI** backend processes requests sent from the frontend and interacts with the AI agent.

- `app = FastAPI()`: Initializes the FastAPI app.
- **LangChain Setup**:
  - `ChatGoogleGenerativeAI`: Integrates the Gemini model for text generation.
  - `create_react_agent()`: Creates a reactive agent for handling the conversation.
- **API Endpoints**:
  - `/negotiate/`: This endpoint processes customer input, sends it to the LangChain agent, and returns the generated response.
  - `/`: Root endpoint to check if the API is running.
- **Negotiation Logic**: The system is initialized with a system message containing the rules and constraints for negotiating, such as ensuring at least a 10% profit margin.

#### 3. **LangChain and Agent**

The negotiation logic is powered by LangChain and the Google Gemini model. The agent is configured with memory (via `MemorySaver`) to maintain the context across the entire conversation. It also uses the `google-serper` tool to retrieve additional information from the web if requested by the user.

#### 4. **Credentials (credentials.py)**

This file stores sensitive API keys (Google Gemini and Serper) for accessing the AI model and performing web searches.

#### 5. **Dependencies (requirements.txt)**

This file lists all the necessary Python libraries, including FastAPI, LangChain, Pydantic, and Streamlit. Use `pip install -r requirements.txt` to install them.

---

### Usage

1. **Start the FastAPI Backend**:
   - Start the FastAPI server to handle the negotiation logic.

2. **Start the Streamlit Frontend**:
   - Launch the Streamlit app to interact with the AI negotiator.

3. **Negotiate with AI**:
   - Chat with the AI about the products, negotiate pricing, and get special offers.
   - The AI will ensure that a minimum 10% profit is made for the company and offer deals for polite or bulk customers.

