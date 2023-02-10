import os

from tkinter import filedialog, Frame, Tk, Button, Label


class MainWindow:
    def __init__(self, master=None):
        self.master = master
        master.title("WaxOgg")

        # self.frame = Frame(master,)
        self.directory_btn = Button(master, text="Select EarWax directory", command=MainWindow.search_for_path(self))
        self.directory_label = Label(master, text=f"{self.directory_btn}")

    browse_dir = Tk()
    browse_dir.withdraw()


    def search_for_path(self):
        curr_dir = os.getcwd()
        path = filedialog.askdirectory(parent=MainWindow.browse_dir, initialdir=curr_dir, title="Select EarWax directory")
        print(f"The path for your directory is {path}")
        return path


    browse_file = Tk()
    browse_file.withdraw()

    def search_for_file_path(self):
        list_of_sources = []
        curr_dir = os.getcwd()
        files = filedialog.askopenfilenames(filetypes=[("OGG files", "*.ogg")], parent=MainWindow.browse_file,
                                            initialdir=curr_dir, title='Select your OGG files')

        for file in files:
            print(f"You chose {file} as a source")
            list_of_sources.append(file)
        return list_of_sources
