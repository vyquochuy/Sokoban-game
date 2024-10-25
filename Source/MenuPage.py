import tkinter as tk

# Mảng các thuật toán và bản đồ
ALGORITHMS = ["BFS", "DFS", "USC", "A*"]
MAPS = [f"Map {i}" for i in range(1, 11)]  # 10 bản đồ

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Định cấu hình hàng và cột để căn giữa
        #self.grid_rowconfigure(0, weight=1)  # Căn giữa theo chiều dọc
        #self.grid_rowconfigure(3, weight=1)  # Tạo khoảng trống ở dưới cùng
        #self.grid_columnconfigure(0, weight=1)  # Căn giữa theo chiều ngang

        # Label
        label = tk.Label(self, text="Ares’s adventure", font=controller.title_font)
        label.grid(row=1, column=0, pady=100, padx=100, sticky="nsew")

        # Button chọn thuật toán
        button1 = tk.Button(self, text="Chọn thuật toán",
                            command=lambda: controller.show_frame("ChoosePage"), height=10, width=30)
        button1.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

        # Button chọn bản đồ
        button2 = tk.Button(self, text="Chọn bản đồ",
                            command=lambda: controller.show_frame("MapPage"), height=10, width=30)
        button2.grid(row=3, column=0, pady=5, padx=5, sticky="nsew")


class ChoosePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="Chọn thuật toán", font=("Helvetica", 20))
        label.grid(row=1, column=0, pady=20, sticky="nsew")

        # Tạo các nút cho mỗi thuật toán
        for idx, algo in enumerate(ALGORITHMS, start=2):
            button = tk.Button(self, text=algo, command=lambda a=algo: self.choose_algorithm(a))
            button.grid(row=idx, column=0, pady=5, padx=10, sticky="nsew")

        # Button quay lại menu
        button_back = tk.Button(self, text="Quay lại Menu",
                                command=lambda: controller.show_frame("MenuPage"))
        button_back.grid(row=len(ALGORITHMS) + 2, column=0, pady=10, sticky="nsew")

    def choose_algorithm(self, algo):
        # Lưu thuật toán được chọn
        self.controller.algorithm = algo
        print(f"Thuật toán đã chọn: {algo}")
        self.controller.show_frame("MenuPage")  # Quay lại menu


class MapPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(12, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="Chọn bản đồ", font=("Helvetica", 20))
        label.grid(row=1, column=0, pady=20, sticky="nsew")

        # Tạo các nút cho mỗi bản đồ
        for idx, map_name in enumerate(MAPS, start=2):
            button = tk.Button(self, text=map_name, command=lambda m=map_name: self.choose_map(m))
            button.grid(row=idx, column=0, pady=5, padx=10, sticky="nsew")

        # Button quay lại menu
        button_back = tk.Button(self, text="Quay lại Menu",
                                command=lambda: controller.show_frame("MenuPage"))
        button_back.grid(row=len(MAPS) + 2, column=0, pady=10, sticky="nsew")

    def choose_map(self, map_name):
        # Lưu bản đồ được chọn
        self.controller.map_name = map_name
        print(f"Bản đồ đã chọn: {map_name}")
        self.controller.show_frame("MenuPage")  # Quay lại menu


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x600")
        self.title("Ares’s adventure")
        self.title_font = ("Helvetica", 18)
        
        # Biến lưu thuật toán và bản đồ đã chọn
        self.algorithm = None
        self.map_name = None

        # Tạo container cho các trang
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Định cấu hình lưới của container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Khởi tạo các trang
        self.frames = {}
        for Page in (MenuPage, ChoosePage, MapPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")  # Hiển thị trang MenuPage đầu tiên

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Đưa frame lên trên


def RunTest():
    app = App()
    app.mainloop()
RunTest()
