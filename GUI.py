import tkinter as tk

def say_hello():
    label.config(text="Hello, World!")

def home():
    label.config(text="Welcome to my GUI")
    lb = tk.Listbox(root)
    lb.insert(1, "BFS")
    lb.insert(2, "DFS")
    lb.insert(3, "UCS")
    lb.insert(4, "Astar")
    lb.place(x=100, y=100)
    lb.pack()

# Create the main window
root = tk.Tk()
root.title("My First GUI")

# Create a label widget
label = tk.Label(root, text="Welcome to my GUI", font=("Helvetica", 16))
label.pack(pady=20)

# Create a button widget
button = tk.Button(root, text="Start", command=home, font=("Helvetica", 14))
button.pack(pady=10)

# button end
button_end = tk.Button(root, text="End", command=root.quit, font=("Helvetica", 14))
button_end.pack(pady=10)

# Start the main event loop
root.mainloop()
