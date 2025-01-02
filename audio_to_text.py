import assemblyai as aai

aai.settings.api_key = "e96a6c1ee3fb4500a5dfd21184e9cd27" 

transcriber = aai.Transcriber()

# You can use a local filepath:
# audio_file = "./example.mp3"

# Or use a publicly-accessible URL:
audio_file = (
    "./test2pt.mp3"
)

config = aai.TranscriptionConfig(speaker_labels=True,language_code="pt")

transcript = transcriber.transcribe(audio_file, config)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

print(transcript.text)