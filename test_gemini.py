import os
import google.generativeai as genai

# Configure the API key
api_key = "AIzaSyDJUFRNAuIbJvPvG0LmaCLfTh6f8K8OGPg"
genai.configure(api_key=api_key)

# Initialize the model with a supported model name
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Test the model
try:
    response = model.generate_content("Hello, what is your name?")
    print("Gemini AI is working correctly!")
    print("Response:", response.text)
except Exception as e:
    print("Error:", str(e))