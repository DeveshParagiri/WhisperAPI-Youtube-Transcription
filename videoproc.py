from moviepy.editor import *
import pytube
import os
import sys



def youtube_preprocess(link, start = None, end = None):
    yt = pytube.YouTube(link)
    yt.register_on_progress_callback(show_progress_bar)
    destination = '.'
    video = yt.streams.filter(only_audio = True).first()

    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)

    new_file = base + '.wav'
    os.rename(out_file, new_file)

    if start and end:
        print(start,end)
        myclip = AudioFileClip(new_file).subclip(get_sec(start),get_sec(end))
        myclip.write_audiofile(new_file)
    return new_file


# Display a download progress bar
def show_progress_bar(stream, _chunk, bytes_remaining):
  current = ((stream.filesize - bytes_remaining)/stream.filesize)
  percent = ('{0:.1f}').format(current*100)
  progress = int(50*current)
  status = '█' * progress + '-' * (50 - progress)
  sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
  sys.stdout.flush()

def get_sec(time_str):
    """Get seconds from time.
    """

    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)