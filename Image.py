from carmera import Carmera
# -*- coding: utf-8 -*-
__author__ = 'Rainer Arencibia'


class Image(object):
    """
    On this class we implements the Object Image from Carmera to call the API methods + adding the error message, and
    others objects useful for a better and safety use of the API.
    # We add some methods for basic pre-processing images.
    Image queries default sort by distance Ascending.
    """

    def __init__(self, key):
        cm = Carmera(api_key=str(key))
        self.img = cm.Image()       # Image Service
        self.img_id_set = set()     # A set for IDs, to avoid duplicate images in any search. Efficient in space & time.

    @staticmethod
    def speed_of_image(img):
        """
        :param img: An image
        :return: speed in meters/sec when image was taken
        """
        return img['properties']['speed']

    @staticmethod
    def url_of_image(img):
        """
        :param img: An image
        :return: URL of the image
        """
        return img['properties']['url']

    @staticmethod
    def size(self):
        """
        Return how many images are in the search.
        :param self: Image object
        :return: Integer
        """
        return len(self.img_id_set)

    @staticmethod
    def get_image(self, id=None):
        """
        :param self: Image object
        :param id: ID of the picture to get.
        :return: An image in Json format.
        """
        try:
            res = self.img.get_by_id(id)
            image = res.json()
            return image
        except Exception as e:
            print(e.code)   # 404
            print(e.error)  # "Not found"
        return None

    @staticmethod
    def search_images_address(self, address=None, radius=None, sort='distance', order='ASC', tags=None, filt=None,
                              range=None, offset=0, limit=5000):
        """
        Method to search using address info + some special settings.
        :param self: Image object.
        :param address: Place to look for some pictures
        :param radius: Distance in meter to look for pictures.
        :param sort: You can sort by almost any response property.
        :param order: Sort the images in order 'asc' or 'desc'
        :param tags: Look for image with a specific tag
        :param filt: Special setting for look for better quality pictures, like speed=0, position, etc.
        :param range: Range of dates to look  for pictures
        :param offset: Integer that indicate tha max number of pages.
        :param limit: Integer that indicate the results page size.
        :return: A set of the pictures ID.
        """
        try:
            options = {
                'address': address,   # '20 Jay St, Brooklyn, NY 11211',
                'radius': radius,     # 300,
                'sort': sort,         # 'radius': radius,
                'filter': filt,       # 'position=1|4,speed>=20',
                'range': range,       # '2017-01-17 00:00:00, 2017-01-17 23:59:59',
                'order': order,       # 'ASC' or 'DESC',
                'tags': tags,         # tags=car.make=bmw,
                'offset': offset,     # {} The pagination offset.
                'limit': limit        # 1 - 5000
            }
            feature_collection = self.img.search(options).json()
            for image in feature_collection['features']:
                self.img_id_set.add(image['properties']['image_id'])
            return self.img_id_set
        except Exception as e:
            print(e.code)
            print(e.error)
        return None

    @staticmethod
    def search_images_coordinates(self, points=None, radius=None, sort='distance', order='ASC', tags=None, filt=None,
                              range=None, offset=0, limit=5000):
        """
        Method to search using address info + some special settings.
        :param self: Image object.
        :param points: points: Polygon area type [[[lon,lat],[lon,lat],[lon,lat],[lon,lat]]].
        :param radius: Distance in meter to look for pictures.
        :param sort: You can sort by almost any response property.
        :param order: Sort the images in order 'asc' or 'desc'
        :param tags: Look for image with a specific tag
        :param filt: Special setting for look for better quality pictures, like speed=0, position, etc.
        :param range: Range of dates to look  for pictures.
        :param offset: Integer that indicate tha max number of pages.
        :param limit: Integer that indicate the results page size.
        :return: A set of the pictures ID.
        """
        try:
            options = {
                'points': points,     # [-74.000173, 40.732752], [long, lat]
                'radius': radius,     # 300,
                'filter': filt,       # 'position=1|4,speed>=20',
                'range': range,       # '2016-07-01,2016-07-15',
                'sort': sort,         # 'distance&order=ASC',
                'order': order,       # 'ASC' or 'DESC'
                'tags': tags,         # tags=safety.score>=8,
                'offset': offset,     # {} The pagination offset.0 Default value
                'limit': limit        # 1 - 5000
            }
            feature_collection = self.img.search(options).json()
            for image in feature_collection['features']:
                self.img_id_set.add(image['properties']['image_id'])
            return self.img_id_set
        except Exception as e:
            print(e.code)
            print(e.error)

        return None

    @staticmethod
    def download_images(self, url_save):
        """
        This method save all the images that are already search.
        :param self: Image Object.
        :param url_save: Location to save all the images searched
        :return: set of images saved, -1 when there is nothing to save.
        """
        if len(self.img_id_set) == 0:
            print("There is nothing to save. Search for some images first.")
            return None
        else:
            try:
                for id in self.img_id_set:
                    # img = Image.get_image_id(image['properties']['image_id'])
                    self.img.download(id, url_save)
                return self.img_id_set
            except Exception as e:
                print(e.code)
                print(e.error)
        return None

    @staticmethod
    def download_images_address(self, address, radius, url_save):
        """
        This method save all the images that are already search.
        :param self: Image Object.
        :param address: Search first for images in that address.
        :param radius: Distance in meters.
        :param url_save: Location to save all the images searched
        :return: set of images saved, -1 when there is nothing to save.
        """
        Image.search_images_address(self, address, radius=radius)
        if len(self.img_id_set) == 0:
            print("There is nothing to save. Search for some images first.")
            return -1
        else:
            try:
                for image in self.img_id_set:
                    # img = Image.get_image_id(image['properties']['image_id'])
                    self.img.download(id['properties']['image_id'], url_save)
                return self.img_id_set
            except Exception as e:
                print(e.code)
                print(e.error)
        return None

    @staticmethod
    def download_images_coordinates(self, points, radius, url_save):
        """
        This method save all the images that are already search.
        :param self: Image Object.
        :param points: Polygon area type [[[lon,lat],[lon,lat],[lon,lat],[lon,lat]]].
        :param radius: Distance in meters.
        :param url_save: Location to save all the images searched
        :return: set of images saved, -1 when there is nothing to save.
        """
        Image.search_images_address(self, points, radius=radius)
        if len(self.img_id_set) == 0:
            print("There is nothing to save. Search for some images first.")
            return -1
        else:
            try:
                for id in self.img_id_set:
                    # img = Image.get_image_id(id['properties']['image_id'])
                    self.img.download(id['properties']['image_id'], url_save)
                return self.img_id_set
            except Exception as e:
                print(e.code)
                print(e.error)
        return None


if __name__ == '__main__':

    AOI = [[[-73.987084387429, 40.7330731785852], [-73.9806062564698, 40.7303859498055],
            [-73.9862746210592, 40.7225563969032], [-73.9922222154312, 40.7243339978445]]]
    AOI_NAME = "East Village"
    DISK = '/home/rainer85ah/Desktop/Carmera/data/'

    image = Image('00bc11acbd9c2690eb453a51b335bbcdd8652ba9')
    print('Test: ', image.__repr__())

    id_set = image.search_images_coordinates(image, points=AOI, radius=1000)
    print('Test: ', id_set.__repr__())

    lista = list(id_set)
    for id in lista:
        print(id)

    res = image.download_images(DISK)
    if res == -1:
        print("Download Failed")


