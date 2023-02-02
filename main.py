from collections import defaultdict
import re
import datetime
import csv
from nltk.stem.snowball import RussianStemmer

def deletePunct(sentence):
        sentence=( re.sub(r'[№"-_/1234567890.:?!()%<>;,+#$&\s]', u' ', sentence))
        return sentence
def stopWords(sentence):
    sentence= [x for x in sentence.lower().split() if x not in stoplist]
    sentence=" ".join(sentence)
    return sentence
def Frequency(sentences):
    frequency=defaultdict(int)
    for sentence in sentences:
        for token in sentence.split():
                frequency[stemmer.stem(token)] += 1
    return frequency

def get_frequency_dict(name,name2):
    with open(name, 'r',encoding='cp1251') as feedback_csv:
        cur = csv.reader(feedback_csv, delimiter=';')
        for c in cur:
             feedback=c[0]
             feedback_class=c[1]
             if feedback_class=='эмоции' :
                 sentences_feedback_emotions.append((stopWords(deletePunct(feedback))))
             if feedback_class=='предложение':
                 sentences_feedback_statements.append((stopWords(deletePunct(feedback))))

    with open(name2, 'r',encoding='cp1251') as feedback_csv:
        cur = csv.reader(feedback_csv, delimiter=';')
        for c in cur:
             feedback=c[0]
             feedback_class=c[1]
             if feedback_class=='эмоции' :
                 sentences_feedback_emotions.append((stopWords(deletePunct(feedback))))
             if feedback_class=='предложение':
                 sentences_feedback_statements.append((stopWords(deletePunct(feedback))))

    frequency_emotions=Frequency(sentences_feedback_emotions)
    frequency_statements=Frequency(sentences_feedback_statements)

    return frequency_emotions,frequency_statements

def analyse_feedback(name,resultname):
    with open(name, 'r',encoding='cp1251') as feedback_csv:
        cur = csv.reader(feedback_csv, delimiter=';')
        with open(resultname, 'w',encoding='cp1251', newline='') as results_csv:
            writer = csv.DictWriter(results_csv, delimiter=';', fieldnames=['sentence','class','emotion_coef','statement_coef'])
            count_mistakes=0
            count_correct=0
            count_sentences_emotions=0
            count_sentences_statements=0
            count_sentences_none=0
            for c in cur:
                sentence=c[0]
                count_emotions=0
                count_statements=0
                emotion_coef=0
                statement_coef=0
                for token in sentence.split():
                    if frequency_emotions[stemmer.stem(token)]>frequency_statements[stemmer.stem(token)]:
                        count_emotions=count_emotions+1
                    elif frequency_emotions[stemmer.stem(token)]<frequency_statements[stemmer.stem(token)]:
                        count_statements=count_statements+1
                    # count_emotions=count_emotions+frequency_emotions[stemmer.stem(token)]
                    # count_statements=count_statements+frequency_statements[stemmer.stem(token)]
                if count_emotions==count_statements:
                    sentence_class='none'
                    count_sentences_none=count_sentences_none+1
                elif count_emotions>count_statements:
                    sentence_class='эмоции'
                    count_sentences_emotions=count_sentences_emotions+1
                else:
                    sentence_class='предложение'
                    count_sentences_statements=count_sentences_statements+1
                count_general=count_emotions+count_statements
                if count_general!=0:
                    emotion_coef=round(count_emotions/count_general,2)
                    statement_coef=round(count_statements/count_general,2)
                writer.writerow({ 'sentence':sentence,'class':sentence_class,'emotion_coef':emotion_coef,'statement_coef':statement_coef})
                if c[1]!=sentence_class:
                    count_mistakes=count_mistakes+1
                if c[1]==sentence_class:
                    count_correct=count_correct+1
        print('Ошибок:'+str(count_mistakes))
        print('Верно:'+str(count_correct))
        print('Эмоции:'+str(count_sentences_emotions))
        print('Предложения:'+str(count_sentences_statements))
        print('Среднее:'+str(count_sentences_none))

def get_token_frequency(frequency_emotions,frequency_statements):
    for token1 in frequency_emotions:
        for token2 in frequency_statements:
            if frequency_emotions[token1]>10 and frequency_statements[token2]>10 and token1==token2:
                frequency_emotions[token1]=0
                frequency_statements[token2]=0
    for token in frequency_emotions:
        if frequency_emotions[token]>10:
            print('Эмоции:'+token+' Count:'+str(frequency_emotions[token]))
    for token in frequency_statements:
        if frequency_statements[token]>10:
            print('Предложение:'+token+' Count:'+str(frequency_statements[token]))

stoplistfile = open('stoplist.txt', 'r',encoding='cp1251').read()
stoplist=set(stoplistfile.split())
sentences_feedback_emotions=[]
sentences_feedback_statements=[]
dictionary={}
stemmer=RussianStemmer(False)
start_time=datetime.datetime.now()

frequency_emotions,frequency_statements=get_frequency_dict('feedback.csv','feedback5.csv')
get_token_frequency(frequency_emotions,frequency_statements)

analyse_feedback('feedback5.csv','result(feedback5).csv')

print('Time elapsed:'+ str(datetime.datetime.now()-start_time))
