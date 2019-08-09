#Algorithm for sorting scores

import sys, os, logging

logging.basicConfig(level=logging.DEBUG,
                #filename='app.log',
                #filemode='w',
                format='%(levelname)s - %(message)s')

text = ""

with open("highscore.txt", "r") as reader:

    text = reader.read()

#logging.info(text)

text_list1 = list(text)

#logging.info(text_list1)

text_list2 = []

mom_text = ""

for ch in text_list1:
    if not ch == "\n":
        mom_text += ch
    else:
        text_list2.append(mom_text)
        mom_text = ""

text_list2.remove(text_list2[0])
text_list2.remove(text_list2[0])
logging.info(text_list2)

text_dict = {text_list2[0] : text_list2[1]}
logging.info(text_dict)
