#Algorithm for sorting scores

import sys, os, logging
import json

logging.basicConfig(level=logging.DEBUG,
                #filename='app.log',
                #filemode='w',
                format='%(levelname)s - %(message)s')


def main():

    text = ""
    text_list1 = []
    text_list2 = []
    text_list3 = []
    text_list4 = []
    mom_text = ""
    title_hold = ""
    write_text = ""
    text_dict = {}

    with open("highscore.txt", "r") as reader:

        text = reader.read()

    text_list1 = list(text)

    for ch in text_list1:
        if not ch == "\n":
            mom_text += ch
        else:
            text_list2.append(mom_text)
            mom_text = ""

    title_hold = text_list2.pop(0)

    for item in text_list2:
        mo_tuple = ()
        mo_tuple = item.split(",")
        mo_tuple[1] = int(mo_tuple[1])
        text_list3.append(mo_tuple)

    def Sort(sub_li):
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l-i-1):
                if (sub_li[j][1] > sub_li[j + 1][1]):
                    tempo = sub_li[j]
                    sub_li[j]= sub_li[j + 1]
                    sub_li[j + 1]= tempo
        return sub_li

    Sort(text_list3)

    text_list3 = list(reversed(text_list3))

    count_n = 0
    for line in text_list3:
        if count_n == 10:
            break
        else:
            text_list4.append(line)
            count_n += 1

    execution_path = os.getcwd()
    f = open('highscore_sorted.txt','w')
    for i in text_list4:
        for j in i:
            write_text = write_text + str(j) + " "
        write_text += "\n"

    write_text = title_hold + "\n" + write_text
    f.writelines(write_text)
    f.close()
    logging.info("List sorted successfully!")

if __name__ == "__main__":
    #Without name == main method, this file would run as soon as it is imported in the main file.
    main()
