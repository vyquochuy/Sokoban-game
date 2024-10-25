     # Tạo container cho các trang
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Định cấu hình lưới của container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)