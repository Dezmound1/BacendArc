import flet as ft
from templates.buttons import MainButton
import requests
import os
from requests import Session

class AddQuizPage:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.cookie = cookie

        self.quiz_title_field = ft.TextField(label="Quiz Title")
        self.questions_list = ft.ListView(height=200, spacing=10)
        self.add_question_button = MainButton(text="Добавить вопрос", on_click=self.add_question)
        self.create_quiz_button = MainButton(text="Создать тест", on_click=self.create_quiz)
        self.back_button = MainButton(text="назад", on_click=self.back)

        self.result_text = ft.Text()

        column = ft.Column(
            [
                ft.Row(
                    [
                        self.quiz_title_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.questions_list,
                ft.Row(
                    [
                        self.add_question_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.create_quiz_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.result_text,
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

        self.page.add(column)
        self.add_question()

    def add_question(self, e=None):
        question_text_field = ft.TextField(label="Question Text")
        right_answer_field = ft.TextField(label="Right Answer")
        question_form = ft.Column(
            [
                question_text_field,
                right_answer_field,
            ],
            spacing=5,
        )
        self.questions_list.controls.append(question_form)
        self.page.update()

    def create_quiz(self, e):
        quiz_title = self.quiz_title_field.value
        questions = []
        for question_form in self.questions_list.controls:
            question_text = question_form.controls[0].value
            right_answer = question_form.controls[1].value
            questions.append({"text": question_text, "right_answer": right_answer})

        quiz_data = {
            "quiz": {"title": quiz_title},
            "question": questions
        }

        s = Session()
        api_url = os.getenv("API_URL", "http://localhost:5000")
        try:
            response = s.post(f"{api_url}/question/add_quiz", json=quiz_data, cookies=self.cookie)

            if response.status_code == 200:
                self.result_text.value = "Тест успешно создан!"
            else:
                self.result_text.value = f"Error creating quiz: {response.status_code} - {response.text}"
        except Exception as ex:
            self.result_text.value = f"Exception: {str(ex)}"
        self.page.update()

    def back(self, e):
        from pages.menu import Menu
        self.master.new_win(Menu, self.cookie)
