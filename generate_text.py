import scrapy
from pathlib import Path

episode = '171'
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://ncode.syosetu.com/n2267be/' + episode + '/']
    Path("./" + episode).mkdir(exist_ok=True)

    def parse(selfself, response):
        tmp = []
        tmp = response.xpath("//p/text()").extract()
        print(len(tmp))
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