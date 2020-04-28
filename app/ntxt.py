import app.arabic_const as arabconst
import string
import re

# -*- coding: utf-8 -*-
""" https://github.com/cltk/cltk/blob/master/cltk/corpus/arabic/alphabet.py """
WESTERN_ARABIC_NUMERALS = ['0','1','2','3','4','5','6','7','8','9']

#EASTERN_ARABIC_NUMERALS = [u'\u06F0', u'\u06F1', u'\u06F2', u'\u06F3', u'\u0664', u'\u06F5', u'\u0666', u'\u06F7', u'\u06F8', u'\u06F9']
EASTERN_ARABIC_NUMERALS = [u'٠', u'١', u'٢', u'٣', u'٤', u'٥', u'٦', u'٧', u'٨', u'٩']

eastern_to_western_numerals = {}
for i in range(len(EASTERN_ARABIC_NUMERALS)):
    eastern_to_western_numerals[EASTERN_ARABIC_NUMERALS[i]] = WESTERN_ARABIC_NUMERALS[i]

# Punctuation marks
COMMA = u'\u060C'
SEMICOLON = u'\u061B'
QUESTION = u'\u061F'

# Other symbols
PERCENT = u'\u066a'
DECIMAL = u'\u066b'
THOUSANDS = u'\u066c'
STAR = u'\u066d'
FULL_STOP = u'\u06d4'
MULITIPLICATION_SIGN = u'\u00D7'
DIVISION_SIGN = u'\u00F7'

arabic_punctuations = COMMA + SEMICOLON + QUESTION + PERCENT + DECIMAL + THOUSANDS + STAR + FULL_STOP + MULITIPLICATION_SIGN + DIVISION_SIGN
all_punctuations = string.punctuation + arabic_punctuations + '()[]{}'

all_punctuations = ''.join(list(set(all_punctuations)))

def strip_tashkeel(text):
    return arabconst.HARAKAT_PAT.sub('', text) 

def strip_tatweel(text):
    return re.sub(u'[%s]' % arabconst.TATWEEL, '', text)

def normalize_hamza(text):
    text = arabconst.ALEFAT_PAT.sub(arabconst.ALEF, text)
    return arabconst.HAMZAT_PAT.sub(arabconst.HAMZA, text)

def normalize_spellerrors(text):
    text = re.sub(u'[%s]' % arabconst.TEH_MARBUTA, arabconst.HEH, text)
    return re.sub(u'[%s]' % arabconst.ALEF_MAKSURA, arabconst.YEH, text)

def normalize_lamalef(text):
    return arabconst.LAMALEFAT_PAT.sub(u'%s%s'%(arabconst.LAM, arabconst.ALEF), text)

def normalize_arabic_text(text):
    text = strip_tashkeel(text)
    text = strip_tatweel(text)
    text = normalize_lamalef(text)
    text = normalize_hamza(text)
    text = normalize_spellerrors(text)
    return text

def convert_eastern_to_western_numerals(text):
    for num in EASTERN_ARABIC_NUMERALS:
        text = text.replace(num, eastern_to_western_numerals[num])
    return text

def remove_all_punctuations(text):
    for punctuation in all_punctuations:
        text = text.replace(punctuation, '')
    return text

def remove_extra_spaces(text):
    return ' '.join(text.split())

#########################################################################################################


'''
very important note:
    The order of the execution of the these function is extremely crucial.
'''

def text_normalization(text):
    text = str(text).lower()
    text = normalize_arabic_text(text)
    text = convert_eastern_to_western_numerals(text)
    text = remove_all_punctuations(text) # MUST BE HERE
    text = remove_extra_spaces(text)

    return text
