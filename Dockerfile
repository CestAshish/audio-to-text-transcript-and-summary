FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the current directory contents into the container at /app
COPY . .

# Install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the Groq API Key
#or set it at runtime ==> docker run -p 7861:7861 --env GROQ_API_KEY=<key> <imagename>
ENV GROQ_API_KEY="your-key"

# Expose the port the app runs on
EXPOSE 7861

# Run the Python script when the container launches
CMD ["python3", "-u", "speech-analysis-using-groq.py"]
