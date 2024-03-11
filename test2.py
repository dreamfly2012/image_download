import re
import requests
import chardet
from bs4 import BeautifulSoup


def get_largest_image(url):
    # 发送请求并获取网页内容
    response = requests.get(url)
    html = response.content

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有的图片标签
    images = soup.find_all('img')

    # 初始化最大图片的URL为空字符串
    max_image_url = ''
    max_size = 0

    # 遍历所有图片标签
    for image in images:
        # 获取图片的URL
        image_url = image.get('src')

        # 如果图片URL不为空，并且以http或https开头，则下载图片并获取其大小
        if image_url and image_url.startswith('http'):
            image_response = requests.get(image_url)
            image_size = len(image_response.content)

            # 如果当前图片大小大于之前的最大图片大小，则更新最大图片URL和大小
            if image_size > max_size:
                max_image_url = image_url
                max_size = image_size

    return max_image_url

query = 'cat'

url = "https://www.google.com/search?q=google&newwindow=1&sca_esv=d1b5aeb9d701f53b&tbm=isch&sxsrf=ACQVn096esyHFmd1oQANwM0iJpdpLhA5rA%3A1710148863176&source=hp&biw=1880&bih=924&ei=_8zuZfbCCM-ekdUPxfi9uAY&iflsig=ANes7DEAAAAAZe7bD0O9fhwRZwCN_NkqZTZQBE35xlDs&ved=0ahUKEwi2voD88OuEAxVPT6QEHUV8D2cQ4dUDCA8&uact=5&oq=google&gs_lp=EgNpbWciBmdvb2dsZTIEECMYJzIEECMYJzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESMgZUMoFWM8UcAJ4AJABAJgB8QGgAckMqgEDMi03uAEDyAEA-AEBigILZ3dzLXdpei1pbWeYAgmgAvgMqAIKwgIHECMY6gIYJ5gDDJIHBTIuMC43oAelMg&sclient=img"

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

pattern = r'(?<=url=)https?://[^\s&]+'


# 使用findall方法找到所有匹配的字符串
image_links = re.findall(pattern, web_page_source_code)

image_links = set(image_links)

filtered_urls = [url for url in image_links if "google.com" not in url]

images = []

if filtered_urls:
    for url in filtered_urls:
        largest_url = get_largest_image(url)
        images.append(largest_url)


print(images)

