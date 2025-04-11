import tkinter as tk

from settings import settings


class StartMenu:
    def __init__(self, root: tk.Tk, game_start) -> None:
        self.root = root
        self.game_start = game_start
        self.build_root()

    def build_root(self):
        self.root.title("Tetris")
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=1)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root_width = int(screen_width * 3 / 4)
        self.root_height = int(screen_height * 3 / 4)
        self.root.geometry(f"{self.root_width}x{self.root_height}")

        self.show_start_menu()

    def show_start_menu(self) -> None:
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=1, column=1, sticky="nsew")
        self.buttons_frame.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.buttons_frame.grid_columnconfigure([0, 1, 2], weight=1)

        tk.Button(
            self.buttons_frame, text="Play", command=self.start, font=("Arial", 16)
        ).grid(row=0, column=1, sticky="ew")

        tetris_plus_options = ["Off", "On"]
        tetris_plus_frame = tk.Frame(self.buttons_frame)
        tetris_plus_frame.grid(row=1, column=1, sticky="ew")
        tetris_plus_frame.grid_columnconfigure([0, 1, 2], weight=1)
        tk.Label(tetris_plus_frame, text="Tetris Plus:", font=("Arial", 16)).grid(
            row=0,
            column=0,
        )
        tk.OptionMenu(
            tetris_plus_frame,
            tk.StringVar(tetris_plus_frame, tetris_plus_options[0]),
            # tk.StringVar(self.buttons_frame, "Tetris Plus"),
            *tetris_plus_options,
            command=lambda state: settings.set_tetris_plus(state),
        ).grid(row=0, column=1, sticky="nsew", columnspan=3)

        music_options = ["On", "Off"]
        music_frame = tk.Frame(self.buttons_frame)
        music_frame.grid(row=2, column=1, sticky="ew")
        music_frame.grid_columnconfigure([0, 1, 2], weight=1)
        tk.Label(music_frame, text="Music:", font=("Arial", 16)).grid(row=0, column=0)
        tk.OptionMenu(
            music_frame,
            tk.StringVar(music_frame, music_options[0]),
            *music_options,
            command=lambda state: settings.set_music(state),
        ).grid(row=0, column=1, columnspan=2, sticky="nsew")

        difficulty_options = ["EASY", "MEDIUM", "HARD"]
        difficulty_frame = tk.Frame(self.buttons_frame)
        difficulty_frame.grid(row=3, column=1, sticky="ew")
        difficulty_frame.grid_columnconfigure([0, 1, 2], weight=1)
        tk.Label(difficulty_frame, text="difficulty:", font=("Arial", 16)).grid(
            row=0, column=0
        )
        tk.OptionMenu(
            difficulty_frame,
            tk.StringVar(difficulty_frame, difficulty_options[0]),
            *difficulty_options,
            command=lambda state: settings.set_difficulty(state),
        ).grid(row=0, column=1, columnspan=2, sticky="nsew")

        tk.Button(
            self.buttons_frame, text="Exit", command=self.root.quit, font=("Arial", 16)
        ).grid(row=4, column=1, sticky="ew")

    def start(self):
        self.game_start()
        self.buttons_frame.destroy()
