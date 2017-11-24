#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Считаем, что архив распакован в папку books, она находится в той же папке, что и все остальные файлы.
#Заливать 300ГБ на гит -- очень не хочется.

from bottle import request, run, route, template
import os

import requests
import bs4
import random
import os

SERVER = "./server/"
BOOKS = SERVER + "books/"

def getAuthorsList():
	list_authors = os.listdir(BOOKS)
	if ".DS_Store" in list_authors:
		list_authors.remove(".DS_Store")
	return list_authors

def getBooksByAuthor(author):
	list_books = os.listdir(BOOKS + author + '/')	
	return list_books

@route('/')
def main():
	list_authors = getAuthorsList()
	books = {}
	for author in list_authors:
		books[author] = getBooksByAuthor(author)
	page = template(SERVER + 'list_of_authors', authors=list_authors, books=books)
	return page

@route('/author/<name>/')
def getAuthorpage(name):
	list_books = getBooksByAuthor(name)
	page = template(SERVER + 'list_of_books', list_books=list_books, author=name)
	return page

@route('/author/<authorName>/book/<bookName>/')
def getBookText(authorName, bookName):
	f = open(BOOKS + authorName + '/' + bookName, 'r')
	book_text = f.read()
	page = template(SERVER + 'book_text', text=book_text)
	return page

def booksMining():

	if not os.path.exists(BOOKS):
		os.mkdir(BOOKS)

	COUNT_OF_BOOKS = 100
	for i in range(COUNT_OF_BOOKS):
		try:
			bookId = random.randint(1000, 15000)
			link = "https://www.gutenberg.org/ebooks/" + str(bookId)
			#link = "https://www.gutenberg.org/ebooks/10516"
			page = requests.get(link).text
			soup = bs4.BeautifulSoup(page, 'html5lib')
			h1 = soup.find('h1').text
			idx = h1.rfind(' by ')
			book = h1[:idx]
			name = h1[idx+4:]

			link = "http://www.gutenberg.org/cache/epub/" + str(bookId) + "/pg" + str(bookId) + ".txt"
			page = requests.get(link).text
			soup = bs4.BeautifulSoup(page, 'html5lib')
			book_text = soup.find('body').text

			if not os.path.exists(BOOKS + name):
				os.mkdir(BOOKS + name)
			if not os.path.exists(BOOKS + name + '/' + book):
				f = open(BOOKS + name + '/' + book, 'w')
				f.write(book_text)
				f.close()
		except:
			continue


booksMining()
run(host='localhost', port=5555, debug=True)
