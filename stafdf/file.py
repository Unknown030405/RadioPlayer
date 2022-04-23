import bs4
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    result = requests.get("https://yandex.ru/images/search?text=background%20azul&isize=small&itype=png")

    beautified = BeautifulSoup(result.text, features="html.parser")
    images = beautified.find_all(["img"], {"class" : "serp-item__thumb"})

    print(images[0].get_attribute_list("src"))

    print(*map(lambda x: x.split("src=")[1][:-2], images), sep="\n")