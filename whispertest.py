import whisper

model = whisper.load_model("tiny.en")
audio = whisper.load_audio(r"T:\2021-12-23 09-55-41.mkv")
results = model.transcribe(audio, word_timestamps=True)
print(results)

segments = results["segments"]
for segment in segments:
    print(f"ID: {segment['id']}\nStart: {segment['start']}, End: {segment['end']}\nText: {segment['text']}\nNoSpeechProb: {segment['no_speech_prob']}\n")
    formatted_words = [f"\t{segment['words'][i]['word']}: Start: {segment['words'][i]['start']}, End: {segment['words'][i]['end']}" for i in range(len(segment["words"]))]
    for word in formatted_words:
        print(word)