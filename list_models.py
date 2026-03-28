import google.generativeai as genai

# Configure the API key
api_key = "AIzaSyDJUFRNAuIbJvPvG0LmaCLfTh6f8K8OGPg"
genai.configure(api_key=api_key)

# List available models
try:
    for model in genai.list_models():
        print(f"Model: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Description: {model.description}")
        print("---")
except Exception as e:
    print("Error:", str(e))