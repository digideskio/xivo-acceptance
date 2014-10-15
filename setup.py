#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import fnmatch
import os

from distutils.core import setup


def is_package(path):
    is_svn_dir = fnmatch.fnmatch(path, '*/.svn*')
    is_test_module = fnmatch.fnmatch(path, '*tests')
    return not (is_svn_dir or is_test_module)


def packages_in(package):
    return [p for p, _, _ in os.walk(package) if is_package(p)]


def files_in(directory):
    for dir, _, files in os.walk(directory):
        for file in files:
            yield '{dir}/{file}'.format(dir=dir, file=file)


packages = (packages_in('xivo_acceptance'))
confd = list(files_in('etc/xivo-acceptance/conf.d'))

setup(
    name='xivo-acceptance',
    version='0.1',
    description='XiVO Acceptance',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/xivo-pbx/xivo-acceptance',
    license='GPLv3',
    packages=packages,
    scripts=[
        'bin/xivo-acceptance',
    ],
    data_files=[
        ('/etc/xivo-acceptance', ['etc/xivo-acceptance/default.ini']),
        ('/etc/xivo-acceptance/conf.d', confd)
    ],
)
