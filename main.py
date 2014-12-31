import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty

class PhephaListItem(BoxLayout, Label):
    directory = StringProperty()
    filename = StringProperty()


class Wallpapers(Screen):
    data = ListProperty()

    def args_converter(self, row_index, filename):
        result = {
            "filename": filename,
            "directory": self.directory
        }
        return result


class WallphephaApp(App):
    def build(self):
        self.wallpapers = Wallpapers(name="wallpapers")

        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.wallpapers)
        return root


if __name__ == "__main__":
    WallphephaApp().run()
