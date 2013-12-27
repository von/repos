repos
=====

https://github.com/von/repos

A script for tracking and managing git repositories.

Installation
------------

    git clone https://github.com/von/repos.git
    cd repos
    ./setup.py install

Usage
-----

Add a repository to the list of tracked repositories:

    repos add .

To search for repos, use `repo find`. Add `-a` to automatically add them.

    repos find -a ~

The list of managed repos is stored in `~/.repos`

To check all your repos for needed pushes, pulls or commits:

    repos check

To go to the next repo that needs a push, pull or commit:

    eval `repos next`

