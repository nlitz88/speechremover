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
- 