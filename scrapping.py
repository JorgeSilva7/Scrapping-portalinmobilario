import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import json

LAST_POSTS_NAME = "last_posts"
CRITERIA_POSTS_NAME = "criteria_posts"

BATHS = 1
DORMS = 1
LOCATION = "providencia-metropolitana"


def get_soup(url):
    """ Get SOUP (html) instance from url"""
    page = requests.get(url)

    return BeautifulSoup(page.content, 'html.parser')


def get_appartments():
    """ Main function for get 50 (last_posts.json) posts and the first 15 ordered by criteria (criteria_posts.json)"""

    criteria = define_criteria()

    print("Loading ...")

    # Get SOUP for scrapping
    soup = get_soup(
        "https://www.portalinmobiliario.com/arriendo/departamento/{dorms}-dormitorio/{location}/_Banos_{baths}".format(dorms=DORMS, location=LOCATION, baths=BATHS))

    # Set posts_array with post info
    posts_array = get_posts(soup)
    write_in_json(posts_array, LAST_POSTS_NAME)

    # Set m2 value per post
    set_m2_value(posts_array)

    # Order posts array for criteria (cheeper to expensive)
    criteria_posts_array = order_by_key(posts_array, criteria)
    write_in_json(criteria_posts_array, CRITERIA_POSTS_NAME)


def get_posts(soup):
    """ Get posts in html and return posts with info"""

    posts = soup.find_all(class_='ui-search-layout__item')

    posts_array = []
    for post in posts:
        post_info = get_post_info(post)
        post_info and posts_array.append(post_info)

    return posts_array


def get_post_info(post):
    """ Get post info (price, address, information, square_meters, link)"""

    price_simbol = post.find(class_='price-tag-symbol').text
    if not 'UF' in price_simbol:
        price_txt = post.find(
            class_='price-tag-fraction').text.replace(".", "")
        price = extract_numbers(price_txt)
        address = post.find(
            class_="ui-search-item__group__element ui-search-item__location").text
        information = post.find_all(
            class_="ui-search-item__group__element ui-search-item__information")[1].text
        square_meters = post.find(
            class_="ui-search-card-attributes__attribute").text
        square_meters = extract_numbers(
            square_meters) if "m²" in square_meters else None
        link = post.find(class_="ui-search-link", href=True)["href"]
        return {"price": price, "address": address, "information": information, "square_meters": square_meters, "link": link}


def set_m2_value(posts):
    """ Set square meters value per post"""
    for post in posts:
        post["square_meteres_value"] = (
            post["price"] / post["square_meters"]) if post["square_meters"] else None


def extract_numbers(txt):
    """ Extract numbers from string. Split into a list where each word in text, then check if the splited string is a digit and return first value in array """
    numbers = [int(s) for s in txt.split() if s.isdigit()]
    return numbers[0]


def order_by_key(posts, key_name):
    """ Order list of posts by key (min to max). Only posts with the key_name value different from null"""
    posts_with_criteria = [
        post for post in posts if post[key_name]]
    return sorted(posts_with_criteria, key=itemgetter(key_name))


def define_criteria():
    criteria = input(
        "Please enter the criteria (square_meters_value, square_meters or price):\n")
    if criteria == 'square_meters_value':
        return "square_meteres_value"
    elif criteria == 'price':
        return "price"
    elif criteria == 'square_meters':
        return "square_meters"
    else:
        print("The criterias must be a square_meters_value, square_meters or price")
        return define_criteria()


def write_in_json(data, json_name):
    try:
        with open(json_name+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        print(json_name+".json file has been created")
    except Exception as e:
        print("An error has ocurred: "+str(e))


# Call main function
get_appartments()
