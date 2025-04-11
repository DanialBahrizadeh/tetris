from pygame import mixer


class Settings:
    def __init__(self):
        self.music_on = True

        self.difficulty = "EASY"

        self.tetris_plus = False
        self.tetris_mode = "NORMAL"
        mixer.init()
        self.play_music()

    def play_music(self):
        if not self.music_on:
            return

        mixer.music.load("assets/music/tetris_theme.mp3")
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

    def toggle_tetris_plus(self):
        self.tetris_plus = not self.tetris_plus

    def set_tetris_plus(self, state) -> None:
        if state == "On":
            self.tetris_plus = True
        else:
            self.tetris_plus = False

    def set_music(self, state) -> None:
        if state == "On":
            self.play_music()
        else:
            self.stop_music()

    def set_difficulty(self, state):
        settings.difficulty = state


settings = Settings()
