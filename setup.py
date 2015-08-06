# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name         = 'sgfSpider',
    version      = '0.1',
    packages     = find_packages(exclude=['tests*']),
    description  = 'sgfSpider',
    scripts      = [],
    author       = 'david hodges',
    author_email = '',
    install_requires = ['scrapy', 'ipython', 'pytest']
)
