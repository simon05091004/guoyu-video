#!/usr/bin/env python3
"""把 head.html（樣式）＋ body.html（版型與程式）＋ data.json 組成 ../index.html。"""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
p = lambda *a: os.path.join(here, *a)

head = io.open(p("head.html"), encoding="utf-8").read()
body = io.open(p("body.html"), encoding="utf-8").read()
data = io.open(p("data.json"), encoding="utf-8").read()
body = body.replace("__DATA__", data)

full = ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="康軒版國小六年級國語每一課的 YouTube 補充影片索引，'
        '含課文朗讀、導讀、語詞修辭與延伸主題。">\n'
        + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')

out = p("..", "index.html")
io.open(out, "w", encoding="utf-8").write(full)
print("寫出 %s（%d bytes）" % (os.path.normpath(out), len(full)))
