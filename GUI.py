import os

from tkinter import filedialog, Frame, Tk


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


browse_dir = Tk()
browse_dir.withdraw()


def search_for_path():
    curr_dir = os.getcwd()
    path = filedialog.askdirectory(parent=browse_dir, initialdir=curr_dir, title="Select EarWax directory")
    print(f"The path for your directory is {path}")
    return path


browse_file = Tk()
browse_file.withdraw()


def search_for_file_path():
    list_of_sources = []
    curr_dir = os.getcwd()
    files = filedialog.askopenfilenames(parent=browse_file, initialdir=curr_dir, title='Select files')
    for file in files:
        print(f"You chose: {file}")
        list_of_sources.append(file)
    return list_of_sources
