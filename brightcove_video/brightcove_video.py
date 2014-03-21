# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import re
import requests
import urlparse

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from .utils import load_resource, render_template


# Globals ###########################################################

log = logging.getLogger(__name__)


# Classes ###########################################################

class BrightcoveVideoBlock(XBlock):
    """
    XBlock providing a video player for videos hosted on Brightcove
    """
    href = String(help="The URL of the video to display", default='http://bcove.me/4kgaw9rb',
                  scope=Scope.content)
    title = String(help="Title", default='Default video', scope=Scope.content)
    api_key = String(help="Key to access the Brightcove API",
                     default='JqnRdhYvLWNtVJllXkMzGGGTh66uLLmz8JB8YlcZQlC8OX94H4ZXXw..',
                     scope=Scope.content)
    api_bcpid = String(help="Brightcove API - PlayerID", default='3222036674001', scope=Scope.content)
    api_bckey = String(help="Brightcove API - PlayerKey", default='AQ~~,AAAC7X9CySE~,W5r6gx4kdiU9bUyJM5snIevMWD2gUysk', scope=Scope.content)
    api_bctid = String(help="Brightcove API - @videoPlayer", default='3271663601001', scope=Scope.content)

    def student_view(self, context):
        """
        Player view, displayed to the student
        """
        fragment = Fragment()
        fragment.add_content(render_template('templates/html/brightcove_video.html', {
            'self': self,
        }))
        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/brightcove_video.css'))
        fragment.add_javascript_url(
                self.runtime.local_resource_url(self, 'public/js/vendor/brightcove_experiences.js'))
        fragment.add_javascript_url(
                self.runtime.local_resource_url(self, 'public/js/brightcove_video.js'))

        fragment.initialize_js('BrightcoveVideoBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(render_template('templates/html/brightcove_video_edit.html', {
            'self': self,
        }))
        fragment.add_javascript(load_resource('public/js/brightcove_video_edit.js'))

        fragment.initialize_js('BrightcoveVideoEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        log.info(u'Received submissions: {}'.format(submissions))

        self.api_key = submissions['api_key']

        if submissions.get('href', self.href) != self.href: # URL changed
            self.href = submissions['href']

            # Update the video details
            self.set_api_params_from_href()

        return {
            'result': 'success',
        }

    def set_api_params_from_href(self):
        """
        Retreives parameters identifying a Brightcove video when dealing with
        the API, based on its short URL. The short URL is a convenience for the 
        user, which can use a short URL to add a video to Studio after uploading in
        Brightcove.
        """
        bc_response = requests.get(self.href)
        bc_url = bc_response.url
        log.info('Brightcove URL received from API: {}'.format(bc_url))
        bc_url_parts = urlparse.urlparse(bc_url)

        bc_url_splitpath = re.split('bcpid', bc_url_parts.path)
        self.api_bcpid = str(bc_url_splitpath[1])

        bc_url_querystring = urlparse.parse_qs(bc_url_parts.query)
        self.api_bckey = str(bc_url_querystring['bckey'][0])
        self.api_bctid = str(bc_url_querystring['bctid'][0])

        bc_url = 'https://api.brightcove.com/services/library'
        payload = {'command':'find_video_by_id',
                   'token': self.api_key,
                   'video_id': str(self.api_bctid),
                   'video_fields': 'name,shortDescription'}
        bc_response = requests.get(bc_url, params=payload)
        if not bc_response:
            log.warn('Could not get reply from Brightcove API for this video URL')
            return

        bc_json = bc_response.json()
        self.title = bc_json['name']
