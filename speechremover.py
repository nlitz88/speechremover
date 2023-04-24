import numpy as np
from typing import Tuple

# class AudioChunk:

#     def __init__(self, audio_ndarray, audio_samplerate, audio_sampledepth):
#         self.audio_ndarray = audio_ndarray
#         self.audio_samplerate = audio_samplerate
#         self.audio_sampledepth = audio_sampledepth

def convert_timestamp(timestamp: str):
    """Function that converts a string timestamp in format "ss.ms" to a tuple, where
    the first value is the number of seconds, and the second value is the number of
    milliseconds. Returns Tuple(int, int)"""
    seconds, millis = timestamp.split(".")
    return (int(seconds), int(millis))

def timestamp_to_index(audio_ndarray: np.ndarray, audio_samplerate: int, timestamp: str) -> int:
    """Function that takes a timestamp from a provided audio array and returns the
    index of the sample that timestamp corresponds to. 
    
    Parameters
    ----------
    audio_ndarray: np.ndarray
        The audio data array that your timestamp comes from.

    audio_samplerate: int
        The sample rate of the audio array provided above. This is necessary to
        understand how time maps to the provided audio data.
    
    timestamp: str
        The timestamp from the audio that you want the corresponding sample of. Note:
        this should be provided in format "s.ms" s = # seconds and  = #
        milliseconds.

    Returns
    -------
    An integer index from the provided audio_ndarray that most closely corresponds
    with the provided timestamp."""

    # Convert the string timestamp to milliseconds.
    seconds, millis = convert_timestamp(timestamp=timestamp)
    
    # Compute the offset from the beginning of the audio_ndarray, which is more
    # accurately called a "sample array," where each entry in the numpy array is a
    # sample.
    offset = int(seconds*audio_samplerate + (millis/1000)*audio_samplerate)

    return offset

def get_num_samples_from_timestamps(start_timestamp: str, end_timestamp: str) -> int:
    """Function that returns the number of samples covered by a word, provided its
    timestamps as strs.

    Parameters
    ----------
    start_timestamp: str
        The starting timestamp from the audio that you want the corresponding sample
        of. This should be provided in formation: "s.ms"

    end_timestamp: str
        The ending timestamp from the audio that you want the corresponding sample
        of. This should be provided in formation: "s.ms"

    Returns
    -------
    The integer number of audio sample values that correspond with this word.
    """
    return timestamp_to_index(end_timestamp) - timestamp_to_index(start_timestamp)

def generate_1000hz_bleep(num_samples: int, sample_rate: int) -> np.ndarray:
    """Function that generates a 1000 Hz sine wave that spans the number of samples
    you provide. 1000 Hz chosen, as this is the most commonly used frequency for
    profanity censoring sounds. Note that the audio generated has only a 16-bit
    sample depth.

    Parameters
    ----------
    num_samples: str
        The number of samples this sine wave will span / be comprised of.
    sample_rate: int
        The number of samples per second.
    
    Returns
    ----------
    An ndarray of length num_samples whose values create a 1000 Hz sine wave.
    """
    
    duration_s = num_samples/sample_rate
    t = np.linspace(0, duration_s, num_samples, False)
    note = np.sin(1000 * t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio:np.ndarray = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

def generate_silence(num_samples: int) -> np.ndarray:
    """Returns blank filler audio."""
    return np.zeros(num_samples).astype(np.int16)

def replace_audio_between(audio_ndarray: np.ndarray, start_timestamp: str, end_timestamp: str, replacement_audio: np.ndarray) -> np.ndarray:
    """Takes in a numpy array of audio samples and replaces all values between the
    start and end with the provided replacement_audio."""

    start_index = timestamp_to_index(start_timestamp)
    end_index = timestamp_to_index(end_timestamp)
    replace_indices = np.arange(start=start_index, stop=end_index, step=1)
    audio_ndarray[replace_indices] = replacement_audio

    return audio_ndarray

def replace_audio_with_1000hz_bleep(audio_ndarray: np.ndarray, start_timestamp: str, end_timestamp: str, sample_rate: int) -> np.ndarray:
    """Shortcut function to call without having to generate your own replacement signal."""
    bleep = generate_1000hz_bleep(get_num_samples_from_timestamps(start_timestamp=start_timestamp, end_timestamp=end_timestamp), sample_rate=sample_rate)
    return replace_audio_between(audio_ndarray, start_timestamp, end_timestamp, bleep)

def remove_words():
    return

if __name__ == "__main__":
    seconds, millis = convert_timestamp("32.88")
    print(f"Seconds: {seconds}, Milliseconds: {millis}")