# ----------------------------------------------------------------
# Author: wayneferdon wayneferdon@hotmail.com
# Date: 2022-02-12 06:25:49
# LastEditors: wayneferdon wayneferdon@hotmail.com
# LastEditTime: 2022-10-07 20:16:04
# FilePath: \Wox.Plugin.ChromeBookmarks\main.py
# ----------------------------------------------------------------
# Copyright (c) 2022 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

# -*- coding: utf-8 -*-
from ChromeWox import *

class GetBookmarks(ChromeWox):
    with(
        open('./plugin.json','r') as pluginJson,
        open(os.environ['localAppData'.upper()] + '/../Roaming/Wox/Settings/Settings.json','r') as settingJson
    ):
        plugInID = json.load(pluginJson)['ID']
        __actionKeyword__ = json.load(settingJson)['PluginSettings']['Plugins'][plugInID]['ActionKeywords'][0]

    def _getDatas_(self):
        return Cache.getBookmarks()

    def _getResult_(self, regex:RegexList, data:Bookmark):
        item = data.title + ';' + data.path + ';' + data.url + '/'
        if not regex.match(item):
            return
        match data.type:
            case Bookmark.Type.url:
                return WoxResult(data.title, data.url, data.icon, self._datas_.index(data), self._openUrl_.__name__, True, data.url).toDict()
            case Bookmark.Type.folder:
                if data.url == regex.queryString:
                    # if right in the quering folder, not return it
                    return
                return WoxResult(data.title, data.url, data.icon, self._datas_.index(data), 'Wox.ChangeQuery', False, GetBookmarks.__actionKeyword__ + ' ' + data.url, True).toDict()

    def _extraContextMenu_(self, data:Bookmark):
        return [self.getCopyDataResult('Directory', data.directory, ChromeData.FOLDER_ICON)]

if __name__ == '__main__':
    GetBookmarks()
    # GetBookmarks().query('other/')