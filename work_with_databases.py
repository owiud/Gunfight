import re
import sqlite3
from difflib import SequenceMatcher

try:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
except sqlite3.Error:
    print("Не удалось подключиться к базе данных.")

# is_logged_in - проверка авторизации пользователя. True - вход в аккаунт выполнен.
is_logged_in = False


class InsecurePasswordLength(Exception):
    pass


class NoNumbersInPassword(Exception):
    pass


class NoLettersInDifferentRegisters(Exception):
    pass


class NoSpecialSymbols(Exception):
    pass


class TooCommonPassword(Exception):
    pass


class IncorrectEmailFormat(Exception):
    pass


class PasswordsAreDifferent(Exception):
    pass


class Check:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # Требования к паролю Пользователя сформированы на основании на исследовании Hive Systems.
    # Ссылка на исследование Hive Systems: https://www.hivesystems.io/blog/are-your-passwords-in-the-green.

    # Список распространенных паролей сформирован на основании ежегодного отчёта NordPass.
    # Ссылка на отчёт NordPass: https://nordpass.com/most-common-passwords-list.
    def check_password(self):
        try:
            if len(self.password) < 12:
                raise InsecurePasswordLength
            if re.search("[0-9]", self.password) is None:
                raise NoNumbersInPassword
            if not any(symbol.islower() for symbol in self.password):
                raise NoLettersInDifferentRegisters
            if not any(letter.isupper() for letter in self.password):
                raise NoLettersInDifferentRegisters
            if re.search("[!@#$%^&*]", self.password) is None:
                raise NoSpecialSymbols

            max_similarity = 0.75
            with open("common-passwords.txt", encoding="utf-8") as source_file:
                password = self.password.lower()
                source_data = source_file.readlines()
                source_file.close()
                for common_password in source_data:
                    common_password = common_password.lower()
                    similarity = SequenceMatcher(
                        None, password, common_password
                    ).ratio()
                    if similarity > max_similarity:
                        raise TooCommonPassword
            return True

        except InsecurePasswordLength:
            return "Пароль должен содержать минимум 12 символов."

        except NoNumbersInPassword:
            return "Пароль должен содержать минимум 1 цифру."

        except NoLettersInDifferentRegisters:
            return "Пароль должен содержать буквы в разных регистрах."

        except NoSpecialSymbols:
            return "Пароль должен содержать минимум 1 символ из !@#$%^&*"

        except TooCommonPassword:
            return "Ваш пароль слишком распространён."

    # Корректный адрес электронной почты по следующему шаблону: имя_пользователя@имя_почтового_сервера.
    def check_email(self):
        try:
            regular_string = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            template = re.compile(regular_string)
            if re.fullmatch(template, self.email) is None:
                raise IncorrectEmailFormat()

            return True
        except IncorrectEmailFormat:
            return "Некорректный формат почты."

    # Проверка существования учётной записи осуществляется по адресу электронной почты. 
    def whether_user(self):
        is_email_correct = self.check_email()
        is_password_correct = self.check_password()
        try:
            if is_email_correct and is_password_correct:
                with con:
                    all_emails = cur.execute(
                        "SELECT email FROM users"
                    ).fetchall()
                    if (self.email,) in all_emails:
                        request = "SELECT password FROM users WHERE email = ?"
                        original_password = cur.execute(
                            request, (self.email,)
                        ).fetchall()
                        if original_password[0][0] == self.password:
                            return True
                        if original_password[0][0] != self.password:
                            raise PasswordsAreDifferent
                    else:
                        return False
            else:
                if is_email_correct and isinstance(is_password_correct, str):
                    return is_password_correct
                if isinstance(is_email_correct, str) and is_password_correct:
                    return is_email_correct
                if isinstance(is_email_correct, str) and isinstance(
                        is_password_correct, str
                ):
                    return is_email_correct

        except PasswordsAreDifferent:
            return "Пароли не совпадают."


class User:
    # Таблица в базе данных содержит следующие колонки: email, password.
    def create_account_or_login(self):
        global is_logged_in
        email = input()
        password = input()
        check_result = Check(email, password).whether_user()
        if check_result:
            pass
        elif isinstance(check_result, str):
            pass
        elif not check_result:
            with con:
                sql = "INSERT INTO users (email, password) values(?, ?)"
                data = [(email, password)]
                con.executemany(sql, data)
            is_logged_in = True
        return is_logged_in

    def delete_account(self):
        email = input()
        password = input()
        check_result = Check(email, password).whether_user()
        if check_result:
            with con:
                request = "DELETE from users where email = ?"
                cur.execute(request, (email,))
        elif type(check_result) is str:
            pass

    def update_profile_information(self):
        email = input()
        password = input()
        new_email = input()
        new_password = input()
        if len(new_email) == 0:
            new_email = email
        elif len(new_password) == 0:
            new_password = password
        elif len(new_password) == 0 and len(new_email) == 0:
            new_email, new_password = email, password
        check_result_old_data = Check(email, password).whether_user()
        check_result_new_data = Check(email, password).whether_user()
        if check_result_old_data and check_result_new_data:
            with con:
                request = (
                    "UPDATE users SET email = ?, password = ? WHERE email = ?"
                )
                data = [(new_email, new_password, email)]
                con.executemany(request, data)
