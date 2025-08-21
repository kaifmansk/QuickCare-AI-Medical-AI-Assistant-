import gradio as gr
from gtts import gTTS
import os

def process_input():
    # Generate a test audio file
    test_text = "This is a test of the autoplay functionality"
    output_filepath = "test_audio.mp3"
    
    tts = gTTS(text=test_text, lang='en', slow=False)
    tts.save(output_filepath)
    
    return "Test Response", output_filepath

# Create the interface with autoplay
test_interface = gr.Interface(
    fn=process_input,
    inputs=[],
    outputs=[
        gr.Textbox(label="Test Text Output"),
        gr.Audio(label="Test Audio Output", autoplay=True)
    ],
    title="Autoplay Test"
)

# Launch the interface on port 5001
test_interface.launch(server_name="0.0.0.0", server_port=5001, debug=True)