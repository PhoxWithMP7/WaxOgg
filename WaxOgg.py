from GUI import search_for_path, search_for_file_path
from actions import generate_manager


BASE_EARWAX_DIR = search_for_path()
list_of_sources = search_for_file_path()

generate_manager(list_of_sources, BASE_EARWAX_DIR)
