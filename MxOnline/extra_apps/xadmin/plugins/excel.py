# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/18 下午 11:12'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from django.shortcuts import render


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        # nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)