# -*- coding: utf-8 -*-
TITLE  = u'LFP'
PREFIX = '/video/lfp'

LFP_BASE_URL     = 'http://www.lfp.es'
LFP_MULTIMEDIA   = '%s/multimedia' % LFP_BASE_URL

LFP_ICON          = 'lfp.png'
ICON              = 'default-icon.png'
LFP_HL_ICON       = 'highlights.png'
LFP_VIDEO_ICON    = 'video.png'
LFP_PHOTO_ICON    = 'photo.png'
LFP_LALIGATV_ICON = 'laligatv.png'
SEARCH_ICON       = 'search-icon.png'
SETTINGS_ICON     = 'settings-icon.png'

ART = 'futbol.jpg'

HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Connection': 'keep-alive',
  'Origin': LFP_BASE_URL,
  'Referer': LFP_MULTIMEDIA
}

from lfputil import L
from lfpvideo import *
from lfpfoto import *
from laligatv import *
from lfpsearch import *

################################################################################
def Start():

  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = TITLE
  #ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)
  PhotoAlbumObject.thumb = R(ICON)

  HTTP.CacheTime = CACHE_1HOUR

################################################################################
@handler(PREFIX, TITLE, art=ART, thumb=LFP_ICON)
def lfp_main_menu():

  oc = ObjectContainer()

  oc.add(DirectoryObject(
    key = Callback(lfp_resumenes),
	title = L("Highlights"),
    summary = L("enjoy lfp highlight videos"),
    thumb = R(LFP_HL_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_videos),
	title = L("Other Videos"),
    summary = L("enjoy other videos on lfp website"),
    thumb = R(LFP_VIDEO_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_fotos),
	title = L("Photos"),
    summary = L("enjoy the photos on lfp website"),
    thumb = R(LFP_PHOTO_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_laligatv),
    title = L("La Liga TV"),
    summary = L("enjoy live Adelante League matches"),
    thumb = R(LFP_LALIGATV_ICON)
  ))

  if Client.Product != 'PlexConnect':
    oc.add(InputDirectoryObject(
      key     = Callback(lfp_search),
      title   = L('Search LFP Videos'),
      prompt  = L('Search for LFP Videos'),
      summary = L('Search for LFP Videos'),
      thumb   = R(SEARCH_ICON)
    ))

  return oc
