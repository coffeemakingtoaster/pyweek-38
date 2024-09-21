from direct.showbase.DirectObject import DirectObject, messenger

from os.path import join

from constants.events import EVENT_NAMES

class MusicHandler(DirectObject):
    def __init__(self):
        super().__init__()
        self.normal_music = self.__load_music("normal")
        self.evil_music = self.__load_music("sneaky")
        self.accept(EVENT_NAMES.GOTO_MAIN_MENU, self.__start_normal)
        self.accept(EVENT_NAMES.SNEAKING, self.__toggle_sneak)
        self.normal_music.play()

    def __toggle_sneak(self, sneaking):
        if sneaking:
            self.__start_evil()
        else:
            self.__start_normal()

    def __load_music(self, name):
        background_music = base.loader.loadMusic(join("assets", "music", f"{name}.mp3"))
        background_music.setLoop(True)
        return background_music

    def __start_normal(self, _=None):
        self.evil_music.stop()
        self.normal_music.play()

    def __start_evil(self, _=None):
        self.normal_music.stop()
        self.evil_music.play()

