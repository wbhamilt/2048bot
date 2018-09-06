#! python3
# 2048.py - plays a game of 2048
# needs hella work

#NOTE - the game determines coordinates in (column, row) format!!!!

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import numpy

tileValues = ['2', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048']
buffer = .2

#functions *******************************************************************************
def readBoard():
	board = numpy.zeros((4,4))
	board[0][0] = findSlot('1-1')
	board[1][0] = findSlot('2-1')
	board[2][0] = findSlot('3-1')
	board[3][0] = findSlot('4-1')

	board[0][1] = findSlot('1-2')
	board[1][1] = findSlot('2-2')
	board[2][1] = findSlot('3-2')
	board[3][1] = findSlot('4-2')

	board[0][2] = findSlot('1-3')
	board[1][2] = findSlot('2-3')
	board[2][2] = findSlot('3-3')
	board[3][2] = findSlot('4-3')

	board[0][3] = findSlot('1-4')
	board[1][3] = findSlot('2-4')
	board[2][3] = findSlot('3-4')
	board[3][3] = findSlot('4-4')
	
	return board

# helper function to readBoard()
def findSlot(position):
	answer = 0
	for i in tileValues:
		try:
			tile11 = browser.find_element_by_css_selector('div.tile.tile-'+ i +'.tile-position-'+ position)
			answer = i
		except Exception:
			pass
	return answer
	
def beginGame():
	previousBoard = numpy.zeros((4,4))
	time.sleep(3)
	try:
		time.sleep(buffer)
		main_page.send_keys(Keys.DOWN)
		time.sleep(buffer)
		main_page.send_keys(Keys.LEFT)
		time.sleep(buffer)
		main_page.send_keys(Keys.DOWN)
		time.sleep(buffer)
		main_page.send_keys(Keys.LEFT)
		time.sleep(buffer)
		main_page.send_keys(Keys.DOWN)
	except Exception:
		print('off to a bad start - intro sequence threw exception')
	return

#bottom row is assumed to be board[x][3]
#I DONT THINK THESE WORK
def checkBottomRowMerge(board):
	"This function returns true if there is any valid merge from shifting the bottom row left"
	if (board[0][3] == board[1][3] or board[1][3] == board[2][3] or board[2][3] == board[3][3]):
		return True
	else:
		return False
	return

def checkVerticalBottomMerge(board):
	"this function returns true if shifting down would result in a merge to benefit the bottom row"
	if ((board[0][3] == board[0][2]) or (board[1][3] == board[1][2]) or (board[2][3] == board[2][2]) or (board[3][3] == board[3][2])):
		return True
	else:
		return False
	return

def checkIfMoveDidNothing(current, previous):
	"This might be completely wrong"
	return ((current == previous).all())


# end of functions **********************************************************************




browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')
main_page = browser.find_element_by_tag_name('html')
game_over = browser.find_element_by_class_name("retry-button")
# browser.find_element_by_class_name("game-container")


c = 0
emptyMoveCount = 0
currentBoard = readBoard()
previousBoard = numpy.zeros((4,4))
beginGame()

#this loop is the core of the game
while (not game_over.is_displayed()):
	currentBoard = readBoard()
	if ((currentBoard == previousBoard).all()):
		emptyMoveCount += 1
	else:
		emptyMoveCount = 0
	
	try:
		time.sleep(.1)
		main_page.send_keys(Keys.LEFT)
		time.sleep(.1)
		main_page.send_keys(Keys.LEFT)
		time.sleep(.1)
		main_page.send_keys(Keys.DOWN)

		if((c % 5) == 0):
			time.sleep(.1)
			main_page.send_keys(Keys.RIGHT)
		
	except Exception as e:
		print("something fucked up after this many times: ", c)
		time.sleep(.5)
		browser.refresh()
		browser.execute_script("window.scrollTo(0, 10);")
		print(e)
		print(type(e))
		print(e.args)

	c+=1
	previousBoard = currentBoard


finalScore = currentBoard.max()
print ("done! final score was : ", finalScore) #eventually display score to command line




		

		
# NOTES
# game is located at <div class="game-container">

# right now, all of this is crap
	# WebDriverWait(browser, 30).until(EC.presence_of_element_located(browser.find_element_by_tag_name('html')))
	# def getBoard(BeautifulSoup board): THIS IS INCORRECT SYNTAX
	#page = requests.get(browser.current_url)
	#<div class="tile-inner">4</div>

	
# THE LINE BELOW SUCCESSFULLY MADE A TILE OBJECT WHEN TILE 1-1 HAD THE VALUE OF 4***************************************
# tile1-1 = browser.find_element_by_css_selector('div.tile.tile-4.tile-position-1-1')
