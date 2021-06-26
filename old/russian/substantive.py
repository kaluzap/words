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
active_case = ""
found = False
text_to_speak = ""

df = pd.read_csv("words.csv")
print(df.head())

def sound():
    global text_to_speak
    text_to_speak = text_to_speak.replace('[ohne pl.]', '')
    text_to_speak = text_to_speak.replace('[ohne s.], ', '')
    speech = gTTS(text_to_speak, lang = 'ru', slow = False)
    speech.save("text.mp3")
    os.system("mplayer text.mp3")
    
def random_case() -> str:
    x = random.rand()
    if x < 0.75:
        return "s"
    return "p"


def get_a_word():#df_in : pd.DataFrame) -> dict:
    global count_total
    global text_to_speak
    global active_word
    global active_case
    global df
    
    try:
        df_sample = df.sample()
    except ValueError as err:
        print("No hay mas palabras!!!")
        return active_word, active_case
    
    word = df_sample.iloc[0].to_dict()
    #df = df.drop(df_sample.index)
    print(f"Quedan {df.shape[0]} palabras")
    count_total += 1
    
    case = random_case()
    if (word['plural'] == 'ohne') and (case == 'p'):
        case = 's'
    if (word['word'] == word['plural']):
        case = 's'
    if (word['word'] == 'ohne'):
        case = 'p'
    
    if case == 's':
        text_to_speak = word['word']
    else:
        text_to_speak = word['plural']
        
    return word, case


def create_string_word(color):
    global active_case
    global active_word
    if active_case == 's':
        text = active_word['word']
    else:
        text = active_word['plural']
    label_word.setStyleSheet(f'color: {color}')
    label_word.setText(text)
    label_tranlation.setText(f"({active_word['translation']})")


def create_string_result(color):
    global active_case
    global active_word
    global text_to_speak
    text = ""
    if active_word['word'] == '---':
        text += ''
    else:
        text += active_word['word'] + ", "
        
    if active_word['plural'] == '---':
        text += ''
    else:
        text += f"{active_word['plural']}"
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

    
def button_der(): 
    global count_good
    global active_case
    global active_word
    global already_tested
    global found
    if found:
        return
    if (active_case == 's') and (active_word['gender'] == 'm'):
       if not already_tested:
           count_good += 1
       label_status.setText("верно!! :)")
       create_string_word('red')
       create_string_result('red')
       create_string_count()
       found = True
    else:
       label_status.setText("неправильно!! :(")
       already_tested =  True


def button_die(): 
    global count_good
    global active_case
    global active_word
    global already_tested
    global found
    if found:
        return
    if (active_case == 's') and (active_word['gender'] == 'f'):
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('blue')
       create_string_result('blue')
       create_string_count()
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True


def button_das(): 
    global count_good
    global active_case
    global active_word
    global already_tested
    global found
    if found:
        return
    if (active_case == 's') and (active_word['gender'] == 'n'):
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('green')
       create_string_result('green')
       create_string_count()
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True


def button_diepl(): 
    global count_total 
    global count_good
    global active_case
    global active_word
    global already_tested
    global found
    if found:
        return
    if (active_case == 'p') or (active_word['word'] == active_word['plural']):
       if not already_tested:
           count_good += 1
       label_status.setText("richtig!!")
       create_string_word('orange')
       create_string_result('orange')
       create_string_count()
       found = True
    else:
       label_status.setText("falsch")
       already_tested =  True


def button_next(): 
    global count_total 
    global count_good
    global active_case
    global active_word
    global already_tested
    global found
    if not found:
        return
    active_word, active_case = get_a_word()
    label_status.setText("")
    create_string_word('black')
    label_result.setText("")
    print(f"active word: {active_word}")
    print(f"active_case: {active_case}")
    already_tested =  False
    found = False


def button_pd():
    global df
    global count_good
    global count_total
    df = pd.read_csv("words.csv")
    count_good = 0
    count_total = 1
    button_next()
    print(df.head())
    print(df.tail())
    
    
app = QApplication(sys.argv) 

window = QWidget() 
window.resize(400,300) 
window.setWindowTitle("der Artikel") 

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

label_tranlation = QLabel("(palabra)")
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

 
 
 

btn1 = QPushButton('мужской')
btn1.setStyleSheet('QPushButton {font-weight: bold; color: red;}')
#btn1.move(30, 200)

btn2 = QPushButton('женский')
btn2.setStyleSheet('QPushButton {font-weight: bold; color: blue;}')
#btn2.move(150, 200)

btn3 = QPushButton('средний')
btn3.setStyleSheet('QPushButton {font-weight: bold; color: green;}')
#btn3.move(270, 200)
        
btn4 = QPushButton('множественное')
btn4.setStyleSheet('QPushButton {font-weight: bold; color: orange;}')
#btn4.move(390, 200)

btn_next = QPushButton('->')
btn_next.setStyleSheet('QPushButton {font-weight: bold; color: black;}')
#btn_next.move(390, 200)

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


#button.clicked.connect(buttonClickedHandler)
btn1.clicked.connect(button_der)
btn2.clicked.connect(button_die) 
btn3.clicked.connect(button_das) 
btn4.clicked.connect(button_diepl)
btn_next.clicked.connect(button_next) 
btn_sound.clicked.connect(sound)
btn_pd.clicked.connect(button_pd)
        
active_word, active_case = get_a_word()#df)
create_string_word('black')
create_string_count()

window.show() 

sys.exit(app.exec_()) 
