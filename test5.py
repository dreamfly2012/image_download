import re

html_content = '/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=https://fr.wikipedia.org/wiki/Logo_de_Google&amp;ved=2ahUKEwjLseCe8-uEAxWvU6QEHYwhCFoQr4kDegQIBRAC&amp;usg=AOvVaw3f9ytcMKmq6eEVywXBgfE6'

pattern = r'(?<=url=)https?://[^\s&]+'
url = re.search(pattern, html_content)

if url:
    print(url.group(0))
else:
    print("URL not found")