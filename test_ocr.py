import pytesseract
from PIL import Image
import os

# Set the path to tesseract executable for Windows (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def test_tesseract():
    try:
        # Print Tesseract version
        print("Tesseract version:", pytesseract.get_tesseract_version())
        print("Tesseract is properly installed!")
        
        # Test with a sample image if available
        # Create a simple test image with text
        test_image_path = "test_ocr.png"
        if os.path.exists(test_image_path):
            try:
                image = Image.open(test_image_path)
                text = pytesseract.image_to_string(image)
                print("OCR text extracted from test image:")
                print(text)
            except Exception as e:
                print(f"Error extracting text from image: {e}")
        else:
            print("No test image found. Create a test image to verify OCR functionality.")
            
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract OCR is not installed or not found in PATH.")
        print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("After installation, make sure to add it to your system PATH.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tesseract()