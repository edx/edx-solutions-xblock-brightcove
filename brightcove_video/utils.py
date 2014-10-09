# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import pkg_resources

from django.template import Context, Template

from xblockutils.resources import ResourceLoader


log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)
