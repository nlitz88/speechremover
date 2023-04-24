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
    offset = seconds*audio_samplerate + (millis/1000)*audio_samplerate

    return offset

if __name__ == "__main__":
    seconds, millis = convert_timestamp("32.88")
    print(f"Seconds: {seconds}, Milliseconds: {millis}")