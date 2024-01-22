import sqlite3

try:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
except sqlite3.Error:
    print("Не удалось подключиться к базе данных.")


class WorkWithDataBases:
    def __init__(self, email: str = None, password: str = None) -> None:
        """
        Принимает и устанавливает адрес электронной почты и пароль.
        :param email: адрес электронной почты Пользователя
        :param password: пароль Пользователя
        """
        self.email = email
        self.password = password
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

    def create_new_account(self) -> None:
        """
        Добавляет пароль, результаты, количество игровых монет, показатель наличия пушки из магазина Пользователя в
        базу данных.
        """
        self.con.executemany("INSERT INTO Users (email, password, results, money, new_gun) values(?, ?, ?, ?, ?)",
                             [(self.email, self.password, "0 0", 0, 0)])
        self.con.commit()

    def get_all_information_about_user(self) -> tuple[str, str, int, int]:
        """
        :return: пароль, результаты, количество игровых монет, показатель наличия пушки из магазина Пользователя
        """
        return self.cur.execute("SELECT * FROM Users WHERE email = ?", (self.email,)).fetchall()[0][1:]

    def account_existence(self) -> bool:
        """
        :return: True / False - показатель существования аккаунта
        """
        return (self.email,) in self.cur.execute("SELECT email FROM Users").fetchall()

    def add_results_to_database(self, result: bool) -> None:
        """
        Записывает результаты в базу данных.
        В случае победы добавляет Пользователю 10 игровых монет.
        :param result: показатель выигрыша
        """
        results = WorkWithDataBases(self.email).get_all_information_about_user()[1].split()
        if result:
            self.con.executemany("UPDATE users SET results = ?, money = ? WHERE email = ?",
                                 [(f"{int(results[0]) + 1} {results[1]}",
                                   int(self.get_all_information_about_user()[2]) + 10, self.email)])
            self.con.commit()
        else:
            self.con.executemany("UPDATE users SET results = ? WHERE email = ?",
                                 [(f"{results[0]} {int(results[1]) + 1}", self.email)])
            self.con.commit()

    def cash_out(self) -> None:
        """
        Снимает 10 игровых монет за покупку пушки в магазине.
        """
        self.con.executemany("UPDATE users SET money = ?, new_gun = ? WHERE email = ?",
                             [(int(self.get_all_information_about_user()[2]) - 10, True, self.email)])
        self.con.commit()
