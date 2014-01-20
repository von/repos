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
        'repos': [
            'add = repos.AddCommand:AddCommand',
            'check = repos.CheckCommand:CheckCommand',
            'find = repos.FindCommand:FindCommand',
            'next = repos.NextCommand:NextCommand',
        ],
    },
    install_requires=[
        "GitPython>0.3.1",  # Tried with 0.3.2 RC1
        "cliff>1.5.0",  # Used 1.5.2
    ],

    author="Von Welch",
    author_email="von@vwelch.com",
    description="Manage my git repositories",
    license="Apache2",
)
