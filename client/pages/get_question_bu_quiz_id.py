import flet as ft
from templates.buttons import MainButton
import requests
import os
from requests import Session


class QuestionsPage:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.cookie = cookie
        self.error = False

        self.quiz_id_field = ft.TextField(label="Quiz ID")
        self.fetch_button = MainButton(text="Показать вопросы", on_click=self.fetch_questions)
        self.back_button = MainButton(text="Назад", on_click=self.back)
        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            controls=[],
        )

        column = ft.Column(
            [
                ft.Row(
                    [
                        self.quiz_id_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.fetch_button,
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
                self.panel,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.add(column)

    def fetch_questions(self, e):
        quiz_id = int(self.quiz_id_field.value)
        s = Session()
        api_url = os.getenv("API_URL", "http://localhost:5000")
        try:
            response = s.get(f"{api_url}/question/get_questions_by_quiz?quiz_id={quiz_id}", cookies=self.cookie)

            if response.status_code == 200:
                questions = response.json()
                self.display_questions(questions)
            else:
                self.result_text.value = f"Error fetching data: {response.status_code} - {response.text}"
        except Exception as ex:
            self.result_text.value = f"Коннекта нет, сервис не доступен"
        self.page.update()

    def display_questions(self, questions):
        self.panel.controls.clear()
        for question in questions:
            question_item = ft.ExpansionPanel(
                bgcolor=ft.colors.AMBER,
                header=ft.ListTile(
                    title=ft.Text(f"Question ID: {question['question_id']}"),
                ),
                content=ft.ListTile(
                    title=ft.Text(f"Text: {question['text']}"),
                    subtitle=ft.Text(f"Right Answer: {question['right_answer']}"),
                ),
            )
            self.panel.controls.append(question_item)
        self.page.update()
    
    def void(self, e):
        if self.error == False:
            self.page.add(ft.Text("Сервис недоступен", size=20))
            self.error = True
        else:
            pass

    def back(self, e):
        from pages.menu import Menu

        self.master.new_win(Menu, self.cookie)
