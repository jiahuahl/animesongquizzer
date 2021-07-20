import sys
import subprocess
import os
import random

GUESSDURATION = 10
ANSWERDURATION = 8
SONGCOUNT = 10
MAXTRY = 50
CHANGEBACKGROUND = 4

FONT = "BowlbyOneSC-Regular.ttf"
FFMPEG = 'G:\Scripts\FFmpeg\staticbuild\\bin\\ffmpeg.exe -loglevel error -stats '
ADDTEXTARGS = " -vf \"drawtext=fontfile='c\:\\\Windows\\\Fonts\\\\"+FONT+"':text='{}':x={}:y={}:fontsize={}:fontcolor=white:bordercolor=black:borderw=10\" "
NUMTEXTARGS = " -vf \"drawtext=fontfile='c\:\\\Windows\\\Fonts\\\\"+FONT+"':text='{}':x={}:y={}:fontsize={}:fontcolor=white:bordercolor=black:borderw=10\" "

RESIZE = " -vf scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1:color=black,setdar=16/9 "
VIDEO = "video.mp4"
COLORKEY = " -filter_complex \"[1:v]colorkey=0x44B521:0.4:0.0[ckout];[0:v][ckout]overlay[vout]\" -map \"[vout]\" "

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def MakeSegment(index, folder, qDuration, aDuration):
    info = open(folder+"info.txt", "r")
    title = ""
    atime = ""
    qstart = ""
    qend = ""

    for line in info:
        if line.startswith("title"):
            title = line[line.find(":")+1:].strip()
        elif line.startswith("atime"):
            atime = float(line[line.find(":")+1:].strip())
        elif line.startswith("qstart"):
            qstart = float(line[line.find(":")+1:].strip())
        elif line.startswith("qend"):
            qend = float(line[line.find(":")+1:].strip())

    info.close()
    
    length = int(get_length(folder + VIDEO))
    qend = min(qend, length - float(qDuration))
    startTime = random.randint(qstart, qend)

    qVid = MakeCountdown(folder, str(qDuration), startTime)
    qAns = MakeAnswer(folder, str(aDuration), title, atime)

    addText = NUMTEXTARGS.format(str(index), "100", "100", "200")
    cmd = FFMPEG + "-y -i " + qVid + " -i " + qAns + " -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]\""
    cmd = cmd + " -map \"[outv]\" -map \"[outa]\" -vsync 2 -b:a 320k " + "unnormalizedclip.mp4"
    os.system(cmd)

    cmd = FFMPEG + '-y -i unnormalizedclip.mp4 -filter:a loudnorm -b:a 320k ' + addText + "output\\" + str(index) + ".mp4"
    os.system(cmd)

    #cmd = FFMPEG + "-y -i " + "normalized.mp4" + addText + "-b:a 320k " + "output\\" + str(index) + ".mp4"
    #os.system(cmd)
    
    return

def MakeCountdownTemplate(pickedTemplate, countdown):
    background = "background.mp4"
    countdown = str(countdown)
    cmd = FFMPEG + "-y -i " + pickedTemplate + " -t " + countdown + " " + RESIZE + background
    os.system(cmd)

    clockStart = 10 - int(countdown)
    cmd = FFMPEG + "-y -i " + background + " -ss " + str(clockStart) + " -i assets\\countdowntimer.mp4" + COLORKEY + "-b:a 320k " + "countdown.mp4"
    os.system(cmd)

def MakeCountdown(folder, countdown, startTime):
    outputName = "question.mp4"
    background = "background.mp4"
 
    cmd = FFMPEG + "-y -i " + "countdown.mp4" + " -ss " + str(startTime) + " -i " + folder + VIDEO + " -t " + countdown + " -map 0:v:0 -map 1:a:0 -b:a 320k " + outputName
    os.system(cmd)
    
    return outputName

def MakeAnswer(folder, aDuration, title, atime):
    outputName = "answer.mp4"
    answerClip = "answerClip.mp4"
    cmd = FFMPEG + "-y -ss " + str(atime) + " -i " + folder + VIDEO + " -t " + aDuration + " " + RESIZE + " -b:a 320k " + answerClip
    os.system(cmd)

    titleLen = len(title)
    fontSize = min(160, max(80, titleLen * -3 + 190))

    if (titleLen > 30):
        divider = title.find(" ", int(titleLen / 2))
        title = title[:divider] + "\f" + title[divider+1:]

    addText = ADDTEXTARGS.format(title, "(w-text_w)/2", "h-th-100", str(fontSize))
    cmd = FFMPEG + "-y -i " + answerClip + addText + " -b:a 320k " + outputName
    os.system(cmd)
    
    return outputName

def TestSingleFile():
    info = open("info.txt", "r")
    title = ""
    atime = ""
    qstart = ""
    qend = ""

    for line in info:
        if line.startswith("title"):
            title = line[line.find(":")+1:].strip()
        elif line.startswith("atime"):
            atime = float(line[line.find(":")+1:].strip())
        elif line.startswith("qstart"):
            qstart = float(line[line.find(":")+1:].strip())
        elif line.startswith("qend"):
            qend = float(line[line.find(":")+1:].strip())

    info.close()
    output = MakeAnswer("", str(ANSWERDURATION), title, atime)

    cmd = FFMPEG + "-y -i "+ output +" -filter:a loudnorm " + "-b:a 320k " + "normalized.mp4"
    os.system(cmd)

    addText = NUMTEXTARGS.format("test", "100", "100", "200")
    cmd = FFMPEG + "-y -i " + "normalized.mp4" + addText + "-b:a 320k " + "output.mp4"
    os.system(cmd)
    
def CountDatabase():
    totalDir = 0
    for base, dirs, files in os.walk("data"):
        for directories in dirs:
            totalDir += 1
    return totalDir

def CountOutput():
    totalFiles = 0
    for base, dirs, files in os.walk("output"):
        for file in files:
            totalFiles += 1
    return totalFiles

def CanPick(songFolder, context):
    info = open(songFolder + "info.txt")
    title = ""
    copyright = ""
    
    for line in info:
        if line.startswith("title"):
            title = line[line.find(":")+1:].strip()
        if line.startswith("copyright"):
            copyright = line[line.find(":")+1:].strip()

    info.close()
    
    print("checking: " + title)

    if (copyright == "true"):
        if (max(GUESSDURATION, ANSWERDURATION) > 8):
            print("rejecting because clips are too long, will get copyrighted")
            return False

    AlreadyExist = title in context
    print(context)

    bShouldPick = AlreadyExist is not True
    if (bShouldPick):
        context.append(title)
        print("picking: " + title)
    
    return bShouldPick

def PickNewBackground(backgroundContext):
    backgrounds = os.listdir("assets\\backgrounds")
    random.shuffle(backgrounds)
    for background in backgrounds:
        if (background not in backgroundContext):
            backgroundContext.append(background)
            MakeCountdownTemplate("assets\\backgrounds\\" + background, GUESSDURATION)
            break
    
def MakeVideo():
    totalVids = CountDatabase()
    songTotal = min(totalVids, SONGCOUNT)

    NumberUsedBackground = 0
    backgroundContext = []
    PickNewBackground(backgroundContext)
    
    context = []

    for i in range(1, songTotal + 1):
        if (NumberUsedBackground >= CHANGEBACKGROUND):
            NumberUsedBackground = 0
            PickNewBackground(backgroundContext)
        for j in range(MAXTRY):
            randFolder = "data\\" + random.choice(os.listdir("data")) + "\\"
            if (CanPick(randFolder, context)):
                MakeSegment(i, randFolder, GUESSDURATION, ANSWERDURATION)
                NumberUsedBackground += 1
                break

    concatFile = open("concatFile.txt", 'w')
    songsMade = min(songTotal, CountOutput())
    for i in range(songsMade):
        concatFile.write('file \'output\\' + str(i+1) + ".mp4\'\n")
    concatFile.close()

    cmd = FFMPEG + '-y -f concat -safe 0 -i concatFile.txt -c copy -b:a 320k output.mp4'
    os.system(cmd)

  #  cmd = FFMPEG + '-y -i unnormalized.mp4 -filter:a loudnorm -b:a 320k output.mp4'
  #  os.system(cmd)

def main(argv):
    MakeVideo()
    #test single file
    #TestSingleFile()

if __name__ == "__main__":
    main(sys.argv[1:])
