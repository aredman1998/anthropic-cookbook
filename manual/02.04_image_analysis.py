# 03.04: validate all input

import anthropic 

import os
from typing import Dict, Any

from PIL import Image       
from io import BytesIO      
import base64               

class ImageProcessor:
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def analyze_image(self, prompt:str, image_path: str, type: str) -> dict:
       
        if not os.path.isfile(image_path):
            print(f"File {image_path} does not exist.\nFrom your terminal make sure you that are at the top of the anthropic notebook!!")
            return None
        
        try:
            with open(image_path, "rb") as image_file:  

                binary_img = image_file.read()
                base64_img = base64.b64encode(binary_img)
                base64_img_string = base64_img.decode('utf-8')

        except anthropic.AnthropicError as e:
            print(f"An error occurred: {e}")
            return None
        
        message_list    = [
                {
                    "role": "user",

                    "content": [            
                        {
                            "type": "text", 
                            "text": prompt
                        },
                        {
                            "type": "image", 
                            "source": {
                                        "type":         "base64",           # Encoding 
                                        "media_type":   "image/" + type,    # Type
                                        "data":         base64_img_string   # Img. variable
                                        }
                        }
                    ]
                }
            ]       

        response = self.client.messages.create(
            model       = "claude-3-5-sonnet-latest",
            max_tokens  = 2048,
            temperature = 0,
            messages    = message_list
            )

        return response.content[0].text

    # New class function to validate the input prompt
    def validate_input(self, prompt: str) -> bool:
        """
        Validate the input prompt. 
        We will check three conditions:
            i) The prompt is a string
            ii) The prompt is not empty
            iii) The prompt is not too long

        Args:
            prompt (str): The input prompt to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(prompt, str):
            return False
        
        if len(prompt.strip()) == 0:
            return False
        
        if len(prompt) > 1000:  # Example length limit
            return False
        
        return True     

if __name__ == "__main__":

    processor  = ImageProcessor()
    image_path = "./images/bball.jpg" 

    type = image_path.split('.')[-1] 
    if type == "jpg":
        extension = "jpeg"

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'quit':
            break

        # Check for valid input
        if not processor.validate_input(prompt):
                print("Invalid input. Please try again.")
                continue        

        result = processor.analyze_image(prompt,image_path,extension)

        if result:
            print("Analysis Result:", result)
        else:
            print("Failed to analyze the image.")