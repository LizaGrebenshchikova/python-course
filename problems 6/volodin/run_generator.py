#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import sys
import pandas as pd

from dialogsgenerator.agent import Agent
from dialogsgenerator.randomdialog import RandomDialog

MAX_DIALOGS = 99999999999

def generate(rd, count_dialogs=5):
	"""
	Генерирует count_dialogs диалогов с помощью rd.generate().
	Возвращаемый объект является генератором.
	"""

	yield from list(map(lambda x: rd.eval(), range(count_dialogs)))

def write(dialogs, target):
	"""
	Записывает сгенерированные диалоги dialogs (это объект-генератор) в поток target.
	"""

	#Копипаста из RandomDialog
	if dialogs is None:
		return

	def printOneDialog(n):
		dialog = next(dialogs)
		def printInFile(msgs):
			target.write('turn {0}\n'.format(msgs[1]))
			target.write("\n".join(msgs[0]))
			target.write('\n\n')

		target.write('dialog {0}\n'.format(n))
		list(map(printInFile, zip(dialog, range(len(dialog)))))

	list(map(printOneDialog, range(MAX_DIALOGS)))

TRUMP_KB = "../trump.csv"
CLINTON_KB = "../clinton.csv"

class Target():

	def __init__(self, name="sys.stdout"):

		if name == "sys.stdout" or name is None:
			self.target = sys.stdout
			self.isClose = False
		else:
			self.target = open(name, "w")
			self.isClose = True

	def getTarget(self):

		return self.target

	def __del__(self):

		if self.isClose:
			self.target.close()

def parseArgs():

	parser = argparse.ArgumentParser()

	parser.add_argument("-o", "--output", help="Поток вывода")
	parser.add_argument("-t", "--trump_kb", help="Путь к файлу с репликами Трампа")
	parser.add_argument("-c", "--clinton_kb", help="Путь к файлу с репликами Клинтон")

	args = parser.parse_args()

	target = Target(args.output)

	if args.trump_kb:
		trump = args.trump_kb
	else:
		trump = TRUMP_KB

	if args.clinton_kb:
		clinton = args.clinton_kb
	else:
		clinton = CLINTON_KB

	clinton = pd.read_csv(clinton, encoding="utf-8")
	trump = pd.read_csv(trump, encoding="utf-8")

	return target, trump, clinton

if __name__ == "__main__":

	target, trump, clinton = parseArgs()

	rd = RandomDialog([Agent(clinton, "clinton"), Agent(trump, "trump")], max_len = 5)

	dialogs = generate(rd, 4)

	write(dialogs, target.getTarget())
