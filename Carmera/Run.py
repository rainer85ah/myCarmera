from carmera import Carmera
import requests
from Carmera.Image import Image

# -*- coding: utf-8 -*-
__author__ = 'Rainer Arencibia'

"""Parameter or settings from the app"""
DISK = '/home/rainer85ah/Desktop/Carmera/data/'
AOI = [[[-73.987084387429, 40.7330731785852], [-73.9806062564698, 40.7303859498055],
        [-73.9862746210592, 40.7225563969032], [-73.9922222154312, 40.7243339978445]]]
AOI_NAME = "East Village"
URL = 'https://api.carmera.com/v1/'
headers = {'Authorization': 'api-key {00bc11acbd9c2690eb453a51b335bbcdd8652ba9}'}
FORMAT = 'Content-Type: application/vnd.geo+json'
AUTH = {'api-key': '00bc11acbd9c2690eb453a51b335bbcdd8652ba9'}
"""
Download Images. Sizes 5: tiny 360 x 272, small 640 x 480, medium 960 x 720, large 1280 x 960,
        Native:
        Forward Facing Cameras 1280 x 960,
        Side Facing Cameras    3264 x 2448.

GET https://api.carmera.com/v1/images/{image_id}/download/?apikey={your-api-key}&size=small
"""
image_object = Image('00bc11acbd9c2690eb453a51b335bbcdd8652ba9')
image_object.download_images_coordinates(points=AOI, radius=1000, url_save=DISK)

url = 'https://api.carmera.com/v1/images/{image_id}/download/?apikey={your-api-key}&size=small'
try:
        connection = requests.get(URL, headers=headers)
        print('Test:', connection.status_code)
        print('Test:', connection.content)
        print('Test:', connection.url)
        print('Test:', connection.status_code)
except Exception as e:
        print(e.__str__())