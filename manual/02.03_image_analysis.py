# 03.03: do repeated requests from the user.

import anthropic 

import os
from typing import Dict, Any

from PIL import Image       
from io import BytesIO      
import base64               

class ImageProcessor:
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    # Now pass the prompt as an input
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

if __name__ == "__main__":

    processor  = ImageProcessor()
    image_path = "./images/bball.jpg" 

    type = image_path.split('.')[-1] 
    if type == "jpg":
        extension = "jpeg"

    # To repeatedely prompt the user for input use this forever loop
    while True:
        prompt = input("Enter a prompt: ")

        # i) Check to see if the user input a 'quit' command. 
        #    Use lower() to ensure that regardless of case, 
        #    we get the same message.
        if prompt.lower() == 'quit':

            # Exit the loop prematurely. As such it will run to the end and end the program.
            break

        result = processor.analyze_image(prompt,image_path,extension)

        if result:
            print("Analysis Result:", result)
        else:
            print("Failed to analyze the image.")