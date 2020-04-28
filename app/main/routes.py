
from flask import render_template, redirect, flash, url_for, abort, jsonify, request
from app import Config
from datetime import datetime
import time
from functools import wraps
from app.main import main_bp as bp
from clsfr import logreg, vectorizer, vectorizerTfidf, svmTfidf, rfTfidf, NBTfidf, LogRegTfidf
from sklearn.linear_model import LogisticRegression
from tashaphyne.stemming import ArabicLightStemmer
import string
import app.ntxt as ntxt


@bp.context_processor
def injector():
    return {
        'now' : datetime.utcnow(),
        'site_name': Config.SITE_NAME
    }





@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def fun():
    return render_template("review.html")



def normalizeAlif(txt):
    alfs = "أ إ آ".split(" ")
    for alf in alfs:
        txt = txt.replace(alf, "ا")
    return txt.replace("ؤ", "و").replace("ى","ي")

def removeStopWords(txt):
    stop_words = """في من مع على الى""".split(' ')
    new_word = []
    for word in txt.split(' '):
        if word in stop_words:continue
        new_word.append(word)
    return ' '.join(new_word)

def removeRepeated(txt):
    return " ".join(set(txt.split()))

def stripNonArabic(txt):
    arabic_alpha = set(list(" ابتةثجحخدذرزسشصضطظعغفقكلمنهويآأؤإئى"))
    res = ''
    for t in txt:
        if t in arabic_alpha: res += t
    return res

def normalizeArabic(txt):
    tashkeels = "َ ً ُ ٌ ِ ٍ ْ ".split(' ')
    punctuation = set("/ × ؛ ،".split(' '))
    punctuation.add(string.punctuation)
    arabic_alpha = set(list(" ابتةثجحخدذرزسشصضطظعغفقكلمنهويآأؤإئى"))
    
    res = ''
    for t in txt:
        if t in tashkeels or t in punctuation or t not in arabic_alpha: continue 
        else: res += t
    
    res += ' ' + " ".join([ ArabicLightStemmer().light_stem(wd) for wd in res.split(" ") ])
    return   removeRepeated(removeStopWords(normalizeAlif(res)))

def makePred(txt):    
    normalized = normalizeArabic(txt)
    normalizedTfidf = ntxt.text_normalization(stripNonArabic(txt))
    results = {} 

    if not normalized: results['logreg']=-1
    
    if not normalizedTfidf: 
        results['logregtfid']=-1
        results['rf']=-1
        results['svm']=-1
        results['mnb']=-1
        results['total']=-1
        results['decision'] = 'NA'
        return results
    
    
    results['logreg'] = int(logreg.predict_proba(vectorizer.transform([normalized]))[0][1] * 100)
    results['mnb'] = int(NBTfidf.predict_proba(vectorizerTfidf.transform([normalizedTfidf]))[0][1] * 100)
    results['svm'] = int(svmTfidf.predict_proba(vectorizerTfidf.transform([normalizedTfidf]))[0][1] * 100)    
    results['rf'] = int(rfTfidf.predict_proba(vectorizerTfidf.transform([normalizedTfidf]))[0][1] * 100)    
    results['logregtfid'] = int(LogRegTfidf.predict_proba(vectorizerTfidf.transform([normalizedTfidf]))[0][1] * 100)    

    results['total'] = sum(results.values()) / len(results.values())
    results['decision'] = ( results['total'] >= 50 and results['total'] <= 60 ) * 'NET' or  ( results['total'] >= 60 ) * 'POS' or 'NEG'
    return results





@bp.route('/pred_api/', methods=['GET'])
def pred_api():
    """ makes a vote record in the database, flag indicates wheather up or down"""
    comment_body = request.args.get("txt") 
    if not comment_body:
         return jsonify({})
    return jsonify(makePred(comment_body))


@bp.route('/pred/', methods=['POST'])
def make_pred():
    """ makes a vote record in the database, flag indicates wheather up or down"""
    req_json = request.get_json()
    comment_body = req_json.get('content')
    return jsonify(makePred(comment_body))



