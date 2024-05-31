import flet as ft
from flet import Container


class MainButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.ElevatedButton(
            content=ft.Column(
                [
                    ft.Text(
                        value=text,
                        size=20,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=50,
            width=260,
            on_click=on_click,
            bgcolor=ft.colors.with_opacity(1, "#FF544D"),
            style=ft.ButtonStyle(
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.with_opacity(1, "#FF544D")),
                },
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=20),
                },
            ),
        )


class CupertinoButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.CupertinoFilledButton(
            content=ft.Column(
                [
                    ft.Text(
                        value=text,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=60,
            width=300,
            opacity_on_click=0.3,
            on_click=on_click,
            
        )
