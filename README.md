"# animesongquizzer" 

i wanted to make an anime OP guessing video, but it looked easily automatable
so i did that

i don't expect anyone else to use this code, so you will have to modify hard coded file refs

main usage:
requires a folder called 'data', with subfolders inside, 1 for each song

each subfolder needs an 'info.txt', and a 'video.mp4'
info.txt will have the info required to draw clips/segments from 'video.mp4'

here's the format for info.txt (subject to change):
title: 
song:
anime:
type: [op|ed|insert]
artist:
qstart: time in seconds from vid start where the 'question' portion of footage can be drawn
qend: time in seconds from vid start where the 'question' portion of footage can no longer be drawn
atime: time in seconds in the video to display clip of 'answer' portion
difficulty: [easy|medium|hard]
copyright: (optional)

example:
title: Beastars S1
song: Wild Side
anime: Beastars
type: op
artist: ALI
qstart: 0
qend: 60
atime: 49
difficulty: medium
copyright: true


other requirements:
again, code is not meant to run out of the box
but here's what I used if you want to get it working:
python
need MMFPEG installed - you need to rename path to it in the script
need assets\backgrounds - folder of images to pull from to use as backgrounds for 'question' portion
need assets\countdowntimer.mp4 - this is a green-screen graphic that will be overlayed on top of the background to be a countdown timer

yea i guess you also need the BowlbyOneSC-Regular.ttf font installed
