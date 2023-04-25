import os

from tkinter import filedialog, Frame, Tk


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
    files = filedialog.askopenfilenames(filetypes=[("OGG files", "*.ogg")], parent=browse_file,
                                        initialdir=curr_dir, title='Select your OGG files')

    for file in files:
        print(f"You chose {file} as a source")
        list_of_sources.append(file)
    return list_of_sources
