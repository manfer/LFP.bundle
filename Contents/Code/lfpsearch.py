# -*- coding: utf-8 -*-
LFP_SEARCH = "%s/buscador/{0}/?filtro=videos" % LFP_BASE_URL
LFP_SEARCH_PAGE = "%s/buscador/{0}/page/{1}/?filtro=videos" % LFP_BASE_URL

################################################################################
@route(PREFIX+'/search', page = int)
def lfp_search(query, page = 1):

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
        thumb = Resource.ContentsOfURLWithFallback(url = video_thumb),
        art = Resource.ContentsOfURLWithFallback(url = video_thumb)
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
