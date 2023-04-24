import whisper

model = whisper.load_model("tiny.en")
audio = whisper.load_audio(r"T:\2021-12-23 09-55-41.mkv")
results = model.transcribe(audio)

segments = results["segments"]
for segment in segments:
    print(f"ID: {segment['id']}\nStart: {segment['start']}, End: {segment['end']}\nText: {segment['text']}\n")