import random,pygame,time,sys
from pygame.locals import *
FPS=30
WW=640
WH=480
FLASHSPEED=500
FLASHDELAY=200
BUTTONSIZE=200
GAP=20
TIMEOUT=4
#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK
XMARGIN = (WW - (2*BUTTONSIZE) - GAP)/2
YMARGIN = (WH - (2*BUTTONSIZE) - GAP)/2

YELLOWRECT = pygame.Rect(XMARGIN,YMARGIN,BUTTONSIZE,BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + GAP,YMARGIN,BUTTONSIZE,BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN,YMARGIN + BUTTONSIZE + GAP,BUTTONSIZE,BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + GAP,YMARGIN + BUTTONSIZE + GAP,BUTTONSIZE,BUTTONSIZE)

def main() :
	global FPSCLOCK,DISPLAYSURF,BASICFONT,BEEP1,BEEP2,BEEP3,BEEP4
	pygame.init()
	FPSCLOCK=pygame.time.Clock()
	DISPLAYSURF=pygame.display.set_mode((WW,WH))
	pygame.display.set_caption('Simulate')
	BASICFONT=pygame.font.Font('freesansbold.ttf', 16)
	infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
	infoRect = infoSurf.get_rect()
	infoRect.topleft = (10, WH - 25)
	BEEP1 = pygame.mixer.Sound('beep1.ogg')
	BEEP2 = pygame.mixer.Sound('beep2.ogg')
	BEEP3 = pygame.mixer.Sound('beep3.ogg')
	BEEP4 = pygame.mixer.Sound('beep4.ogg')

	pattern=[]
	currentStep = 0
	lastClickTime = 0
	score = 0

	waitingforinput=False
	while True:
		clickedbutton=None
		DISPLAYSURF.fill(bgColor)
		drawbuttons()

		scoreSurf = BASICFONT.render('Score :' + str(score), 10, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WW  - 100, 10)
		DISPLAYSURF.blit(scoreSurf, scoreRect)
		DISPLAYSURF.blit(infoSurf,infoRect)
		checkforquit()

		for event in pygame.event.get() :
			if event.type == MOUSEBUTTONUP :
				mousex,mousey = event.pos
				clickedbutton = getButtonClicked(mousex,mousey)
			elif event.type == KEYDOWN :
				if event.key == K_q:
					clickedbutton = YELLOW
				elif event.key == K_w:
					clickedbutton = BLUE
				elif event.key == K_a :
					clickedbutton = RED
				elif event.key == K_s :
					clickedbutton = GREEN

		if not waitingforinput :
			pygame.display.update()
			pygame.time.wait(1000)
			pattern.append(random.choice((YELLOW,RED,BLUE,GREEN)))
			for button in pattern :
				flashbuttonAnimation(button)
				pygame.time.wait(FLASHDELAY)
			waitingforinput=True

		else :
			if clickedbutton and clickedbutton == pattern[currentStep] :
				flashbuttonAnimation(clickedbutton)
				currentStep+=1
				lastClickTime = time.time()

				if currentStep == len (pattern):
					changeBackgroundAnimation()
					score += 1
					waitingforinput = False
					currentStep = 0

			elif (clickedbutton and clickedbutton != pattern[currentStep]):
				gameOverAnimation()
				pattern = []
				currentStep = 0
				waitingforinput = False
				score = 0
				pygame.time.wait(1000)
				changeBackgroundAnimation


		pygame.display.update()
		FPSCLOCK.tick(FPS)


def terminate() :
	pygame.quit()
	sys.exit()


def drawbuttons(): 
	pygame.draw.rect(DISPLAYSURF,YELLOW , YELLOWRECT)
	pygame.draw.rect (DISPLAYSURF , RED , REDRECT)
	pygame.draw.rect(DISPLAYSURF  , BLUE , BLUERECT	)
	pygame.draw.rect(DISPLAYSURF , GREEN , GREENRECT)


def checkforquit():
	for event in pygame.event.get(QUIT) : 
		terminate()
	for event in pygame.event.get(KEYUP) :
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event)

def flashbuttonAnimation(color, animationSpeed=50):
	if color == YELLOW:
		sound = BEEP1
		flashColor = BRIGHTYELLOW
		rectangle = YELLOWRECT
	elif color == BLUE:
		sound = BEEP2
		flashColor = BRIGHTBLUE
		rectangle = BLUERECT
	elif color == RED:
		sound = BEEP3
		flashColor = BRIGHTRED
		rectangle = REDRECT
	elif color == GREEN:
		sound = BEEP4
		flashColor = BRIGHTGREEN
		rectangle = GREENRECT

	origSurf = DISPLAYSURF.copy()
	flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
	flashSurf = flashSurf.convert_alpha()
	r, g, b = flashColor
	sound.play()
	for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
		for alpha in range(start, end, animationSpeed * step):
			checkforquit()
			DISPLAYSURF.blit(origSurf, (0, 0))
			flashSurf.fill((r, g, b, alpha))
			DISPLAYSURF.blit(flashSurf, rectangle.topleft)
			pygame.display.update()
			FPSCLOCK.tick(FPS)
	DISPLAYSURF.blit(origSurf, (0, 0))


def changeBackgroundAnimation(animationSpeed=40):
	global bgColor
	newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	newBgSurf = pygame.Surface((WW, WH))
	newBgSurf = newBgSurf.convert_alpha()
	r, g, b = newBgColor
	for alpha in range(0, 255, animationSpeed): # animation loop
		checkforquit()
		DISPLAYSURF.fill(bgColor)

		newBgSurf.fill((r, g, b, alpha))
		DISPLAYSURF.blit(newBgSurf, (0, 0))

		drawbuttons() # redraw the buttons on top of the tint

		pygame.display.update()
		FPSCLOCK.tick(FPS)
	bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
	origSurf = DISPLAYSURF.copy()
	flashSurf = pygame.Surface(DISPLAYSURF.get_size())
	flashSurf = flashSurf.convert_alpha()
	BEEP1.play() # play all four beeps at the same time, roughly.
	BEEP2.play()
	BEEP3.play()
	BEEP4.play()
	r, g, b = color
	for i in range(3): # do the flash 3 times
		for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
			for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
				checkforquit()
				flashSurf.fill((r, g, b, alpha))
				DISPLAYSURF.blit(origSurf, (0, 0))
				DISPLAYSURF.blit(flashSurf, (0, 0))
				drawbuttons()
				pygame.display.update()
				FPSCLOCK.tick(FPS)



def getButtonClicked(x, y):
	if YELLOWRECT.collidepoint( (x, y) ):
		return YELLOW
	elif BLUERECT.collidepoint( (x, y) ):
		return BLUE
	elif REDRECT.collidepoint( (x, y) ):
		return RED
	elif GREENRECT.collidepoint( (x, y) ):
		return GREEN
	return None


if __name__ == '__main__':
    main()






























