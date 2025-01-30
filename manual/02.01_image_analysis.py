# 03.01: Multi-modal code to analyze images. 

# This project has more import tools that will help us achieve more functionality.
import anthropic 

# Import os lets you have access to OS tools. It will help us to 
import os

# Module to help us encode images as strings
import base64               

# Create a  class for Image Processing
# For more on classes, return to our intro_to_python. 
class ImageProcessor:
    def __init__(self):
        '''
        __init__ is called the "constructor" of the class. 
        It takes care of initializing key routines. 
        For this class, it initializes the API key and client.
        This code only works if the API_KEY is set as an environment variable.
        '''

        # Instantiate the client
        self.client = anthropic.Anthropic()
    
    def analyze_image(self, image_path, type):
        """
        Analyzing images in Anthropic is a bit more challenging, because their system is not designed to
        consume images directly, only JSON data. Instead images have to be encoded as text!

        Some things that we will need to handle before handing an image are:
        1. Validation:   Providing the correct path
        2. Endocing:     Encoding the iamge as text, which will take 2 steps: (i) encode as base64 and (ii) decode as utf-8
        3. Content Prep: message_list will now have 2 dictionaries to handle: a text prompt and an image definition.
           
        Args:
            image_path (str):   Path to the image file
            type (str):         Type of image file (jpeg, png, etc)
            
        Returns:
            dict: Text message responding prompt response.
        """

        # Start with a prompt
        prompt = f"Analyze this image. Identify the character in the main image, if there is one. Provide a historicy summary of this peron."

        
        # 1) Validate the image path
        if not os.path.isfile(image_path):
            print(f"File {image_path} does not exist.\nFrom your terminal make sure you that are at the top of the anthropic notebook!!")
            return None
        
        # 2) Encode binary image data to base64 string, which is an encoding of images in ASCII string format. U
        
        # Try blocks handle exceptions (i.e. crashes). # If an exception occurs, the rest of the block is skipped.
        try:

            # Read image using binary values. 
            with open(image_path, "rb") as image_file:  # Creates a file object that allows you to interact with the content.

                # Read the binary data from the file object
                binary_img = image_file.read()

                # Encode the binary data as base64.
                base64_img = base64.b64encode(binary_img)

                # Finally convert the base64 image into a string
                base64_img_string = base64_img.decode('utf-8')

        except anthropic.AnthropicError as e:
            print(f"An error occurred: {e}")
            return None
        
        # 3) Prepare the content for the message_list
        message_list    = [
                {
                    "role": "user",

                    # Content will be a list of 2 dictionaries for text and image
                    "content": [            

                        # Text: type-text + prompt                            
                        {
                            "type": "text", 
                            "text": prompt
                        },

                        # Image: type-image + source
                        {
                            "type": "image", 

                            # Key details of the image
                            "source": {
                                        "type":         "base64",           # Encoding 
                                        "media_type":   "image/" + type,    # Type
                                        "data":         base64_img_string   # Img. variable
                                        }
                        }
                    ]
                }
            ]       

        # Create an instance of the message object with (i) model, (ii) token, (iii) temperature, and (iv) message info. 
        response = self.client.messages.create(

            # Set the model type you want to use 
            model       = "claude-3-5-sonnet-latest",

            # Set the maximum number of output tokens to 1024. Token's are the smallest unit of text in a language model.
            # They can be a word, half a word, or even a single character.
            max_tokens  = 2048,

            # Set the temperature to 0. Temperature controls randomness. A value of 0 means the model will always choose the most likely token.
            temperature = 0,

            # Pass in the message_list that contains text and image data
            messages    = message_list

            )

        # Return the prompt response
        return response.content[0].text

if __name__ == "__main__":

    # 1) Instantiate the ImageProcessor
    processor = ImageProcessor()

    # 2) Image Path
    # Note: open a folder in Visual Studio directly to the anthropic-cookbook.
    #       this will set it as the parent folder. 
    #       You should then be able to enter the images folder with the ./images relative path.
    #       You can select any image thereafter.
    image_path = "./images/bball.jpg" 

    # 3) Image Extension
    # Get the image extension and set it to jpeg (needed by anthropic) if .jpg
    #   Split your string into "before period" and "after period" parts
    #   The [-1] index is used to get the last element of the list
    type = image_path.split('.')[-1] # keeps whatever is after period as string
    if type == "jpg":
        extension = "jpeg"

    # 4) Send image via API and enact prompt.
    result = processor.analyze_image(image_path,extension)

    # Print the analysis result
    if result:
        print("Analysis Result:", result)
    else:
        print("Failed to analyze the image.")