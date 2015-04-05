# -*- coding: utf-8 -*-
from lfputil import L

LFP_LALIGATV_DIRECTOS = '%s/laligatv' % LFP_BASE_URL
LFP_LALIGATV_RESUMENES = '%s/laligatv/resumenes' % LFP_BASE_URL
LFP_LALIGATV_RESUMENES_TEMPORADA = '%s/laligatv/resumenes/{0}' % LFP_BASE_URL
LFP_LALIGATV_RESUMENES_JORNADA = '%s/laligatv/resumenes/{0}/jornada/{1}' % LFP_BASE_URL
LFP_LALIGATV_EXTRAS = '%s/laligatv/extras' % LFP_BASE_URL
LFP_LALIGATV_EXTRAS_TEMPORADA = '%s/laligatv/extras/{0}' % LFP_BASE_URL
LFP_LALIGATV_EXTRAS_JORNADA = '%s/laligatv/extras/{0}/jornada/{1}' % LFP_BASE_URL
LFP_LALIGATV_SHOWS = '%s/laligatv/programas' % LFP_BASE_URL
LFP_LALIGATV_SHOWS_TEMPORADA = '%s/laligatv/programas/{0}' % LFP_BASE_URL
LFP_LALIGATV_SHOWS_POST = '%s/includes/ajax.php?action=reload_webtv_programa_aspire' % LFP_BASE_URL

RE_JSON = Regex('\.setup\(({.+?})\)\.', Regex.DOTALL)

################################################################################
@route(PREFIX+'/laligatv')
def lfp_laligatv():
  oc = ObjectContainer( title2 = u'La Liga TV' )

  oc.add(DirectoryObject(
    key = Callback(lfp_laligatv_directos),
    title = L('Live'),
    summary = L('enjoy Adelante League live matches'),
    thumb = R(LFP_LALIGATV_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_laligatv_resumenes),
    title = L('Highlights'),
    summary = L('Adelante League hightlights'),
    thumb = R(LFP_LALIGATV_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_laligatv_extras),
    title = L('Extras'),
    summary = L('Adelante League extra videos'),
    thumb = R(LFP_LALIGATV_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback(lfp_laligatv_shows),
    title = L('Shows'),
    summary = L('Adelante League shows'),
    thumb = R(LFP_LALIGATV_ICON)
  ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/directos')
def lfp_laligatv_directos():
  oc = ObjectContainer( title2 = L('Live') )

  content = HTML.ElementFromURL(
    LFP_LALIGATV_DIRECTOS,
    headers = HTTP_HEADERS
  )
  directos = content.xpath('//div[contains(@class, "jornadas")]')

  for directo in directos:
    fecha = directo.xpath('./preceding-sibling::*/text()')[0]
    hora = directo.xpath('.//span[@class="hora_partido_otras_competiciones"]/text()')[0]
    equipo_local = directo.xpath('.//span[@class="equipo_local_otras_competiciones"]/text()')[0]
    equipo_visitante = directo.xpath('.//span[@class="equipo_visitante_otras_competiciones"]/text()')[0]
    title = equipo_local + ' - ' + equipo_visitante
    summary = hora + ' | ' + fecha
    try:
      url = directo.xpath('./a[contains(@class, "directo-webtv")]/@href')[0]
      oc.add(DirectoryObject(
        key = Callback(
          lfp_laligatv_directo,
          url = url,
          title = title
        ),
        title = unicode(title),
        summary = unicode(summary),
        thumb = R(LFP_LALIGATV_ICON)
      ))
    except:
      oc.add(DirectoryObject(
        key = Callback(
          lfp_laligatv_nodirecto,
          title = title
        ),
        title = unicode(title),
        summary = unicode(summary),
        thumb = R(LFP_LALIGATV_ICON)
      ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/directo')
def lfp_laligatv_directo(url, title):
  oc = ObjectContainer( title2 = unicode(title) )

  page = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1MINUTE
  )
  content = HTML.StringFromElement(page)

  thumb = page.xpath('//meta[@property="og:image"]/@content')[0]

  try:
    json = RE_JSON.search(content, Regex.DOTALL).group(1)
    json = JSON.ObjectFromString(json)
    m3u8_url = json['sources'][0]['file']

    oc.add(VideoClipObject(
      key = Callback(
        lfp_laligatv_playHLS,
        url = m3u8_url,
        title = title,
        thumb = thumb
      ),
      rating_key = title,
      items = [
        MediaObject(
          #protocol = Protocol.HLS,
          container = Container.MP4,
          video_codec = VideoCodec.H264,
          audio_codec = AudioCodec.AAC,
          audio_channels = 2,
          parts = [
            PartObject(
              key = m3u8_url
            )
          ]
        )
      ],
      title = unicode(title),
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))
  except:
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_nodirecto,
        title = title
      ),
      title = unicode(title),
      thumb = R(LFP_LALIGATV_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/nodirecto')
def lfp_laligatv_nodirecto(title):
  return ObjectContainer(
    title2   = unicode(title),
    header   = L('No Broadcast'),
    message  = L('no broadcast at this moment'),
    no_cache = True
  )

################################################################################
@route(PREFIX+'/laligatv/resumenes')
def lfp_laligatv_resumenes():

  data = HTML.ElementFromURL(
    LFP_LALIGATV_RESUMENES,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  temporadas = data.xpath('//select[@name="change_temporadas"]/option')

  oc = ObjectContainer( title2 = L('Highlights') )

  for temporada in temporadas:
    id_temporada = temporada.xpath('./@value')[0]
    name = temporada.xpath('./text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_resumenes_temporada,
        temporada = id_temporada,
        title = name
      ),
      title = name,
      thumb = R(LFP_LALIGATV_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/resumenes/temporada/{temporada}')
def lfp_laligatv_resumenes_temporada(temporada, title):

  url = LFP_LALIGATV_RESUMENES_TEMPORADA.format(temporada)

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  jornadas = data.xpath('//select[@name="change_jornadas"]/option')

  oc = ObjectContainer( title2 = unicode(title) )

  for jornada in jornadas:
    # Use try to ignore the option without value
    try:
      id_jornada = int(jornada.xpath('./@value')[0].split('/')[1])
      name = jornada.xpath('./text()')[0]
      oc.add(DirectoryObject(
        key = Callback(
          lfp_laligatv_resumenes_jornada,
          temporada = temporada,
          jornada = id_jornada,
          title = name
        ),
        title = name,
        thumb = R(LFP_LALIGATV_ICON)
      ))
    except:
      pass

  return oc

################################################################################
@route(PREFIX+'/laligatv/resumenes/jornada/{temporada}/{jornada}', jornada = int)
def lfp_laligatv_resumenes_jornada(temporada, jornada, title):

  url = LFP_LALIGATV_RESUMENES_JORNADA.format(temporada, jornada)

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
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
        lfp_laligatv_play,
        url = url,
        title = title
      ),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))

  if int(jornada) > 1:
    anterior_jornada = jornada - 1
    oc.add(NextPageObject(
      key   = Callback(
        lfp_laligatv_resumenes_jornada,
        temporada = temporada,
        jornada = anterior_jornada,
        title = unicode(L('Day') + ' ' + str(anterior_jornada)),
      ),
      title = L('Previous Day') + ' >>'
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/extras')
def lfp_laligatv_extras():

  data = HTML.ElementFromURL(
    LFP_LALIGATV_EXTRAS,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  temporadas = data.xpath('//select[@name="change_temporadas"]/option')

  oc = ObjectContainer( title2 = L('Extras') )

  for temporada in temporadas:
    id_temporada = temporada.xpath('./@value')[0]
    name = temporada.xpath('./text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_extras_temporada,
        temporada = id_temporada,
        title = name
      ),
      title = name,
      thumb = R(LFP_LALIGATV_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/extras/temporada/{temporada}')
def lfp_laligatv_extras_temporada(temporada, title):

  url = LFP_LALIGATV_EXTRAS_TEMPORADA.format(temporada)

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  jornadas = data.xpath('//select[@name="change_jornadas"]/option')

  oc = ObjectContainer( title2 = unicode(title) )

  for jornada in jornadas:
    # Use try to ignore the option without value
    try:
      id_jornada = int(jornada.xpath('./@value')[0].split('/')[1])
      name = jornada.xpath('./text()')[0]
      oc.add(DirectoryObject(
        key = Callback(
          lfp_laligatv_extras_jornada,
          temporada = temporada,
          jornada = id_jornada,
          title = name
        ),
        title = name,
        thumb = R(LFP_LALIGATV_ICON)
      ))
    except:
      pass

  return oc

################################################################################
@route(PREFIX+'/laligatv/extras/jornada/{temporada}/{jornada}', jornada = int)
def lfp_laligatv_extras_jornada(temporada, jornada, title):

  url = LFP_LALIGATV_EXTRAS_JORNADA.format(temporada, jornada)

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
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
        lfp_laligatv_play,
        url = url,
        title = title
      ),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))

  if int(jornada) > 1:
    anterior_jornada = jornada - 1
    oc.add(NextPageObject(
      key   = Callback(
        lfp_laligatv_extras_jornada,
        temporada = temporada,
        jornada = anterior_jornada,
        title = unicode(L('Day') + ' ' + str(anterior_jornada)),
      ),
      title = L('Previous Day') + ' >>'
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/play')
def lfp_laligatv_play(url, title):

  try:
    data = HTML.ElementFromURL(
      url,
      headers = HTTP_HEADERS,
      cacheTime = CACHE_1DAY
    )
  except:
    raise Ex.MediaNotAvailable

  video = data.xpath('//div[contains(@class,  "player_highlight")]/@data-url')[0]

  oc = ObjectContainer(
    title2 = unicode(title)
  )

  oc.add(URLService.MetadataObjectForURL(video))

  return oc

################################################################################
@route(PREFIX+'/laligatv/shows')
def lfp_laligatv_shows():

  data = HTML.ElementFromURL(
    LFP_LALIGATV_SHOWS,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1DAY
  )

  temporadas = data.xpath('//select[@name="change_temporadas"]/option')

  oc = ObjectContainer( title2 = L('Shows') )

  for temporada in temporadas:
    id_temporada = temporada.xpath('./@value')[0]
    name = temporada.xpath('./text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_shows_temporada,
        temporada = id_temporada,
        title = name
      ),
      title = name,
      thumb = R(LFP_LALIGATV_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/shows/temporada/{temporada}')
def lfp_laligatv_shows_temporada(temporada, title):

  url = LFP_LALIGATV_SHOWS_TEMPORADA.format(temporada)

  data = HTML.ElementFromURL(
    url,
    headers = HTTP_HEADERS,
    cacheTime = CACHE_1HOUR
  )

  oc = ObjectContainer( title2 = unicode(title) )

  videos = data.xpath('//a[contains(@class, "video-webtv_programa-aspire")]')

  for video in videos:
    hash = video.xpath('.//@href')[0][1:]
    thumb = video.xpath('.//img/@src')[0]
    title = video.xpath('.//span[@class="title"]/text()')[0]
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_shows_play,
        hash = hash,
        title = title
      ),
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/shows/play')
def lfp_laligatv_shows_play(hash, title):

  oc = ObjectContainer( title2 = unicode(title) )

  content = HTTP.Request(
    LFP_LALIGATV_SHOWS_POST,
    headers = HTTP_HEADERS,
    values = {
      'hash': hash,
      'id_competicion': 2
    },
    cacheTime = CACHE_1MINUTE
  ).content

  try:
    json = RE_JSON.search(content).group(1)
    json = JSON.ObjectFromString(json)
    m3u8_url = json['sources'][0]['file']
    thumb = json['image']

    oc.add(VideoClipObject(
      key = Callback(
        lfp_laligatv_playHLS,
        url = m3u8_url,
        title = title,
        thumb = thumb
      ),
      rating_key = title,
      items = [
        MediaObject(
          #protocol = Protocol.HLS,
          container = Container.MP4,
          video_codec = VideoCodec.H264,
          audio_codec = AudioCodec.AAC,
          audio_channels = 2,
          parts = [
            PartObject(
              key = m3u8_url
            )
          ]
        )
      ],
      title = unicode(title),
      thumb = Resource.ContentsOfURLWithFallback(url = thumb),
      art = Resource.ContentsOfURLWithFallback(url = thumb)
    ))
  except:
    oc.add(DirectoryObject(
      key = Callback(
        lfp_laligatv_nodirecto,
        title = title
      ),
      title = unicode(title),
      thumb = R(LFP_LALIGATV_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/laligatv/playhls')
def lfp_laligatv_playHLS(url, title, thumb):
  oc = ObjectContainer( title2 = title )

  oc.add(VideoClipObject(
    key = Callback(
      lfp_laligatv_playHLS,
      url = url,
      title = title,
      thumb = thumb
    ),
    rating_key = title,
    items = [
      MediaObject(
        #protocol = Protocol.HLS,
        container = Container.MP4,
        video_codec = VideoCodec.H264,
        audio_codec = AudioCodec.AAC,
        audio_channels = 2,
        parts = [
          PartObject(
            key = url
          )
        ]
      )
    ],
    title = title,
    thumb = Resource.ContentsOfURLWithFallback(url = thumb),
    art = Resource.ContentsOfURLWithFallback(url = thumb)
  ))

  return oc
