import scrapy
import os
import shutil
import pydub
import sys
from pathlib import Path
import re

episode = "2"
stop_episode = "4"
dirpath = episode + "/"

Path("./text").mkdir(exist_ok=True)
Path("./text/" + episode).mkdir(exist_ok=True)
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://ncode.syosetu.com/n2267be/' + episode + '/']
    base_urls = 'http://ncode.syosetu.com/n2267be/'
    def parse(self, response):
        '''
        get next episode variable
        '''
        next_episode_str = response.xpath(
            '//div[contains(@class, "novel_bn")]').extract_first()
        check = "前"
        k = 0
        for i in range(len(next_episode_str)):
            if check in next_episode_str[i]:
                k = i
        next_episode_str = next_episode_str[k + 6:]
        r = next_episode_str[18:]
        next_episode = ''.join(x for x in r if x.isdigit())
        if next_episode == stop_episode:
            return 0
        episode = int(next_episode) - 1
        print("episode: {}".format(episode))
        Path("./text/" + str(episode)).mkdir(exist_ok=True)
        '''
        extract text file from webpage
        '''
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

        raw_filename = 'text/' + str(episode) + '/' + '[raw]' + str(episode) + '.txt'
        print("raw_filename: {}".format(raw_filename))
        with open(raw_filename, 'w', encoding='utf8') as f:
            for i in range(len(raw)):
                print("{}: {}".format(i, raw[i]))
                f.write(raw[i])
                f.write("\n")
        txt_filename = 'text/' + str(episode) + '/' + '[txt]' + str(episode) + '.txt'
        print("txt_filename: {}".format(txt_filename))
        with open(txt_filename, 'w', encoding='utf8') as f:
            for i in range(len(text)):
                f.write(text[i])
                f.write("\n")

        next_page_url = self.base_urls + next_episode + '/'
        yield scrapy.Request(next_page_url, callback=self.parse)