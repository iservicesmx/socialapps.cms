from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='socialapps.cms',
      version=version,
      description="A Content Management System for SocialApps",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='socialapps cms blufrog',
      author='Erik Rivera',
      author_email='erik@rivera.pro',
      url='http://rivera.pro',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['socialapps'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'django-mptt',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
