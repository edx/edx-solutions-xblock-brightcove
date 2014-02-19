# -*- coding: utf-8 -*-

# Imports ###########################################################

import os
from setuptools import setup


# Functions #########################################################

def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


# Main ##############################################################

setup(
    name='xblock-brightcove',
    version='0.1',
    description='XBlock - Brightcove Video Player',
    packages=['brightcove_video'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': 'brightcove-video = brightcove_video.BrightcoveVideoBlock',
    },
    package_data=package_data("brightcove_video", "static"),
)
