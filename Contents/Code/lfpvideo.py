# -*- coding: utf-8 -*-
from lfputil import L

LFP_JORNADA      = '%s/includes/ajax.php?action=reload_multimedia_jornada' % LFP_BASE_URL
LFP_OTROS_VIDEOS = '%s/includes/ajax.php?action=reload_multimedia_otros_videos' % LFP_BASE_URL
LFP_GALA         = '%s/gala-lfp-2013-2014' % LFP_BASE_URL
LFP_CFL          = '%s/champions-for-life-2014' % LFP_BASE_URL

################################################################################
@route(PREFIX+'/resumenes')
def lfp_resumenes():

  oc = ObjectContainer( title2 = L("Highlights") )

  oc.add(DirectoryObject(
    key = Callback(
      lfp_temporadas,
      id_competicion = '1',
      title = L("BBVA League Highlights")
    ),
	title = L("BBVA League"),
    summary = L("enjoy BBVA League matches highlights")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_temporadas,
      id_competicion = '2',
      title = L("Adelante League Highlights")
    ),
	title = L("Adelante League"),
    summary = L("enjoy Adelante League matches highlights")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos')
def lfp_videos():

  oc = ObjectContainer( title2 = L("Videos") )

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "lfp-world-challenge",
      title = L("LFP World Challenge")
    ),
	title = L("LFP World Challenge"),
    summary = L("LFP teams playing arround the world")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "entrevistas-lfp",
      title = L("LFP Interviews")
    ),
	title = L("LFP Interviews"),
    summary = L("interviews to members of the LFP")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "gala-lfp-201314",
      title = L("LFP 2014 Awards Ceremony")
    ),
	title = L("LFP 2014 Awards Ceremony"),
    summary = L("the 2014 awards ceremony best moments")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "champions-for-life",
      title = L("Champions for Life")
    ),
	title = L("Champions for Life"),
    summary = L("match for the childhood")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "el-clasico",
      title = L("The Classic")
    ),
	title = L("The Classic"),
    summary = L("the rivalry matches Barcelona vs Real Madrid")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "america",
      title = L("America")
    ),
	title = L("America"),
    summary = L("american Players in LFP")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_otros_videos,
      slug = "otros",
      title = L("Others")
    ),
	title = L("Others"),
    summary = L("other videos from LFP")
  ))

  return oc

################################################################################
@route(PREFIX+'/temporadas/{id_competicion}')
def lfp_temporadas(id_competicion, title):

  data = HTML.ElementFromURL(
    LFP_MULTIMEDIA,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  temporadas = data.xpath('//select[@id="temporadas_comp' + id_competicion + '"]/option')

  oc = ObjectContainer( title2 = unicode(title) )

  for temporada in temporadas:
    id_temporada = temporada.xpath('./@value')[0]
    name = temporada.xpath('./text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_jornadas,
        id_competicion = id_competicion,
        id_temporada = id_temporada,
        title = name
      ),
      title = name
    ))

  return oc

################################################################################
@route(PREFIX+'/jornadas/{id_competicion}/{id_temporada}')
def lfp_jornadas(id_competicion, id_temporada, title):

  data = HTML.ElementFromURL(
    LFP_MULTIMEDIA,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  jornadas = data.xpath('//select[@id="jornadas_comp' + id_competicion + '_temp' + id_temporada + '"]/option')

  oc = ObjectContainer( title2 = unicode(title) )

  for jornada in jornadas:
    id_jornada = jornada.xpath('./@value')[0]
    name = jornada.xpath('./text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_jornada,
        id_competicion = id_competicion,
        id_temporada = id_temporada,
        jornada = id_jornada,
        title = name
      ),
      title = name
    ))

  return oc

################################################################################
@route(PREFIX+'/jornada/{id_competicion}/{id_temporada}/{jornada}')
def lfp_jornada(id_competicion, id_temporada, jornada, title):

  data = HTML.ElementFromURL(
    LFP_JORNADA,
    headers = HTTP_HEADERS,
    values = {
      'id_competicion': id_competicion,
      'id_temporada': id_temporada,
      'jornada': jornada,
    },
    cacheTime = CACHE_1HOUR
  )

  oc = ObjectContainer( title2 = unicode(title) )

  videos = data.xpath('//a[contains(@class, "video-fancybox")]')

  for video in videos:
    url = video.xpath('.//@href')[0]
    thumb = video.xpath('.//img/@src')[0]
    title = video.xpath('.//span[@class="title"]/text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_play,
        url = url,
        title = title
      ),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))

  if int(jornada) > 1:
    anterior_jornada = str(int(jornada) - 1)
    oc.add(NextPageObject(
      key   = Callback(
        lfp_jornada,
        id_competicion = id_competicion,
        id_temporada = id_temporada,
        jornada = anterior_jornada,
        title = unicode(L('Day') + ' ' + anterior_jornada),
      ),
      title = L('Previous Day') + ' >>'
    ))

  return oc

################################################################################
@route(PREFIX+'/otros/{slug}')
def lfp_otros_videos(slug, title):

  oc = ObjectContainer( title2 = unicode(title) )

  data = HTML.ElementFromURL(
    LFP_OTROS_VIDEOS,
    headers = HTTP_HEADERS,
    values = { 'slug': slug },
    cacheTime = CACHE_1DAY
  )

  videos = data.xpath('//div[contains(@class, "each_video")]')

  for video in videos:
    url = video.xpath('.//a[contains(@class, "cdn-video")]/@href')[0]
    thumb = video.xpath('.//img/@src')[0]
    title = video.xpath('.//span[@class="title"]/text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_play,
        url = url,
        title = title
      ),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))

  return oc

################################################################################
@route(PREFIX+'/play')
def lfp_play(url, title):

  try:
    data = HTML.ElementFromURL(
      url,
      headers = HTTP_HEADERS,
      cacheTime = CACHE_1DAY
    )
  except:
    raise Ex.MediaNotAvailable

  video = url

  meta_content = data.xpath('//meta[@name="twitter:player"]/@content')[0]
  if 'youtube' in meta_content:
    video = meta_content

  oc = ObjectContainer(
    title2 = unicode(title)
  )

  oc.add(URLService.MetadataObjectForURL(video))

  return oc
