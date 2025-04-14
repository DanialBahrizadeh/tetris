import tkinter as tk
import random
from time import time

# from tetris_picecs import IShapePiece
from start_menu import StartMenu
import tetris_picecs
from settings import settings


# the Game main class
class Game:
    GRID_SIZE = 16

    def __init__(self):
        self.root = tk.Tk()
        # self.root = root if root else tk.Tk()
        self.tetris_grid = []
        self.pieces_that_can_move = []
        self.score = 0
        self.spawn_time = 500
        self.level = 1
        # self.root.attributes('-fullscreen', True)
        # self.root.mainloop()
        # self.settings = Settings()

        # icon = tk.PhotoImage(file="assets/icons/icon.png")
        # self.root.iconphoto(True, icon)
        # self.root.iconbitmap("assets/icons/icon.ico")

        self.start_menu()

    def start_menu(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root_width = int(screen_width * 3 / 4)
        self.root_height = int(screen_height * 3 / 4)
        StartMenu(self.root, self.start)

    def start(self):
        # select_level_screen.grid_forget()
        # self.initial_level = level
        if settings.difficulty == "EASY":
            self.spawn_time = 1000
        elif settings.difficulty == "MEDIUM":
            self.spawn_time = 800
        else:
            self.spawn_time = 500

        self.initial_spawn_time = self.spawn_time

        self.build_gui()
        self.spawn()

    def build_gui(self):
        # self.root.attributes('-fullscreen', True)

        # the tetris frame
        tetris_frame = tk.Frame(
            self.root, width=self.root_height, height=self.root_height, bg="black"
        )
        tetris_frame.grid(row=0, column=1, rowspan=3)
        tetris_frame.grid_propagate(False)

        tetris_frame.rowconfigure(tuple(range(0, Game.GRID_SIZE)), weight=1)
        tetris_frame.columnconfigure(tuple(range(0, Game.GRID_SIZE)), weight=1)
        # index = 0
        for row in range(Game.GRID_SIZE):
            self.tetris_grid.append([])
            for col in range(Game.GRID_SIZE):
                squre = tk.Label(
                    tetris_frame, borderwidth=1, relief="solid", bg="#333", fg="white"
                )
                squre.grid(row=row, column=col, sticky="nswe")
                self.tetris_grid[row].append(squre)
                # index+=1
        # print(*self.tetris_grid, sep="\n************************************")
        # self.tetris_grid[5][7].config(bg="black")
        self.root.bind(
            "<Key>",
            lambda e: self.move(e.keysym) if e.keysym != "Up" else self.rotate(),
        )

        self.score_canvas = tk.Canvas(self.root)

        self.score_canvas.grid(row=0, column=0)

        self.score_canvas.bind("<Configure>", self.draw_responsive_diamond)

        self.level_canvas = tk.Canvas(self.root)

        self.level_canvas.grid(row=0, column=2)

        self.level_canvas.bind("<Configure>", self.draw_responsive_circle)

        buttons_frame = tk.Frame()
        buttons_frame.grid(row=2, column=2)

        tk.Button(
            buttons_frame,
            text="Mute/Play Music",
            command=settings.toggle_music,
            font=("Arial", 16),
        ).grid(row=1, column=0, sticky="ew")
        tk.Button(
            buttons_frame, text="Exit", command=self.root.quit, font=("Arial", 16)
        ).grid(row=2, column=0, sticky="ew")

        # tk.Checkbutton(
        #     self.root,
        #     text="Tetris Plus",
        #     variable=tk.BooleanVar(self.root, settings.tetris_plus),
        #     command=settings.toggle_tetris_plus,
        #     font=("Arial", 16),
        # ).grid(row=2, column=0)

        if settings.tetris_plus:
            self.tetris_mode_label = tk.Label(
                self.root, text=settings.tetris_mode, font=("Arial", 16)
            )
            self.tetris_mode_label.grid(row=2, column=0)
        self.screen_frame = tk.Frame(self.root, bg="#1D1616")
        self.screen_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.screen_frame.grid_rowconfigure((0, 1, 2), weight=1)

        game_over_frame = tk.Frame(self.screen_frame, bg="#1D1616")

        game_over_frame.grid_columnconfigure((0, 1, 2), weight=1)
        game_over_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        game_over_frame.grid(row=1, column=1)

        # self.screen_frame.grid(row=0,column=0,sticky="nsew", rowspan=3, columnspan=3)
        self.screen_frame.grid_forget()
        # self.game_over_frame.lift(self.score_canvas)
        # self.game_over_frame.grid_forget()
        tk.Label(
            game_over_frame,
            text="Game Over",
            fg="#D84040",
            bg="#EEEEEE",
            font=("Arial", 48),
            relief="solid",
        ).grid(row=0, column=0, columnspan=4, ipadx=20, ipady=20)
        tk.Label(game_over_frame, bg="#1D1616").grid(row=1, column=1)
        tk.Button(
            game_over_frame, text="Restart", bg="#EEEEEE", command=self.restart
        ).grid(row=2, column=0, columnspan=2, sticky="we")
        self.game_over_score_label = tk.Label(
            game_over_frame,
            text=f"Score: {self.score} Level: {self.level}",
            bg="#EEEEEE",
        )
        self.game_over_score_label.grid(row=2, column=3, sticky="we")

    def spawn(self, col=0):
        self.del_ghost_pieces()
        # if (settings.tetris_mode == "FLIP"): return
        if self.is_it_over():
            # self.game_over_frame.grid(row=1,column=1,sticky="n")
            self.screen_frame.grid(
                row=0, column=0, sticky="nsew", rowspan=3, columnspan=3
            )
            self.game_over_score_label.config(
                text=f"Score: {self.score} Level: {self.level}"
            )

            settings.stop_music()
            return

        if (
            settings.tetris_mode not in ["NORMAL", "DOUBLE_TROBLE"]
            and time() - self.event_timer >= 5
        ):
            self.back_to_normal()
        self.clear_full_rows()

        row = 0
        if settings.tetris_mode == "GRAVITY_SHIFT":
            row = 15
        if not col:
            col = random.choice(range(16))
        form = random.choice(range(4))
        piece = random.choice(
            [
                tetris_picecs.IShapePiece,
                tetris_picecs.JShapePiece,
                tetris_picecs.LShapePiece,
                tetris_picecs.OShapePiece,
                tetris_picecs.SShapePiece,
                tetris_picecs.ZShapePiece,
                tetris_picecs.TShapePiece,
            ]
        )(row, col, form)
        # piece = tetris_picecs.IShapePiece(0,col)
        # piece = tetris_picecs.TShapePiece(row,col)
        # piece = tetris_picecs.OShapePiece(0,col)

        # if(settings.tetris_mode != "DOUBLE_TROBLE"):
        if settings.tetris_mode != "FLIP":
            for point in piece.ghost_piece():
                self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

            for point in piece.position:
                self.tetris_grid[point[0]][point[1]].config(bg=piece.color, fg="black")
        else:
            for point in self.flip_one_piece(piece.ghost_piece()):
                self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

            for point in self.flip_one_piece(piece.position):
                # print(-point[1]-1,point[0], "\n")
                self.tetris_grid[point[0]][point[1]].config(bg=piece.color, fg="black")

        self.pieces_that_can_move.append(piece)
        self.after_id = self.root.after(self.spawn_time, self.move)
        self.last_spawned_col = col

    def move(self, dir="Down"):
        if settings.tetris_mode != "DOUBLE_TROBLE":
            self.pieces_that_can_move = [
                piece
                for piece in self.pieces_that_can_move
                if piece.can_it_move("Down")
            ]
        elif (
            len(
                [
                    piece
                    for piece in self.pieces_that_can_move
                    if piece.can_it_move("Down")
                ]
            )
            == 0
        ):
            self.pieces_that_can_move = []
            settings.tetris_mode = "NORMAL"
            self.tetris_mode_label.config(text="NORMAL")

        if len(self.pieces_that_can_move) == 0:
            if settings.tetris_mode == "DOUBLE_TROBLE":
                settings.tetris_mode = "NORMAL"
            self.spawn()
            #  self.double_troble()
            self.root.after_cancel(self.after_id)
            self.after_id = self.root.after(self.spawn_time, self.move)
            return

        those_i_want_to_move = [
            piece for piece in self.pieces_that_can_move if piece.can_it_move(dir)
        ]

        if settings.tetris_mode != "FLIP":
            for piece in those_i_want_to_move:
                # print(piece)
                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                # if(piece.ghost_piece()):
                for point in piece.ghost_piece():
                    self.tetris_grid[point[0]][point[1]].config(bg="#333")

                for point in piece.position:
                    self.tetris_grid[point[0]][point[1]].config(bg="#333", fg="white")

                piece.move(dir)

                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                # if(piece.ghost_piece()):
                for point in piece.ghost_piece():
                    self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

                for point in piece.position:
                    self.tetris_grid[point[0]][point[1]].config(
                        bg=piece.color, fg="black"
                    )
        else:
            for piece in those_i_want_to_move:
                for point in self.flip_one_piece(piece.ghost_piece()):
                    self.tetris_grid[point[0]][point[1]].config(bg="#333")

                for point in self.flip_one_piece(piece.position):
                    self.tetris_grid[point[0]][point[1]].config(bg="#333", fg="white")

                piece.move(dir)

                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                # if(piece.ghost_piece()):
                for point in self.flip_one_piece(piece.ghost_piece()):
                    self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

                for point in self.flip_one_piece(piece.position):
                    self.tetris_grid[point[0]][point[1]].config(
                        bg=piece.color, fg="black"
                    )
        # for point in piece.position:
        # self.tetris_grid[point[0]][point[1]].config(bg="black")
        if dir == "Down":
            self.score += 10
            self.score_canvas.itemconfig("score", text=self.score)
            self.root.after_cancel(self.after_id)
            self.check_and_inc_level()
            self.after_id = self.root.after(self.spawn_time, self.move)
        # if(settings.tetris_mode == "DOUBLE_TROBLE"):
        #     self.del_ghost_pieces()

    def rotate(self):
        self.pieces_that_can_move = [
            piece for piece in self.pieces_that_can_move if piece.can_it_move("Down")
        ]
        those_i_want_to_move = [
            piece for piece in self.pieces_that_can_move if piece.can_it_move(dir)
        ]

        if settings.tetris_mode != "FLIP":
            for piece in those_i_want_to_move:
                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                for point in piece.ghost_piece():
                    self.tetris_grid[point[0]][point[1]].config(bg="#333")

                for point in piece.position:
                    self.tetris_grid[point[0]][point[1]].config(bg="#333", fg="white")

                piece.rotate()

                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                for point in piece.ghost_piece():
                    self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

                for point in piece.position:
                    self.tetris_grid[point[0]][point[1]].config(
                        bg=piece.color, fg="black"
                    )
        else:
            for piece in those_i_want_to_move:
                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                for point in self.flip_one_piece(piece.ghost_piece()):
                    self.tetris_grid[point[0]][point[1]].config(bg="#333")

                for point in self.flip_one_piece(piece.position):
                    self.tetris_grid[point[0]][point[1]].config(bg="#333", fg="white")

                piece.rotate()

                # if(settings.tetris_mode != "DOUBLE_TROBLE"):
                for point in self.flip_one_piece(piece.ghost_piece()):
                    self.tetris_grid[point[0]][point[1]].config(bg="#cc99ff")

                for point in self.flip_one_piece(piece.position):
                    self.tetris_grid[point[0]][point[1]].config(
                        bg=piece.color, fg="black"
                    )

    def is_it_over(self):
        return tetris_picecs.TetrisPieceInterface.check_game_over()

    def del_ghost_pieces(self):
        ghost_squres = [
            self.tetris_grid[i][j]
            for i in range(16)
            for j in range(16)
            if self.tetris_grid[i][j].cget("bg") == "#cc99ff"
        ]

        for ghost_squre in ghost_squres:
            ghost_squre.config(bg="#333")

    def clear_full_rows(self):
        if not tetris_picecs.TetrisPieceInterface.is_any_row_clear():
            return

        mode = settings.tetris_mode

        if mode in ["FLIP", "GRAVITY_SHIFT", "PHANTOM_BLOCKS"]:
            self.back_to_normal()

        all_cleared_row_indexs = tetris_picecs.TetrisPieceInterface.clear_full_rows()

        self.score += (
            len(all_cleared_row_indexs) * 1000
            + (len(all_cleared_row_indexs) - 1) * 1000
        )
        self.score_canvas.itemconfig("score", text=self.score)
        for cleared_row_index in all_cleared_row_indexs:
            colors = [
                [self.tetris_grid[i][j].cget("bg") for j in range(16)]
                for i in range(16)
            ]
            #  for point in self.tetris_grid[cleared_row_index]:
            #   point.config(bg="#333")
            # print(colors)
            for row_index in range(1, cleared_row_index + 1):
                # for point in self.tetris_grid[row_index]:
                for col_index in range(16):
                    self.tetris_grid[row_index][col_index].config(
                        bg=colors[row_index - 1][col_index]
                    )
                    if getattr(
                        self.tetris_grid[row_index - 1][col_index], "old_color", None
                    ):
                        self.tetris_grid[row_index][col_index].old_color = getattr(
                            self.tetris_grid[row_index - 1][col_index],
                            "old_color",
                            None,
                        )
                        delattr(self.tetris_grid[row_index - 1][col_index], "old_color")
                    # print(colors[row_index-1][col_index])

        self.check_and_inc_level()
        if mode == "NORMAL" and settings.tetris_plus:
            # self.gravity_shift()
            # self.double_troble()
            # self.phantom_blocks()
            # self.flip_all_pieces()

            events = [
                self.gravity_shift,
                self.double_troble,
                self.phantom_blocks,
                self.flip_all_pieces,
            ]

            random.choice(events)()
            # print(settings.tetris_mode)
            self.tetris_mode_label.config(text=settings.tetris_mode)

    def restart(self):
        # self.game_over_frame.grid_forget()
        if settings.tetris_mode != "NORMAL":
            self.back_to_normal()

        self.screen_frame.grid_forget()

        self.score = 0
        self.score_canvas.itemconfig("score", text=self.score)

        for row in self.tetris_grid:
            for point in row:
                point.config(bg="#333")

        tetris_picecs.TetrisPieceInterface.all_taken_positions = [
            [0 for _ in range(16)] for _ in range(16)
        ]

        settings.play_music()

    def draw_responsive_diamond(self, _):
        self.score_canvas.delete(tk.ALL)

        width = self.score_canvas.winfo_width()
        height = self.score_canvas.winfo_height()

        cx, cy = width // 2, height // 2
        d = min(width, height) // 4

        diamonds_coordinates = [cx, cy + d, cx + d, cy, cx, cy - d, cx - d, cy]

        self.score_canvas.create_text(
            cx,
            cy - (1.25 * d),
            text="Score",
            font=("Arial", d // 2, "bold"),
            fill="black",
        )
        self.score_canvas.create_polygon(
            diamonds_coordinates, fill="yellow", outline="black", width=3
        )
        self.score_canvas.create_text(
            cx,
            cy,
            text=self.score,
            font=("Arial", d // 3, "bold"),
            fill="black",
            tags="score",
        )

    def draw_responsive_circle(self, _):
        self.level_canvas.delete(tk.ALL)

        width = self.level_canvas.winfo_width()
        height = self.level_canvas.winfo_height()

        cx, cy = width // 2, height // 2
        d = min(width, height) // 4

        self.level_canvas.create_text(
            cx,
            cy - (1.25 * d),
            text="Level",
            font=("Arial", d // 2, "bold"),
            fill="black",
        )

        self.level_canvas.create_oval(
            cx - d, cy - d, cx + d, cy + d, fill="purple", outline="black", width=3
        )

        self.level_canvas.create_text(
            cx,
            cy,
            text=str(self.level),
            font=("Arial", d // 3, "bold"),
            fill="black",
            tags="level",
        )

    def check_and_inc_level(self):
        self.level = self.score // 1000 + 1
        self.level_canvas.itemconfig("level", text=self.level)
        self.spawn_time = int(
            max(
                self.initial_spawn_time
                - (self.level - 1) * self.initial_spawn_time * 0.025,
                self.initial_spawn_time * 0.025,
            )
        )
        # self.spawn_time = 10000

    def back_to_normal(self):
        if settings.tetris_mode == "GRAVITY_SHIFT":
            # tetris_picecs.TetrisPieceInterface.back_to_normal()
            self.undo_gravity_shift()
        elif settings.tetris_mode == "PHANTOM_BLOCKS":
            self.undo_phantom_block()
        elif settings.tetris_mode == "FLIP":
            self.undo_flip()
        self.tetris_mode_label.config(text=settings.tetris_mode)
        # print("NORMAL")

    def gravity_shift(self):
        move_from_to = tetris_picecs.TetrisPieceInterface.gravity_shift()
        # print(move_from_to)

        for transition in move_from_to:
            # print(transition)
            self.tetris_grid[transition[1][0]][transition[1][1]].config(
                bg=self.tetris_grid[transition[0][0]][transition[0][1]].cget("bg")
            )
            self.tetris_grid[transition[0][0]][transition[0][1]].config(bg="#333")

        if tetris_picecs.TetrisPieceInterface.is_any_row_clear():
            self.clear_full_rows()
            self.gravity_shift()
        self.event_timer = time()

    def undo_gravity_shift(self):
        move_from_to = tetris_picecs.TetrisPieceInterface.undo_gravity_shift()
        # print(move_from_to)

        for transition in move_from_to:
            # print(transition)
            self.tetris_grid[transition[1][0]][transition[1][1]].config(
                bg=self.tetris_grid[transition[0][0]][transition[0][1]].cget("bg")
            )
            self.tetris_grid[transition[0][0]][transition[0][1]].config(bg="#333")
        # self.clear_full_rows()

    def double_troble(self):
        settings.tetris_mode = "DOUBLE_TROBLE"
        self.root.after(
            # self.spawn_time * 2,
            100,
            self.spawn,
            (self.last_spawned_col + 5) % 15,
        )

    def phantom_blocks(self):
        settings.tetris_mode = "PHANTOM_BLOCKS"
        collored_blocks = [
            self.tetris_grid[i][j]
            for i in range(16)
            for j in range(16)
            if self.tetris_grid[i][j].cget("bg") not in ["#333", "#cc99ff"]
        ]

        for block in collored_blocks:
            # block.config(old_color = block.cget("bg"))
            block.old_color = block.cget("bg")
            block.config(bg="#333")

        self.event_timer = time()

    def undo_phantom_block(self):
        settings.tetris_mode = "NORMAL"
        old_collored_blocks = [
            self.tetris_grid[i][j]
            for i in range(16)
            for j in range(16)
            if getattr(self.tetris_grid[i][j], "old_color", None)
        ]

        for block in old_collored_blocks:
            block.config(bg=getattr(block, "old_color", "#333"))
            block.old_color = None

    def flip_one_piece(self, piece_position):
        return [[col, -row - 1] for [row, col] in piece_position]

    def flip_all_pieces(self):
        settings.tetris_mode = "FLIP"
        colors = [
            [self.tetris_grid[i][j].cget("bg") for j in range(16)] for i in range(16)
        ]

        for row_index in range(16):
            for col_index in range(16):
                # print(col_index,row_index,"\n")
                self.tetris_grid[row_index][col_index].config(
                    bg=colors[-col_index - 1][row_index]
                )
        self.event_timer = time()

    def undo_flip(self):
        settings.tetris_mode = "NORMAL"
        colors = [
            [self.tetris_grid[i][j].cget("bg") for j in range(16)] for i in range(16)
        ]

        for row_index in range(16):
            for col_index in range(16):
                # print(col_index,row_index,"\n")
                self.tetris_grid[row_index][col_index].config(
                    bg=colors[col_index][-row_index - 1]
                )


if __name__ == "__main__":
    tetris = Game()
    # tetris.gui()
    # tetris.spawn()
    tetris.root.mainloop()
