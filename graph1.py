
#!/usr/bin/python
# -*- coding = <'utf-8'> -*-
import re
import heapq
from lxml import etree
import numpy as np
import itertools
import sys
import networkx as nx
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup
import cPickle as pickle

## open the file for reading
file_Name = "soupsfile"
fileObject = open(file_Name, 'rb')
#load the object from the file into var b
NewRs = pickle.load(fileObject)

NewSoups = [BeautifulSoup(NewR, "lxml") for NewR in NewRs]
#captions = [soup.find_all("div", class_ = "photocaption") for soup in NewSoups]
#print(len(captions))

captions = []
def CAPTIONS():
    for NewSoup in NewSoups:
        for cap in NewSoup.select(".photocaption"):
            cap_text = cap.text.strip()
            if cap_text != '':
                captions.append(cap_text)
    return captions

captions = CAPTIONS()
print len(captions) #108079
caps = []
def CAPS():
    for NewSoup in NewSoups:
        for cap in NewSoup.find_all("font"):
            cap_text = cap.text.strip()
            if cap_text != '':
                caps.append(cap_text)
    return caps

CAPS = CAPS()
print 'CAPS: {}'.format(len(CAPS))  #5491
 
All_captions = captions + CAPS  # total 113570 captions
print 'All Captions: {}'.format(len(All_captions))

Filtered_captions = filter(lambda x: len(x) < 250, All_captions)
print 'Filtered Captions: {}'.format(len(Filtered_captions))  #113361


names_list = ["Dr and Mrs","Dr","Mayor","Ms ","Sir","and friends", "and friend","and daughter","and son",\
            "dancers","and family","and guest","and artist","Honoree","with friends","Mr and Mrs",\
            "Mrand Mrs","Mr ","Mrs ","OSL Board Member", " MD", " Jr", " Jr"," MD", " PhD", "Photographs by",\
            'Chairmen', 'PatrickMcMullan.com']
names_dict = dict.fromkeys(names_list,'') # convert names_list to replacement dictionary
names_dict['with'] = ','
remove_words = re.compile('|'.join(names_dict.keys())) # create regex for all in dict

Filtered_captions = [All_captions[i].split() for i in range(len(Filtered_captions))]
print 'Split Captions: {}'.format(len(Filtered_captions))

#results = [[word for word in Filtered_captions[i] if word not in names_list] for i in range(len(Filtered_captions))]
#print 'total names: {}'.format(len(results))
#results = [' '.join(results[i]) for i in range(len(results))]

Filtered_captions = [re.sub('\.','',' '.join(Filtered_captions[i])) for i in xrange(len(Filtered_captions))] # remove .
results = [remove_words.sub(lambda m: names_dict[m.group(0)], Filtered_captions[i]) \
            for i in xrange(len(Filtered_captions))] # remove all words in names_list
results = [re.sub('\(.*\)','', results2[i]) for i in xrange(len(results))] # remove all parenthetical

def splice(element):
    _names = element.split(',')
    return _names
def remove_and(_names):
    _name_list =[]
    _name_list_filtered = []
    for _name in _names:
        _name = re.sub('\W+and\W+?', '!!!', _name)
        _name_list.append(re.sub('^\W+','', _name).split('!!!'))
    
    for _name in _name_list:
        if not len(_name) == 1:
            for i in xrange(len(_name)):
                if len(_name[i].split()) == 1:
                    _name_list_filtered.append([_name[i] + ' ' + re.search(r'\s(\w+[\s\w+]?)',_name[i+1]).group(1)])
                else:
                    _name_list_filtered.append([_name[i]])
        else:
            _name_list_filtered.append(_name)
    return [item for sublist in _name_list_filtered for item in filter(lambda x: len(x) < 35,sublist)]

clean_names = []
#for i in xrange(len(results)):
#    if remove_and(splice(results[i])) != []:
#        clean_names.append(remove_and(splice(results[i])))

for i in range(len(results)):
    if remove_and(splice(results[i])) != []:
        print remove_and(splice(results[i]))
