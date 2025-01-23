# 01.02: Study the role of changing the number of tokens. 
import anthropic

# Always strt by creating the client object. 
client = anthropic.Anthropic()

# Create a list with one dictionary that includes two keys: role and content. 
# Role can have values like: user, system, or assistant.
# Content is a list of dictionaries that include the type of content and the text of the content.
message_list = [
        {
            # The user role is used to indicate that the message or prompt is from the user
            "role": "user",

            # Introduce metadata for the prompt message. Mainly: (i) it's type, which will be text and (ii) the prompt itself.
            "content": [
                {
                    "type": "text",
                    "text": "Why is the ocean salty?"
                }
            ]
        }
    ]

# Create an instance of the message object with (i) model, (ii) token, (iii) temperature, and (iv) message info.
message = client.messages.create(

    # Set the model type you want to use 
    model       = "claude-3-5-sonnet-latest",

    # Set the maximum number of output tokens to 1024. Token's are the smallest unit of text in a language model.
    # They can be a word, half a word, or even a single character.
    max_tokens  = 1024,

    # Pass in the message_list that contains user and prompt information
    messages    = message_list
)
print(message.content[0].text)