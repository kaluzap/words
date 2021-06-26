import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QFont
import pandas as pd
from numpy import random
from gtts import gTTS 
import os

count_good = 0
count_total = 0
already_tested = False
active_word = ""
active_options = ""
found = False
text_to_speak = ""

df = pd.read_csv("data_verbs.py")
print(df.head())

def sound():
    global text_to_speak
    speech = gTTS(text_to_speak, lang = 'de', slow = False)
    speech.save("text.mp3")
    os.system("mplayer text.mp3")

    
def button_1():
    global active_word
    global active_options
    global count_good
    global already_tested
    global found
    if found:
        return
    if active_word['translation'] == active_options[0]:
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('red')
       create_string_result('red')
       create_string_count()
       label_tranlation.setText(f"({active_word['translation']})")
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True
   

def button_2():
    global active_word
    global active_options
    global count_good
    global already_tested
    global found
    if found:
        return
    if active_word['translation'] == active_options[1]:
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('blue')
       create_string_result('blue')
       create_string_count()
       label_tranlation.setText(f"({active_word['translation']})")
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True
    pass

def button_3():
    global active_word
    global active_options
    global count_good
    global already_tested
    global found
    if found:
        return
    if active_word['translation'] == active_options[2]:
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('green')
       create_string_result('green')
       create_string_count()
       label_tranlation.setText(f"({active_word['translation']})")
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True
    pass

def button_4():
    global active_word
    global active_options
    global count_good
    global already_tested
    global found
    if found:
        return
    if active_word['translation'] == active_options[3]:
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('orange')
       create_string_result('orange')
       create_string_count()
       label_tranlation.setText(f"({active_word['translation']})")
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True
    pass

def get_a_word() -> (dict, list):
    global count_total
    global text_to_speak
    global active_word
    global active_options
    global df
    
    try:
        df_sample = df.sample(4)
    except ValueError as err:
        print("No hay mas palabras!!!")
        return active_word, active_options
    
    print(df_sample.head())
    word = df_sample.iloc[0].to_dict()
    #df = df.drop(df_sample.index[0])
    #print(f"Quedan {df.shape[0]} palabras")
    count_total += 1
    lst_words = [df_sample.iloc[0]['translation'],
                 df_sample.iloc[1]['translation'],
                 df_sample.iloc[2]['translation'],
                 df_sample.iloc[3]['translation']]
    random.shuffle(lst_words)
    btn1.setText(lst_words[0])
    btn2.setText(lst_words[1])
    btn3.setText(lst_words[2])
    btn4.setText(lst_words[3])
    text_to_speak = word["infinitive"]
    print(word)
    print(lst_words)
    return word, lst_words


def create_string_word(color):
    global active_word
    label_word.setStyleSheet(f'color: {color}')
    label_word.setText(f"{active_word['infinitive']}")
    #label_tranlation.setText(f"({active_word['translation']})")


def create_string_result(color):
    global active_word
    global text_to_speak
    text = f"{active_word['infinitive']}, {active_word['participle_II']}"        
    label_result.setStyleSheet(f'color: {color}')
    label_result.setText(text)
    text_to_speak = text
    
    
def create_string_count():
    global count_total 
    global count_good
    frac = count_good/count_total
    text =f"({count_good}/{count_total}) = {count_good/count_total:.4f}"
    if frac > 0.9:
        text += "   :)"
    elif frac < 0.5:
        text += "   :'("
    else:
        text += "   :("
    label_count.setText(text)


def button_next(): 
    global count_total 
    global count_good
    global active_options
    global active_word
    global already_tested
    global found
    if not found:
        return
    active_word, active_options = get_a_word()
    label_status.setText("")
    create_string_word('black')
    label_result.setText("")
    print(f"active word: {active_word}")
    print(f"active_options: {active_options}")
    already_tested =  False
    label_tranlation.setText(f"()")
    found = False


def button_pd():
    global df
    df = pd.read_csv("data_verbs.py")
    print(df.head())
    print(df.tail())
    
    
app = QApplication(sys.argv) 

window = QWidget() 
window.resize(400,300) 
window.setWindowTitle("Verbs") 

layout = QGridLayout(window) 

label_status = QLabel(" ")
label_status.setAlignment(Qt.AlignCenter)
layout.addWidget(label_status,0,0)
fnt = QFont('Open Sans', 8, QFont.Bold)
label_status.setFont(fnt)
label_status.setStyleSheet('color: black')

label_word = QLabel("WORTE")
label_word.setAlignment(Qt.AlignCenter)
layout.addWidget(label_word,1,0)
fnt = QFont('Open Sans', 20, QFont.Bold)
label_word.setFont(fnt)
label_word.setStyleSheet('color: black')

label_tranlation = QLabel("()")
label_tranlation.setAlignment(Qt.AlignCenter)
layout.addWidget(label_tranlation,2,0)
fnt = QFont('Open Sans', 8, QFont.Bold)
label_tranlation.setFont(fnt)
label_tranlation.setStyleSheet('color: gray')

label_result = QLabel(" ")
label_result.setAlignment(Qt.AlignCenter)
layout.addWidget(label_result,3,0)
fnt = QFont('Open Sans', 12, QFont.Bold)
label_result.setFont(fnt)
label_result.setStyleSheet('color: black')

label_count = QLabel("count") 
label_count.setAlignment(Qt.AlignCenter) 
layout.addWidget(label_count,4,0) 
fnt = QFont('Open Sans', 8, QFont.Bold)
label_count.setFont(fnt)
label_count.setStyleSheet('color: black')


btn1 = QPushButton('1')
btn1.setStyleSheet('QPushButton {font-weight: bold; color: red;}')

btn2 = QPushButton('2')
btn2.setStyleSheet('QPushButton {font-weight: bold; color: blue;}')

btn3 = QPushButton('3')
btn3.setStyleSheet('QPushButton {font-weight: bold; color: green;}')

btn4 = QPushButton('4')
btn4.setStyleSheet('QPushButton {font-weight: bold; color: orange;}')

btn_next = QPushButton('->')
btn_next.setStyleSheet('QPushButton {font-weight: bold; color: black;}')

btn_sound = QPushButton('sound')
btn_sound.setStyleSheet('QPushButton {font-weight: bold; color: black;}')

btn_pd = QPushButton('data')
btn_pd.setStyleSheet('QPushButton {font-weight: bold; color: black;}')

horLayout = QHBoxLayout() 
horLayout.addStretch(1) 
horLayout.addWidget(btn1)
horLayout.addWidget(btn2)
horLayout.addWidget(btn3)
horLayout.addWidget(btn4)
horLayout.addStretch(1) 
layout.addLayout(horLayout,5,0)
 
horLayout1 = QHBoxLayout() 
horLayout1.addStretch(1) 
horLayout1.addWidget(btn_pd)
horLayout1.addWidget(btn_sound)
horLayout1.addWidget(btn_next)
horLayout1.addStretch(1) 
layout.addLayout(horLayout1,6,0) 


btn1.clicked.connect(button_1)
btn2.clicked.connect(button_2) 
btn3.clicked.connect(button_3) 
btn4.clicked.connect(button_4)

btn_next.clicked.connect(button_next) 
btn_sound.clicked.connect(sound)
btn_pd.clicked.connect(button_pd)

active_word, active_options = get_a_word()
create_string_word('black')
create_string_count()

window.show() 
sys.exit(app.exec_()) 
