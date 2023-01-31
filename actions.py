import random
import shutil
import re
import sys

from typing import List, Optional

# List of general Todos , this is mainly for different versions
# TODO: -V4: Modify with GUI sounds on a whim (delete, change ID, refresh sounds so no dupes)
#       -V3-4: Add a way to reset options with GUI incase something goes bad (deletion of new IDs , fresh audiojet file)
#       -V2: Add a GUI (lmao)
#       -V2: Test this on linux
#       -V2: Create Error handling (No directories given, incorrect files given, Template not present)
#       -V3 : Exe package

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

    # Calls governing the jet file , don't touch without having a perfectly working solution
    reformat_audio_jet(selected_dir)
    fix_line(selected_dir)

    for source in list_of_sources:
        # 20000 is used by existing IDs for the ogg files
        # 90000 and 80000 as well as 40000 are used by announcers and others
        # Random int might pose an issue if by chance they have overlapping IDs

        earwax_dir = selected_dir
        source_id = random.randint(50000, 80000)
        source_name = find_source_name(source)
        new_entry = create_new_entry_for_audio_jet(source_name, source_id)

        copy_ogg_to_earwax_audio(source, source_id, earwax_dir)
        create_spectrum_from_template(source_id, earwax_dir)
        write_to_audio_jet(new_entry, earwax_dir)
        print(f"Added new entry for {source}\n")

    # Fix the stuff we delete up there with the reformat
    reformat_audio_jet_fix(selected_dir)


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


def check_for_spectrum_template(earwax_dir: str) -> None:
    target = f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}Template.jet"
    try:
        shutil.copy(f"{earwax_dir}{TEMPLATE_SPECTRUM}", target)
    except Exception as error:
        print("You either gave no directory or the Template is corrupted/not present\n")
        print(f"Stack trace: {error} \n")


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


# My hope is by showing you this terribleness that I never have to fucking touch files ever again in my life and
# that no one will ever ask me to write a file editing function ever again either
def reformat_audio_jet(earwax_dir: str) -> None:
    try:
        with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "r+", encoding='utf-8') as audio_jet:
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
