#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Считаем, что архив распакован в папку books, она находится в той же папке, что и все остальные файлы.
#Заливать 300ГБ на гит -- очень не хочется.

from bottle import request, run, route, template
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

run(host='localhost', port=5555, debug=True)
