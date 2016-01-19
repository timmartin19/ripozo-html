from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import webbrowser

import unittest2
from ripozo import ResourceBase, restmixins, apimethod, Relationship, ListRelationship

from ripozo_html import HTMLAdapter


class DumbTests(unittest2.TestCase):
    file_name = 'temp.html'

    def tearDown(self):
        # os.remove(self.file_name)
        pass

    def test_simple(self):
        class MyResource(ResourceBase):
            pks = 'id',
            _relationships = (
                Relationship('some_rel', embedded=True, relation='RelatedResource', required=True),
                ListRelationship('other_rel', embedded=True, relation='RelatedResource', required=True)
            )

            @apimethod(methods=['GET'])
            def something(cls, request):
                return cls(properties=dict(id=1, value='It Worked'))

        class RelatedResource(ResourceBase):
            pks = 'id',

        rel_list = [dict(id=i, value='another') for i in range(2, 30)]
        res = MyResource(properties=dict(id=1, value='It Worked!',
                                         some_rel=dict(id=1, value='something'), other_rel=rel_list))
        adapter = HTMLAdapter(res, base_url='http://localhost:5000/')
        with open(self.file_name, 'w') as html_page:
            html_page.write(adapter.formatted_body)
        resp = webbrowser.open(self.file_name)
        assert False