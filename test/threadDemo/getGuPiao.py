#-*- coding: utf-8 -*-

import csv
from xml.etree.ElementTree import Element, ElementTree
import requests
from xml_pretty import pretty

def download(url):
	