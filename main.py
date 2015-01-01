import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.label import Label

import subprocess
import fileinput
import sys
import os
import re


class PhephaView(Screen):
    filename = StringProperty()
    image_url = StringProperty()


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

    def set_wallpaper(self, filepath):
        command = "feh --bg-scale " + filepath
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        homepath = os.path.expanduser("~")
        self.change_in_file(homepath+"/.xprofile", filepath)
        process.communicate()

    def change_in_file(self, filename, new_wallpaper):
        wallpaper_command = "feh --bg-scale "
        if os.path.isfile(filename):
            for line in fileinput.input(filename, inplace=True):
                if re.match(r''+wallpaper_command, line) is not None:
                    line = wallpaper_command + new_wallpaper + "\n"
                    sys.stdout.write(line)
                else:
                    sys.stdout.write(line)

    def view_phepha(self, filename):
        name = 'phepha{}'.format(filename)

        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = PhephaView(
            name=name,
            filename=filename,
            image_url=filename
            )

        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name

    def view_phepha_list(self):
        self.transition.direction = 'right'
        self.root.current = 'wallpapers'


if __name__ == "__main__":
    WallphephaApp().run()
