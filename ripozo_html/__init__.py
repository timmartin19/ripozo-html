from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from jinja2 import Environment, FileSystemLoader
from ripozo import adapters
from ripozo.adapters.base import AdapterBase
from ripozo.utilities import titlize_endpoint
from ripozo.resources.resource_base import create_url
from ripozo.resources.constants import input_categories
from ripozo import fields
import six

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
_TEMPLATE_LOADER = FileSystemLoader(searchpath=_TEMPLATE_DIR)
_JINJA_ENV = Environment(loader=_TEMPLATE_LOADER)

_FIELD_TYPES = {
    fields.BaseField: 'text',
    fields.BooleanField: 'checkbox',
    fields.DateTimeField: 'datetime',
    fields.FloatField: 'number',
    fields.IntegerField: 'integer',
    fields.StringField: 'text'
}


class _HTMLField(object):
    """
    A holder in place of a namedtuple due to performance
    """
    def __init__(self, name, type_, default):
        """
        A data holder to construct an HTMl field.

        :param unicode name: The name of the field
        :param unicode type_: The html type of the input
        :param unicde default: The default value for the field
        """
        self.name = name
        self.type_ = type_
        self.default = default


class HTMLAdapter(AdapterBase):
    """
    An adapter that displays browser readable content.  This content
    is still 100% ReSTful simply displaying the content in an easy to read
    manner.  Perfect for development or getting users comfortable with using
    the API.

    :param list[unicode] formats: The formats that this adapter exposes
    """
    formats = ['text/html']
    _default_adapters = (adapters.BasicJSONAdapter, adapters.JSONAPIAdapter,
                         adapters.SirenAdapter, adapters.HalAdapter)

    def __init__(self, resource=None, base_url='', adapters=None):
        """
        Initialize an adapter capable of showing the resources available
        on the API

        :param resource: The resource that is being formatted.
        :type resource: ripozo.resource.resource_base.ResourceBase
        :param str|unicode base_url: The url to prepend to
            all of the urls.
        :param adapters: A list of adapters whose formats will be displayed to the user.
        :type adapters: list[ripozo.adapters.AdapterBase]|tuple(ripozo.adapters.AdapterBase)
        :param tuple adapters: The adapters to show when
            as available options in the api.
        """
        super(HTMLAdapter, self).__init__(resource, base_url=base_url)
        self._adapter_types = adapters if adapters is not None else self._default_adapters

    def __call__(self, resource, **kwargs):
        """
        Creates a new instance of the HTMLAdapter from this
        adapter passing the adapters that were used to instantiate
        this adapter instance

        :return: A new HTMLAdapter instance
        :rtype: HTMLAdapter
        """
        return self.__class__(resource, adapters=self._adapter_types, **kwargs)

    def extra_headers(self):
        """
        :return: Returns a dictionary with the Content-Type Header
        :rtype: dict
        """
        return {'Content-Type': self.formats[0]}

    @property
    def formatted_body(self):
        """
        Returns an HTML string that can be rendered by a browser.
        The HTML will also show the formats for various adapters types.

        :return: An HTML string
        :rtype: unicode
        """
        template_vars = dict(resources=[self.resource], adapter=self,
                             actions=self._actions, all_adapters=self._adapters)
        template = _JINJA_ENV.get_template('full.jinja')
        return template.render(template_vars)

    @property
    def _adapters(self):
        """
        :return: A list of adapter dicts for Jinja
        :rtype: list[dict]
        """
        adapter_dicts = []
        for adapter_type in self._adapter_types:
            adapter = adapter_type(self.resource, base_url=self.base_url)
            adapter_dict = dict(name=adapter_type.__name__,
                                content_type=adapter_type.formats[0],
                                body=adapter.formatted_body)
            adapter_dicts.append(adapter_dict)
        return adapter_dicts

    @property
    def _actions(self):
        """
        Gets the list of actions in an appropriate format for Jinja2
        to read.

        :return: The list of actions
        :rtype: list
        """
        actions = []
        for endpoint, options in six.iteritems(self.resource.endpoint_dictionary()):
            options = options[0]
            all_methods = options.get('methods', ('GET',))
            meth = all_methods[0] if all_methods else 'GET'
            base_route = options.get('route', self.resource.base_url)
            route = create_url(base_route, **self.resource.properties)
            route = self.combine_base_url_with_resource_url(route)
            action_fields = self.generate_fields_for_endpoint_funct(options.get('endpoint_func'))
            actn = dict(title=titlize_endpoint(endpoint),
                        method=meth, url=route, fields=action_fields)
            actn['id'] = id(actn)
            actions.append(actn)
        return actions

    def generate_fields_for_endpoint_funct(self, endpoint_func):
        """
        Returns the action's fields for the inputs on the form.

        :param apimethod endpoint_func:
        :return: A dictionary of action fields
        :rtype: dict
        """
        return_fields = []
        fields_method = getattr(endpoint_func, 'fields', None)
        if not fields_method:
            return []
        action_fields = fields_method(self.resource.manager)

        for field in action_fields:
            if field.arg_type is input_categories.URL_PARAMS:
                continue
            field_obj = _HTMLField(field.name, _FIELD_TYPES[type(field)],
                                   self.resource.properties.get(field.name))
            return_fields.append(field_obj)
        return return_fields
