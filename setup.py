#!/usr/bin/env python

from setuptools import Extension, setup


ext_modules = [
    Extension('craspiutil',
              libraries = ['wiringPi'],
              sources=['csensors.c'])
]

setup(name='raspberry-pi-utilities',
      version='0.3.0',
      description='Raspberry Pi utilities',
      author='Yusuke Miyazaki',
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/litesystems/raspberry-pi-utilities',
      packages=['raspiutil'],
      ext_modules=ext_modules,
      test_suite='tests',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
      ]
)
