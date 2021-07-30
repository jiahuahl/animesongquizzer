import sys
import subprocess
import os
import random
import shutil

DATAFOLDER = "data_main"
IMPORTFILE = "import.csv"
VIDEOSRC = "video_importing"
FILEFORMAT =   'title: {}\n'\
               'song: {}\n'\
               'anime: {}\n'\
               'type: {}\n'\
               'artist: {}\n'\
               'qstart: {}\n'\
               'qend: {}\n'\
               'atime: {}\n'\
               'difficulty: {}\n'\
               'copyright: {}\n'

def ImportCsv():
    file = open(IMPORTFILE, "r")

    for line in file:
        if line.startswith("id"):
            continue
        AddOrEditEntry(line)

    file.close()

def AddOrEditEntry(line):
    data = [x.strip() for x in line.split(",")]
    
    id = data[0]
    title = data[1]
    song = data[2]
    anime = data[3]
    songtype = data[4].lower()
    artist = data[5]
    qstart = data[6]
    qend = data[7]
    atime = data[8]
    difficulty = data[9].lower()
    copyright = ""

    if len(data) > 10:
        copyright = True if data[10].lower() == "true" else ""

    print(VIDEOSRC+"\\"+id+".mp4")
    if os.path.isfile(VIDEOSRC+"\\"+id+".mp4") is False:
        print("file with id: {} did have corresponding {}.mp4".format(id, id))
        return
    
    file = ""
    if os.path.isfile(DATAFOLDER+"\\"+id+"\\info.txt") is False:
        os.mkdir(DATAFOLDER+"\\"+id)
        
    file = open(DATAFOLDER+"\\"+id+"\\info.txt", "w")

    outstring = FILEFORMAT.format(title, song, anime, songtype, artist, qstart, qend, atime, difficulty, copyright)

    file.write(outstring)
    file.close()

    shutil.copyfile(VIDEOSRC+"\\"+id+".mp4", DATAFOLDER+"\\"+id+"\\video.mp4")
    
def main(argv):
    ImportCsv()

if __name__ == "__main__":
    main(sys.argv[1:])
