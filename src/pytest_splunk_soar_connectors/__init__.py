# -*- coding: utf-8 -*-
import sys
from . import models
from .plugin import *

import phantom
import phantom.app
import phantom.vault
import phantom.action_result
from phantom import base_connector

sys.modules['phantom'] = phantom
sys.modules['phantom.app'] = phantom.app
sys.modules['phantom.vault'] = phantom.vault
sys.modules['phantom.action_result'] = phantom.action_result
sys.modules['phantom.base_connector'] = base_connector
