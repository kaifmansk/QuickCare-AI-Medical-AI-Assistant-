import os
import requests
import subprocess
import platform
import time
from gtts import gTTS

# Get API key from environment variables with fallback
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "your_groq_api_key")

def text_to_speech_with_elevenlabs_api(input_text, output_filepath):
    """
    Convert text to speech using the ElevenLabs API.
    
    Args:
        input_text (str): The text to convert to speech
        output_filepath (str): Path to save the audio file
        
    Returns:
        str: Path to the saved audio file
    """
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Default voice ID for "Rachel"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": input_text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_filepath, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved to {output_filepath}")
            return output_filepath
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            # Fall back to gTTS if ElevenLabs fails
            return text_to_speech_with_gtts(input_text, output_filepath)
    except Exception as e:
        print(f"Error with ElevenLabs API: {e}")
        # Fall back to gTTS if ElevenLabs fails
        return text_to_speech_with_gtts(input_text, output_filepath)

def get_unique_filename(base_filename):
    """
    Generate a unique filename by adding a timestamp
    
    Args:
        base_filename (str): Original filename
        
    Returns:
        str: Unique filename with timestamp
    """
    name, ext = os.path.splitext(base_filename)
    timestamp = int(time.time())
    return f"{name}_{timestamp}{ext}"

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert text to speech using Google Text-to-Speech.
    
    Args:
        input_text (str): The text to convert to speech
        output_filepath (str): Path to save the audio file
        
    Returns:
        str: Path to the saved audio file
    """
    # Create a unique filename to avoid permission issues
    unique_filepath = get_unique_filename(output_filepath)
    
    language = "en"
    try:
        audioobj = gTTS(
            text=input_text,
            lang=language,
            slow=False
        )
        audioobj.save(unique_filepath)
        print(f"Audio saved to {unique_filepath}")
        return unique_filepath
    except Exception as e:
        print(f"Error generating speech with gTTS: {e}")
        return None

def play_audio_file(filepath):
    """
    Play an audio file based on the operating system
    
    Args:
        filepath (str): Path to the audio file
    """
    os_name = platform.system()
    print(f"Attempting to play audio on {os_name} system")
    
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath], check=True)
        elif os_name == "Windows":  # Windows
            # For MP3 files on Windows, we need to use a different approach
            if filepath.lower().endswith('.mp3'):
                print("Using Windows Media Player for MP3 playback")
                subprocess.run(['powershell', '-c', 
                              f'(New-Object -ComObject WMPlayer.OCX).openPlayer("{os.path.abspath(filepath)}")'], 
                              check=True)
            else:
                subprocess.run(['powershell', '-c', 
                              f'(New-Object Media.SoundPlayer "{filepath}").PlaySync();'], 
                              check=True)
        elif os_name == "Linux":  # Linux
            # Try multiple Linux audio players
            players = [
                ['aplay', filepath],  
                ['mpg123', filepath],
                ['ffplay', '-nodisp', '-autoexit', filepath]
            ]
            
            for player_cmd in players:
                try:
                    subprocess.run(player_cmd, check=True)
                    print(f"Successfully played with {player_cmd[0]}")
                    return
                except (FileNotFoundError, subprocess.SubprocessError):
                    continue
                    
            print("No suitable audio player found on this system")
        else:
            print(f"Unsupported operating system: {os_name}")
    except Exception as e:
        print(f"Error playing audio: {e}")
