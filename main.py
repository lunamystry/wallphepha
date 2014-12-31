import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class Wallpapers(Screen):
    pass


class WallphephaApp(App):
    def build(self):
        self.wallpapers = Wallpapers(name="wallpapers")

        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.wallpapers)
        return root


if __name__ == "__main__":
    WallphephaApp().run()
