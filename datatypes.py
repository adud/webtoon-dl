#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""all the datatypes used in the downloader and the webpages generator"""


class Episode():
    """internal representation of an episode"""
    def __init__(self, title="", name="", origin="", pic_list=None):
        pass

    def generate_soup(self, style):
        """generate a local soup from the episode"""

    @classmethod
    def from_local_episode(cls, soup):
        """initialize a Comic from the soup of a local comic page"""


class Comic():
    """internal representation of whole comics"""
    def __init__(self, scraper, title="", name="", ep_list=None):
        pass

    def generate_soup(self, style, inlined=False):
        """generate a local soup from the comic"""

    @classmethod
    def from_local_comic(cls, soup):
        """initialize a Comic from the soup of a local comic page"""


class Scraper():
    """an abstract class for scraping comics from webpages"""
    def __init__(self, source, cache=True):
        raise NotImplementedError

    def comic_data(self):
        """get the metadata of the comic"""

    def episode_data(self, ep_no):
        """get the metadata of an episode of the comic"""

    def download_episode(self, ep_no):
        """download the pictures of an episode"""
