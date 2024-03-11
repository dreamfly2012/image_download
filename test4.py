import os, sys, re
import string
import random
import requests, grequests
from functools import partial

 
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
headers = { 'User-Agent': USER_AGENT }
 
def get_image_urls_fr_gs(query_key):
    """
        Get all image url from google image search
        Args:
            query_key: search term as of what is input to search box.
        Returns:
            (list): list of url for respective images.
 
    """
 
    query_key = query_key.replace(' ','+')#replace space in query space with +
    tgt_url = 'https://www.google.com.sg/search?q={}&tbm=isch&tbs=sbd:0'.format(query_key)#last part is the sort by relv
    
    proxies = {
        "http": "http://127.0.0.1:9910",
        "https": "http://127.0.0.1:9910",
    }
 
    r = requests.get(tgt_url, headers = headers, proxies=proxies)
 
    urllist = [n for n in re.findall('"ou":"([a-zA-Z0-9_./:-]+.(?:jpg|jpeg|png))",', r.text)] 
 
    return urllist
 
def dl_imagelist_to_dir(urllist, tgt_folder, job_size = 100):
    """
        Download all images from list of url link to tgt dir
        Args:
            urllist: list of the image url retrieved from the google image search
            tgt_folder: dir at which the image is stored
        Kwargs:
            job_size: (int) number of downloads to spawn.
 
    """
    if len(urllist) == 0:
        print ("No links in urllist")
        return
 
    def dl_file(r, folder_dir, filename, *args, **kwargs):
        fname = os.path.join(folder_dir, filename)
        with open(fname, 'wb') as my_file:
            # Read by 4KB chunks
            for byte_chunk in r.iter_content(chunk_size=1024*10):
                if byte_chunk:
                    my_file.write(byte_chunk)
                    my_file.flush()
                    os.fsync(my_file)
 
        r.close()
 
    do_stuff = []
    
 
    for run_num, tgt_url in enumerate(urllist):
        print (tgt_url)
        # handle the tgt url to be use as basename
        basename = os.path.basename(tgt_url)
        file_name = re.sub('[^A-Za-z0-9.]+', '_', basename ) #prevent special characters in filename
 
        #handling grequest
        action_item =  grequests.get(tgt_url, hooks={'response': partial(dl_file, folder_dir = tgt_folder, filename=file_name)}, headers= headers,  stream=True)
        do_stuff.append(action_item)
 
    grequests.map(do_stuff, size=job_size)
 
def dl_images_fr_gs(query_key, tgt_folder):
    """
        Function to download images from google search
 
    """
    url_list = get_image_urls_fr_gs(query_key)
    dl_imagelist_to_dir(url_list, tgt_folder, job_size = 100)
 
if __name__ == "__main__":
 
    query_key= 'python symbol'
    tgt_folder = r'./downloads/'
    dl_images_fr_gs(query_key, tgt_folder)  