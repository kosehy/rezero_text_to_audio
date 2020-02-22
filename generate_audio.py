import ffmpeg
import os
from gtts import gTTS

episode = '169'
def generate_audio():
    raw = []
    txt_filename = episode + '/' + '[raw]' + episode + '.txt'
    input = open(txt_filename, "r", encoding='utf8')
    lines = input.readlines()
    for i in range(len(lines)):
        # print("{}: {}".format(i, lines[i]))
        tts = gTTS(lines[i], lang='ja')
        tts.save(episode + '/' + str(i) + ".mp3")

def concat_audio():
    os.system("ffmpeg -f concat -safe 0 -i <(for f in ./169/*.mp3; done) -c copy 169.mp3")
def main():
    # generate_audio()
    concat_audio()
