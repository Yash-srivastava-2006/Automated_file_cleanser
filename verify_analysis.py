import requests
import time

# Test analyzing a cleansed file
cleansed_filename = 'cleansed_1c0f5256-d173-415b-b8b9-1a5550229567_test_cleansing_verification.txt'
url = f'http://127.0.0.1:5000/analyze/{cleansed_filename}'

print("Testing file analysis functionality...")

response = requests.get(url)

print("Analysis Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Analysis Response:", data)
    
    # Check if analysis was successful
    if 'success' in data and data['success']:
        print("\n✅ ANALYSIS VERIFICATION: SUCCESS - File analysis completed!")
        print(f"Analyzed filename: {data.get('analyzed_filename', 'N/A')}")
        
        # Display extracted text
        print("\nExtracted Text Preview:")
        print("=" * 50)
        print(data.get('extracted_text', '')[:300] + "..." if len(data.get('extracted_text', '')) > 300 else data.get('extracted_text', ''))
        
        # Display final output
        print("\nFinal Output Preview:")
        print("=" * 50)
        print(data.get('final_output', '')[:500] + "..." if len(data.get('final_output', '')) > 500 else data.get('final_output', ''))
    else:
        print("\n❌ ANALYSIS VERIFICATION: FAILED - Analysis did not complete successfully!")
else:
    print("Analysis failed")
    print("Response:", response.text)