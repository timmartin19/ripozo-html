from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import webbrowser

import unittest2
from ripozo import ResourceBase, restmixins, apimethod

from ripozo_html import HTMLAdapter


class DumbTests(unittest2.TestCase):
    file_name = 'temp.html'

    def tearDown(self):
        # os.remove(self.file_name)
        pass

    def test_simple(self):
        class MyResource(restmixins.ResourceBase):
            pks = 'id',

            @apimethod(methods=['GET'])
            def something(cls, request):
                return cls(properties=dict(id=1, value='It Worked'))

        res = MyResource(properties=dict(id=1, value='It Worked!'))
        adapter = HTMLAdapter(res, base_url='http://localhost:5000/')
        with open(self.file_name, 'w') as html_page:
            html_page.write(adapter.formatted_body)
        resp = webbrowser.open(self.file_name)
        assert False
