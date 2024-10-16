# from ui_components import Stopwatch
import flet as ft
import time, datetime


class Stopwatch(ft.Column):
    def __init__(
        self,
        digits_size: float | None = 60,
        buttons_size: float | None = 40,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.digital_clock = ft.Text(
            str(datetime.timedelta(seconds=0)), size=digits_size
        )

        self.button_start = ft.IconButton(
            icon=ft.icons.START_SHARP, icon_size=buttons_size, on_click=self.start_watch
        )  # start button
        self.button_stop = ft.IconButton(
            icon=ft.icons.STOP_CIRCLE_SHARP,
            icon_size=buttons_size,
            on_click=self.stop_watch,
        )  # stop button
        self.button_reset = ft.ElevatedButton(
            text="0", on_click=self.reset_watch, color="#eeeef1", bgcolor="#43474e"
        )  # reset button

        self.controls = [
            self.digital_clock,
            ft.Row(
                [self.button_start, self.button_stop, self.button_reset],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.seconds_passed = 0
        self.running_clock_instances = 0
        self.is_clock_running = True

    def start_watch(self, e):
        if (
            self.running_clock_instances == 1
        ):  # indicates that function has been called before once
            return
        if self.is_clock_running == False:
            self.is_clock_running = True
        self.running_clock_instances += 1
        while self.is_clock_running:
            time.sleep(1)
            self.seconds_passed += 1
            self.digital_clock.value = str(
                datetime.timedelta(seconds=self.seconds_passed)
            )
            self.page.update()

    def stop_watch(self, e):
        self.is_clock_running = False
        self.running_clock_instances = 0
        self.page.update()

    def reset_watch(self, e):
        self.seconds_passed = 0
        self.digital_clock.value = str(datetime.timedelta(seconds=self.seconds_passed))
        self.page.update()

    def build(self):
        return self


def main(page: ft.Page):
    page.title = "Stopwatch"

    # theme
    page.theme_mode = "light"

    # window geometry
    page.window.height = 350
    page.window.width = 500
    page.window.resizable = False

    # alignments
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def change_page(e):
        selected_page = e.control.selected_index
        if selected_page == 0:  # main page is opened
            home_view.visible = True
            about_view.visible = False
        elif selected_page == 1:  # about page is opened
            home_view.visible = False
            about_view.visible = True

        page.update()

    def set_light_theme_mode():
        page.theme_mode = "light"

        # all other ui elements get auto-updated with the above statement
        # so, no need to bother about them
        home_view.button_reset.color = "#eeeef1"
        home_view.button_reset.bgcolor = "#43474e"

        # change button icon accordingly
        page.floating_action_button.icon = ft.icons.DARK_MODE_SHARP
        page.update()

    def set_dark_theme_mode():
        page.theme_mode = "dark"

        # comment is given in the above defined function
        home_view.button_reset.color = "#272a2c"
        home_view.button_reset.bgcolor = "#c3c7cf"

        # change button icon accordingly
        page.floating_action_button.icon = ft.icons.LIGHT_MODE_SHARP
        page.update()

    def change_theme_mode(e):
        if page.theme_mode == "light":
            set_dark_theme_mode()
        elif page.theme_mode == "dark":
            set_light_theme_mode()
        page.update()

    page.appbar = ft.AppBar(title=ft.Text("Stopwatch"))

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.icons.HOME_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HOME_SHARP),
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                label="About",
                icon=ft.icons.LIGHTBULB_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.LIGHTBULB_ROUNDED),
            ),
        ],
        selected_index=0,
        on_change=change_page,
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.DARK_MODE_SHARP, on_click=change_theme_mode
    )

    home_view = Stopwatch(digits_size=90)

    about_view = ft.Column(
        [
            ft.Text("Written by:", size=40),
            ft.Text("Muhammad Altaaf", size=30),
            ft.Container(content=ft.Divider(thickness=2), width=40),
            ft.OutlinedButton(
                icon=ft.icons.LINK_ROUNDED,
                text="Source code",
                on_click=lambda _: page.launch_url(
                    "https://github.com/taaaf11/Simple-Stopwatch"
                ),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=False,
    )
    page.add(home_view, about_view)


if __name__ == "__main__":
    ft.app(target=main)
