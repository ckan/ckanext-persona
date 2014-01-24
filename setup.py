from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-persona',
    version=version,
    description="Use Mozilla Persona to login to CKAN",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Sean Hammond',
    author_email='seanh@seanh.cc',
    url='seanh.sdfeu.org',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.persona'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.persona.plugin:PluginClass
        persona=ckanext.persona.plugin:PersonaPlugin
    ''',
)
