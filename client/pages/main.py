import flet as ft

import time
import requests
import os
from requests import Session

from pages.get_result_by_test import ResultPage
from pages.menu import Menu
from templates.buttons import MainButton


class Main:
    def __init__(self, page: ft.Page, master):
        self.master = master
        self.page = page
        self.error = False

        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.teacher_mail = ft.TextField(label="Put your mail")
        self.teacher_pass = ft.TextField(label="Put your password")
        self.main_button = MainButton("Login", on_click=self.on_click)
        self.result_text = ft.Text()

        self.api_url = os.getenv("API_URL", "http://localhost:5000")

        self.dlg = ft.AlertDialog(
            modal=True,
            content=ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
        )

        main_column = ft.Column(
            [
                ft.Row(
                    [
                        self.teacher_mail,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.teacher_pass,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        self.main_button,
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.add(main_column)

    def on_click(self, e):
        mail = str(self.teacher_mail.value)
        password = str(self.teacher_pass.value)
        sess = Session()
        try:
            response = sess.post("http://127.0.0.1:5000/auth/jwt/login", data={"username": mail, "password": password})
            print(response.cookies)
            cookie = {i.name: i.value for i in response.cookies}
            if response.status_code == 204:
                self.result_text.value = f"Percentage of correct answers: {response.status_code}"
                self.page.add(
                    ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
                )
                time.sleep(1.5)
                self.page.update()
                self.master.new_win(Menu, cookie)
            else:
                self.result_text.value = f"Error fetching data: {response.status_code}"
                self.page.update()
        except Exception as ex:
            self.result_text.value = f"Коннекта нет, сервис не доступен"
        self.page.update()

    def void(self, e):
        if self.error == False:
            self.page.add(ft.Text("Сервис недоступен", size=20))
            self.error = True
        else:
            pass