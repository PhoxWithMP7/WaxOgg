import os
import random
import shutil
import re
import sys

from typing import List, Optional

# List of general Todos , this is mainly for different versions
# TODO: -V4: Modify with GUI sounds on a whim (delete, change ID, refresh sounds so no dupes)
#       -V3-4: Add a way to reset options with GUI incase something goes bad (deletion of new IDs , fresh audiojet file)
#       -V2: Add a Tkinter GUI
#       -V3: Optimize error handling to be more in tune with what the function does
#       -V3 : Exe package
#       -V2: Force copy audio jet file to correct format
#       -V2: Fix the ID mess and get a more comfortable approach

BASE_EARWAX_AUDIO_DIR = r"/content/EarwaxAudio/Audio/"
BASE_EARWAX_JET_FILE = r"/content/EarwaxAudio.jet"
BASE_EARWAX_SPECTRUM_DIR = r"/content/EarwaxAudio/Spectrum/"
TEMPLATE_SPECTRUM = r"/content/EarwaxAudio/Spectrum/Template.jet"


def generate_manager(list_of_sources: List[str], selected_dir: str) -> None:
    """
    Manager handling every action , sets an ID for each iteration and applies whatever is needed
    :param list_of_sources: A list of strings , filled with the paths linking to OGGs
    :param selected_dir: Selected Earwax directory
    :return: Nothing
    """

    earwax_dir = selected_dir
    new_forbidden_ids = []
    existing_forbidden_ids = read_forbidden_ids()

    create_new_spectrum_template(earwax_dir)

    # Calls governing the jet file , don't touch without having a perfectly working solution
    reformat_audio_jet(selected_dir)
    fix_line(selected_dir)

    for source in list_of_sources:
        # 20000 is used by existing IDs for the ogg files
        # 90000 and 80000 as well as 40000 are used by announcers and others
        # Random int might pose an issue if by chance they have overlapping IDs

        # source_id = find_if_id_exists(existing_forbidden_ids, new_forbidden_ids, temporary)
        # print(new_forbidden_ids)

        source_id = random.randint(50000, 80000)
        source_name = find_source_name(source)
        new_entry = create_new_entry_for_audio_jet(source_name, source_id)

        copy_ogg_to_earwax_audio(source, source_id, earwax_dir)
        create_spectrum_from_template(source_id, earwax_dir)

        write_to_audio_jet(new_entry, earwax_dir)
        print(f"Added new entry for {source} as {source_name} with {source_id} ID\n")

    # Fix the stuff we delete up there with the reformat
    reformat_audio_jet_fix(selected_dir)


def find_if_id_exists(existing_forbidden_ids: List[str], new_forbidden_ids: List[str], source_id: int) -> int:
    if str(source_id) in new_forbidden_ids or str(source_id) in existing_forbidden_ids:
        new_source_id = random.randint(50000, 80000)
        find_if_id_exists(existing_forbidden_ids, new_forbidden_ids, new_source_id)
    else:
        new_source_id = source_id
        new_forbidden_ids.append(str(new_source_id))
        write_to_forbidden_ids(str(new_source_id))
        print(new_source_id)
        return new_source_id


def find_source_name(source: str) -> str:
    """
    Function taking a file path then extracting its name for the newly made ogg
    :param source: The source path
    :return: A string that will be the name in the AudioJet file
    """

    pattern = r"(?:\/).*\/(.*)\.ogg"

    # This is awful, I'll have to figure out a better way to catch that error
    print(source)
    if source is None:
        sys.exit("The source is empty\n")
    try:
        source_name = re.search(pattern, source)
        return source_name.group(1)
    except Exception as error:
        print("You either gave no source or the file was not an OGG\n")
        print(f"Stack trace: {error} \n")


def copy_ogg_to_earwax_audio(source_ogg: str, audio_id: int, earwax_dir: str) -> None:
    """
    Copies the ogg to a new audio file with the created ID
    :param source_ogg: The OGG file we are trying to copy
    :param audio_id: Random id created by the manager
    :param earwax_dir: The base earwax directory
    :return: Nothing , creates a new OGG file instead
    """

    target = f"{earwax_dir}{BASE_EARWAX_AUDIO_DIR}{audio_id}.ogg"

    try:
        shutil.copy(source_ogg, target)
        print(f"Creating OGG file with {audio_id} as ID\n")
    except Exception as error:
        print("You either gave no source/directory or the file was not an OGG\n")
        print(f"Stack trace: {error} \n")


def find_template(earwax_dir) -> bool:
    """
    Finds a template inside the earwax directory , can be found anywhere
    :param earwax_dir: The base earwax directory
    :return: True
    """

    target = "Template.jet"
    for root, directories, files in os.walk(f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}"):
        if target in files:
            return True


def create_new_spectrum_template(earwax_dir: str) -> None:
    """
    Creates a new template if it does not exist
    :param earwax_dir: The base earwax directory
    :return: Nothing , creates a new spectrum template file from the longest existing spectrum
    """

    if not find_template(earwax_dir):
        original_template = f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}22740.jet"
        target = f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}Template.jet"
        try:
            shutil.copy(f"{original_template}", target)
            print("Created a new Template.jet")
        except Exception as error:
            print("You either gave no directory or the Template is corrupted/not present\n")
            print(f"Stack trace: {error} \n")
    else:
        print("Template was found\n")


def create_spectrum_from_template(audio_id: int, earwax_dir: str) -> None:
    """
    Create a spectrum file from an existing Template.jet
    :param audio_id: Random id created by the manager
    :param earwax_dir: The base earwax directory
    :return: Nothing, it creates a spectrum file
    """

    target = f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}{audio_id}.jet"
    try:
        shutil.copy(f"{earwax_dir}{TEMPLATE_SPECTRUM}", target)
    except Exception as error:
        print("You either gave no directory or the Template is corrupted/not present\n")
        print(f"Stack trace: {error} \n")


def create_new_entry_for_audio_jet(name: str, audio_id: int, category: Optional[str] = "cartoon") -> str:
    """
    Creates an entry out of a template with relevant fields
    :param name: Name extracted by the regex
    :param audio_id: Random id created by the manager
    :param category: Always cartoon , optional in the future
    :return: String template to be appended
    """

    # TODO: V3: Fix whatever this monstrosity is
    template = ", {" + f'\n\t\t"x": false,' \
                       f'\n\t\t"name": "{name}",' \
                       f'\n\t\t"short": "{name}",' \
                       f'\n\t\t"id": {audio_id},' \
                       f'\n\t\t"categories": ["{category}"]' + "\n\t}"
    return template


def write_to_audio_jet(new_entry: str, earwax_dir: str) -> None:
    """
    Writes the entry to the Audio jet file and appends it
    :param new_entry: New entry template for the audio jet file
    :param earwax_dir: The base earwax directory
    :return: Nothing , creates a new entry in the audio jet file
    """

    try:
        with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
            audio_jet.write(new_entry)
    except Exception as error:
        print("The new audio jet entry was incorrect or no directory was specified\n")
        print(f"Stack trace: {error} \n")


# This is a horrible implementation but this will do for the moment for V2 or V3 this will need to change
def reformat_audio_jet(earwax_dir: str) -> None:
    try:
        with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "r+", encoding='utf-8') as audio_jet:
            # TODO: -V2: Fix bug related to single line jet file , must check if file is single line then remove
            #           last 2 characters and append
            lines_data = audio_jet.readlines()
            audio_jet.seek(0)
            audio_jet.truncate()
            audio_jet.writelines(lines_data[:-2])
    except Exception as error:
        print(f"Stack trace: {error} \n")


def fix_line(earwax_dir: str) -> None:
    try:
        with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
            audio_jet.write("\t}")
    except Exception as error:
        print(f"Stack trace: {error} \n")


def reformat_audio_jet_fix(earwax_dir: str) -> None:
    try:
        with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
            audio_jet.write("]\n}\n")
    except Exception as error:
        print(f"Stack trace: {error} \n")


def read_forbidden_ids() -> List[str]:
    """
    :return: Returns a list from the txt file containing the IDs
    """
    forbidden_list = []
    with open('forbidden_ids.txt') as file:
        for line in file:
            forbidden_list.append(line.rstrip())
    return forbidden_list


def write_to_forbidden_ids(forbidden_id: str) -> None:
    """
    :param forbidden_id: ID to write to the file
    :return: Nothing , creates a new txt file for forbidden IDs if it doesn't exist
    """
    with open('forbidden_ids.txt', 'a+') as forbidden:
        forbidden.write(forbidden_id + "\n")
