from pydub import AudioSegment
from pydub.utils import make_chunks
from videoproc import youtube_preprocess
import math
import os

def chunk_by_size(my_file):
    myaudio = AudioSegment.from_file(my_file)
    channel_count = myaudio.channels    #Get channels
    sample_width = myaudio.sample_width #Get sample width
    duration_in_sec = len(myaudio) / 1000 #Length of audio in seconds
    sample_rate = myaudio.frame_rate
    bit_depth = sample_width * 8 #Bit depth

    wav_file_size = (sample_rate * bit_depth * channel_count * duration_in_sec) / 8

    file_split_size = 22000000  # 24Mb OR 24,000,000 bytes

    total_chunks = int(wav_file_size//file_split_size) + 1

    '''
    Get chunk size by the following method: 
    For X duration_in_sec (X) -->  Y wav_file_size
    For K duration in sec  (K) --> For 24MB file size
    K = X * 10Mb / Y
    '''

    chunk_length_in_sec = math.ceil((duration_in_sec * file_split_size)/wav_file_size)   #in seconds
    chunk_length_ms = chunk_length_in_sec * 1000
    chunks = make_chunks(myaudio, chunk_length_ms)

    if not os.path.exists("process_chunks"):
        os.mkdir("process_chunks")

    #Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        chunk_name = f"process_chunks/chunk{i}.wav"
        chunk.export(chunk_name, format="wav")

    return total_chunks

# audio_file = youtube_preprocess('https://www.youtube.com/watch?v=UU-iWa0Hroc')
# chunk_by_size(audio_file)