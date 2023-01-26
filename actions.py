import random
import shutil
import re
import json

from typing import List, Optional

# List of general Todos , this is mainly for different versions
#TODO:  -V4: Modify with GUI sounds on a whim (delete, change ID, refresh sounds so no dupes)
#       -V3-4: Add a way to reset options with GUI incase something goes bad (deletion of new IDs , fresh audiojet file)
#       -V2: Add a GUI (lmao)
#       -V2: Test this on linux
#       -V2: Create Error handling
#       -V3 : Exe package

BASE_EARWAX_AUDIO_DIR = r"/content/EarwaxAudio/Audio/"
BASE_EARWAX_JET_FILE = r"/content/EarwaxAudio.jet"
BASE_EARWAX_SPECTRUM_DIR = r"/content/EarwaxAudio/Spectrum/"
TEMPLATE_SPECTRUM = r"/content/EarwaxAudio/Spectrum/Template.jet"


def generate_manager(list_of_sources: List[str], selected_dir: str) -> None:
    # Code governing the jet file , dont touch unless you want to kill yourself
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

    # Fix the stuff we delete up there with the reformat
    reformat_audio_jet_fix(selected_dir)


def find_source_name(source: str) -> str:
    pattern = r"(?:\/).*\/(.*)\.ogg"
    source_name = re.search(pattern, source)
    return source_name.group(1)


def copy_ogg_to_earwax_audio(source_ogg: str, audio_id: int, earwax_dir: str) -> None:
    target = f"{earwax_dir}{BASE_EARWAX_AUDIO_DIR}{audio_id}.ogg"

    shutil.copy(source_ogg, target)


def create_spectrum_from_template(audio_id: int, earwax_dir: str) -> None:
    target = f"{earwax_dir}{BASE_EARWAX_SPECTRUM_DIR}{audio_id}.jet"

    shutil.copy(f"{earwax_dir}{TEMPLATE_SPECTRUM}", target)


def create_new_entry_for_audio_jet(name: str, audio_id: int, category: Optional[str] = "cartoon") -> str:
    # TODO: V3: Fix whatever this monstrosity is
    template = ", {" + f'\n\t\t"x": false,' \
                          f'\n\t\t"name": "{name}",' \
                          f'\n\t\t"short": "{name}",' \
                          f'\n\t\t"id": {audio_id},' \
                          f'\n\t\t"categories": ["{category}"]' + "\n\t}"
    return template


def write_to_audio_jet(new_entry: str, earwax_dir: str) -> None:
    with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
        audio_jet.write(new_entry)


# My hope is by showing you this terribleness that I never have to fucking touch files ever again in my life and
# that no one will ever ask me to write a file editing function ever again either
def reformat_audio_jet(earwax_dir:str) -> None:
    with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "r+", encoding='utf-8') as audio_jet:
        lines_data = audio_jet.readlines()
        audio_jet.seek(0)
        audio_jet.truncate()
        audio_jet.writelines(lines_data[:-2])


def fix_line(earwax_dir: str) -> None:
    with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
        audio_jet.write("\t}")


def reformat_audio_jet_fix(earwax_dir:str) -> None:
    with open(f"{earwax_dir}{BASE_EARWAX_JET_FILE}", "a", encoding='utf-8') as audio_jet:
        audio_jet.write("]\n}\n")
