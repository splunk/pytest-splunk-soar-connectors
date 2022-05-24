# -*- coding: utf-8 -*-
import sys
import pytest

import phantom_mock.phantom
import phantom_mock.phantom.app
import phantom_mock.phantom.vault
import phantom_mock.phantom.action_result
import phantom_mock.phantom.base_connector

sys.modules['phantom'] = phantom_mock.phantom
sys.modules['phantom.app'] = phantom_mock.phantom.app
sys.modules['phantom.vault'] = phantom_mock.phantom.vault
sys.modules['phantom.action_result'] = phantom_mock.phantom.action_result
sys.modules['phantom.base_connector'] = phantom_mock.phantom.base_connector