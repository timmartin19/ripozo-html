from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest2

from ripozo_html import HTMLAdapter


class TestHTMLAdapter(unittest2.TestCase):
    def test_actions(self):
        assert False

    def test_generate_fields_for_endpoint_func(self):
        assert False

    def test_adapters(self):
        assert False

    def test_call(self):
        adapter = HTMLAdapter(adapters=[])
        adapter2 = adapter(1)
        self.assertListEqual(adapter2._adapter_types, [])

    def test_init(self):
        adapter = HTMLAdapter(1)
        self.assertEqual(adapter.resource, 1)
        self.assertTupleEqual(adapter._adapter_types, HTMLAdapter._default_adapters)

    def test_init_with_adapters(self):
        adapter = HTMLAdapter(1, adapters=list())
        self.assertListEqual(adapter._adapter_types, [])

    def test_extra_headers(self):
        adapter = HTMLAdapter()
        self.assertDictEqual({'Content-Type': 'text/html'}, adapter.extra_headers())

    def test_formatted_body(self):
        assert False
