#!/usr/bin/python
# -*- coding: latin-1 -*-

# A script to convert the mut.txt file as supplied by the Rabobank (the Netherlands)
# to qif for gnucash

# This file is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This file is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    See <http://www.gnu.org/licenses/> for details on the GNU General Public License.


import csv, string
import sys

class CSV2QIF_Base:

	def __init__(self):
		return

	def run(self, filename):
		reader = csv.reader(open(filename,'r'), delimiter=',', quotechar='"')
		writer = file(self.basename() + '.qif', 'w')
		writer.write(self.qif_header())
		for row in reader:
			#print row
			qifdata = self.row2qif(row)
			#print qifdata
			if not qifdata: continue
			writer.write(self.qifdata2str(qifdata))
			writer.write("^\n")
		writer.close()

class Rabobank(CSV2QIF_Base):

	def basename(self):
		return "Rabobank"

	def qif_header(self):
		return "!Type:Bank\n"

	def row2qif(self, row):
		if len(row) < 11: return None
		return {'D': row[2], 'T': self.creditdebit(row[4], row[3]), 'P': row[6], 'M': row[10], 'N': row[5]}

	def qifdata2str(self, data):
		s = ''
		for key in data.keys():
			if key == 'D':
				date = data[key]
				s = s + key + date[0:4] + '/' + date[4:6] + '/' + date[6:8]
				s = s + "\n"
			else:
				s = s + key + data[key]
				s = s + "\n"
		return s

	def creditdebit(self, credit, transfertype):
		if transfertype == 'D':
			return '-' + credit;
		return credit;

if __name__ == '__main__':
	inputfilename = 'mut.txt'
	instance = Rabobank()
	instance.run(inputfilename)
	print 'Done'
