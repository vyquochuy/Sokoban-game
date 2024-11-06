import tkinter as tk
import Map
import solver
import pygame
from PIL import Image, ImageTk

pygame.init()
pygame.font.init()

# Constants
ALGORITHMS = ["BFS", "DFS", "UCS", "A*"]
MAPS = [f"Map {i}" for i in range(1, 11)]

BUTTON_COLOR = "#D96D37"
TITLE_SIZE = 36
BUTTON_SIZE = 14
GEOMETRY = "1280x720"
TITLE_FONT = "Impact"
BUTTON_FONT = "Helvetica"


class MenuPage(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Ares’s Adventure",
                         font=(TITLE_FONT, TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.25, anchor="center")

        self.start_button = tk.Button(self,
                                      text="Start with " +
                                      self.controller.algorithm,
                                      font=(BUTTON_FONT, BUTTON_SIZE),
                                      bg=BUTTON_COLOR,
                                      fg="white",
                                      command=self.go_to_map_selection,
                                      height=2,
                                      width=15)
        self.start_button.place(relx=0.5, rely=0.4, anchor="center")

        button1 = tk.Button(
            self,
            text="Choose Algorithm",
            font=(BUTTON_FONT, BUTTON_SIZE),
            bg=BUTTON_COLOR,
            fg="white",
            command=lambda: controller.show_frame("ChooseAlgorithm"),
            height=2,
            width=15)
        button1.place(relx=0.5, rely=0.5, anchor="center")

        # Exit button
        button2 = tk.Button(self,
                            text="Exit",
                            font=(BUTTON_FONT, BUTTON_SIZE),
                            bg=BUTTON_COLOR,
                            fg="white",
                            command=self.controller.quit,
                            height=2,
                            width=15)
        button2.place(relx=0.5, rely=0.6, anchor="center")

    def go_to_map_selection(self):
        self.controller.show_frame("MapSelection")

    def update_start_button(self):
        self.start_button.config(text="Start with " +
                                 self.controller.algorithm)


class ChooseAlgorithm(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Choose Algorithm",
                         font=(TITLE_FONT, TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.2, anchor="center")

        for idx, algo in enumerate(ALGORITHMS):
            button = tk.Button(self,
                               text=algo,
                               font=(BUTTON_FONT, BUTTON_SIZE),
                               bg=BUTTON_COLOR,
                               fg="white",
                               command=lambda a=algo: self.choose_algorithm(a),
                               height=2,
                               width=15)
            button.place(relx=0.5, rely=0.35 + idx * 0.1, anchor="center")

        button_back = tk.Button(
            self,
            text="Back to Menu",
            command=lambda: controller.show_frame("MenuPage"),
            font=(BUTTON_FONT, BUTTON_SIZE),
            height=2,
            width=15)
        button_back.place(relx=0.5,
                          rely=0.35 + len(ALGORITHMS) * 0.1,
                          anchor="center")

    def choose_algorithm(self, algo):
        self.controller.algorithm = algo
        print(f"Chosen algorithm: {algo}")

        # Update start button in MenuPage
        self.controller.frames["MenuPage"].update_start_button()
        self.controller.show_frame("MenuPage")


class MapSelection(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Select Map",
                         font=(TITLE_FONT, TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.15, anchor="center")

        for idx, map_name in enumerate(MAPS):
            col = idx % 2  # Column (0 or 1)
            row = idx // 2  # Row (calculated from index)
            button = tk.Button(self,
                               text=map_name,
                               font=(BUTTON_FONT, BUTTON_SIZE),
                               bg=BUTTON_COLOR,
                               fg="white",
                               command=lambda m=map_name: self.choose_map(m),
                               height=2,
                               width=15)
            button.grid(row=row + 1, column=col, padx=10, pady=10)
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

        button_back = tk.Button(
            self,
            text="Back to Menu",
            command=lambda: controller.show_frame("MenuPage"),
            font=(BUTTON_FONT, BUTTON_SIZE),
            height=2,
            width=15)
        button_back.grid(row=(len(MAPS) // 2) + 1,
                         column=0,
                         columnspan=2,
                         pady=20)  # Place back button at the bottom

    def choose_map(self, map_name):
        self.controller.map_name = map_name
        algo = self.controller.algorithm
        print(f"Chosen map: {map_name}")

        map_number = int(map_name.split()[-1])
        if map_number != 10:
            filepath = f"input/input-0{map_number}.txt"
            output_path = f"output/output-0{map_number}.txt"
        else:
            filepath = f"input/input-{map_number}.txt"
            output_path = f"output/output-{map_number}.txt"

        map = Map.init_game(filepath)
        map.draw_map()

        # solution, numberOfNode, run_time, memory_usage = Map.solve(algo, map)
        # run = map.run_game(solution)
        
        # if run:
        #     print(f"Solution found in {len(map.path)} steps")
        #     with open(output_path, "a") as f:
        #         f.write(f"Algorithm:{algo} \n")
        #         f.write(f"steps:{len(map.path)} Weight:{map.total_weight} ")
        #         f.write(
        #             f"Node:{numberOfNode} Time (ms):{run_time} Memory:{memory_usage} MB\n"
        #         )
        #         f.write(f"Path:{map.path} \n")


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(GEOMETRY)
        self.title("Ares’s Adventure")
        self.title_font = (BUTTON_FONT, 18)

        self.algorithm = ALGORITHMS[0]
        self.map_name = None

        bg_image = Image.open("img/Menu background.png")
        bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (MenuPage, ChooseAlgorithm, MapSelection):
            page_name = Page.__name__
            frame = Page(parent=container,
                         controller=self,
                         bg_image=self.bg_image)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


def run_game():
    app = App()
    app.mainloop()


run_game()
