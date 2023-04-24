import whisper
import time

model = whisper.load_model("tiny.en")
short_audio_path = r"C:\Users\nlitz88\Documents\Sound recordings\short_audio.m4a"
audio_path = r"T:\2021-12-23 09-55-41.mkv"
audio_load_start = time.time()
audio = whisper.load_audio(audio_path)
audio_load_end = time.time()
print(f"It took {audio_load_end-audio_load_start}s to load input audio.")
transcribe_start = time.time()
results = model.transcribe(audio, word_timestamps=True)
transcribe_end = time.time()
print(f"It took {transcribe_end - transcribe_start} to transcribe the size {len(audio)} audio.")
print(results)

segments = results["segments"]
for segment in segments:
    print(f"ID: {segment['id']}\nStart: {segment['start']}, End: {segment['end']}\nText: {segment['text']}\nNoSpeechProb: {segment['no_speech_prob']}\n")
    formatted_words = [f"\t{segment['words'][i]['word']}: Start: {segment['words'][i]['start']}, End: {segment['words'][i]['end']}" for i in range(len(segment["words"]))]
    for word in formatted_words:
        print(word)