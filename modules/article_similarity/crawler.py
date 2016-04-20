#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Module to crawl and extract data from blogs."""

import codecs
import requests
from bs4 import BeautifulSoup


def crawl(url, fname):
    """Crawl and extract valid content and write to file."""
    d = requests.get(url).text
    b = BeautifulSoup(d)
    p = [x.text for x in b.find_all("p")]
    c = codecs.open(fname, "w", encoding='utf-8')
    c.write("\n".join(p))

if __name__ == '__main__':
    crawl('http://www.blogspot.com', 'blog')
