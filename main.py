import sys

import requests
import chardet
import sqlite3
import os
import re
from bs4 import BeautifulSoup

import tkinter as tk


def gui():
    root = tk.Tk()
    root.title("谷歌图片下载器")
    #  设置窗口大小800*600
    root.geometry("800x600")

    # 创建输入框和搜索按钮
    search_label = tk.Label(root, text="Enter search query:")
    search_label.pack()
    search_entry = tk.Entry(root)
    search_entry.pack()

    search_button = tk.Button(root, text="Search and Download", command=lambda: get_image_links(search_entry.get()))
    search_button.pack()
    
    # 代理配置
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    menu_proxy = tk.Menu(menubar)
    menubar.add_cascade(label="代理", menu=menu_proxy)

    menu_proxy_http = tk.Menu(menu_proxy)
    
    menu_proxy_http.add_command(label="设置HTTP代理", command=lambda: set_proxy())
  

   
    
    

    root.mainloop()
    
    
# 获取数据库proxy
def get_proxy():
    conn = sqlite3.connect('proxies.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM proxies')
        return c.fetchone()
    except:
        return None
    
    

def set_proxy():
    proxy_url = input("请输入HTTP代理地址: ")
    # 保存到数据库
    save_proxy_to_db(proxy_url) 

def save_proxy_to_db(proxy_url):
    conn = sqlite3.connect('proxies.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS proxies (id INTEGER PRIMARY KEY AUTOINCREMENT, proxy_url TEXT)')
    c.execute("INSERT INTO proxies (proxy_url) VALUES (?)", (proxy_url,))
    conn.commit()
    conn.close()

# 获取图片链接
def get_image_links(query):
    # url = "https://image.baidu.com/search/index?tn=baiduimage&word=" + query
    
    url = "https://www.google.com/search?q="+ query+"&sca_esv=1ede2510a126829b&tbm=isch&sxsrf=ACQVn0_6SwcBqPV8ORX0GsYWXYcj2bqSTQ%3A1710135402846&source=hp&biw=1880&bih=924&ei=apjuZeXWMbedkdUP8NSJoA0&iflsig=ANes7DEAAAAAZe6mesKKmHkwEqJgJJBpBRDVdTuykOvJ&ved=0ahUKEwjls8_pvuuEAxW3TqQEHXBqAtQQ4dUDCA8&uact=5&oq=%E7%8C%AB&gs_lp=EgNpbWciA-eMqzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJ0iKEFChCFjMDnABeACQAQCYAY4DoAGOA6oBAzMtMbgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAICoAKhA6gCCpgDnAOSBwUxLjQtMaAHoBA&sclient=img"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    proxies = get_proxy()
    if proxies is  None:
        proxies = {
            "http": "http://127.0.0.1:9910",
            "https": "http://127.0.0.1:9910",
        }
    
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    encoding = chardet.detect(response.content)["encoding"]
    response.encoding = encoding
    soup = BeautifulSoup(response.text, "html.parser")
    
    a_links = []
    
  
  

    https_pattern = r'/url\?esrc'

    for a in soup.find_all('a', href=re.compile(https_pattern)):
        a_links.append("https://www.google.com" + a['href'])
    
    
    image_links = []
    for img in soup.find_all("img"):
        img_url = img.get("src")
        if img_url:
            image_links.append(img_url)
    return image_links

# 下载图片
def download_images(image_links, folder='downloads'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, link in enumerate(image_links):
        response = requests.get(link)
        if response.status_code == 200:
            image_name = f"image_{i}.jpg"  # 简单的命名方式
            with open(f"{folder}/{image_name}", 'wb') as f:
                f.write(response.content)
            print(f"下载了图片: {image_name}")
        else:
            print(f"无法下载图片: {link}")

def main(args):
    # query = "猫"
    # image_links = get_image_links(query)
    # print(image_links)
   
    gui()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
