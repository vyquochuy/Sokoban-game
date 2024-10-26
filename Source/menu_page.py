import tkinter as tk
import Map
from PIL import Image, ImageTk
import pygame

ALGORITHMS = ["BFS", "DFS", "USC", "A*"]
MAPS = [f"Map {i}" for i in range(1, 11)]  # 10 bản đồ

BUTTON_COLOR = "#D96D37"
TITLE_SIZE = 36
BUTTON_SIZE = 14


class MenuPage(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Ares’s adventure",
                         font=("Helvetica", TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.25, anchor="center")

        self.start_button = tk.Button(self,
                                      text="Bắt đầu với " +
                                      self.controller.algorithm,
                                      font=("Helvetica", BUTTON_SIZE),
                                      bg=BUTTON_COLOR,
                                      fg="white",
                                      command=self.go_to_map_selection,
                                      height=2,
                                      width=15)
        self.start_button.place(relx=0.5, rely=0.4, anchor="center")

        button1 = tk.Button(
            self,
            text="Chọn thuật toán",
            font=("Helvetica", BUTTON_SIZE),
            bg=BUTTON_COLOR,
            fg="white",
            command=lambda: controller.show_frame("ChooseAlgorithm"),
            height=2,
            width=15)
        button1.place(relx=0.5, rely=0.5, anchor="center")

        # Button thoát
        button2 = tk.Button(self,
                            text="Thoát",
                            font=("Helvetica", BUTTON_SIZE),
                            bg=BUTTON_COLOR,
                            fg="white",
                            command=self.controller.quit,
                            height=2,
                            width=15)
        button2.place(relx=0.5, rely=0.6, anchor="center")

    def go_to_map_selection(self):
        self.controller.show_frame(
            "MapSelection")  # Chuyển đến trang chọn bản đồ

    def update_start_button(self):
        self.start_button.config(text="Bắt đầu với " +
                                 self.controller.algorithm)


class ChooseAlgorithm(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Chọn thuật toán",
                         font=("Helvetica", TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.2, anchor="center")

        for idx, algo in enumerate(ALGORITHMS):
            button = tk.Button(self,
                               text=algo,
                               font=("Helvetica", BUTTON_SIZE),
                               bg=BUTTON_COLOR,
                               fg="white",
                               command=lambda a=algo: self.choose_algorithm(a),
                               height=2,
                               width=15)
            button.place(relx=0.5, rely=0.35 + idx * 0.1, anchor="center")

        button_back = tk.Button(
            self,
            text="Quay lại Menu",
            command=lambda: controller.show_frame("MenuPage"),
            height=2,
            width=15)
        button_back.place(relx=0.5,
                          rely=0.35 + len(ALGORITHMS) * 0.1,
                          anchor="center")

    def choose_algorithm(self, algo):
        self.controller.algorithm = algo
        print(f"Thuật toán đã chọn: {algo}")

        # Cập nhật nút bắt đầu trong MenuPage
        self.controller.frames["MenuPage"].update_start_button()

        self.controller.show_frame("MenuPage")


class MapSelection(tk.Frame):

    def __init__(self, parent, controller, bg_image):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_label = tk.Label(self, image=bg_image)
        background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self,
                         text="Chọn bản đồ",
                         font=("Helvetica", TITLE_SIZE),
                         bg=BUTTON_COLOR,
                         fg="white")
        label.place(relx=0.5, rely=0.15, anchor="center")

        for idx, map_name in enumerate(MAPS):
            col = idx % 2  # Cột (0 hoặc 1)
            row = idx // 2  # Hàng (tính toán từ chỉ số)
            button = tk.Button(self,
                               text=map_name,
                               font=("Helvetica", BUTTON_SIZE),
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
            text="Quay lại Menu",
            command=lambda: controller.show_frame("MenuPage"),
            height=2,
            width=15)
        button_back.grid(row=(len(MAPS) // 2) + 1,
                         column=0,
                         columnspan=2,
                         pady=20)  # Đặt nút quay lại ở dưới cùng

    def choose_map(self, map_name):
        self.controller.map_name = map_name
        print(f"Bản đồ đã chọn: {map_name}")

        # code tiếp ở đây :))))))))))

        map_number = int(map_name.split()[-1])
        if map_number != 10:
            filepath = f"input/input-0{map_number}.txt"
        else:
            filepath = f"input/input-{map_number}.txt"

        map = Map.run_game(filepath)


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1280x720")
        self.title("Ares’s adventure")
        self.title_font = ("Helvetica", 18)

        self.algorithm = ALGORITHMS[0]
        self.map_name = None

        bg_image = Image.open("img/Menu background.png")
        bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(
            "sound/menu_sound.mp3")  # Replace with your music file path
        pygame.mixer.music.play(-1)  # Play the music in a loop

        # Tạo container cho các trang
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Định cấu hình lưới của container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Khởi tạo các trang
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


def RunTest():
    app = App()
    app.mainloop()


RunTest()
