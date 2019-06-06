import telebot
import random
import pygame
import sys

# global constants
TOKEN = '864588130:AAEGaWNYx18GFvMO4BLc0_9MCmXK9HQ01n8'
FREQ = 4100     # same as audio CD
BITSIZE = -16   # unsigned 16 bit
CHANNELS = 2    # 1 == mono, 2 == stereo
BUFFER = 1024   # audio buffer size is no. of samples
FRAMERATE = 60  # how often check if playback has finished

morsetab = {
    'a': '.- ',     'b': '-... ',
    'c': '-.-. ',   'd': '--. ',
    'e': '. ',      'f': '..-. ',
    'g': '--. ',    'h': '.... ',
    'i': '.. ',     'j': '.--- ',
    'k': '-.- ',    'l': '.-.. ',
    'm': '-.- ',    'n': '-. ',
    'o': '--- ',    'p': '.--. ',
    'q': '--.- ',   'r': '.-. ',
    's': '... ',    't': '- ',
    'u': '..- ',    'v': '...- ',
    'w': '.-- ',    'x': '-..- ',
    'y': '-.-- ',   'z': '--.. ',
    '0': '----- ',  '1': '.---- ',
    '2': '..--- ',  '3': '...-- ',
    '4': '....- ',  '5': '..... ',
    '6': '-.... ',  '7': '--... ',
    '8': '---... ', '9': '----. ',
    ' ': '|',       ',': '--..-- ',
    '.': '.-.-.- ', '?': '..--.. ',
    ';': '-.-.-. ', ':': '---... ',
    "'": '.----. ', '-': '-....- ',
    '/': '-..-. ',  '(': '-.--.- ',
    ')': '-.--.- ', '_': '..--.- '
}

morse_sound = {
    '.':    'dot.ogg',
    '-':    'dash.ogg',
    ' ':    'short_silence.ogg',
    '*':    'very_short_silence.ogg',
    '|':    'long_silence.ogg'
}


def playsound(soundfile):
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        clock.tick(FRAMERATE)


def play_morse_sound(code):
    for channel_id, dip in enumerate(code):
        try:
            sound = pygame.mixer.Sound(morse_sound[dip])
        except KeyError:
            sound = pygame.mixer.Sound(morse_sound[' '])
        playsound(sound)


def code_to_sound_code(code):
    res = code.replace('..', '.*.')\
        .replace('--', '-*-')\
        .replace('.-', '.*-')\
        .replace('-.', '-*.')\
        .replace('-.', '-*.')\
        .replace('..', '.*.')\
        .replace('--', '-*-')\
        .replace('.-', '.*-')\
        .replace('-.', '-*.')
    return res


def string_to_code(conver_string):
    res = ''
    for c in conver_string:
        try:
            res += morsetab[c]
        except KeyError:
            pass
    return res


pygame.init()
pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

code = string_to_code('sos')
play_morse_sound(code)

bot = telebot.TeleBot(TOKEN)

greetings = ['хола', 'хэллоу', 'здравствуй', 'привет', 'хай', 'здравствуй', 'приветствую', 'hi', 'hello']
invokers = greetings[:]
invokers.append('bot01')


@bot.message_handler(func=lambda message: True)
def say_hi(message):
    if message.text.lower() in invokers:
        bot.reply_to(message, random.choice(greetings).capitalize() + ', ' + message.from_user.username + '!')


bot.polling()
