#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""all the datatypes used in the downloader and the webpages generator"""


class Comic():
    """a class for whole comics"""
    def __init__(self, title="", name="", origin="", ep_list=None):
        pass

    def generate_soup(self, style, inlined=False):
        """generate a soup from the comic"""

    @classmethod
    def from_webtoon_episode(cls, soup):
        """initialize a Comic from the soup of a webtoon episode page"""

    @classmethod
    def from_webtoon_comic(cls, soup):
        """initialize a Comic from the soup of a webtoon comic page"""

    @classmethod
    def from_local_comic(cls, soup):
        """initialize a Comic from the soup of a local comic page"""
