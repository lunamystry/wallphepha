import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty

import os


class PhephaListItem(BoxLayout, Label):
    filename = StringProperty()
    image_url = StringProperty()


class Wallpapers(Screen):
    data = ListProperty()

    def args_converter(self, row_index, item):
        result = {
            "filename": item['filename'],
            "image_url": item['image_url']
        }
        return result


class WallphephaApp(App):
    def build(self):
        self.wallpapers = Wallpapers(name="wallpapers")
        phepha_dir = "/home/leny/Images/wallpapers"

        def load_wallpapers(phepha_dir):
            phepha_list = []
            allowed_exts = ['.png', '.bmp', '.jpg', '.jpeg']
            for dir, dirs, files in os.walk(phepha_dir):
                for filename in files:
                    ext = os.path.splitext(filename)[1]
                    if ext in allowed_exts:
                        phepha_list.append(dict(filename=filename,
                                           image_url=os.path.join(dir,
                                                                  filename)))
            return phepha_list
        self.wallpapers.data = load_wallpapers(phepha_dir)

        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.wallpapers)
        return root


if __name__ == "__main__":
    WallphephaApp().run()
