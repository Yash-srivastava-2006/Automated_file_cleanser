import re
import os

def advanced_cleanse_text(text, filename=""):
    """Advanced text cleansing to remove sensitive and client-specific information"""
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Remove phone numbers (various formats)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    
    # Remove SSN-like patterns
    text = re.sub(r'\b\d{3}-?\d{2}-?\d{4}\b', '[SSN]', text)
    
    # Remove credit card numbers (simplified)
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CREDIT CARD]', text)
    
    # Remove IP addresses
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP ADDRESS]', text)
    
    # Remove dates (MM/DD/YYYY or DD/MM/YYYY format)
    text = re.sub(r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b', '[DATE]', text)
    
    # Remove addresses (simplified pattern)
    text = re.sub(r'\d{1,5}\s[\w\s]+?,?\s*[A-Za-z]{2}\s\d{5}(-\d{4})?', '[ADDRESS]', text)
    
    # Remove MAC addresses
    text = re.sub(r'\b([0-9A-F]{2}[:-]){5}([0-9A-F]{2})\b', '[MAC ADDRESS]', text)
    
    # Remove passport numbers (simplified)
    text = re.sub(r'\b[A-Z]{1,2}\d{6,9}\b', '[PASSPORT]', text)
    
    # Remove driver license numbers (simplified)
    text = re.sub(r'\b[A-Z]{1,2}\d{7,9}\b', '[DRIVER LICENSE]', text)
    
    # Remove client-specific information based on filename
    if filename:
        # Extract potential client name from filename (before extension)
        client_name = os.path.splitext(os.path.basename(filename))[0]
        # Remove client name if it appears in the text (case insensitive)
        if len(client_name) > 3:  # Only if name is long enough to be meaningful
            text = re.sub(re.escape(client_name), '[CLIENT NAME]', text, flags=re.IGNORECASE)
    
    # Remove common client-related terms
    client_terms = [
        r'\bclient\b', r'\bcustomer\b', r'\bcompany\b', r'\borganization\b',
        r'\bcorporation\b', r'\bincorporated\b', r'\blimited\b', r'\bllc\b'
    ]
    
    for term in client_terms:
        text = re.sub(term, '[CLIENT TERM]', text, flags=re.IGNORECASE)
    
    return text

# Test the cleansing function
if __name__ == "__main__":
    # Read the test file
    with open("test_cleansing.txt", "r") as f:
        original_text = f.read()
    
    print("Original Text:")
    print("=" * 50)
    print(original_text)
    print("\n" + "=" * 50)
    
    # Cleanse the text
    cleansed_text = advanced_cleanse_text(original_text, "test_cleansing.txt")
    
    print("\nCleansed Text:")
    print("=" * 50)
    print(cleansed_text)
    print("\n" + "=" * 50)
    
    # Save the cleansed text
    with open("test_cleansing_cleansed.txt", "w") as f:
        f.write(cleansed_text)
    
    print("\nCleansed text saved to 'test_cleansing_cleansed.txt'")