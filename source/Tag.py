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

""" Tag Properties Formatting...
    {
        "tag"        : "car",
        "image_id"   : 1,
        "confidence" : 0.9,
        "roi"        : {
                            "x" : 100,
                            "y" : 200,
                            "w" : 150,
                            "h" : 400
                        },
        "properties" : {
                            "make"  : "jeep",
                            "model" : "wrangler"
                        }
    }
"""


class Tag(object):
    """
    Tags are features detected within an Image, or whole Image descriptions. Both can be associated to properties.
    On this class we implements the Object Tag from source to call the API methods + adding the error message, and
    others objects useful for a better and safety use of the API.
    """
    def __init__(self, key):

        cm = Carmera(api_key=str(key))
        self.tag = cm.Tag()
        self.tag_id_set = set()     # A set for IDs, to avoid duplicate images in any search. Efficient in space & time.

    @staticmethod
    def size(self):
        return len(self.tag_id_set)
