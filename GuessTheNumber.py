from flask import Flask, render_template
from flask_ask import Ask, statement, question, context, session, convert_errors
import random

# Init Flask Ask
APP = Flask(__name__)
ASK = Ask(APP, "/")

# variables:
minNumber = 1
maxNumber = 100

# arrays:
funnyHelloArray = ['Hallo', 'Guten Tag', 'Servus', 'Hallo', 'Guten Tag', 'Hallo', 'Guten Tag', 'Hallo', 'Moin Moin', 'Hallo']
funnyAnswerArray = ['Ein Reh spring hoch, ein Reh spring weit, warum auch nicht, es hat ja Zeit','Ein Naßhorn und ein Trockenhorn spazierten durch die Wüste. Da stolperte das Trockenhorn, unds Naßhorn sagte: Siehste!', 'Meine besten Witze hab ich erzählt, das Publikum lächelte nur leicht gequält. Doch Heiterkeit ohne Maß und Ziel, erregte ich als ich vom Fahrrad fiel', 'Fällt des Bauerns Uhr in Mist, weiß er nicht wie spät es ist', 'Kräht der Maulwurf auf dem Dach, liegt der Hahn vor Lachen flach']

@ASK.launch
def launch():
	session.attributes['number'] = random.randint(minNumber, maxNumber)
	#print('Die gesuchte Zahl ist '+str(session.attributes['number'])+'.')
	session.attributes['guessCounter'] = 0
	session.attributes['hintCounter'] = 0
	session.attributes['userWon'] = 0
	answer = random.choice(funnyHelloArray)+', an welche Zahl zwischen '+str(minNumber)+' und '+str(maxNumber)+' denke ich?'
	return question(answer)

# explain game again if user asks for help:
@ASK.intent('AMAZON.HelpIntent')
def give_help():
	helptext = 'Lass uns ein Spiel spielen. Ich denke an eine Zahl zwischen '+str(minNumber)+' und '+str(maxNumber)+', Du musst raten an welche Zahl ich denke indem du mir Zahlen nennst. Ich sage dir, ob deine genannte Zahl höher oder niedriger ist als meine. Falls du einen Hinweis haben möchtest, sage das Wort Hinweis. Du hast zwei Hinweise pro Runde. Versuche die Zahl in so wenig Anläufen wie möglich zu erraten.'
	return question(helptext)

# end the game before it is solved
@ASK.intent('AMAZON.CancelIntent')
def end_game():
	return statement('Das Spiel wird beendet. Bis zum nächsten Mal.')
@ASK.intent('AMAZON.StopIntent')
def end_game_two():
	return statement('Das Spiel wird beendet. Bis zum nächsten Mal.')
@ASK.intent('endCustomIntent')
def end_game_four():
	return statement('Das Spiel wird beendet. Bis zum nächsten Mal.')

# NO intent, wehn user wants to exit
@ASK.intent('AMAZON.NoIntent')
def end_game_three():
	if session.attributes['userWon'] == 1 : 
		return statement('Okay. Bis zum nächsten Mal.')
	else :
		return question('Ich habe deine Zahl leider nicht verstanden. Bitte wiederhole sie.')

# YES intent, when user wants to start a new game
@ASK.intent('AMAZON.YesIntent')
def end_game_three():
	if session.attributes['userWon'] == 1 : 
		session.attributes['number'] = random.randint(minNumber, maxNumber)
		#print('Die gesuchte Zahl ist '+str(session.attributes['number'])+'.')
		session.attributes['guessCounter'] = 0
		session.attributes['hintCounter'] = 0
		session.attributes['userWon'] = 0
		return question('Okay. An welche Zahl zwischen '+str(minNumber)+' und '+str(maxNumber)+' denke ich jetzt?')
	else :
		return question('Ich habe deine Zahl leider nicht verstanden. Bitte wiederhole sie.')

# none number answers:
@ASK.intent('wordIntent', default={'word': 'empty'})
def ask_again(word):
	if word.lower() == 'abbrechen' or word.lower() == 'stop' or word.lower() == 'beenden' or word.lower() == 'spiel verlassen' or word.lower() == 'verlassen' or word.lower() == 'beende das spiel' or word.lower() == 'spiel beenden' or word.lower() == 'spiel abbrechen' or word.lower() == 'aufhören' or word.lower() == 'exit' or word.lower() == 'cancel' or word.lower() == 'ich möchte aufhören' or word.lower() == 'lass es gut sein' :
		return statement('Das Spiel wird beendet. Bis zum nächsten Mal.')
	else :
		return question('Ich habe dich leider nicht richtig verstanden. Bitte formuliere deine Anfrage oder Zahl erneut.')

# react to the numbers of the user:
@ASK.intent('numberIntent', convert={'number' : int},
#mapping={'number': 'number'},
default={'number': -1})
def guessing_game(number):
	if 'number' in convert_errors:
		return question('Ich habe deine Zahl leider nicht verstanden. Bitte wiederhole sie.')
	if number < 0:
		return question('Ich habe deine Zahl leider nicht verstanden. Bitte wiederhole sie.')
	else:
		session.attributes['guessCounter'] = session.attributes['guessCounter'] + 1
		if number == session.attributes['number']:
			session.attributes['userWon'] = 1
			newGameText = ' Möchtest du eine weitere Runde spielen?'
			if session.attributes['guessCounter'] == 1:
				return question('Home Run! Howl in one! Strike! Du hast die Zahl im ersten Versuch erraten! Sie lautet '+str(session.attributes['number'])+', Möchtest du versuchen, das nochmal zu schaffen?')
			elif session.attributes['guessCounter'] < 5:
				return question('Juhu! Du hast die richtige Zahl erraten! Sie lautet '+str(session.attributes['number'])+', Dafür hast du insgesamt '+str(session.attributes['guessCounter'])+' Versuche benötigt. Das ist sehr gut!'+ newGameText)
			elif session.attributes['guessCounter'] > 10:
				return question('Aus, aus, das Spiel ist aus! Du hast die gesuchte Zahl gefunden! Sie lautet '+str(session.attributes['number'])+', Dafür hast du insgesamt '+str(session.attributes['guessCounter'])+' Versuche benötigt. Das geht aber noch deutlich besser!'+ newGameText)
			else:
				return question('Das ist die gesuchte Zahl! Sie lautet '+str(session.attributes['number'])+', Dafür hast du insgesamt '+str(session.attributes['guessCounter'])+' Versuche benötigt.'+ newGameText)
		else:
			session.attributes['hinttext'] = 'Ich habe deine Zahl leider nicht verstanden. Bitte wiederhole sie.'
			if number < session.attributes['number']:
				if session.attributes['number'] - number > maxNumber/2:
					session.attributes['hinttext'] = 'Die gesuchte Zahl ist viel größer als '+str(number)+'.'
				else:
					session.attributes['hinttext'] = 'Die gesuchte Zahl ist größer als '+str(number)+'.'
			else:
				if number - session.attributes['number'] > maxNumber/2:
					session.attributes['hinttext'] = 'Die gesuchte Zahl ist viel kleiner als '+str(number)+'.'
				else:
					session.attributes['hinttext'] = 'Die gesuchte Zahl ist kleiner als '+str(number)+'.'
			return question(session.attributes['hinttext'])
			
# if user asks for a hint give him one based on the number of hints he already had:
@ASK.intent('hintIntent')
def give_hint():
	session.attributes['hinttext'] = 'kein Hinweis möglich'
	if session.attributes['hintCounter'] == 0:
		if session.attributes['number'] % 5 == 0:
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist durch fünf teilbar.'
		elif session.attributes['number'] % 4 == 0:
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist durch vier teilbar.'
		elif session.attributes['number'] % 3 == 0:
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist durch drei teilbar.'
		elif session.attributes['number'] % 2 == 0:
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist gerade.'
		else:
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist ungerade'
	elif session.attributes['hintCounter'] == 1:
		if chech_prime(session.attributes['number']):
			session.attributes['hinttext'] = 'Die gesuchte Zahl ist eine Primzahl'
		else:
			underNumber = random.randint(session.attributes['number'] - 25, session.attributes['number'] - 5)
			if underNumber < minNumber:
				underNumber = minNumber
			upperNumber = random.randint(session.attributes['number'] + 5, session.attributes['number'] + 25)
			if upperNumber > maxNumber:
				upperNumber = maxNumber
			session.attributes['hinttext'] = 'Die gesuchte Zahl liegt zwischen '+str(underNumber)+' und '+str(upperNumber)+'.'
	else:
		session.attributes['hinttext'] = 'Leider habe ich keinen weiteren Hinweis mehr. Dafür aber einen Reim: '+random.choice(funnyAnswerArray)+'.'
	session.attributes['hintCounter'] = session.attributes['hintCounter'] + 1
	return question(session.attributes['hinttext'])

# method to check if a number is a prime number:
def chech_prime(num):
	if num > 1:
		for i in range(2,num):
			if num % i == 0:
				return False
		else:
			return True
	else:
		return False

if __name__ == '__main__':
	#APP.run(debug=True, host='127.0.0.1', port=5000)
	APP.run(debug=True, host='0.0.0.0', port=1234)
