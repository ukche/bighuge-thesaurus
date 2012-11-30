#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name="django-bighuge",
      author="Joel Cross",
      url="http://github.com/ukch/django-bighuge",
      version='0.1',
      packages=['bighuge'],
      package_dir={'': 'src'},
      package_data={},
      zip_safe=True,
      install_requires=["requests"],
)
