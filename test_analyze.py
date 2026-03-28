import requests

# Test analyzing a cleansed file
filename = 'cleansed_2e2df30f-a872-479b-b9a9-58592c8cf799_test_sensitive_data.txt'
url = f'http://127.0.0.1:5000/analyze/{filename}'

response = requests.get(url)

print("Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Analysis Results:")
    print("Extracted Text:", data.get('extracted_text', '')[:200] + "...")
    print("Final Output:", data.get('final_output', '')[:200] + "...")
    print("Analyzed Filename:", data.get('analyzed_filename', ''))
else:
    print("Error:", response.text)