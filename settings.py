from pygame import mixer

class Settings:

    def __init__(self):

        self.music_on = True
        mixer.init()
        self.play_music()


    def play_music(self):

        if(not self.music_on):
            return

        mixer.music.load("music/tetris_theme.mp3")
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)

    def stop_music(self):
        mixer.music.stop()
    
    def toggle_music(self):
        
        if mixer.music.get_busy():
            mixer.music.pause()
            self.music_on = False
        else:
            mixer.music.unpause()
            self.music_on = True