import os
import gradio as gr
import requests
from transformers import pipeline

def llm_llama(prompt):
    # Retrieve the Groq API key from environment variables
    groq_api_key = os.getenv('GROQ_API_KEY')


    # API endpoint for Groq (Replace with the correct endpoint if different)
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Request payload
    payload = {
        "model": "llama3-8b-8192",  # Replace with your model ID
        "messages": [  # Use 'messages' instead of 'message'
            {
                "role": "user",
                "content": f"List the key points with details from the context: {prompt}"
            }
        ],
        "max_tokens": 800,
        "temperature": 0.1
    }

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        result = response.json()
        # Adjust based on the response structure; assuming 'choices' is present
        choices = result.get('choices', [])
        if choices:
            return choices[0].get('message', {}).get('content', 'No content in response')
        else:
            return 'No choices in response'
    else:
        return f"Error: {response.status_code} - {response.text}"



# Transcribe audio and generate response
def transcript_audio(audio_file):
    try:
        # Initialize the pipeline
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            chunk_length_s=30
        )

        # Transcribe the audio file
        transcript_txt = pipe(audio_file, batch_size=8)["text"]

        # Generate response from the transcription
        result = llm_llama(transcript_txt)
        return result
    except Exception as e:
        print(f"Error processing audio: {e}")
        return f"Error processing audio: {e}"

# Define Gradio interface
audio_input = gr.Audio(sources="upload", type="filepath")
output_text = gr.Textbox()

iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=output_text,
    title="Audio Transcription App",
    description="Upload the audio file"
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7861)

