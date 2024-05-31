import flet as ft
from templates.buttons import MainButton
import os
from requests import Session

class StudentsPage:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.cookie = cookie
        self.no_stud = False
        self.error = False  

        self.group_id_field = ft.TextField(label="Group ID")
        self.fetch_button = MainButton(text="Показать студентов", on_click=self.fetch_students)
        self.back_button = MainButton(text="Назад", on_click=self.back)
        self.no_students_text = ft.Text("В группе нет студентов", size=25)  
        self.result_text = ft.Text(size=20) 

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
                        self.group_id_field,
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
                self.result_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.add(column)

    def fetch_students(self, e):
        group_id = int(self.group_id_field.value)
        s = Session()
        api_url = os.getenv("API_URL", "http://localhost:5000")
        try:
            response = s.get(f"{api_url}/group/get_stud_by_group?group_id={group_id}", cookies=self.cookie)

            if response.status_code == 200:
                students = response.json()
                self.display_students(students)
            else:
                self.result_text.value = f"Error fetching data: {response.status_code}"
        except Exception as ex:
            self.result_text.value = f"Exception: {str(ex)}"
        self.page.update()

    def display_students(self, students):
        self.panel.controls.clear()
        if self.no_stud:  
            self.page.remove(self.no_students_text)
            self.no_stud = False

        if students:
            self.panel.controls = [
                ft.ExpansionPanel(
                    bgcolor=ft.colors.AMBER,
                    header=ft.ListTile(
                        title=ft.Text(f"Student ID: {student['id']}"),
                    ),
                    content=ft.ListTile(
                        title=ft.Text(f"Email: {student['email']}"),
                        subtitle=ft.Text(
                            f"Name: {student['first_name']} {student['last_name']}\nRole: {student['role']}"
                        ),
                    ),
                )
                for student in students
            ]
        else:
            if not self.no_stud:
                self.page.add(self.no_students_text)
                self.no_stud = True

        self.page.update()

    def back(self, e):
        from pages.menu import Menu
        self.master.new_win(Menu, self.cookie)

    def void(self, e):
        if not self.error:
            self.page.add(self.text)
            self.error = True
