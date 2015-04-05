# -*- coding: utf-8 -*-

################################################################################
def L(string):
  Request.Headers['X-Plex-Language'] = Prefs["language"].split("/")[1]
  local_string = Locale.LocalString(string)
  return str(local_string).decode()
