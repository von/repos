#!/usr/bin/env python
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="repos",
    version="0.1",
    packages=["repos"],
    # http://pythonhosted.org/setuptools/setuptools.html#automatic-script-creation  # noqa
    entry_points={
        'console_scripts': [
            'repos = repos.script:main',
        ],
    },
    install_requires=[
        "GitPython",
    ],

    author="Von Welch",
    author_email="von@vwelch.com",
    description="Manage my git repositories",
    license="Apache2",
)
