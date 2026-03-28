import pytesseract
import sys
import os

def check_tesseract():
    print("Checking Tesseract OCR installation...")
    
    # Print the expected path
    expected_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"Expected Tesseract path: {expected_path}")
    
    # Check if the expected path exists
    if os.path.exists(expected_path):
        print("✓ Tesseract executable found at expected location")
    else:
        print("✗ Tesseract executable NOT found at expected location")
    
    # Try to get Tesseract version
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract version: {version}")
        print("✓ Tesseract is properly installed and accessible!")
        return True
    except pytesseract.TesseractNotFoundError as e:
        print(f"✗ TesseractNotFoundError: {e}")
        print("\nTroubleshooting steps:")
        print("1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install Tesseract and make sure to check 'Add to PATH' during installation")
        print("3. Restart your command prompt/terminal after installation")
        print("4. If still not working, manually set the path in app.py:")
        print(f"   pytesseract.pytesseract.tesseract_cmd = r'{expected_path}'")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    check_tesseract()