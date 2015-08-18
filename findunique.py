import optparse
import re
import os
from threading import *

screenLock = Semaphore(value=1)
global count
def input(match):
	response = raw_input( '\n''Is this "' + match + '" you want, type (Y/N): ')
	return response

def checkfile(srcfile):

	if not os.path.isfile(srcfile):
		print '[+] File ' + srcfile + ' does not exist.Please check file name'
		exit(0)

	if not os.access(srcfile,os.R_OK):
		print '[+] '+ srcfile + ': Access Denied'
		exit(0)

	
def positionbased(delimiter, position, srcfile):

	f = open(srcfile,'r')

	for line in f.readlines():
		splitline = re.split(delimiter,line)
		keyPosition = splitline[position]
	
		if keyPosition in keylist:
			continue
		else :
			screenLock.acquire()
			if count == 0:
				print "\n[+] Split line shown below\n"
				print splitline
				response = input(keyPosition)
				if (response == 'N'):
					exit(0)
				else:
					if os.path.exists(srcfile+'.unique'):
						os.remove(srcfile+'.unique')
						count=+1
					else:
						keylist.append(keyPosition)
						output = open(srcfile+'.unique','a')
						output.write(line)
						screenLock.release()

			keylist.append(keyPosition)
			output = open(srcfile+'.unique','a')
			output.write(line)
			screenLock.release()
					
	f.close()
	output.close()
	print "Result Generated. Please check output file"
	print "No. of unique line: "+str(len(keylist))

def keybased(delimiter,key,srcfile):
	global count
	count = 0
	f = open(srcfile,'r')
	for line in f.readlines():
		splitline = re.split(delimiter,line)

		if key in splitline:
			keyPosition = splitline.index(key)
			uniqueword = splitline[keyPosition+1]
			if uniqueword in keylist:
				continue
			else:
				screenLock.acquire()
				if count == 0:
					print "\n[+] Line has been split as shown below\n"
					print splitline
					response = input(uniqueword)
					if response == 'N':
						exit(0)
					else:
						if os.path.exists(srcfile+'.unique'):
							os.remove(srcfile+'.unique')
							count=+1
						else:
							keylist.append(keyPosition)
							output = open(srcfile+'.unique','a')
							output.write(line)
							print keylist
							screenLock.release()

				keylist.append(uniqueword)
				output = open(srcfile+'.unique','a')
				output.write(line)
				screenLock.release()
	f.close()
	print "Result Generated. Please check output file"
	print "No. of unique line: "+str(len(keylist))

def regEx(delimiter, regex, srcfile):

	pattern = re.compile(regex)
	f = open(srcfile,'r')

	for line in f.readlines():

		splitline = re.split(delimiter, line)
		patternkey = pattern.search(str(splitline))
		if patternkey:
			key = patternkey.groups()
		if key in keylist:
			continue
		else:
			screenLock.acquire()
			if count == 0:
				print "\n[+] Line has been split as shown below\n"
				print splitline
				response = input(str(key))
				if (response == 'N'):
					exit(0)
				else:
					if os.path.exists(srcfile+'.unique'):
						os.remove(srcfile+'.unique')
						count=+1
					else:
						keylist.append(key)
						output = open(srcfile+'.unique','a')
						output.write(str(line))
						print keylist
						screenLock.release()
			keylist.append(key)
			output = open(srcfile+'.unique','a')
			output.write(str(line))
			screenLock.release()
	f.close()
	output.close()
	print "Result Generated. Please check output file"
	print "No. of unique line: "+str(len(keylist))
	
def main():
	global keylist
	global count
	count = 0
	keylist = []
	parser = optparse.OptionParser('\n\n'+'%prog ' + '-f <filename> -d <delimiter> -p <filepoiition> '+ 'or' +' -k <keyword> ' + 'or' + ' -r <RegEx>' )
	parser.add_option('-d' ,dest ='delimiter', type='string', help = 'specify delimiter/delimiters seperated by pipe and use escape character or regex wherever necessary')
	parser.add_option('-p' ,dest ='position', type='int', help = 'specify position of unique word')
	parser.add_option('-k' ,dest ='key', type='string', help = 'specify word that appears before unique Word')
	parser.add_option('-f' ,dest ='srcfile', type='string', help = 'specify source file')
	parser.add_option('-r' ,dest ='regex', type='string', help = 'specify RegEx within paranthesis to match unique word/string')
	
	(options, args) = parser.parse_args()
	delimiter = options.delimiter
	position = options.position
	key = options.key
	srcfile = options.srcfile
	regex = options.regex

	if (delimiter!=None ) and (position!=None) and (srcfile!=None):

		checkfile(srcfile)
		print "Performing position-based matching"
		positionbased(delimiter, position, srcfile)

	elif (delimiter!=None ) and (key!=None) and (srcfile!=None):
		checkfile(srcfile)
		print "Performing key-based matching"
		keybased(delimiter, key, srcfile)

	elif (delimiter!=None ) and (regex!=None) and (srcfile!=None):
		checkfile(srcfile)
		print "Performing RegEx on input file"
		regEx(delimiter, regex, srcfile)

	else:	
		print parser.usage

if __name__=='__main__':
	main()