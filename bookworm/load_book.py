import requests


def from_path(book_path):
    with open(book_path) as f:
        book = f.read()
    return book


def from_url(url):
    return requests.get(url).text
