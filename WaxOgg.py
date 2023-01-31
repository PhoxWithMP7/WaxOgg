import time

from GUI import search_for_path, search_for_file_path
from actions import generate_manager

print("Welcome to WaxOgg, you'll be asked a couple stuff, just follow the instructions and you'll be fine\n")
time.sleep(3)

BASE_EARWAX_DIR = search_for_path()
if not BASE_EARWAX_DIR:
    print("WARNING: YOU GAVE NO EARWAX DIRECTORY PLEASE RESELECT\n")
    print("You will be asked again , dont fuck it up\n")
    time.sleep(2)
    BASE_EARWAX_DIR = search_for_path()

print("Please wait a couple of seconds\n")
time.sleep(3)

list_of_sources = search_for_file_path()
if not list_of_sources:
    print("WARNING: YOU GAVE NO SOURCES PLEASE RESELECT\n")
    print("You will be asked again , dont fuck it up\n")
    time.sleep(2)
    list_of_sources = search_for_file_path()

print("Pulling all sources and modifying everything necessary\n")
print("You might see a bunch of stuff getting printed\n")
time.sleep(4)

generate_manager(list_of_sources, BASE_EARWAX_DIR)
