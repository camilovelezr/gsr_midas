import itertools
import re
import tempfile
import zipfile
import os
import requests
import shutil
import json
import hashlib
import urllib
from zeppelingsr import CordraSession, Zeppelin
from alive_progress import alive_bar

l = input("Is the CordraSession local? (https://localhost:8443)?(y/n) ")

#l = 'y'

if l=="y":
    cs = CordraSession("https://localhost:8443", acls  = {"readers":["public"], "writers":["public"]})
else:
    cs = CordraSession()


url = "https://data.nist.gov/rmm/records/?@id=ark:/88434/mds2-2476"
t = requests.get(url)
j = dict(t.json()['ResultData'][0])['components'] # obtain JSON and create dict of components
download_urls = [] # initialize download_urls list
for e in j: # for every element in the list of components
    for (x,y) in e.items(): # search within the key value pairs, those keys == "downloadURL"
        if (x == "downloadURL"):
            if not (re.search(".sha256$", y)): # do not include checksums
                download_urls.append(y)


def iskev(x): # function to remove keV.zip
    if re.search(r"25%20keV.zip$", x):
        return True
    else:
        return False

download_urls = list(itertools.filterfalse(iskev, download_urls)) # apply iskev

# checksums: url+".sha256"

def getname(x):
    return urllib.parse.unquote(x.split("/")[-1].split(".zip")[0]).replace(" ", "_")

class size():
    def __init__(self, x):
        s = x*(10**-9)
        if s>=1:
            self.value = round(s, 2)
            self.unit = "Gigabytes"
        else:
            self.value = round(s*(10**3), 1)
            self.unit = "Megabytes"


class tempZeppelin(): # class to define a temporary Zeppelin
    def __init__(self, url):
        self.url = url # download url of zip file
        self.name = getname(url) # get name of sample
        ch = requests.get(url+".sha256", stream = True) # get checksum from url
        self.checksum = ch.text
        print("Sending request\n")
        r = requests.get(url, stream=True)
        content_length = int(r.headers['Content-Length'])
        s = size(content_length)
        print(f"Downloading {s.value} {s.unit}")
        self.i, self.path = tempfile.mkstemp()
        with open(self.path, "r+b") as f:
            with alive_bar((content_length//2048)+1, title=f"Downloading {self.name}", bar="classic2") as bar:
                for chunk in r.iter_content(chunk_size=2048):
                    f.write(chunk) # write content to tempfile
                    bar()
            f.seek(0)
            print(f"Verifying checksum\n")
            b = f.read()
            _sha = hashlib.sha256(b).hexdigest() # get hash from zip
            assert self.checksum == _sha # make sure both hashes match
            f.seek(0)
            t = zipfile.ZipFile(f) # read as zip
            folder = f"{tempfile.gettempdir()}/{self.name}_unzip" # path of dir where extract
            print(f"Extracting zip file\n")
            t.extractall(path = folder) # extract content into /unzip
            print(f"Done\n")
        os.close(self.i) # close tmp
        os.remove(self.path) # remove zip file
        self.path = folder # establish path as path of dir of files
        self.Zeppelin = Zeppelin(self.path) # create a Zeppelin object from the dir

def update_uuid(zeppelin):
    with open("uuid.json", "r+") as jf:
        d = json.load(jf)
        d[zeppelin.sample] = zeppelin.uuid
        jf.seek(0)
        json.dump(d, jf, indent=4)

def zload(cordra, url, max=None):
    z = tempZeppelin(url)
    try:
        z.Zeppelin.upload_all(cordra, max)
        update_uuid(z.Zeppelin)
    except BaseException as e:
        print(e)
    finally:
        shutil.rmtree(z.path)

def z_all(max=None):
    for url in download_urls:
        zload(cs, url, max)

z_all(10)




