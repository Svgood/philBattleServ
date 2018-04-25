import mysql.connector


if __name__ == '__main__':

    db = mysql.connector.connect(user="root", password="Svgood22",
                                 host="127.0.0.1", database="phibattle")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())


    exit(0)
    for line in f:
        i += 1

        if i % 2 == 0:
            line = line[:line.find("\n")]
            if "`" in line:
                line = line[:line.find("`")] + line[line.find("'") + 1:]
            mas.append(line)

            print(line)
            if len(mas) == 5:
                try:
                    cursor.execute(
                        """INSERT INTO questions (text, ans1, ans2, ans3, ans4) VALUES ('{}', '{}', '{}', '{}', '{}');""".format(
                            mas[0], mas[1], mas[2], mas[3], mas[4]))
                except:
                    pass
                mas = []
    f.close()
    db.commit()


    db.close()