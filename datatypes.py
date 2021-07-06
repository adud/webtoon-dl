#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""all the datatypes used in the downloader and the webpages generator"""

import sys

from urllib.request import Request, urlopen
from shutil import copyfileobj
from os import makedirs
from os.path import join, realpath, dirname  # , isfile, isdir, exists
from http.cookiejar import MozillaCookieJar
from bs4 import BeautifulSoup, FeatureNotFound

FILENAME = sys.argv[0]
DIRNAME = dirname(sys.argv[0])
VERB = True
DRY = False

TEST = "https://www.webtoons.com/fr/romance/lore-olympus/episode-139/"\
    "viewer?title_no=1825&episode_no=144"


def log_message(message, pipe=sys.stdout):
    """Log a message to a specific pipe (defaulting to stdout)."""
    print("{}: {}".format(FILENAME, message), file=pipe)


def log(message):
    """If verbose, log an event."""
    if not VERB:
        return
    log_message(message)


def error(message, exit_code=None):
    """Log an error. If given a 2nd argument, exit using that error code."""
    log_message("error: " + message, sys.stderr)
    if exit_code:
        sys.exit(exit_code)


def mkdir(*args, **kwargs):
    """makes directory if not dry-run mode"""
    if not DRY:
        return makedirs(*args, **kwargs)
    log("faking make directory" + str(args))


class Episode():
    """internal representation of an episode"""
    def __init__(self, browser, title="", name="", origin="", img_list=None):
        self.browser = browser
        self.title = title
        self.name = name
        self.origin = origin
        self.img_list = img_list

    def make_turner(self, *links):
        """return a soup containing a link to the next/prev page and
        the index, if None is given, the link becomes invisible
        takes 3 args:
        prev: the address of the previous page or None
        top: the address of the index or None
        next: the address of the next page or None"""

        soup = BeautifulSoup()
        soup.append(soup.new_tag("div", attrs={"class": "paginate"}))
        for link, text in zip(links, ["Prev", "Top", "Next"]):
            tag = soup.new_tag('a')
            if link is None:
                tag['style'] = "visibility: hidden"
            else:
                tag['href'] = link
                tag.string = text
                soup.div.append(tag)

        return soup

    def generate_soup(self, page):
        """generate a local soup from the episode"""
        with open(join(DIRNAME, "template-internal.html")) as f:
            soup = BeautifulSoup(f, "html.parser")

        soup.head.title.string = self.title

        turner = self.make_turner(*page) if page is not None else ""
        soup.body.append(turner)
        soup.body.extend([soup.new_tag("img", src=f) for f in self.img_list])
        soup.body.append(turner)

        return soup

    @classmethod
    def from_local_episode(cls, soup):
        """initialize a Comic from the soup of a local comic page"""


class Comic():
    """internal representation of whole comics"""
    def __init__(self, origin, browser, title="", name="", ep_list=None):
        self.origin = origin
        self.browser = browser
        self.title = title
        self.name = name
        self.ep_list = ep_list

    def generate_soup(self, style, stype=0):
        """generate a local soup from the comic
        style: the style to use
        stype: 0 loaded, 1 inlined, 2 put in the episode folder"""

    @classmethod
    def from_local_comic(cls, soup):
        """initialize a Comic from the soup of a local comic page"""


class Browser():
    """an abstract class for scraping comics from webpages"""
    def __init__(self, verb=0):
        raise NotImplementedError

    def comic(self, soup):
        """create a Comic object from a scraping soup"""
        raise NotImplementedError

    def episode(self, url):
        """create an Episode object from an url"""
        soup = self.get_soup(url)
        return Episode(self, soup.title.string, self.get_ep_name(soup),
                       url, self.get_image_urls(soup))

    # def episode2comic(self, path):
    #     """given an episode path, returns the comic path"""

    def download_picture(self, url, outfile):
        """download a picture from the site
        url: the url of the picture
        outfile: the output file"""
        raise NotImplementedError

    def get_soup(self, url):
        """download a webpage from an url and convert it into a soup"""
        raise NotImplementedError

    def get_image_urls(self, soup):
        """Retrieve all image URLs to download from an episode soup
        qual: the quality in the webtoon query"""
        raise NotImplementedError

    def get_ep_name(self, soup):
        """Retrieve the name of an episode from an episode soup"""
        raise NotImplementedError

    def get_co_title(self, soup):
        """Retrieve the name of a comic from an episode soup"""
        raise NotImplementedError


class WebToonBrowser(Browser):
    """a browser for the webtoon site
    """

    jar = MozillaCookieJar(join(realpath(dirname(FILENAME)), "cookies.txt"))
    referer_header = {"Referer": 'http://www.webtoons.com'}

    def __init__(self):
        self.jar.load()

    def get_soup(self, url):
        """download a webpage from an url and convert it into a soup
        using the cookie of infinity to bypass GDPR gate"""
        log("Downloading url {}".format(url))
        req = Request(url)
        self.jar.add_cookie_header(req)
        with urlopen(req) as page:
            try:
                soup = BeautifulSoup(page, "lxml")
            except FeatureNotFound:
                log("lxml not found, fallback to default")
                soup = BeautifulSoup(page)
        return soup

    def download_image(self, url, target):
        """download a image from the site
        url: the url of the image
        target: the output file name
        uses a referer to be accepted"""
        log("Downloading image at {} to {}".format(url, target))
        req = Request(url, headers=self.referer_header)
        if not DRY:
            with urlopen(req) as response, open(target, "wb") as outfile:
                copyfileobj(response, outfile)
        return

    def get_image_urls(self, soup, qual=""):
        """Retrieve all image URLs to download from an episode soup
        qual: the quality in the webtoon query"""
        return [img["data-url"].replace("?type=q90", qual)
                for img in soup(class_="_images")]

    def get_ep_name(self, soup):
        """Retrieve the name of an episode from an episode soup"""
        return soup.title.string.split("|")[0].strip()

    def get_co_title(self, soup):
        """Retrieve the name of a comic from an episode soup"""
        return soup.title.string.split("|")[1].strip()


if __name__ == "__main__":
    print(FILENAME)
    truc = WebToonBrowser()
    ep = truc.episode(TEST)
    print(ep.title)
