import scrapy
import os
import shutil
import sys
from pathlib import Path
from generate_audio import *

episode = "169"
dirpath = episode + "/"
output_file = "[txt]" + episode + "_" + "output.mp3"

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://ncode.syosetu.com/n2267be/' + episode + '/']
    Path("./" + episode).mkdir(exist_ok=True)
    def parse(selfself, response):
        tmp = response.xpath("//p/text()").extract()
        print(len(tmp))
        k = 0
        check = "第"
        for i in range(len(tmp)):
            if check in tmp[i][0]:
                k = i
        raw = []
        for i in range(k, len(tmp)):
            raw.append(tmp[i])

        text = []
        check_script = "「"
        for i in range(k, len(tmp)):
            if check_script in tmp[i][0]:
                text.append("")
                text.append(tmp[i])
                text.append("")
            else:
                text.append(tmp[i])

        raw_filename = episode + '/' + '[raw]' + episode + '.txt'
        with open(raw_filename, 'w', encoding='utf8') as f:
            for i in range(len(raw)):
                print("{}: {}".format(i, raw[i]))
                f.write(raw[i])
                f.write("\n")
        txt_filename = episode + '/' + '[txt]' + episode + '.txt'
        with open(txt_filename, 'w', encoding='utf8') as f:
            for i in range(len(text)):
                f.write(text[i])
                f.write("\n")

        raw = []
        txt_filename = episode + '/' + '[raw]' + episode + '.txt'
        input = open(txt_filename, "r", encoding='utf8')
        lines = input.readlines()
        for i in range(len(lines)):
            print("{}: {}".format(i, lines[i]))
            tts = gTTS(lines[i], lang='ja')
            tts.save(episode + '/' + str(i) + ".mp3")
        last_index = len(lines) - 1
        tts = gTTS(lines[last_index], lang='ja')
        tts.save(episode + '/' + str(last_index) + ".mp3")

        filenames = glob.glob(dirpath + "*.mp3")
        base = []
        for i in filenames:
            tmp = os.path.basename(i)
            tmp_filename = os.path.splitext(tmp)[0]
            base.append(int(tmp_filename))
        base.sort()
        filenames.clear()        os.system(cmd)
        for i in base:
            filenames.append(str(i) + ".mp3")
        combined = AudioSegment.empty()
        for filename in filenames:
            audio_filename = AudioSegment.from_mp3(dirpath + filename)
            combined += audio_filename
            print(filename)
        audio_filename = AudioSegment.from_mp3("empty.mp3")
        combined += audio_filename
        combined += audio_filename
        combined += audio_filename
        combined += audio_filename
        combined.export(dirpath + output_file, format="mp3")

        cmd = "ffmpeg -i %s -filter:a \"atempo=1.25\" -vn %s.mp3" % (dirpath + output_file, "[txt]" + episode + "_output_1.25")
        shutil.copyfile("./" + episode + '/' + '[txt]' + episode + '.txt', "./" + '[txt]' + episode + '.txt')
