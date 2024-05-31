import flet as ft
from templates.buttons import MainButton
import requests
import os
from requests import Session
import matplotlib.pyplot as plt

class ResultPage:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.cookie = cookie

        self.quiz_id_field = ft.TextField(label="Quiz ID")
        self.student_id_field = ft.TextField(label="Student ID")
        self.result_text = ft.Text()

        self.fetch_button = MainButton(text="Просмотреть", on_click=self.fetch_percentage)
        self.back_button = MainButton(text="Назад", on_click=self.back)

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
                        self.student_id_field,
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.add(column)


    def fetch_percentage(self, e):
        quiz_id = int(self.quiz_id_field.value)
        student_id = int(self.student_id_field.value)
        s = Session()
        api_url = os.getenv("API_URL", "http://localhost:5000")
        try:
            response = s.get(
                f"{api_url}/answer/get_correct_answers_percentage?quiz_id={quiz_id}&student_id={student_id}", cookies=self.cookie
            )

            if response.status_code == 200:
                percentage = response.json()
                self.result_text.value = f"Percentage of correct answers: {percentage}%"
                self.create_chart(percentage)
            else:
                self.result_text.value = f"Error fetching data: {response.status_code}"
        except Exception as ex:
            self.result_text.value = f"Коннекта нет, сервис не доступен"
        self.page.update()
    
    def create_chart(self, percentage):
        labels = ['Correct Answers', 'Incorrect Answers']
        sizes = [percentage, 100 - percentage]
        colors = ['#4CAF50', '#FF5252']
        explode = (0.1, 0)

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title("Percentage of Correct Answers")
        plt.show()
    
    def back(self, e):
        from pages.menu import Menu
        self.master.new_win(Menu, self.cookie)
