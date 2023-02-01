# WaxOgg Version 1.5.2
A program to easily mod Jackbox' EarWax

## Disclaimer
This program is currently in v1.5.2 which means it can easily break your EarWax installation. Have a copy at the ready incase you need to start anew and make sure you are always giving the correct directory and uncorrupted OGG files.
### The script currently does not sport a Template.jet file yet for the spectrum, you will have to create one by using one of the existing spectrum files. You can use the spectrum file with ID 22740 as a template as it is the longest. This is an oversight and will be fixed by v2.0
#### There is a bug if your AudioFile.jet is a one liner , it will delete its entire content. Make sure your jet file is properly formated before using this

# How does WaxOgg work ?
WaxOgg is a python script that takes existing ogg audio files and adds them to EarWax to obtain modded sounds.
This currently supports adding multiple at once or singular files. I personally do not recommend you add them manually as it'll take you forever.

How EXACTLY does it function ?
1. WaxOgg will ask you your base EarWax directory and will do the rest from there.
2. It will ask your desired ogg files , will create copies with new IDs and add them into your EarWax audio at "/content/EarwaxAudio/Audio/".
3. It'll create a copy of a spectrum template and link it to its correct ID.
4. Finally it adds all your entries into the audio jet file under "/content/EarwaxAudio.jet". All IDs are within 50000 and 80000.

# How to run this ?
I will release a V2 with a GUI to help you use this more easily , expect Valve time on it , but do expect it.
In the meantime , here's how you run it.
1. [Install Python](https://www.python.org/downloads/) , yes you need python to run this program , you need Python 3 , the version shouldnt matter but if you are unsure go with 3.9.
2. Download the Zip file and extract it wherever you want
3. Launch WaxOgg.py inside the folder with the command ```python WaxOgg.py``` or ```python3 WaxOgg.py``` depending on your installation or if you are on windows simply double click the file to execute it
4. Follow the instructions given.
5. You're done !

# Credits
- Me for creating this
- [Ironminer888](https://gamebanana.com/members/1740235) at Gamebanana for creating the [guide](https://gamebanana.com/tuts/13522) that inspired this
- A genius for the working regex and technical assistance
