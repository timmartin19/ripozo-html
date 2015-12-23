from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup


setup(
    author='Tim Martin',
    author_email='tim.martin@vertical-knowledge.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Other/Proprietary License',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='An HTML adapter for ripozo.  HATEOAS, ReSTful, and Hypermedia APIs.',
    extras_require={
        'dev': [
            'sphinx',
            'zest.releaser'
        ]
    },
    install_requires=[
        'ripozo',
        'jinja2'
    ],
    keywords='REST ReSTful Hypermedia HATEOAS Hypertext API python '
             'flask django ripozo SQL sqlalchemy database',
    name='ripozo-html',
    packages=['ripozo_html'],
    test_suite='tests',
    tests_require=[
        'mock',
        'tox',
        'unittest2'
    ]
)
