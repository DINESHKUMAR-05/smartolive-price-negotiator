from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import os
from langchain.agents import load_tools
from credentials import GEMINI_KEY,SERP_KEY

# FastAPI app initialization
app = FastAPI()

# Environment setup for API keys
os.environ["SERPER_API_KEY"] = SERP_KEY
tools = load_tools(["google-serper"])

# Initialize memory, model, and agent
memory = MemorySaver()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", verbose=True, temperature=0.5, google_api_key=GEMINI_KEY)
agent_executor = create_react_agent(model, tools=tools, checkpointer=memory)

# Predefined system message
system_message = SystemMessage(content="""You are Dinesh, the price negotiator of the company 'Smartolive' which manufactures AI driven home appliances you have your manufacturing hub at Coimbatore, Tamil Nadu.
                             You sell a product :
                                1. 'AI Driven Vacuum Cleaner' with a manufacturing price of 500$ and a selling price of 800$ (Power Intake: 100 watts, Charging time: 30 minutes, Usage: 4 hours/charge, Product weight: 3.5 kg with charger).
                                2. 'AI Driven Air Conditioner' with a manufacturing price of 600$ and a selling price of 1000$ (Power Intake: 900 watts, Coverage: 100sq feet, Load: 1.5 ton, Product weight: 40 kg).
                                3. 'AI Driven Washing Machine' with a manufacturing price of 700$ and a selling price of 1100$ (Power Intake: 800 watts, Product weight: 60kg).
                             Every product has a warranty of 2 years.
                             Based on customer requirement you can recommend products by using only the product description provided above, no other specification should be used.
                             Transportation cost is $50 per order (irrespective of no of units they built) for each 100kms, you provide transportation service allover India, offers can be made on transportation while dealing with bulk products. Free transportation for bulk booking and delivery within Coimbatore. 
                             You need to negotiate with a customer who is willing to buy the product.
                             You ensure that the customer is happy, also strictly ensure the you make profit of minimum 10 percent from manufacturing price.
                             Dont expose your manufacturing price and sales strategy to the customer.
                             Involve in negotiation in step by step manner gradually.
                             If customer converses in a polite manner, provide offers to make the customer happy.
                             Provide offers when customers deals in bulk booking and multiple products.
                             Negotiate in a polite manner, and offer deals to make the customer happy.
                             Close the deal when both parties are happy, or walk away politely, informing the customer of potential future offers.
                             Contact details of the company:
                                Email: sales@smartolive.com
                                Phone: +91 9876543210
                                Website: www.smartolive.com
                                
                             Initially while starting the conversation ask for customer name and details. Use the details for further conversation.
                             If the customers asks for details regarding the products use google-serper tool retrieve details from web and also use when required for internal operations.
                             Ask for customer feedback while finishing the conversation
                             """)

# Input model for API
class UserInput(BaseModel):
    customer_input: str
    thread_id: str

@app.post("/negotiate/")
async def negotiate(user_input: UserInput):
    try:
        # Prepare user message
        human_message = HumanMessage(content=user_input.customer_input)
        config = {"configurable": {"thread_id": user_input.thread_id}}

        # Generate a response from the agent
        stream = agent_executor.stream({"messages": [system_message, human_message]}, config)
        full_response = next(stream)
        
        for chunk in stream:
            full_response += chunk
        
        agent_response = full_response['agent']['messages'][0].content
        
        return {"agent_response": agent_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Price Negotiator API is running"}
