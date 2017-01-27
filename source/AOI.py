from carmera import Carmera
# -*- coding: utf-8 -*-
__author__ = 'Rainer Arencibia'

"""
MIT License

Copyright (c) 2016 Rainer Arencibia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

""" Area of Interest Polygon Format...
    [[
        [{lon}, {lat}], # top-left
        [{lon}, {lat}], # top-right
        [{lon}, {lat}], # bottom-right
        [{lon}, {lat}]  # botton-left
    ]]
    Compressed as a URL parameter:
    ?aoi=[[[{lon},{lat}],[{lon},{lat}],[{lon},{lat}],[{lon},{lat}]]]
"""



class AOI(object):
    """
    Class useful for search for Image(s) in an Area of Interest.
    Area of Interest queries default sort by Captured On Ascending.
    """
    def __init__(self, key):
        cm = Carmera(api_key=str(key))
        self.aoi = cm.Aoi()       # AOI Service
        self.aoi_id_set = set()

    @staticmethod
    def size_all_aois(self):
        return len(self.aoi_id_set)

    @staticmethod
    def get_last_update(self, aoi):
        """
        :param self:
        :param aoi:
        :return: Updated AOI timestamp.
        """
        return aoi['updated_at']

    @staticmethod
    def get_name(self, aoi):
        """
        :param self:
        :param aoi: array AOI
        :return: Return the name of a given AOI. String
        """
        return aoi['properties']['name']

    @staticmethod
    def get_id(self, aoi):
        """
        :param self:
        :param aoi: array AOI
        :return: Return the ID of a given AOI. Integer
        """
        return aoi['properties']['id']

    @staticmethod
    def size_of_aoi(self, aoi):
        """
        :param self:
        :return: Return the number of images for a given AOI.
        """
        return len(aoi['features'])

    @staticmethod
    def get_aoi_by_id(self, aoi_id, sort='captured_on', order='ASC', filt=None, tags=None, range=None, offset=0, limit=5000):
        """
        Get an Area of Interest.
        :param self: Image object.
        :param aoi_id: AOI object. [[[lon,lat],[lon,lat],[lon,lat],[lon,lat]]]
        :param sort: You can sort by almost any response property.
        :param order: Sort the images in order 'asc' or 'desc'
        :param tags: Look for image with a specific tag
        :param filt: Special setting for look for better quality pictures, like speed=0, position, etc.
        :param range: Range of dates to look  for pictures
        :param offset: Integer that indicate tha max number of pages.
        :param limit: Integer that indicate the results page size.
        :return: Retrieve an AOI you created.
        """
        try:
            optional_params = {
                'sort': sort,       # 'captured_on',
                'order': order,     # 'ASC' or 'DESC'
                'filter': filt,     # filter=speed>=20,
                'range': range,     # '2016-07-01,2016-07-15',
                'tags': tags,       # tags=safety.score>=8,
                'offset': offset,   # {} The pagination offset.
                'limit': limit,     # 1 - 5000
            }
            feature_collection = self.aoi.get_by_id(aoi_id, optional_params).json()
            self.aoi_id_set.add(AOI.id_aoi(feature_collection))
            return feature_collection
        except Exception as e:
            print(e.code)
            print(e.error)
        return None

    @staticmethod
    def search(self, aoi=None, sort='captured_on', order='ASC', filt=None, range=None, tags=None, offset=0, limit=1000):
        """
        Search for Image(s) in an Area of Interest.
        :param self: Image object.
        :param aoi: AOI object. [[[lon,lat],[lon,lat],[lon,lat],[lon,lat]]]
        :param sort: You can sort by almost any response property.
        :param order: Sort the images in order 'asc' or 'desc'
        :param tags: Look for image with a specific tag
        :param filt: Special setting for look for better quality pictures, like speed=0, position, etc.
        :param range: Range of dates to look  for pictures
        :param offset: Integer that indicate tha max number of pages.
        :param limit: Integer that indicate the results page size.
        :return: Retrieve an AOI you created.
        """
        try:
            options = {
                'aoi': aoi,         # [[ [-73.967585111145, 40.713012592205], [-73.95994617987, 40.710540324112],
                                    #    [-73.956856275085, 40.715549824536], [-73.965010190491, 40.718347173747] ]],
                'sort': sort,       # 'captured_on',
                'order': order,     # 'ASC' or 'DESC'
                'filter': filt,     # filter=position=1|4,speed>=20,
                'range': range,     # '2016-07-01,2016-07-15',
                'tags': tags,       # tags=safety.score>=8,
                'offset': offset,   # {} The pagination offset.0 Default value
                'limit': limit,     # 1 - 1000
            }
            feature_collection = self.aoi.search(options).json()
            self.aoi_id_set.add(feature_collection['id'])
            img_id_set = set()
            for image in feature_collection['features']:
                img_id_set.add(image['properties']['image_id'])
            return img_id_set
        except Exception as e:
            print(e.code)
            print(e.error)
        return None

    @staticmethod
    def create_aoi(self, aoi, name):
        """
        Create an Area of Interest. Define a GeoJSON Polygon and save the AOI for repeated access.
        :param self: AOI object
        :param aoi: AOI array
        :param name: name of the AOI
        :return: Return the AOI create it and add to the set of AOIs
        """
        try:
            res = self.aoi.create(aoi, name).json()
            self.aoi_id_set.append(res['id'])
            return res['id']
        except Exception as e:
            print(e.code)
            print(e.error)
        return None

    @staticmethod
    def update_aoi(self, aoi_id, aoi, name):
        """
        Update an Area of Interest
        :param self:
        :param aoi_id:
        :param aoi:
        :param name:
        :return:
        """
        try:
            res = aoi.update(aoi_id, aoi, name).json()
            self.aoi_id_set.discard(aoi_id)
            self.aoi_id_set.append(res['id'])
            return self.aoi_id_set
        except Exception as e:
            print(e.code)
            print(e.error)
        return None
