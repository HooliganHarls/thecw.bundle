import re, string, datetime
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

TheCW_PLUGIN_PREFIX   = "/video/TheCW"

TheCW_ROOT            = "http://www.cwtv.com"
TheCW_SHOWS_LIST      = "http://www.cwtv.com/shows"
EP_URL             = "http://www.cwtv.com/cw-video/"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(TheCW_PLUGIN_PREFIX, MainMenu, "The CW", "icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.art = R('art-default.jpg')
  MediaContainer.title1 = 'TVLand Full Episodes'
  DirectoryItem.thumb=R("icon-default.jpg")
  
####################################################################################################
#def MainMenu():
#    dir = MediaContainer(mediaType='video')
#    dir.Append(Function(DirectoryItem(MeatList, "Full Episodes"), pageUrl = TheCW_SHOWS_LIST))
#    
#    return dir
#
####################################################################################################
def MainMenu():
    
    
    dir = MediaContainer(mediaType='video')
    pageUrl=TheCW_SHOWS_LIST
    Log(pageUrl)
    content = XML.ElementFromURL(pageUrl, True)
    Log(content)
    for item in content.xpath('//ul[@id="shows-all-list"]//li/div'):
  
        
        link = item.xpath("a")[0].get('href').replace("/shows","")
        link=EP_URL + link
        link=link.replace('video//','video/')
        title = item.xpath("a/img")[0].get('title')
        title=title.replace("-"," ")
        thumb=item.xpath("a/img")[0].get('src')
        thumb=TheCW_ROOT + thumb
        Log(link)
        Log(title)
        dir.Append(Function(DirectoryItem(eplist, title=title, thumb=thumb), pageUrl=link))
    return dir
	
####################################################################################################
def eplist(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    content = XML.ElementFromURL(pageUrl, isHTML=True)
    for item in content.xpath('//div[contains(@id,"videotabcontents_2")]//div/div[@class="videowrapped"]'):
        link =item.xpath("a")[0].get('href')
        link=TheCW_ROOT + link
        thumb = item.xpath("a/span/img")[0].get('src') 
        Log(thumb)
        page = HTTP.Request(link)
        mediakey=re.compile("var curPlayingGUID = '(.+?)';").findall(page)[0]
        title =item.xpath("a/span")[1].text
        link="http://www.cwtv.com/images/dsplayer/vsplayer.swf?config=vsplayer.xml&mediaKey=" + mediakey + "&alwaysAutoPlay=true"
        Log(link)

        dir.Append(WebVideoItem(url=link, title=title, thumb=thumb))
    return dir

