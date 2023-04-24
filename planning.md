# Speech Remover
Goals of speech remover:

1. Classify raw audio feed (from microphone or file) as "speech" or "not speech"
2. Remove/Negate/Modify portions of raw audio bytestream that are classified as
   speech
3. Return updated raw audio bytestream with bytes containing speech modified.

# Extension for CMPSC442 Project
For CMPSC 442, our goal is not to simply remove audio that has been classified as
speech. Rather, we only want to remove/modify audio data that is speech and that has
been transcribed to a word that appears on a specified word blacklist.

This transcription process should be able to be added to a boolean-style decision
making pipeline, wherein audio data that's clasified as speech can also pass through
a series of additional checks for additional classification to determine whether or
not it should be removed.

To achieve this transcription, I think I'll try and use OpenAI's whisper model. Seems
to be a roughly SOTA, transformer-based transcription model, and then some.

# Planning
- Okay, first, before actually deciding to use whisper, I need to figure out
  everything it can do.
- I.e., can it do the task of classification as "speech" or "not speech," or does it
  only transcribe without providing much other information.
- The "speech" or "not speech" decision should ideally be determined using some sort
  of deep learning approach, but I feel like webrtcvad is already a solid option, and
  that may already be using some sort of powerful model under the hood, anyways.

- Okay, so it looks like whisper can transcribe audio data that we throw at it--as
  well as give us time stamps and everything.
- Additionally, it can also output word timestamps, which is pretty handy.
- It also spits out a probably for each word, and then for each overarching segment
  of text, it outputs whether it thinks that segment is speech or not
  (no_speech_prob). 
- So, it looks like I could probably make this work if I creatively integrate it with
  a realtime audio stream.
- However, I'm a little worried it will be tough to do, as it seems like it wants 30s
  of audio at a time.
- Let me test it with shorter audio clips. If inference time is somehow lower with
  all of the rest of the input data padded with zeroes, then maybe this is a
  reasonable realtime possibility.

- Okay: After testing, it looks like it will always process a 30s chunk at a time.
  While this is adjustable in the audio python file, I'm assuming that's not really
  meant to be changed in the name of performance.
- Could experiment with it, but the point is: There is a fixed time associated with
  every 30s chunk (or less) of audio that you pass to it.
- Therefore, if we stick to 30, we'll want to make sure we pass in all 30s

# Realtime Dataflow With Planning

1. Audio data is streamed into a buffer that holds 30s worth of audio.
2. As soon as there's an available 30s chunk filled in a synchronized FIFO queue, a
   consumer thread will pick it up and pass it into whisper. Whisper transcribes it
   with segment and word timestamps.
3. That consumer thread then proceeds to modify the original byte stream based on the
   timestamps of blacklisted words.
4. Once modification (censoring) is complete, it takes the audio and streams it back
   to the specified destination (or writes it to file.)
- It takes 30s to fill the buffer, and then let's say a few seconds to modify the
  audio data. From there, it's ready to be sent out in a total of like 30 to 33
  seconds.
- Therefore, we would require a more generous, padded delay of about 45 seconds or so
  to expect audio to be ready. In the case of streaming audio back, could send it
  back as soon as it's ready, or send it out at a certain interval. If doing this
  with stream sockets, it would depend on the size of the buffer, as that's
  ultimately what it would be reading from to grab the audio. Looks like the default
  stream socket buffer size is 32KB. At 16KHz with 16 bits == 2 bytes per sample,
  which means you can fit about 16,000 samples == 1s of audio in that buffer at a
  time. The max buffer size looks like it could only hold about 8s worth of audio.
- I'm pretty sure, however, that the connection itself manages these buffers. I.e.,
  you can tell it to send as much data as you have, and it will send it as soon as it
  can. I.e., it's handled by the protocol and you don't have to worry about it.

# File Based Dataflow

1. Audio data is fed directly into whisper, as you can just load the whole audio file
   and feed that directly into whisper.
2. Then call the same function that modifies the numpy array / byte stream based on
   the timestamps of blacklisted words.

# Todo:
1. Create function that modifies numpy audio array returned by ```load_audio``` based
   on the word timestamps. I.e., you put in time stamps, and it spits out a range of
   byte indices (or indices in the numpy array) that correspond with those
   timestamps.
   - Caveat with this one: THe 16KHz audio that we want to modify is the internal
     audio representation--not necessarily the bitrate of the audio that was passed
     in or that we expect out.
   - Therefore, I'm thinking I'll need another helper function that maps those
     timestamps to the corresponding bytes based on the recording bitrate. I need to
     look for ways to obtain this from an audio file, or calculate it.
2. Create a function that modifies the numpy entries or bytes in an audio array
   (using the above function to map words and their timestamps to array indices)
   based on a list of specified words.