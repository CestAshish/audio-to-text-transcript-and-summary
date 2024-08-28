import os
import traceback

import requests
import gradio as gr
from transformers import pipeline

# Retrieve the Groq API key from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# API endpoint for Groq
groq_url = "https://api.groq.com/openai/v1/chat/completions"

# Define the Groq API request function
def generate_response(prompt):
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 800,
        "temperature": 0.1
    }
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(groq_url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        choices = result.get('choices', [])
        if choices:
            return choices[0].get('message', {}).get('content', 'No content in response')
        return 'No choices in response'
    return f"Error: {response.status_code} - {response.text}"

# Define the prompt template
def create_prompt(context):
    return f"""
    <s><<SYS>>
    List the key points with details from the context: 
    [INST] The context : {context} [/INST] 
    <</SYS>>
    """

# Speech-to-text function
import logging

logging.basicConfig(level=logging.DEBUG)

def transcript_audio(audio_file):
    try:
        logging.debug(f"Received audio file: {audio_file}")
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            chunk_length_s=30,
        )
        transcript_txt = pipe(audio_file, batch_size=8)["text"]
        logging.debug(f"Transcript: {transcript_txt}")
        prompt = create_prompt(transcript_txt)
        logging.debug(f"Generated prompt: {prompt}")
        result = generate_response(prompt)
        logging.debug(f"Generated response: {result}")
        return result
    except Exception as e:
        logging.error(f"Error: {traceback.format_exc()}")
        return f"An error occurred: {e}"

# Gradio interface
audio_input = gr.Audio(sources="upload", type="filepath")
output_text = gr.Textbox()

iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=output_text,
    title="Audio Transcription App",
    description="Upload the audio file"
)

# Launch the Gradio app on localhost
iface.launch(server_name="localhost", server_port=7860)

#
# print(generate_response(create_prompt(transcript_audio("temp.mp3"))))
