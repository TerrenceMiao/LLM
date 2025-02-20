# 🔗 Source Configuration

# Source Type
# @param ["YouTube Video", "Google Drive Video Link", "Dropbox Video Link", "Local File"]
Type_of_source = "YouTube Video"

# Source URL or Path
# @param {type:"string"}
Source = "https://www.youtube.com/watch?v=b0XI-cbel1U&ab_channel=Fireship"

# Set variables based on user input
Type = Type_of_source
URL = Source

# Use YouTube Captions
# If source is a Youtube video, it's recommended to use the available YouTube captions to save on transcription time and API usage.
# @param {type:"boolean"}
use_Youtube_captions = True

# 🌐 API Configuration
# The summarization process uses the API key specified in `api_key` variable.
# Ensure you have set the required environment variables or Colab secrets for your API keys.
# @param ["Groq", "OpenAI", "Custom"]
api_endpoint = "Groq"

# Define endpoints and models based on the selected API
endpoints = {
    "Groq": "https://api.groq.com/openai/v1",
    "OpenAI": "https://api.openai.com/v1",
    "Custom": "http://localhost:1234/v1",  # Example custom endpoint
}
base_url = endpoints.get(api_endpoint)

# Define models based on the selected API
model = {
    "Groq": "llama-3.3-70b-versatile",
    "OpenAI": "gpt-4o-mini",
    "Custom": "custom-model-id",  # Placeholder for any custom model
}.get(api_endpoint)

# 🎤 Transcription Settings
# The transcription settings are applied only if you want to use Whisper transcription and not Youtube Captions.
# If you plan to use Whisper API endpoint (only Groq endpoint is supported for now) you have to specify your Groq API key in `api_key_groq`.
# Why use `api_key_groq` and `api_key`? So that you can use a different API for summarization (e.g., OpenAI), specify the corresponding API key in `api_key`.
# If using locally Whisper: remember to switch the runtime type in Google Colab to a GPU instance (e.g., T4). Go to Runtime > Change runtime type and select GPU as the hardware accelerator.

# Transcription Method
# @param ["Cloud Whisper", "Local Whisper"]
transcription_method = "Cloud Whisper"

# Language (ISO-639-1 code, e.g., "en" for English)
# @param {type:"string"}
language = "en"

# Initial Prompt for Whisper (Optional)
# @param {type:"string"}
initial_prompt = ""

transcript_file_name = ""

regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

import re

video_id = re.search(regex, URL).group(1)

# Libraries and helper functions
# Re-run if you change settings in the previous cell

import subprocess
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

    drive.mount("/content/drive")


# Function to get configuration value
def get_api_key():
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

    subprocess.run(command_convert, check=True)


import openai

client = openai.OpenAI(api_key=get_api_key(), base_url=base_url)

# Video fetching
# Re-run cell if you change the source URL
skip_transcription = False
transcription_text = ""
textTimestamps = ""


def seconds_to_time_format(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def download_youtube_audio_only(url):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    saved_path = audio_stream.download(mp3=True, output_path=".", skip_existing=True)
    return saved_path


def download_youtube_captions(url):
    print("Video URL = ", url, " with video_id = ", video_id)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except:
        for available_transcript in transcript_list:
            if available_transcript.is_translatable:
                transcript = available_transcript.translate("en").fetch()
                break

    transcription_text = ""
    for entry in transcript:
        start_time = seconds_to_time_format(entry["start"])
        transcription_text += f"{start_time} {entry['text'].strip()}\n"

    transcript_file_name = f"{video_id}_captions.md"

    with open(transcript_file_name, "w", encoding="utf-8") as f:
        f.write(transcription_text)

    return transcription_text, transcript_file_name


if Type == "YouTube Video":
    # Clean YouTube url from timestamp
    URL = re.sub("\&t=\d+s?", "", URL)
    if use_Youtube_captions:
        transcription_text, transcript_file_name = download_youtube_captions(URL)
        skip_transcription = True
    else:
        video_path_local = download_youtube_audio_only(URL)
        # Process the audio file to reduce its size
        processed_audio_path = os.path.splitext(video_path_local)[0] + "_processed.mp3"
        process_audio_file(video_path_local, processed_audio_path)
        video_path_local = processed_audio_path  # Update to the processed file path

elif Type == "Google Drive Video Link":
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            "drive/MyDrive/" + URL,
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
    subprocess.run(["wget", URL, "-O", "dropbox_video.mp4"], check=True)
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
    local_file_path = Source
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

    for audio_file_path in audio_files:
        if transcription_method == "Local Whisper":
            # Local Whisper transcription
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
    print("Using YouTube captions for transcription.")

# Save the transcription
if not skip_transcription:
    transcript_file_name = "transcription.md"
    with open(transcript_file_name, "w", encoding="utf-8") as f:
        f.write(transcription_text)
else:
    transcript_file_name = f"{video_id}_captions.md"

# @param ['Summarization', 'Only grammar correction with highlights','Distill Wisdom', 'Questions and answers']
prompt_type = "Custom Summarisation"
# Fetch prompts using curl
# prompts = json.loads(subprocess.check_output(['curl', '-s', 'https://raw.githubusercontent.com/martinopiaggi/summarize/refs/heads/main/prompts.json']))
# Load prompts from local JSON file
with open("prompts.json", "r") as file:
    prompts = json.loads(file.read())
summary_prompt = prompts[prompt_type]

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

final_summary = ""


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
            ) # Assuming you want the first timestamp per chunk
        else:
            timestamp_ranges.append("")
        cleaned_texts.append(
            chunk.strip()
        ) # Strip to remove any leading/trailing whitespace
    return cleaned_texts, timestamp_ranges


def format_timestamp_link(timestamp):
    if Type == "YouTube Video":
        hours, minutes, seconds = map(int, timestamp.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return f"{timestamp} - {URL}&t={total_seconds}"
    else:
        return f"{timestamp}"


import concurrent.futures
import time


def summarize(prompt):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": summary_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_output_tokens,
    )
    return completion.choices[0].message.content


def process_and_summarize(text):
    texts = [
        text[i : i + chunk_size] for i in range(0, len(text), chunk_size - overlap_size)
    ]
    cleaned_texts, timestamp_ranges = extract_and_clean_timestamps(texts)
    summaries = []

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
                )
                summary_piece += "\n"
                summaries.append((idx, summary_piece))
            except Exception as exc:
                print(f"Chunk {idx} generated an exception: {exc}")
                time.sleep(10)
                future_to_chunk[executor.submit(summarize, texts[idx])] = idx

    summaries.sort() # Ensure summaries are in the correct order
    final_summary = "\n\n".join([summary for _, summary in summaries])

    # Save the final summary
    final_name = (
        transcript_file_name.replace(".md", "_FINAL.md")
        if Type != "Dropbox video link"
        else "final_dropbox_video.md"
    )
    with open(final_name, "w") as f:
        f.write(final_summary)

process_and_summarize(transcription_text)
