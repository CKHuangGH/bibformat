import re
import webbrowser
import time

# 第一步：讀取 bib.txt 並提取網址（使用 utf-8 編碼）
with open('bib.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正則表達式抓取所有網址並清理掉後面的非字母數字字符
urls = re.findall(r'(https?://\S+)', content)
cleaned_urls = [re.sub(r'[^\w:/.-]+$', '', url) for url in urls]

# 第二步：將乾淨的網址寫入 url.txt
with open('url.txt', 'w', encoding='utf-8') as url_file:
    for url in cleaned_urls:
        url_file.write(url + '\n')

# # 第三步：讀取 url.txt 並自動打開每個網址，並停留 10 秒
# with open('url.txt', 'r', encoding='utf-8') as url_file:
#     for url in url_file:
#         webbrowser.open(url.strip())  # 打開網址
#         time.sleep(10)  # 停留 10 秒

# # 第四步：程式結束
# print("所有網址已打開，程式結束。")
