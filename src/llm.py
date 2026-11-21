import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model_name = os.getenv("CHAT_MODEL")
api_key = os.getenv("GEMINI_API_KEY")

# Step 1: Check that the settings were loaded
print("Model  :", model_name)
print("API key:", "loaded" if api_key else "MISSING")

# Step 2: Create the model
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=api_key,
    thinking_level="medium",   # less thinking = much faster answers
    timeout=120,            # stop waiting after 2 minutes
    max_retries=1,          # show errors instead of retrying silently
)

# Step 3: Send a request and measure the time
print("Sending request...")
start = time.time()
response = llm.invoke("What is diabetes? Answer in one sentence.")
print(f"Done in {time.time() - start:.1f} seconds\n")

# Step 4: Print only the answer text
print("Answer:", response.text)