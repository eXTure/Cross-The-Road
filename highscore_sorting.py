#Algorithm for sorting scores

import sys, os, logging
import json

logging.basicConfig(level=logging.DEBUG,
                #filename='app.log',
                #filemode='w',
                format='%(levelname)s - %(message)s')

filename = 'commands.txt'

commands = {}
with open("highscore.txt", "r") as fh:
    for line in fh:
        if line == "Name|Score":
            continue

        #x = line.split(",")
        #x = line.strip()
        #logging.info(x)
        command = line.strip().split(',', 1) # description
        logging.info(commands) # + description
        #commands[command[0][0]] = command[0][1]
        #logging.info(commands)
#    momment = ""
#    for line in fh:
#        while not line == "\n":
#            momment += line
#            logging.info(momment)
#        else:
#            break

#print(json.dumps(commands, indent=2, sort_keys=True))

#text = ""

#with open("highscore.txt", "r") as reader:

#    text = reader.read()

#logging.info(text)

#text_dict = {}

#for i in text:
#    if i == String
#text_list1 = list(text)
#logging.info(text_dict)
#logging.info(text_list1)

#text_list2 = []

#mom_text = ""

#for ch in text_list1:
#    if not ch == "\n":
#        mom_text += ch
#    else:
#        text_list2.append(mom_text)
#        mom_text = ""

#text_list2.remove(text_list2[0])
#text_list2.remove(text_list2[0])
#logging.info(text_list2)

#text_list3 = []
#for chr in text_list2:
#    if not ch == ",":
#        logging.info(chr)
#        mom_text += chr
        #logging.info(mom_text)
#    else:
        #logging.info(mom_text)
#        text_list3.append(mom_text)
        #logging.info(mom_text, text_list3)
#        mom_text = ""

#logging.info(text_list3)
