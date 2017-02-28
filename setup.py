import os

from setuptools import setup, find_packages

README = 'Read Readme.md'
CHANGES = 'Initial'

# using requirements.txt
requires = [
    ]

# testing with behavior and pytest
tests_require = [
    ]

setup(name='aaa_manager',
      version='0.0',
      description='aaa_manager',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = aaa_manager:main
      """,
      )
