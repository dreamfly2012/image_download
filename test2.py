import re
import requests
import chardet
from bs4 import BeautifulSoup

query = 'cat'

url = 'https://www.google.com.sg/search?q={}&tbm=isch&tbs=sbd:0'.format(query)

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


proxies = {
    "http": "http://127.0.0.1:9910",
    "https": "http://127.0.0.1:9910",
}

response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
encoding = chardet.detect(response.content)["encoding"]
response.encoding = encoding
soup = BeautifulSoup(response.text, "html.parser")

web_page_source_code = response.text

urllist = [n for n in re.findall('"ou":"([a-zA-Z0-9_./:-]+.(?:jpg|jpeg|png))",', web_page_source_code)] 

# 使用findall方法找到所有匹配的字符串
image_links = re.findall(pattern, web_page_source_code)

# 输出结果
for link in image_links:
    print(link)