from bs4 import BeautifulSoup
import requests
import urllib
import re
import os


# lists
urls = []

# function created


class Crawler:
    def scrape(self, site):
        global urls
        # getting the request from url
        r = requests.get(site)
        # converting the text
        s = BeautifulSoup(r.text, "html.parser")

        for i in s.find_all("a"):
            href = i.attrs['href']
            urls.append(href)
            if href.endswith("/") and "../" not in href:
                newsite = site+href
                if newsite not in urls:
                    # urls.append(newsite)
                    # calling it self
                    self.scrape(newsite)


class ArtifactDownloader:
    def download_artifacts(self, urls, location):
        current_path = os.path.dirname(os.path.realpath(__file__))
        download = current_path+location
        os.makedirs(current_path, exist_ok=True)
        for url in urls:
            if "test" in url and url.endswith(".zip"):
                print(url)
                r = requests.get(url, stream=True)
                filename = url.split("/")[-1]
                open(f"{download}\{filename}", 'wb').write(r.content)


# main function
if __name__ == "__main__":
    site = "http://192.168.0.73:8081/service/rest/repository/browse/maven-releases/test/test/"
    cr = Crawler()
    cr.scrape(site)
    dl = ArtifactDownloader()
    dl.download_artifacts(urls, "/download")
