import tkinter
import tkinter.ttk
from tkinter.scrolledtext import ScrolledText


class FileHost(tkinter.LabelFrame):
    def __init__(self, parent, file, file_id, title, name):
        super().__init__(parent, text=title)
        self.file = file
        self.file_id = file_id
        self.name = name

        file_label = tkinter.Label(self, text=f"{file}")
        file_id_label = tkinter.Label(self, text=f"{file_id}")
        name_label = tkinter.Label(self, text=name)

        file_label.grid(row=1, column=0)
        file_id_label.grid(row=1, column=1, padx=50)
        name_label.grid(row=1, column=2, padx=50)


class FileBar(tkinter.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)

        explanation_file_label = tkinter.Label(self, text="File")
        explanation_file_id_label = tkinter.Label(self, text="ID")

        explanation_file_label.grid(row=1, column=0)
        explanation_file_id_label.grid(row=1, column=1, padx=50)


root = tkinter.Tk()
root.title("WaxOgg")


root.geometry("550x600")

custom_label = tkinter.Button(root, text="Custom sounds")
custom_label.pack()
extra_options_button = tkinter.Button(root, text="Options")
extra_options_button.pack()

file_bar = FileBar(root)
file_bar.pack(fill=tkinter.X)

text = ScrolledText(root, state='disable')
text.pack(fill='both', expand=True)

test_frame = tkinter.Frame(text, name="yes")


for number in range(50):
    host = FileHost(test_frame, file="C:/directory/directory/directory/directory/directory/directory/file", file_id=number, title=f"Test {number}", name="Test")
    host.pack(side="top", padx=4, pady=1, fill=tkinter.X)

text.window_create('1.0', window=test_frame)

changeDirectory = tkinter.Button(root, text="Change Earwax Directory")
changeDirectory.pack()

directory_path = "/directory/test"
directoryBox = tkinter.Label(root, text=directory_path)
directoryBox.pack()

addSound = tkinter.Button(root, text="Add sounds")
addSound.pack()


root.mainloop()
