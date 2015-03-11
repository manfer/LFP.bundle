# -*- coding: utf-8 -*-

TITLE  = u'LFP'
PREFIX = '/video/lfp'

LFP_BASE_URL     = 'http://www.lfp.es'
LFP_MULTIMEDIA   = '%s/multimedia' % LFP_BASE_URL
LFP_JORNADA      = '%s/includes/ajax.php?action=reload_multimedia_jornada' % LFP_BASE_URL
LFP_OTROS_VIDEOS = '%s/includes/ajax.php?action=reload_multimedia_otros_videos' % LFP_BASE_URL
LFP_GALA         = '%s/gala-lfp-2013-2014' % LFP_BASE_URL
LFP_CFL          = '%s/champions-for-life-2014' % LFP_BASE_URL

LFP_SEARCH = "%s/buscador/{0}/?filtro=videos" % LFP_BASE_URL
LFP_SEARCH_PAGE = "%s/buscador/{0}/page/{1}/?filtro=videos" % LFP_BASE_URL

LFP_ICON        = 'lfp.png'
ICON            = 'default-icon.png'
LFP_HL_ICON     = 'highlights.png'
LFP_VIDEO_ICON  = 'video.png'
LFP_PHOTO_ICON  = 'photo.png'

SEARCH_ICON     = 'search-icon.png'
SETTINGS_ICON   = 'settings-icon.png'

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

  Locale.DefaultLocale = Prefs["language"].split("/")[1]

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

  if Client.Product != 'PlexConnect':
    oc.add(InputDirectoryObject(
      key     = Callback(lfp_search),
      title   = L('Search LFP Videos'),
      prompt  = L('Search for LFP Videos'),
      summary = L('Search for LFP Videos'),
      thumb   = R(SEARCH_ICON)
    ))

  return oc

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
      thumb = thumb
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
      thumb = thumb
    ))

  return oc

################################################################################
@route(PREFIX+'/fotos')
def lfp_fotos():

  oc = ObjectContainer( title2 = L('Photos') )

  oc.add(DirectoryObject(
    key = Callback(
      lfp_galeria_liga,
      id_competicion = "1",
      title = L("BBVA League")
    ),
	title = L("BBVA League"),
    summary = L("BBVA League teams photos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_galeria_liga,
      id_competicion = "2",
      title = L("Adelante League")
    ),
	title = L("Adelante League"),
    summary = L("Adelante League teams photos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      lfp_galerias,
      url = "http://www.lfp.es/multimedia/temporada-2014-2015/copa-del-rey",
      title = L("King's Cup")
    ),
	title = L("King's Cup"),
    summary = L("King's cup photo galeries")
  ))

  oc.add(PhotoAlbumObject(
    key = Callback(
      lfp_galeria,
      galeria = 'gallery4_5',
      url = LFP_MULTIMEDIA,
      title = L('Europe 2014-2015')
    ),
    rating_key = 'lfp_gallery4_5',
    title = L('Europe 2014-2015'),
    summary = L('BBVA league teams in european competitions')
  ))

  oc.add(PhotoAlbumObject(
    key = Callback(
      lfp_galeria,
      galeria = 'gallery',
      url = LFP_GALA,
      title = L('2013-2014 LFP Awards Ceremony')
    ),
    rating_key = 'lfp_gallery_gala_2013_2014',
    title = L('2013-2014 LFP Awards Ceremony'),
    summary = L('2013-2014 LFP Awards Ceremony photo gallery')
  ))

  oc.add(PhotoAlbumObject(
    key = Callback(
      lfp_galeria,
      galeria = 'gallery',
      url = LFP_CFL,
      title = L('Champions for Life')
    ),
    rating_key = 'lfp_gallery_cfl',
    title = L('Champions for Life'),
    summary = L('match for the childhood photo gallery')
  ))

  return oc

################################################################################
@route(PREFIX+'/galerialiga/{id_competicion}')
def lfp_galeria_liga(id_competicion, title):

  oc = ObjectContainer( title2 = unicode(title) )

  data = HTML.ElementFromURL(
    LFP_BASE_URL,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  equipos = data.xpath('//div[@id="galeria_' + id_competicion + '"]/div/a')

  for equipo in equipos:
    title = equipo.xpath('.//@title')[0]
    url   = equipo.xpath('.//@href')[0]
    rel   = equipo.xpath('.//@rel')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_galerias,
        url = url,
        title = title
      ),
      title = title,
      thumb = R(rel + '.png')
    ))

  return oc

################################################################################
@route(PREFIX+'/galerias')
def lfp_galerias(url, title):

  oc = ObjectContainer( title2 = unicode(title) )

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  galerias = data.xpath('//div[@class="marco_galeria"]')

  for galeria in galerias:
    id      = galeria.xpath('.//div[@class="box_foto"]/a/@data-fancybox-group')[0]
    title   = galeria.xpath('.//div[@class="box_foto"]/a/@title')[0]
    summary = u" - ".join(galeria.xpath('.//div[@class="box_titulo_galeria"]/div/text()'))
    thumb   = galeria.xpath('.//div[@class="box_foto"]/a/img/@src')[0]

    try:
      title = unicode(title.encode("Latin-1"))
    except:
      title = title

    try:
      summary = unicode(summary.encode("Latin-1"))
    except:
      summary = summary
	
    oc.add(PhotoAlbumObject(
      key = Callback(
        lfp_galeria,
        galeria = id,
        url = url,
        title = summary
      ),
      rating_key = 'lfp_' + id,
      title = title,
      summary = summary,
      thumb = Resource.ContentsOfURLWithFallback(thumb)
    ))

  return oc

################################################################################
@route(PREFIX+'/galeria/{galeria}')
def lfp_galeria(galeria, url, title):

  oc = ObjectContainer( title2 = unicode(title) )

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  photos = data.xpath('//a[@data-fancybox-group="' + galeria + '"]')

  for index, photo in enumerate(photos):
    url = photo.xpath('./@href')[0]
    oc.add(PhotoObject(
      key = url,
      rating_key = 'lfp_' + galeria + '_foto' + str(index),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url)
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

################################################################################
@route(PREFIX+'/search/{query}')
def lfp_search(query, page = 1):

  page = int(page) 

  oc = ObjectContainer(
    title2 = unicode(L('Search Results') + ': ' + query  + ' | ' + L('Page') + ' ' + str(page))
  )

  noresults = ObjectContainer(
    header   = L('Video not found'),
    message  = L('Video not found'),
    no_cache = True
  )

  url = LFP_SEARCH.format(query) if (page == 1) else LFP_SEARCH_PAGE.format(query, str(page)) 
  content = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS
  )
  videos = content.xpath('//div[@id="contenedor_noticias"]/div[contains(@class, "subnoticia")]')

  if len(videos) > 0:
    for video in videos:
      video_title   = video.xpath('.//span[@class="titular_subnoticia_comun"]/text()')[0].strip()
      video_url     = video.xpath('.//a/@href')[0]
      video_thumb   = video.xpath('.//img/@src')[0]
      video_summary = video.xpath('.//span[@class="texto_subnoticia_comun"]//text()')
      video_summary = "\n".join(video_summary)

      oc.add(DirectoryObject(
        key = Callback(
          lfp_play,
          url = video_url,
          title = video_title
        ),
        title = video_title,
        summary = video_summary,
        thumb = Resource.ContentsOfURLWithFallback(video_thumb)
      ))

    paginador = content.xpath('//div[@id="paginacion_otras_noticias"]/span/following-sibling::a')

    if len(paginador) > 0:
      oc.add(NextPageObject(
        key = Callback(
          lfp_search,
          query = query,
          page = page + 1
        ),
        title = L('Next Page') + ' >>'
      ))

    return oc
  else:
    return noresults

################################################################################
def L(string):
  local_string = Locale.LocalString(string)
  return str(local_string).decode()