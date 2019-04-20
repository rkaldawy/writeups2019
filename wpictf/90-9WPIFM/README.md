# 90.9 WPIFM - Stegonography - 300 Points

I (Remy) wrote this challenge, so of course my writeup will be biased... I wrote it! However, this writeup walks through how the challenge could be solved without any prior understanding on how it works.

## Challenge Description:

What song is this?

https://drive.google.com/open?id=1cdtUOw8ha3LGWTteIvXnGsHjMUZo7xeh

WARNING: LOUD!!! Start at low volume.

made by rm -k

## Lookin' at it

Following the drive link, we are presented with a six minute audio file. The audio file has bursts of music interrupted by segments of radio static; it sounds as though someone keeps flipping through radio channels on an old radio. The music itself is a mix of electronic, happy hardcore, future funk, J-pop, and eurobeat. The author of this challenge must be a total weeb... but he does have a good taste in music. At the end of the audio, there is an extended clip of the outro of Modjo's Lady; looks like they found the music they wanted. French house is a nice genre of music.

So my first intuition here is that data is being encoded in how the data is presented, and *not* within the data itself. Specifically, a further examination is warranted on how the static interrupts the music clips. With that being said, it makes sense to run the audio clip through some editing software to analyze it. Audacity should do the trick here.

![alt text](https://github.com/rkaldawy/writeups2019/blob/master/wpictf/90-9WPIFM/audacity.png "The Audio in Audacity")

Theres a couple pieces of important information we can pry just by looking at the audio. First, and most obviously, static chunks come in units of .25 seconds, while audio chunks come in units of one second. One could (and should) infer that these are the stardard units for ech type of audio. If this audio was binary, a one-second music chunk could be a '1' while a quarter-second static segment could be a '0'.

Second, and perhaps less obviously, the same static sample is being used for each static chunk. Take a look at the chunk between 6.75 and 7.0, and the chunk between 9.0 to 9.25: they are the same! Furthermore, it seems like the author left a full, unaltered sample of the static audio chunk in the first three seconds of the audio. We can use this audio sample as a reference to identify which parts of the audio are static, and which parts are music.

At this point, it seems very promising to break the audio down into binary data, based on the static and music chunks. Since we know that the static audio is the same, throughout the entire clip, we just need to develop a system that can identify spans of that audio.

## Breakin' down the audio

There are probably many ways to accomplish the task of breaking down the audio into data. Admittedly, I'm a computer scientist (and not an electrical engineer or signals engineer), so the way that I do this probably is not optimal. In any case, I decided to use a fast fourier transform of the static sample at the beginning of the audio file to compare it with transforms of quarter second chunks of the audio. By comparing the resulting frequencies of the two transforms, in a process called correllation, it is possible to determine whether or not that quarter second segment has static or music. 

Since we are given a full sample of the static at the beginning of the file, I match segments of static exactly. If I find that a given chunk has the first quarter second of static, I then check if the next quarter second has *the next* quarter second of static. When I eventually find music, I reset my static check back to the first quarter second.

The code in  fft\_solver.py will take the audio and break it down into static chunks (denoted 'B') and audio chunks (denoted 'W'). It took a bit of parameter tweaking to get the correlation tollerance to work properly so that there were no false positives. I also made sure to slice off the 3-second static sample at the beginning of the audio and the music at the end (since we can assume it was placed there for aesthetic purposes). Looking at the generated pattern, it may at first seem like random chunks of bits. However, a certain pattern emerges which betrays what the bits represent. Within the stream, this pattern is visible:

**BBBBBBB**WWBWWBWWBBW**BBBBBBB** **BWWWWWB**WWWBBBBWBBW**BWWWWWB**......

Interesting. If I didn't know any better, that looks like the makings of the corner patterns of a QR code! Following through with this idea, we can try illustrating a QR code. 

## Constructing the QR code

Static chunks will form black pixels, while music chunks will form white pixels. Since we know what the corner patterns of a QR code look like, we can infer what the length of the QR code is, such that we achieve the desired patterns at the corners. Recreating the QR code gives us the following:

![alt text](https://github.com/rkaldawy/writeups2019/blob/master/wpictf/90-9WPIFM/output.bmp "The QR Code")

Scanning it will get us the flag: WPI{ju$t\_P1cK\_@\_s0Ng}.

This was the only challenge in WPICTF 2019 that had no solution. In my opinion, stegonography is the hardest CTF category, so it isn't unreasonable that a challenge should have *very few* solves. However, no solves at all is a sign that the challenge did not give people enough of an indicator that they were going in the right direction. In retrospect, I could have put a subtle hint somewhere in the challenge to tell people to look for QR codes. At the very least, I hope people enjoyed listening to the challege, and getting to hear some of the music that I like.

