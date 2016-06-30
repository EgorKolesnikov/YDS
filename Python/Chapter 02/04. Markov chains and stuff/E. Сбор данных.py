# -*- encoding: utf-8 -*-
from urllib2 import urlopen
import bs4


def get_urls_with_books(site, url):
    urls_with_books = []
    soup = bs4.BeautifulSoup(urlopen(site + url).read(), 'lxml')
    for book in soup.findAll('td', attrs={'class': 'books-list-cell'}):
        link = book.find('a')
        urls_with_books.append((site + link['href']).encode('utf8'))
    return urls_with_books[2::2]


def get_text_from_page(page):
    soup = bs4.BeautifulSoup(page, 'lxml')
    text = ''
    for p in soup.findAll('p'):
        text += ''.join(map(unicode, p.findAll(text=True))) + '\n'
    return text


def collect_books(site, start_url, max_books=5):
    book_number = 0
    urls = get_urls_with_books(site, start_url)
    for url in urls[0:max_books]:
        book_number += 1
        print 'Book proceeding: ', book_number, 'of', max_books
        conn = urlopen(url)
        book = get_text_from_page(conn.read())
        with open('book' + str(book_number) + '.txt', 'w') as file:
            file.write(book.encode('utf8'))
    return book_number


def save_in_one_file(books_found):
    with open('all_books.txt', 'w') as out_file:
        for number in xrange(1, books_found):
            with open('book' + str(number) + '.txt', 'r') as file:
                out_file.write(file.read() + '\n')


def main():
    site = u'http://ubooki.ru'.encode('utf8')
    start_url = u'/художественная-литература/боевики/'.encode('utf8')
    books_found = collect_books(site, start_url, max_books=20)
    save_in_one_file(books_found)

if __name__ == '__main__':
    # main()
    pass
