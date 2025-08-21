import os
# Add this at the top of your gradio_app.py file - before importing any modules
os.environ["GROQ_API_KEY"] = "your_groq_api_key"
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs_api

GROQ_API_KEY = "your_groq_api_key"
system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_input(audio_filepath, image_filepath):
    # Process patient's voice
    speech_to_text_output = transcribe_with_groq(
        stt_model="whisper-large-v3",  
        audio_filepath=audio_filepath, 
        GROQ_API_KEY=GROQ_API_KEY)

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze"
    
    # Generate audio response
    output_filepath = "doctor_response.mp3"
    text_to_speech_with_elevenlabs_api(input_text=doctor_response, output_filepath=output_filepath)
    
    # Return all outputs for Gradio to display
    return speech_to_text_output, doctor_response, output_filepath


# Create the interface
iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Patient's Voice"),
        gr.Image(type="filepath", label="Medical Image")
    ],
    outputs=[
        gr.Textbox(label="Patient's Speech Transcription"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response", autoplay=True)  # Set autoplay to True
    ],
    title="QUICKCARE AI",
    description="Record your voice to ask about a medical condition and upload an image for analysis."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=5000, debug=True)
