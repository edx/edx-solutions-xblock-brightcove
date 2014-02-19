# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging

from xblock.core import XBlock
from xblock.fields import BlockScope, Scope, String, UserScope
from xblock.fragment import Fragment

from .utils import load_resource, render_template


# Globals ###########################################################

log = logging.getLogger(__name__)


# Classes ###########################################################

class BrightcoveVideoBlock(XBlock):
    """
    XBlock providing a video player for videos hosted on Brightcove
    """
    href = String(help="The URL of the video to display", default='http://bcove.me/10w7plii',
                  scope=Scope.content)
    api_key = String(help="Key to access the Brightcove API", default='',
                     scope=Scope(UserScope.NONE, BlockScope.DEFINITION))

    def student_view(self, context):
        """
        Player view, displayed to the student
        """
        fragment = Fragment()
        fragment.add_content(render_template('templates/html/brightcove_video.html', {
            'self': self,
        }))
        fragment.add_css(load_resource('static/css/brightcove_video.css'))
        fragment.add_javascript(load_resource('static/js/brightcove_video.js'))

        fragment.initialize_js('BrightcoveVideoBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        return fragment
