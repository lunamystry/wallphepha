import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.uix.button import Button

import subprocess
import fileinput
import sys
import os
import re


class EditableLabel(BoxLayout, Label):
    field = ObjectProperty()

    def __init__(self, **kwargs):
        super(EditableLabel, self).__init__(**kwargs)
        self.show(None)

    def edit(self, label):
        if label is not None:
            self.remove_widget(self.field)
        self.field = TextInput(text=self.text,
                               on_text_validate=self.show,
                               focus=True,
                               multiline=False)
        self.field.bind(focus=self.on_focus)
        self.add_widget(self.field)

    def on_focus(self, instance, value):
        if not value:
            self.show(instance)

    def show(self, textinput):
        if textinput is not None:
            self.remove_widget(self.field)
            self.text = textinput.text
        self.field = Button(text=self.text,
                            background_color=[1, 0, 0, 0],
                            on_press=self.edit)
        self.add_widget(self.field)


class PhephaView(Screen):
    filename = StringProperty()
    image_url = StringProperty()


class PhephaListItem(BoxLayout, ListItemButton):
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
    phepha_dir = StringProperty()

    def build(self):
        self.wallpapers = Wallpapers(name="wallpapers")
        self.phepha_dir = "/home/leny/Images/wallpapers"

        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.wallpapers)
        return root

    def load_wallpapers(self, phepha_dir):
        phepha_list = []
        allowed_exts = ['.png', '.bmp', '.jpg', '.jpeg']
        for dir, dirs, files in os.walk(phepha_dir):
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in allowed_exts:
                    phepha_list.append(dict(filename=filename,
                                       image_url=os.path.join(dir,
                                                              filename)))
        self.wallpapers.data = phepha_list

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

    def rename(self, old_path, new_path):
        if os.path.isfile(old_path):
            os.rename(old_path, new_path)
            self.load_wallpapers(self.phepha_dir)


if __name__ == "__main__":
    WallphephaApp().run()
