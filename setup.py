#!/usr/bin/env python

from setuptools import setup


setup(name='mailchimp',
      version='0.1',
      description='Mailchimp API written in python',
      author='Lelia Rubiano',
      author_email='lrubiano10@gmail.com',
      url='https://github.com/GearPlug/mailchimp',
      packages=['mailchimp'],
      install_requires=[
          'requests',
      ],
      keywords='mailchimp',
      zip_safe=False,
      license='GPL',
     )