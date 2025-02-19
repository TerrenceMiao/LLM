# @markdown ## 🔗 **Source Configuration**

# @markdown **Source Type**
Type_of_source = "YouTube Video"  # @param ["YouTube Video", "Google Drive Video Link", "Dropbox Video Link", "Local File"]

# @markdown **Source URL or Path**
Source = "https://www.youtube.com/watch?v=b0XI-cbel1U"  # @param {type:"string"}

# Set variables based on user input
Type = Type_of_source
URL = Source

# @markdown **Use YouTube Captions**

# @markdown If source is a Youtube video, it's recommended to use the available YouTube captions to save on transcription time and API usage.

use_Youtube_captions = True  # @param {type:"boolean"}

# @markdown ---
# @markdown ## 🌐 **API Configuration**

# @markdown The summarization process uses the API key specified in `api_key` variable.
# @markdown Ensure you have set the required environment variables or Colab secrets for your API keys.

api_endpoint = "Groq"  # @param ["Groq", "OpenAI", "Custom"]

# Define endpoints and models based on the selected API
endpoints = {
  "Groq": "https://api.groq.com/openai/v1",
  "OpenAI": "https://api.openai.com/v1",
  "Custom": "http://localhost:1234/v1"  # Example custom endpoint
}
base_url = endpoints.get(api_endpoint)

# Define models based on the selected API
model = {
  "Groq": "llama-3.3-70b-versatile",
  "OpenAI": "gpt-4o-mini",
  "Custom": "custom-model-id"  # Placeholder for any custom model
}.get(api_endpoint)

# @markdown ---
# @markdown ## 🎤 **Transcription Settings**
# @markdown The transcription settings are applied only if you want to use Whisper transcription and not Youtube Captions.

# @markdown If you plan to use Whisper API endpoint (only **Groq** endpoint is supported for now) you have to specify your Groq API key in `api_key_groq`.

# @markdown Why use `api_key_groq` and `api_key` ? So that you can use a different API for summarization (e.g., OpenAI), specify the corresponding API key in `api_key`.

# @markdown If using locally Whisper: remember to switch the runtime type in Google Colab to a GPU instance (e.g., T4). Go to **Runtime** > **Change runtime type** and select **GPU** as the hardware accelerator.

# @markdown **Transcription Method**
transcription_method = "Cloud Whisper"  # @param ["Cloud Whisper", "Local Whisper"]

# @markdown **Language** (ISO-639-1 code, e.g., "en" for English)
language = "en"  # @param {type:"string"}

# @markdown **Initial Prompt for Whisper** (Optional)
initial_prompt = ""  # @param {type:"string"}


# @markdown ## Libraries and helper functions
# @markdown Re-run if you change settings in the previous cell

import subprocess
import re
import os
import json

from dotenv import load_dotenv

if use_Youtube_captions:
  from youtube_transcript_api import YouTubeTranscriptApi

if (not Type == "YouTube Video") or (not use_Youtube_captions):
  if transcription_method == "Local Whisper":
    import whisper
  else:
    from groq import Groq

if Type == "YouTube Video":
  from pytubefix import YouTube

if Type == "Google Drive Video Link":
  from google.colab import drive
  drive.mount('/content/drive')

# Function to get configuration value
def get_api_key():
  if api_endpoint == "Groq":
    return get_groq_api_key()
  try:
    from google.colab import userdata
    api_key = userdata.get('api_key')
  except ImportError:
    load_dotenv()
    api_key = os.getenv('api_key')

  if not api_key:
    raise ValueError("API key not found in environment variables or Colab secrets")

  return api_key

def get_groq_api_key():
  try:
    from google.colab import userdata
    groq_api_key = userdata.get('api_key_groq')
  except ImportError:
    load_dotenv()
    groq_api_key = os.getenv('api_key_groq')

  if not groq_api_key:
    raise ValueError("Groq API key not found in environment variables or Colab secrets")

  return groq_api_key

# Converts the audio file to MP3 with low sample rate and bitrate to reduce the file size (to stay in audio file API limits)
def process_audio_file(input_path, output_path):
  command_convert = [
    'ffmpeg', '-y', '-i', input_path,
    '-ar', str(8000),
    '-ac', str(1),
    '-b:a', '16k',
    output_path
  ]

  subprocess.run(command_convert, check=True)

import openai
client = openai.OpenAI(api_key = get_api_key(), base_url=base_url)
