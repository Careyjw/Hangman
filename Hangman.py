#Jim Carey
#Hangman
#CS 343
#FAll 2018
#11/4/18
def transparent(remainingWords):
	print("words remaining: "+str(len(remainingWords)))
#reads file and creates tuple of the words
def read(filename):
	with open(filename) as file:
		words=file.read().splitlines()
	return words
#askes for number of guesses, with a smart-ass comment if you ask for alot of guesses
def promptGuesses():
	while(1):
		try:
			guesses = int(input("Number of guesses: "))
			if(guesses > 0 and guesses < 20):
				return guesses            
			elif(guesses>=20):
				print("You are no fun... fine")
				return guesses
		except ValueError:
			print("Invalid input\n")   
#the prompt for getting the word length the player wants.
def promptForWordLength(words):
	wordLengths =[];  
	for word in words:
		length = word.__len__()
		if(length not in wordLengths):
			wordLengths.append(length)
	wordLengths.sort()
	print("Available word lengths "+str(wordLengths))
	while(1):
		try:
			length = int(input("Enter word Length: "))
			if(length in wordLengths):
				return length
			else:
				print("I do not have a word at that length")
		except ValueError:
			print("Invalid input, please input a number")		
#creates blank word for the start of game
def initializeWordStatus(length):
	status = ""
	for i in range(0,length):
		status += "-"
	return status
# Return list of all words with length requested by player
def initializeRemainingWords(lines,length):
	words = []
	for word in lines:
		if(word.__len__() == length):
			words.append(word)
	return words
#creates the list of words left in the game
def generateListOfWords(remainingWords, guess, familyToReturn):
	words = []
	for word in remainingWords:
		wordFamily = ""
		for letter in word:
			if(letter == guess):
				wordFamily += guess
			else:
				wordFamily += "-"
				
		if(wordFamily == familyToReturn):
			words.append(word)
	return words
#creats the string that is desplayed on screen
def getWordStatus(wordFamily,lettersGuessed):
	status = ""
	for letter in wordFamily:
		if(letter in lettersGuessed):
			status += letter
		else: 
			status += "-"
	return status
#creates the word family dictionaries
def generateWordFamiliesDictionary(remainingWords, guess):
	wordFamilies = dict()
	for word in remainingWords:
		status = ""
		for letter in word:
			if(letter == guess):
				status += guess
			else:
				status += "-"
				
		if(status not in wordFamilies):
			wordFamilies[status] = 1
		else:
			wordFamilies[status] = wordFamilies[status] + 1
	return wordFamilies
# Return the list of words remaining that player can guess from
def getRemainingWords(guess, remainingWords, numOfGuesses, wordLength):#letter, wordFamily, guesses, length):   
	wordFamilies = generateWordFamiliesDictionary(remainingWords, guess)
	
	familyToReturn = initializeWordStatus(wordLength)
	canAvoidGuess = numOfGuesses == 0 and familyToReturn in wordFamilies
	
	if(canAvoidGuess):
		familyToReturn = initializeWordStatus(wordLength)
	else:
		familyToReturn = highestCount(wordFamilies)

	words = generateListOfWords(remainingWords, guess, familyToReturn)
	return words
#asks the player for their guess, and formats correctly
def promptForGuess(lettersGuessed):
	guessing=1
	while (guessing):
		letter= str(input("Please guess a letter: ").lower())
		if letter in lettersGuessed:
			print("You already guessed that letter.")
		elif len(letter)==1:
			return letter
		elif letter[0].isalpha():
			print("You guessed more than one letter, using the first one.")
			return letter[0]
#helper method for showing the current game
def printGame(lettersGuessed, guesses, status):
	print("Current game status: " + str(status) )
	print("Guesses remaining: " + str(guesses))
	print("Guesses made: " + str(lettersGuessed))
#finds the family that has the most remaining (the main cheating method)
def highestCount(wordFamilies):
	familyToReturn = ""
	maxCount = 0
	for wordFamily in wordFamilies:
		if wordFamilies[wordFamily] > maxCount:
			maxCount = wordFamilies[wordFamily]
			familyToReturn = wordFamily
	return familyToReturn
#main
def play():
	playing=1
	words=read("dictionary.txt")
	debug=int(input("would you like to see the amount of words available?(1 for yes, 0 for no): "))
	while(playing):
		wordLength=promptForWordLength(words)
		numOfGuesses=promptGuesses()
		remainingWords=initializeRemainingWords(words,wordLength)
		wordStat=initializeWordStatus(wordLength)
		lettersGuessed=[]
		game=1
		while(game):
			if debug:
				transparent(remainingWords)
			printGame(lettersGuessed,numOfGuesses,wordStat)
			guess=promptForGuess(lettersGuessed)
			lettersGuessed.append(guess)
			numOfGuesses-=1
			remainingWords = getRemainingWords(guess, remainingWords, numOfGuesses, wordLength)
			wordStat= getWordStatus(remainingWords[0], lettersGuessed)
			
			if guess in wordStat:
				numOfGuesses+=1
			if "-" not in wordStat:
				game=0
				print("You guessed the word! it was: "+str(remainingWords[0]))
				playing=int(input("Play again? (1 for yes, 0 for no): "))
			if (numOfGuesses == 0 and game==1):
				game=0
				print("You Lose! the word was: "+str(remainingWords[0]))
				playing=int(input("Play again? (1 for yes, 0 for no): "))
		print("Thanks for playing! have a great day!")
#the flag to redirect main
if __name__ == '__main__': play()