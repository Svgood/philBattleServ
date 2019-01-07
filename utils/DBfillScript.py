import mysql.connector
import os

if __name__ == '__main__':

    db = mysql.connector.connect(user="root", password="Svgood22",
                                 host="127.0.0.1", database="phibattle")

    cursor = db.cursor()
    i = 0
    category = 0
    total = []
    mas = []


    while(True):
        print("Type category: \n 0 - All \n 1 - Philosophy \n 2 - Ukrainian")
        category = input()
        if (category in ["1", "0", "2"]):
            category = int(category)
            break


    with open("filefile.csv") as file:
        for f in file:
            i += 1
            #print(f)
            mas.append(f.replace("\n", ""))
            if i % 5 == 0:
                print(mas)
                total.append(mas)
                mas = []

    for obj in total:
       cursor.execute(
           """INSERT INTO questions (text, ans1, ans2, ans3, ans4, category) VALUES ('{}', '{}', '{}', '{}', '{}', {});""".format(
               obj[0], obj[1], obj[2], obj[3], obj[4], 1))
    print("added succesfull")
    db.commit()
    db.close()