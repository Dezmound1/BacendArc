import flet as ft
from templates.buttons import MainButton
import requests

class AnnouncementsPage:
    def __init__(self, page: ft.Page, master, cookie: dict):
        self.master = master
        self.page = page
        self.no_announcements = False
        self.error = False
        self.cookie = cookie

        self.fetch_button = MainButton(text="Показать объявления", on_click=self.fetch_announcements)
        self.back_button = MainButton(text="Назад", on_click=self.back)
        self.no_announcements_text = ft.Text("Нет объявлений", size=25)
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

    def fetch_announcements(self, e):
        api_url = "http://localhost:8001"
        try:
            response = requests.get(f"{api_url}/announcements/")

            if response.status_code == 200:
                announcements = response.json()
                self.display_announcements(announcements)
            else:
                self.result_text.value = f"Error fetching data: {response.status_code}"
        except Exception as ex:
            self.result_text.value = f"Exception: {str(ex)}"
        self.page.update()

    def display_announcements(self, announcements):
        self.panel.controls.clear()
        if self.no_announcements:
            self.page.remove(self.no_announcements_text)
            self.no_announcements = False

        if announcements:
            self.panel.controls = [
                ft.ExpansionPanel(
                    bgcolor=ft.colors.AMBER,
                    header=ft.ListTile(
                        title=ft.Text(f"Title: {announcement['title']}"),
                    ),
                    content=ft.ListTile(
                        title=ft.Text(f"Content: {announcement['content']}"),
                    ),
                )
                for announcement in announcements
            ]
        else:
            if not self.no_announcements:
                self.page.add(self.no_announcements_text)
                self.no_announcements = True

        self.page.update()

    def back(self, e):
        from pages.menu import Menu
        self.master.new_win(Menu, self.cookie)

    def void(self, e):
        if not self.error:
            self.page.add(self.text)
            self.error = True