import flet as ft

from templates.buttons import MainButton, CupertinoButton

from pages.get_stud_by_group import StudentsPage
from pages.get_result_by_test import ResultPage
from pages.get_question_bu_quiz_id import QuestionsPage
from pages.post_test import AddQuizPage

class Menu:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.cookie = cookie
        self.error = False


        self.result_by_test = MainButton("Результаты теста", on_click=self.get_result_by_test)
        self.second_button = MainButton("Вопросы по тесту", on_click=self.get_questions_by_quiz_id)
        self.third_button = MainButton("Создать тест", on_click=self.post_question)
        self.thorth_button = MainButton("Студенты в группе", on_click=self.get_student_by_group)
        self.back_button = MainButton("Назад", on_click=self.back)

        self.main_column = ft.Column(
            [
                ft.Row(
                    [
                        self.result_by_test,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.second_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.third_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.thorth_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.back_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        page.add(self.main_column)

    def get_result_by_test(self, e):
        self.master.new_win(ResultPage, self.cookie)
    
    def get_questions_by_quiz_id(self, e):
        self.master.new_win(QuestionsPage, self.cookie)

    def post_question(self, e):
        self.master.new_win(AddQuizPage, self.cookie)
    
    def get_student_by_group(self, e):
        self.master.new_win(StudentsPage, self.cookie)

    def void(self, e):
        print("its ok!")

    def back(self, e):
        from pages.main import Main
        self.master.new_win(Main)

    def void(self, e):
        if self.error == False:
            self.page.add(ft.Text("Сервис недоступен", size=20))
            self.error = True
        else:
            pass