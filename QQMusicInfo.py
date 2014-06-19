#!/usr/bin/python
#-*-coding: utf-8 -*-
'''
Created on 2013-4-20

Python 2.7

@author: qyou
'''

import urllib2
def html(url):
    return urllib2.urlopen(url).read()

import re
# get all the sub html urls
def getSongUrls(singerID):
    if len(singerID) == 1:
        pageLabel = singerID
    elif singerID[-2] == '0':
        pageLabel = singerID[-1]
    else:
        pageLabel = singerID[-2:]
    entryUrl = r'http://music.qq.com/midportal/static/singer/json/song/%s/%s_1_1.js?loginUin=0&hostUin=0&format=jsonp&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&jsonpCallback=MusicJsonCallback&needNewCode=0' % (pageLabel, singerID)
    totalNoHtml = html(entryUrl)
    m = re.search('total:(?P<totalNo>\d+)', totalNoHtml)
    assert m
    totalNo = int(m.group('totalNo'))
    SONG_NO_PER_PAGE = 60
    pageNo = totalNo/SONG_NO_PER_PAGE + 1
    songUrls = []
    for i in range(1,pageNo+1):
        songUrl = r'http://music.qq.com/midportal/static/singer/json/song/%s/%s_1_%s.js?loginUin=0&hostUin=0&format=jsonp&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&jsonpCallback=MusicJsonCallback&needNewCode=0' % (pageLabel, singerID, i)
        songUrls.append(songUrl)
    return songUrls

# sub song info page analyze        
class SongInfoPage(object):
    def __init__(self, songInfoUrl):
        self.html = html(songInfoUrl)
    def extractSongInfos(self):
        songInfos = []
        pattern = r'musicData:"(?P<songID>\d+)\|(?P<songName>.+?)\|(?P<singerID>\d+)\|(?P<singerName>.+?)\|(?P<abumID>\d+)\|(?P<abumName>.+?)\|\d+\|(?P<songTime>\d+)\|'
        for m in re.finditer(pattern, self.html):
            songInfo = (m.group('songName'), m.group('singerName'), m.group('abumName'), m.group('songTime'))
            songInfos.append(songInfo)
        return songInfos
# get all the song info by singerID    
def getSongInfosBySingerID(singerID):
    songInfoUrls = getSongUrls(singerID)
    songInfos = []
    for songInfoUrl in songInfoUrls:
        songInfoPage = SongInfoPage(songInfoUrl)
        songInfosPerPage = songInfoPage.extractSongInfos()
        songInfos += songInfosPerPage
    return songInfos

    
#############################
#-----MAIN ENTRY-------------
#############################    
def main(args):
    singerID_XuWei = '3376'
    songInfos = getSongInfosBySingerID(singerID_XuWei)
    print u"共有 %d首:" % len(songInfos)
    for songInfo in songInfos:
        print u"%s|%s|%s|%s秒" % (songInfo[0],
               songInfo[1], 
               songInfo[2],
               songInfo[3])    

import sys
import time
if __name__ == '__main__':
    tic = time.time()
    main(sys.argv)
    toc = time.time()
    print "Elapse %s seconds!" % (toc-tic)
