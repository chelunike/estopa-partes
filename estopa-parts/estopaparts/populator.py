from ast import arg
import os, datetime, django
import re
import random

from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

import base64
from django.contrib.auth.hashers import make_password

# Import your settings here
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estopaparts.settings')
django.setup() 

import faker, random
from faker.providers import internet, misc, person, address, date_time

# Import your models here
from website.models import *

jake = faker.Faker()

# Add Providers
jake.add_provider(internet)
jake.add_provider(misc)
jake.add_provider(person)
jake.add_provider(address)
jake.add_provider(date_time)

# Num of objects
num_buyers = 10
num_sellers = 10
num_admins = 6
num_products = 10

# Some Random data
DEFAULT_PASSWD = '1234'
PRODUCT_PATH = 'media/products/'

# ------------------------------------- NO TOCAR ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# Core functions
def populator_register(obj, callback, num=5, *args, **kwargs):
    count_objs = obj.objects.all().count()
    if count_objs >= num:
        print("Enough {1} in database ({0})".format(count_objs, obj.__name__))
    else:
        total = num - count_objs
        print("Not enough {0} in database generating ({1}/{2})".format(obj.__name__, total, num))
        #print('Not enough '+obj.__name__+' in database generating (' + total + '/' + num + ')')
        for i in range(total):
            callback(*args, **kwargs)

def model_choice(model):
    query = model.objects.all()
    return random.choice(query)

# Image Class
class Unsplash(object):
    """Unsplash Class"""
    BASE_URL = 'https://api.unsplash.com/'

    def __init__(self, args):
        super(Unsplash, self).__init__()
        self.args = args
        self.buffer = None
        self.buffer_clean = False

    def set(self, name, value, overwrite=True):
        if name in self.args.keys():
            if overwrite:
                self.args[name] = value
        else:
            self.args[name] = value
        return (name in self.args.keys() and overwrite)

    def get(self, name):
        if name in self.args.keys():
            return self.args[name]
        return None

    def search_photos(self, query):
        self.args['query'] = query
        self.args['per_page'] = 50
        self.request_photos(self.BASE_URL + 'search/photos')
        return self.list

    def random_photo(self):
        if not self.buffer_clean and self.list is None:
            self.request_photos(self.BASE_URL + 'search/photos')
        if self.buffer_clean and self.list is not None:
            return random.choice(self.list['results'])

    def request_photos(self, url):
        result = None
        try:
            response = requests.get(url, params=self.args)
            if response.status_code == requests.codes.ok:
                data = response.json()
                if 'results' in data.keys():
                    self.buffer = data
                    self.list = data['results']
                    self.buffer_clean = True
                    result = self.buffer
            else:
                print(response)
        except Exception as e:
            print('Error loading request: ', e)
        return result


class UrlImage(object):
    """UrlImage Class"""

    def __init__(self, url):
        super(UrlImage, self).__init__()
        self.url = url
        self.data = None

    def get_data(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',    
            }
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                self.data = base64.b64encode(response.content)
                print('Image fetched !!')
            else:
                print('Error loading image: ', response)
        except Exception as e:
            print(' Error while retreive image: ', e)
        return self.data

    def save_file(self, path):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(self.data))
            file.close()


def example_unsplash():
    print('Hola')
    args = {
    #    'client_id': ACCESS_KEY,
        'query': 'hairdresser',
    }
    splash = Unsplash(args)

    splash.search_photos('hairdresser')
    path = "photos/photo{0}.jpg"
    for i in range(30):
        photo = splash.random_photo()
        print(photo['urls']['raw'])
        image = UrlImage(photo['urls']['raw'])
        image.get_data()
        image.save_file(path.format(i))


class Product(object):

    def __init__(self) -> None:
        super().__init__()
        self.id = ''
        self.name = ''
        self.description = ''
        self.brand = ''
        self.category = ''
        self.price = 0
        self.discount = 0
        self.image = None
        self.image_path = ''
        self.rating = 0

    def __str__(self):
        return self.name + ' ' + self.brand + ' ' + str(self.price)+ ' ' \
            + str(self.discount) + ' ' + str(self.rating) + ' ' + self.image

class PCComponentes(object):
    SECTIONS_URLS = [
        "https://www.pccomponentes.com/placas-base",
        "https://www.pccomponentes.com/procesadores",
        "https://www.pccomponentes.com/discos-duros",
        "https://www.pccomponentes.com/discos-duros-ssd",
        "https://www.pccomponentes.com/tarjetas-graficas",
        "https://www.pccomponentes.com/memorias-ram",
        "https://www.pccomponentes.com/grabadoras-dvd-blu-ray",
        "https://www.pccomponentes.com/multilectores",
        "https://www.pccomponentes.com/tarjetas-sonido",
        "https://www.pccomponentes.com/torres",
        "https://www.pccomponentes.com/ventiladores",
        "https://www.pccomponentes.com/fuentes-alimentacion", 
        "https://www.pccomponentes.com/modding",
        "https://www.pccomponentes.com/capturadoras",
        "https://www.pccomponentes.com/cables-internos-de-pc",
        "https://www.pccomponentes.com/conectividad",
    ]

    def __init__(self) -> None:
        super().__init__()
        self.products = []
    
    def get_page(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',    
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print('Error loading request: ', e)
        return None
    
    def generate_products(self, page):
        products = page.find_all('article', {'class': 'c-product-card'})
        for p in products:
            p_data = Product()
            if 'data-id' in p.attrs.keys():
                p_data.id = p['data-id']
            if 'data-name' in p.attrs.keys():
                p_data.name = p['data-name']
            if 'data-brand' in p.attrs.keys():
                p_data.brand = p['data-brand']
            if 'data-category' in p.attrs.keys():
                p_data.category = p['data-category']

            actual_price = 0
            if 'data-price' in p.attrs.keys():
                actual_price = float(p['data-price'])
            
            image = p.findChild('img')
            if image and 'src' in image.attrs.keys():
                p_data.image = image['src']
                p_data.image = p_data.image.replace('//', 'https://').replace('w-220-220', 'w-530-530')
            
            div = p.findChild('div', {'class': 'c-product-card__prices-pvp'})
            price = actual_price
            if div != None:
                price_text = div.findChild('span')
                if price_text != None:
                    price_text = price_text.text
                    price_text = price_text.replace('€', '').replace(',', '.')
                    price = float(price_text)
                    p_data.discount = ((price - actual_price) / price)*100
            else:
                p_data.discount = 0
            p_data.price = price
            #import ipdb; ipdb.set_trace()
            self.products.append(p_data)

    def save_image(self, url, path):
        image = UrlImage(url)
        image.get_data()
        if not os.path.exists(path):
            os.mkdir(path)
        a = urlparse(url)
        final_path = os.path.join(path, os.path.basename(a.path))
        image.save_file(final_path)
        return final_path

    def get_products(self):
        for url in self.SECTIONS_URLS:
            page = self.get_page(url)
            self.generate_products(page)
        return self.products

    def get_section(self, i):
        return self.SECTIONS_URLS[i]
    
    def get_random_section(self):
        return random.choice(self.SECTIONS_URLS)


# ------------------------------------- NO TOCAR ------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

# Generate images
pcc = PCComponentes()
pcc.generate_products(pcc.get_page('https://www.pccomponentes.com/placas-base'))

# Generations Functions
def generate_user(tipo = 2):
    try:
        user = {
            'tipo': tipo,
            'nif': '12345678Z',
            'nombre': jake.first_name(),
            'apellidos': jake.last_name(),
            'correo': jake.email(),
            'clave': make_password(DEFAULT_PASSWD),
        }

        Usuario.objects.create(**user)
        return True
    except Exception as e:
        return False


def generate_product():
    try:
        p = pcc.products.pop()
        image_path = pcc.save_image(p.image, PRODUCT_PATH)
        product = {
            'nombre': p.name,
            'descripcion': p.id + ' ' + p.name + ' ' + p.category + ' ' + p.brand,
            'precio': p.price,
            'oferta': p.discount,
            'cantidad': random.randint(1, 100),
            'imagen': image_path.replace('media/', ''),
            'marca': p.brand,
            'vendedor_id': 8,
        }
        
        Producto.objects.create(**product)
        return True
    except Exception as e:
        print('Error generating product: ', e)
        return False


# Register the models to populate
populator_register(Usuario, generate_user, num_admins, 0)
populator_register(Usuario, generate_user, num_sellers, 1)
populator_register(Usuario, generate_user, num_buyers, 2)
populator_register(Producto, generate_product, num_products)




