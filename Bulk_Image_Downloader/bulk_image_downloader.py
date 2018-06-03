import urllib2
import os
import json
from bs4 import BeautifulSoup


def get_soup(url,header):
    """
    :param url: google image search url
    :param header: takes in a header
    :return: html content
    """

    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def main():
    """
    :return: Null
    """
    
    # Searching for the specific image via google image search

    name = raw_input("image name : ")
    
    image_type = "img"
    
    name = name.split()
    
    name = '+'.join(name)
    
    url = "https://www.google.co.in/search?q="+name+"&source=lnms&tbm=isch"
    
    # Add the directory for your image

    folder = "Pictures"

    header = {'User-Agent':
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    soup = get_soup(url,header)

    # Fetch actual links

    actual_images=[]

    for a in soup.find_all("div",{"class":"rg_meta"}):

        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        actual_images.append((link,Type))

    if not os.path.exists(folder):
        
        os.mkdir(folder)

    folder = os.path.join(folder, name.split()[0])

    if not os.path.exists(folder):

        os.mkdir(folder)

    # Download images

    for i, (img, Type) in enumerate(actual_images):

        try:

            req = urllib2.Request(img, headers={'User-Agent' : header})
            raw_img = urllib2.urlopen(req).read()

            count = len([i for i in os.listdir(folder) if image_type in i]) + 1

            print(count)

            if len(Type) == 0:

                fp = open(os.path.join(folder, image_type + "_"+ str(count)+".jpg"), 'wb')

            else:

                fp = open(os.path.join(folder, image_type + "_"+ str(count)+"."+Type), 'wb')

            fp.write(raw_img)

            fp.close()

        except Exception as exe:

            print("could not load : "+ str(img))
            print(exe)

if __name__ == "__main__":
    main()
