# 🔗 Source Configuration

# Source Type
# @param ["YouTube Video", "Google Drive Video Link", "Dropbox Video Link", "Local File"]
Type_of_source = "YouTube Video"

# Source URL or Path
# @param {type:"string"}
Source = "https://www.youtube.com/watch?v=b0XI-cbel1U&ab_channel=Fireship"

# Set variables based on user input
Type = Type_of_source
# URL = Source

# Use YouTube Captions
# If source is a Youtube video, it's recommended to use the available YouTube captions to save on transcription time and API usage.
# @param {type:"boolean"}
# use_Youtube_captions = True

# 🌐 API Configuration
# The summarization process uses the API key specified in `api_key` variable.
# Ensure you have set the required environment variables or Colab secrets for your API keys.
# @param ["Groq", "OpenAI", "Custom", "Local", "OpenRouter"]
api_endpoint = "Groq"

# Define endpoints and models based on the selected API
endpoints = {
    "Groq": "https://api.groq.com/openai/v1",
    "OpenAI": "https://api.openai.com/v1",
    "Custom": "http://localhost:1234/v1",  # Example custom endpoint
    "Local": "http://localhost:11434/v1",  # Example local endpoint
    "OpenRouter": "https://openrouter.ai/api/v1",  # Example OpenRouter endpoint
}
base_url = endpoints.get(api_endpoint)

# Define models based on the selected API
model = {
    "Groq": "llama-3.3-70b-versatile",
    "OpenAI": "gpt-4o-mini",
    "Custom": "custom-model-id",  # Placeholder for any custom model
    "Local": "llama3.3",  # Placeholder for any local model
    # "OpenRouter": "deepseek/deepseek-chat-v3-0324:free",  # Placeholder for any OpenRouter model
    "OpenRouter": "deepseek/deepseek-r1:free",  # Placeholder for any OpenRouter model
}.get(api_endpoint)

# 🎤 Transcription Settings
# The transcription settings are applied only if you want to use Whisper transcription and not Youtube Captions.
# If you plan to use Whisper API endpoint (only Groq endpoint is supported for now) you have to specify your Groq API key in `api_key_groq`.
# Why use `api_key_groq` and `api_key`? So that you can use a different API for summarization (e.g., OpenAI), specify the corresponding API key in `api_key`.
# If using locally Whisper: remember to switch the runtime type in Google Colab to a GPU instance (e.g., T4). Go to Runtime > Change runtime type and select GPU as the hardware accelerator.

# Transcription Method
# @param ["Cloud Whisper", "Local Whisper"]
transcription_method = "Local Whisper"

# Language (ISO-639-1 code, e.g., "en" for English)
# @param {type:"string"}
language = "en"

regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

# @param ['Summarization', 'Only grammar correction with highlights','Distill Wisdom', 'Questions and answers']
# prompt_type = "Summarization"
# Fetch prompts using curl
# prompts = json.loads(subprocess.check_output(['curl', '-s', 'https://raw.githubusercontent.com/martinopiaggi/summarize/refs/heads/main/prompts.json']))
# Load prompts from local JSON file
# with open("prompts.json", "r") as file:
#     prompts = json.loads(file.read())
# summary_prompt = prompts[prompt_type]

# Parallel API calls (mind rate limits)
# @param
parallel_api_calls = 30

# Chunk size (tokens) (mind model context length). Higher = less granular summary.
# Rule of thumb: 28k for 3h, 10k for 1h, 5k for 30min, 4k for shorter.
# @param
chunk_size = 10000

# Overlap (tokens) between chunks
# @param
overlap_size = 20

# Max output tokens of each chunk (mind model limits). Higher = less granular summary.
# Rule of thumb: 4k, 2k or 1k depending on content density.
# @param
max_output_tokens = 4096


import re
import subprocess
import os
import platform
is_apple_silicon = platform.processor() == 'arm'

# import json

import concurrent.futures
import time

import openai

from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi

if transcription_method == "Local Whisper":
    if is_apple_silicon:
        import mlx_whisper
    else:
        import whisper
else:
    from groq import Groq

if Type == "YouTube Video":
    from pytubefix import YouTube

if Type == "Google Drive Video Link":
    from google.colab import drive

    drive.mount("/content/drive")

import config


# Function to get configuration value
def get_api_key():
    print("LLM Runtime Environment: " + api_endpoint)

    if api_endpoint == "Groq":
        return get_groq_api_key()
    try:
        from google.colab import userdata

        api_key = userdata.get("api_key")
    except ImportError:
        load_dotenv(".env.local")
        load_dotenv()
        api_key = os.getenv("api_key")

    if not api_key:
        raise ValueError("API key not found in environment variables or Colab secrets")

    return api_key


def get_groq_api_key():
    try:
        from google.colab import userdata

        groq_api_key = userdata.get("api_key_groq")
    except ImportError:
        load_dotenv(".env.local")
        load_dotenv()
        groq_api_key = os.getenv("api_key_groq")

    if not groq_api_key:
        raise ValueError(
            "Groq API key not found in environment variables or Colab secrets"
        )

    return groq_api_key


# Converts the audio file to MP3 with low sample rate and bitrate to reduce the file size (to stay in audio file API limits)
def process_audio_file(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        command_convert = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-ar",
            str(8000),
            "-ac",
            str(1),
            "-b:a",
            "16k",
            output_path,
        ]

        subprocess.run(command_convert, check=True, capture_output=True)

        # Clean up input file if it's a temporary file
        if "_processed" not in input_path and input_path != output_path:
            os.remove(input_path)

    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e.stderr.decode()}")
        raise


def seconds_to_time_format(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def download_youtube_audio_only(url):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    saved_path = audio_stream.download(output_path=".", skip_existing=True)
    return saved_path


def download_youtube_captions():
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(config.video_id)

        # Try to get transcript in preferred language first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                config.video_id, languages=[language]
            )
        except:
            # If preferred language not available, try to get any translatable transcript
            transcript = None
            for available_transcript in transcript_list:
                if available_transcript.is_translatable:
                    transcript = available_transcript.translate(language).fetch()
                    break

            if not transcript:
                return ""

        # Process transcript
        transcription_text = "\n".join(
            f"{seconds_to_time_format(entry['start'])} {entry['text'].strip()}"
            for entry in transcript
        )

        # Save transcript
        with open(f"{config.video_id}_captions.md", "w", encoding="utf-8") as f:
            f.write(transcription_text)

        return transcription_text

    except Exception as e:
        print(f"No captions found or, error downloading captions")
        return ""


def extract_and_clean_timestamps(text_chunks):
    timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2})")
    cleaned_texts = []
    timestamp_ranges = []
    for chunk in text_chunks:
        timestamps = timestamp_pattern.findall(chunk)
        if timestamps:
            for timestamp in timestamps:
                # Remove each found timestamp from the chunk
                chunk = chunk.replace(timestamp, "")
            timestamp_ranges.append(
                timestamps[0]
            )  # Assuming you want the first timestamp per chunk
        else:
            timestamp_ranges.append("")
        cleaned_texts.append(
            chunk.strip()
        )  # Strip to remove any leading/trailing whitespace
    return cleaned_texts, timestamp_ranges


def format_timestamp_link(timestamp):
    if Type == "YouTube Video":
        hours, minutes, seconds = map(int, timestamp.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        # return f"{timestamp} - {URL}&t={total_seconds}"
        return f""
    else:
        return f"{timestamp}"


def summarize(prompt):
    summary_prompt = (
        "Summarize the YouTube transcript with timestamp. "
        + "Each paragraph should begin with a timestamp in the format HH:MM:SS which holds markdown link to "
        + "YouTube URL " + config.URL + " at specified seconds, "
        + "and markdown bold notation on a new line. "
        + "Here is the transcript: "
    )

    completion = config.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": summary_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_output_tokens,
    )
    return completion.choices[0].message.content


def process_and_summarize(text):
    if not text:
        return "No transcript available to summarize"

    try:
        # Split text into chunks with overlap
        texts = [
            text[i : i + chunk_size] for i in range(0, len(text), chunk_size - overlap_size)
        ]
        cleaned_texts, timestamp_ranges = extract_and_clean_timestamps(texts)
        summaries = []

        # Process chunks in parallel with retry logic
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=parallel_api_calls
        ) as executor:
            future_to_chunk = {
                executor.submit(summarize, text_chunk): idx
                for idx, text_chunk in enumerate(texts)
            }
            for future in concurrent.futures.as_completed(future_to_chunk):
                idx = future_to_chunk[future]
                try:
                    summarized_chunk = future.result()
                    summary_piece = (
                        format_timestamp_link(timestamp_ranges[idx])
                        + "\n\n"
                        + summarized_chunk
                        + "\n"
                    )
                    summaries.append((idx, summary_piece))
                except Exception as exc:
                    print(f"Chunk {idx} generated an exception: {exc}")
                    time.sleep(10)
                    future_to_chunk[executor.submit(summarize, texts[idx])] = idx

        summaries.sort()  # Ensure summaries are in the correct order
        final_summary = "\n\n".join([summary for _, summary in summaries])

        # Clean up excessive newlines in the final summary
        final_summary = re.sub(r'\n{3,}', '\n\n', final_summary)

        # Save the final summary
        final_name = (
            f"{config.video_id}_captions.md".replace(".md", "_FINAL.md")
            if Type != "Dropbox video link"
            else "final_dropbox_video.md"
        )
        with open(final_name, "w") as f:
            f.write(final_summary)

        return final_summary

    except Exception as e:
        return f"Error during summarization: {str(e)}"


# Add at the top of the file with other imports
from functools import lru_cache

# Add before the Flask routes
# In-memory cache for video summaries
cacheEnabled = True
video_summary_cache = {}

def video_summary(Link):
    if not Link or not Link.strip():
        return "Please provide a valid URL"

    # Remove timestamp parameter from YouTube URL if present
    if '&t=' in Link:
        parts = Link.split('&')
        # Filter out any parameter that starts with 't='
        parts = [p for p in parts if not p.startswith('t=')]
        Link = parts[0] + '&'.join([''] + parts[1:]) if len(parts) > 1 else parts[0]
    # Remove channel parameter from YouTube URL if present
    if '&ab_channel=' in Link:
        parts = Link.split('&')
        # Filter out any parameter that starts with 'ab_channel='
        parts = [p for p in parts if not p.startswith('ab_channel=')]
        Link = parts[0] + '&'.join([''] + parts[1:]) if len(parts) > 1 else parts[0]
    config.URL = Link.strip()
    print("Video URL =", config.URL)

    # Check if summary exists in cache
    if cacheEnabled and (config.URL in video_summary_cache):
        print(f"Cache hit for URL: {config.URL}")
        return video_summary_cache[config.URL]

    video_id_match = re.search(regex, config.URL)
    if not video_id_match:
        return "Invalid YouTube URL format"

    config.video_id = video_id_match.group(1)

    config.client = openai.OpenAI(api_key=get_api_key(), base_url=base_url)

    # Video fetching
    # Re-run cell if you change the Source URL
    skip_transcription = False
    transcription_text = ""
    # textTimestamps = ""

    if Type == "YouTube Video":
        # Clean YouTube url from timestamp
        config.URL = re.sub("\&t=\d+s?", "", config.URL)
        transcription_text = download_youtube_captions()
        if transcription_text:
            skip_transcription = True
        else:
            video_path_local = download_youtube_audio_only(config.URL)
            # Process the audio file to reduce its size
            processed_audio_path = (
                os.path.splitext(video_path_local)[0] + "_processed.mp3"
            )
            process_audio_file(video_path_local, processed_audio_path)
            video_path_local = processed_audio_path  # Update to the processed file path

    elif Type == "Google Drive Video Link":
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                "drive/MyDrive/" + config.URL,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                "gdrive_audio.wav",
            ],
            check=True,
        )
        video_path_local = "gdrive_audio.wav"
        # Process the audio file to reduce its size
        processed_audio_path = os.path.splitext(video_path_local)[0] + "_processed.mp3"
        process_audio_file(video_path_local, processed_audio_path)
        video_path_local = processed_audio_path  # Update to the processed file path

    elif Type == "Dropbox Video Link":
        subprocess.run(["wget", config.URL, "-O", "dropbox_video.mp4"], check=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                "dropbox_video.mp4",
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                "dropbox_video_audio.wav",
            ],
            check=True,
        )
        video_path_local = "dropbox_video_audio.wav"
        # Process the audio file to reduce its size
        processed_audio_path = os.path.splitext(video_path_local)[0] + "_processed.mp3"
        process_audio_file(video_path_local, processed_audio_path)
        video_path_local = processed_audio_path  # Update to the processed file path

    elif Type == "Local File":
        local_file_path = config.URL
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                local_file_path,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                "local_file_audio.wav",
            ],
            check=True,
        )
        video_path_local = "local_file_audio.wav"
        # Process the audio file to reduce its size
        processed_audio_path = os.path.splitext(video_path_local)[0] + "_processed.mp3"
        process_audio_file(video_path_local, processed_audio_path)
        video_path_local = processed_audio_path  # Update to the processed file path

    # Transcription
    # Re-run cell if you change transcription settings
    if not skip_transcription:
        transcription_text = ""

        if video_path_local:
            # Single file transcription
            audio_files = [video_path_local]
        else:
            # Multiple chunk files
            audio_files = audio_chunks

        # Initial Prompt for Whisper (Optional)
        # @param {type:"string"}
        initial_prompt = ""

        for audio_file_path in audio_files:
            # Local Whisper transcription
            if transcription_method == "Local Whisper":
                if is_apple_silicon:
                    transcription = mlx_whisper.transcribe(
                        audio_file_path,
                        initial_prompt=initial_prompt or None,
                        word_timestamps=True,
                    )
                else:
                    # Load whisper model first
                    model_whisper = whisper.load_model("base")
                    transcription = model_whisper.transcribe(
                        audio_file_path,
                        beam_size=5,
                        language=None if language == "auto" else language,
                        task="translate",
                        initial_prompt=initial_prompt or None,
                    )

                for segment in transcription["segments"]:
                    start_time = seconds_to_time_format(segment["start"])
                    transcription_text += f"{start_time} {segment['text'].strip()} "

            elif transcription_method == "Cloud Whisper":
                # Cloud Whisper using Groq API
                groq_client = Groq(api_key=get_groq_api_key())
                with open(audio_file_path, "rb") as audio_file:
                    transcription_response = groq_client.audio.transcriptions.create(
                        file=(os.path.basename(audio_file_path), audio_file.read()),
                        model=(
                            "distil-whisper-large-v3-en"
                            if language == "en"
                            else "whisper-large-v3"
                        ),
                        prompt=initial_prompt or None,
                        response_format="verbose_json",
                        language=None if language == "auto" else language,
                        temperature=0.0,
                    )

                # Corrected code using dot notation
                for segment in transcription_response.segments:
                    start_time = seconds_to_time_format(segment["start"])
                    transcription_text += f"{start_time} {segment['text'].strip()} "
    else:
        print(
            "Using YouTube captions, or Groq's Cloud Whisper if captions are unavailable, for transcription."
        )

    # Save the transcription
    if not skip_transcription:
        with open(f"{config.video_id}_captions.md", "w", encoding="utf-8") as f:
            f.write(transcription_text)

    # Store in cache
    video_summary_cache[config.URL] = process_and_summarize(transcription_text)

    return video_summary_cache[config.URL]


import gradio as gr

iface = gr.Interface(
    fn=video_summary,
    inputs=gr.Textbox(placeholder="Enter YouTube URL here ..."),
    outputs=gr.Markdown(label="Video Summary", line_breaks=True),
)

from flask import Flask, jsonify, request
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# CORS(app, resources={
#     r"/*": {
#         "origins": ["chrome-extension://your-extension-id", "http://localhost:3000"],
#         "methods": ["GET", "POST"],
#         "allow_headers": ["Content-Type"]
#     }
# })

@app.route("/")
def say_hello():
    return "Hello, Video Summary!"

@app.route('/', methods=['POST'])
def get_video_summary():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    result = video_summary(video_url)

    return jsonify({
        "url": video_url,
        "summary": result
    })

@app.route('/reset', methods=['POST'])
def clear_cache():
    video_summary_cache.clear()

    return jsonify({
        "message": "Cache cleared successfully",
        "cache_size": len(video_summary_cache)
    })


from threading import Thread

def run_flask():
    app.run(debug=False)

def run_gradio():
    iface.launch(share=False)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Gradio in the main thread
    run_gradio()
