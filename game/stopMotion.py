import pygame, random, os, sys, spritesheet
from nlp import speech

pygame.init()

## Game settings
gameScreen = pygame.display.set_mode((512,512), 0, 32)
pygame.display.set_caption('Gunma Pronunciation Game')
#FPS = 1

"""class spritesheet:
	def _init_(self, filename, cols, rows):
	self.sheet = pygame.image.load(filename)
	self.cols = cols
	self.rows = rows
	self.totalCellCount = cols * rows
	self.rect = self.sheet.get_rect()
	w = self.cellWidth = self.rect.width/cols
	h = self.cellHeight = self.rect.height/rows
	hw,hh = self.cellCenter = (w/2, h/2)
	self.cells = list(index % cols * w , index/cols * h ) """
	
"""
##Textures and Images
ss = spritesheet.spritesheet('testgunmaspritesheet.png')
#image = ss.image_at((0, 0, 87, 94))
gunmaImages = []
for i in range(1, 8):
	gunmaImages[i-1] = ss.image_at((0, 0, 87 * i, 94))
"""
	
##Information should be passed from interface
words = ['Red', 'Blue', 'Black', 'White', 'Yellow', 'Orange', 'Green', 'Purple', 'Brown']
wordCategory = 'Colors'
lvl = 0

numEnemies = 8				#need to determine based on the words array length
enemyCounter = numEnemies	

gunmachanTexture = 'gunma.png'
enemy2Texture = 'enemy2.png'
enemy3Texture = 'enemy3.png'
groundTexture = 'ground.png'
enemy1Texture = 'enemy1.png'
skyTexture = 'sky.png'
cloudTexture = 'cloud.png'
mouseTexture = 'mouse.png'
enemyStopperTexture = 'enemyStopper.png'
sky = pygame.image.load(skyTexture)
cloud = pygame.image.load(cloudTexture)
ground = pygame.image.load(groundTexture)
gunmachan = pygame.image.load(gunmachanTexture)
enemy1 = pygame.image.load(enemy1Texture)
enemy2 = pygame.image.load(enemy2Texture)
enemy3 = pygame.image.load(enemy3Texture)
mouse = pygame.image.load(mouseTexture)
enemyStopper = pygame.image.load(enemyStopperTexture)

basicfont = pygame.font.SysFont(None, 40)
guiText0 = 'Category: ' + wordCategory
text0 = basicfont.render(guiText0, True, (0, 0, 0), None)
textrect0 = text0.get_rect()
textrect0.centerx = 120 	
textrect0.centery = 15 		

guiText = 'Level: ' + str(lvl)
text = basicfont.render(guiText, True, (0, 0, 0), None)
textrect = text.get_rect()
textrect.centerx = 60 		#gameScreen.get_rect().centerx
textrect.centery = 45 		#gameScreen.get_rect().centery

correctText = basicfont.render(' Correct - C key', True, (0, 255, 0), None)		
correctTextRect = correctText.get_rect()
correctTextRect.centerx = 100
correctTextRect.centery = 450

incorrectText = basicfont.render('Incorrect - I key', True, (255, 0, 0), None)		
incorrectTextRect = incorrectText.get_rect()
incorrectTextRect.centerx = 100
incorrectTextRect.centery = 480

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
run = True

wrongList = []
correctList = []

enemyArray = [enemy1, enemy2, enemy3]
currEnemy = random.choice(enemyArray)

groundX = 0 
groundY = 300
cloud1X = 25
cloud1Y = 25
cloud2X = 150
cloud2Y = 50
cloud3X = 300
cloud3Y = 150
gunmachanX = 50
gunmachanY = 256
currEnemyX = 500
currEnemyY = 280
enemyStopperX = 200
enemyStopperY = 280

isPaused = False
isStopped = False

if not isPaused:
	currEnemySpeed = 3
	cloudSpeed = 5

currWord = words[0]
del words[0]
basicfont4 = pygame.font.SysFont(None, 24)
wordText = basicfont4.render(currWord, True, (0, 0, 0), (255, 255, 255))
wordRect = wordText.get_rect()
wordRect.centerx = currEnemyX + 15
wordRect.centery = currEnemyY - 25

pauseText = basicfont.render('Temp Pause Screen', True, (0, 0, 0), None)
pauseRect = pauseText.get_rect()
pauseRect.centerx = gameScreen.get_rect().centerx
pauseRect.centery = gameScreen.get_rect().centery

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				isPaused = not isPaused
			if event.key == pygame.K_c:
				if isStopped:
					correctList.append(currWord)
					isStopped = False
					currEnemyX -= 3
			if event.key == pygame.K_i:
				if isStopped:
					wrongList.append(currWord)
					isStopped = False
					currEnemyX -= 3	
		if event.type == pygame.QUIT:
		   pygame.quit()
		   quit()
	gameScreen.blit(sky, (0,0))
	
	screenboundx, screenboundy = gameScreen.get_size()

	if currEnemyX <= -25 and len(words) > 0:		#Move enemy R -> L
		currEnemy = random.choice(enemyArray)
		currEnemyX = screenboundx
		currEnemyY = 280
		currWord = words[0]
		del words[0]
		wordText = basicfont4.render(currWord, True, (0, 0, 0), (255, 255, 255))
		wordRect = wordText.get_rect()
		wordRect = wordText.get_rect()
		wordRect.centerx = currEnemyX + 15
		wordRect.centery = currEnemyY - 25	

	if not isStopped:
		currEnemySpeed = 3
		cloudSpeed = 5
	
	if(currEnemyX == enemyStopperX):
		currEnemySpeed = 0
		cloudSpeed = 0
		isStopped = True;
		#call chris software
		s = speech.Speech(lvl)
		if s.record_and_validate(currWord):
			correctList.append(currWord)		
			isStopped = False
			currEnemyX -= 3
		else:
			wrongList.append(currWord)
			isStopped = False
			currEnemyX -= 3	
			
	if cloud1X <= -50:								#Move cloud1 R -> L
		cloud1X = screenboundx
		cloud1Y = 25 + random.randrange(100)
	
	if cloud2X <= -50:								#Move cloud2 R -> L
		cloud2X = screenboundx
		cloud2Y = 50 + random.randrange(150)
	
	if cloud3X <= -50:								#Move cloud2 R -> L
		cloud3X = screenboundx
		cloud3Y = 10 + random.randrange(50)
	
	if not len(words) == 0:
		gameScreen.blit(ground, (groundX, groundY))
		#gameScreen.blit(enemyStopper, (enemyStopperX, enemyStopperY))
		gameScreen.blit(currEnemy, (currEnemyX, currEnemyY))
		gameScreen.blit(wordText, wordRect)
		gameScreen.blit(gunmachan, (gunmachanX, gunmachanY))
		gameScreen.blit(cloud, (cloud1X, cloud1Y))
		gameScreen.blit(cloud, (cloud2X, cloud2Y))
		gameScreen.blit(cloud, (cloud3X, cloud3Y))
		gameScreen.blit(text, textrect)
		gameScreen.blit(text0, textrect0)
		gameScreen.blit(correctText, correctTextRect)
		gameScreen.blit(incorrectText, incorrectTextRect)
		#debugger = "Debug: " + str(currEnemyX) + "    " + str(enemyStopperX) + "   " + str(currEnemySpeed)
		#debugText = basicfont4.render(debugger, True, (0, 0, 0), None)
		#debugRect = debugText.get_rect()
		#debugRect.centerx = gameScreen.get_rect().centerx + 100
		#debugRect.centery = gameScreen.get_rect().centery + 200
		#gameScreen.blit(debugText, debugRect)
	else:											#End game info
		stringEndText = 'Temp End Screen'
		endText = basicfont.render(stringEndText, True, (0, 0, 0), None)
		endRect = endText.get_rect()
		endRect.centerx = gameScreen.get_rect().centerx 
		endRect.centery = gameScreen.get_rect().centery - 100
		gameScreen.blit(endText, endRect)
		incList = 'Incorrect List: ' + ' , '.join(wrongList)
		incText = basicfont4.render(incList, True, (0, 0, 0), None)
		incRect = incText.get_rect()
		incRect.centerx = gameScreen.get_rect().centerx
		incRect.centery = gameScreen.get_rect().centery
		gameScreen.blit(incText, incRect)
		corrList = 'Correct List: ' + ' , '.join(correctList)
		corrText = basicfont4.render(corrList, True, (0, 0, 0), None)
		corrRect = corrText.get_rect()
		corrRect.centerx = gameScreen.get_rect().centerx
		corrRect.centery = gameScreen.get_rect().centery + 100
		gameScreen.blit(corrText, corrRect)
	
	if not isPaused:														
		currEnemyX -= currEnemySpeed
		cloud1X -= cloudSpeed
		cloud2X -= cloudSpeed
		cloud3X -= cloudSpeed
		wordRect.centerx = currEnemyX + 15
		wordRect.centery = currEnemyY - 25	
	else:
		gameScreen.blit(pauseText, pauseRect)	
	
	mousex,mousey = pygame.mouse.get_pos()
	mousex -= mouse.get_width()/2
	mousey -= mouse.get_height()/2
	gameScreen.blit(mouse, (mousex, mousey))
	clock.tick(20)
	pygame.display.update()

