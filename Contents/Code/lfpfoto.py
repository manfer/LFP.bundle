# -*- coding: utf-8 -*-

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

    try:
      title = unicode(title.encode("Latin-1"))
    except:
      title = title

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
      title = unicode(title),
      thumb = Resource.ContentsOfURLWithFallback(url)
    ))

  return oc
