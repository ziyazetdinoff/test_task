import db
import script


if __name__ == "__main__":
    db.create_db()  # создание и заполнение БД
    script.form_answer()  # создание словаря с остановками для каждого ЖК и его конвертация в excel
