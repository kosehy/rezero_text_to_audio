#!/usr/bin/env python
import glob
from pydub import AudioSegment
import os
from gtts import gTTS

def generate_audio(episode, dirpath):
    """
    generate audio file from google tts
    :return:
    """
    raw = []
    txt_filename = dirpath + '[raw]' + episode + '.txt'
    input = open(txt_filename, "r", encoding='utf8')
    lines = input.readlines()
    for i in range(len(lines)):
        print("{}: {}".format(i, lines[i]))
        if lines[i] and lines[i].strip():
            tts = gTTS(lines[i], lang='ja')
            tts.save(dirpath + str(i) + ".mp3")
        else:
            continue
    last_index = len(lines) - 1
    tts = gTTS(lines[last_index], lang='ja')
    tts.save(dirpath + str(last_index) + ".mp3")

def concat_audio(dirpath, output_file):
    """
    concat whole audio files to one output audio file
    :return:
    """
    """
    ffmpeg -f concat -safe 0 -i <(for f in ./169/*.mp3; do echo "file '$PWD/$f'"; done) -c copy output.mp3
    """
    # cmd = "ffmpeg -f concat -safe 0 -i < for f in ./%s/*.mp3; do echo \"file '$PWD/$f'\" done -c copy output_%s.mp3" % (episode, episode)
    # os.system(cmd)
    filenames = glob.glob(dirpath + "*.mp3")
    base = []
    for i in filenames:
        tmp = os.path.basename(i)
        tmp_filename = os.path.splitext(tmp)[0]
        base.append(int(tmp_filename))
    base.sort()
    filenames.clear()
    for i in base:
        filenames.append(str(i) + ".mp3")
    combined = AudioSegment.empty()
    for filename in filenames:
        audio_filename = AudioSegment.from_mp3(dirpath + filename)
        combined += audio_filename
        print(filename)
    audio_filename = AudioSegment.from_mp3("empty.mp3")
    combined += audio_filename
    combined.export(dirpath + output_file, format="mp3")

def speedup_audio(episode, dirpath, output_file):
    cmd = "ffmpeg -i %s -filter:a \"atempo=1.25\" -vn %s.mp3" % (dirpath + output_file, dirpath +  "[txt]" + episode + "_output_1.25")
    os.system(cmd)


for i in range(176, 200):
    episode = str(i)
    dirpath = './text/' + episode + "/"
    output_file = episode + "_output.mp3"

    generate_audio(episode, dirpath)
    concat_audio(dirpath, output_file)
    speedup_audio(episode, dirpath, output_file)
