from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    # Create a new image with white background
    width, height = 400, 200
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Add some text to the image
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        # Fallback if default font is not available
        font = None
    
    text = "This is a test image for OCR.\nEmail: test@example.com\nPhone: 555-123-4567"
    text_position = (20, 20)
    
    # Draw the text on the image
    draw.text(text_position, text, fill='black', font=font)
    
    # Save the image
    image.save('test_ocr.png')
    print("Test image 'test_ocr.png' created successfully!")
    print("You can now use this image to test OCR functionality.")

if __name__ == "__main__":
    create_test_image()