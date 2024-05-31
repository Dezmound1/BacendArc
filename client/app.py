import flet as ft
from pages.main import Main


class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_resizable = False
        self.page.window_height = 650
        self.page.window_width = 450
        self.views = None
        self.new_win(Main)

    def new_win(self, class_name_page, params=None):
        if self.views:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)
        else:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)


def main(page: ft.Page):
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
