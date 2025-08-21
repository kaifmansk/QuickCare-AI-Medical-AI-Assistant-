import os
import base64
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def encode_image(image_path):
    """
    Encode an image to base64 format for processing with vision models.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_query(query, encoded_image, model="llama-3.2-90b-vision-preview", api_key=None):
    """
    Analyze an image with a specific query using Groq's vision models.
    
    Args:
        query (str): The text query to ask about the image
        encoded_image (str): Base64 encoded image
        model (str): The LLM model to use
        api_key (str, optional): Groq API key
        
    Returns:
        str: The model's response
    """
    if api_key is None:
        api_key = GROQ_API_KEY  # Use the global variable as fallback
    
    client = Groq(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    
    return chat_completion.choices[0].message.content
