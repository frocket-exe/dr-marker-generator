swears = ["fuck", "cunt"]
keywords = [
    "spawning", "forest", "flower", "birch", "dark", "garden", "cherry", 
    "taiga", "pine", "spruce", "jungle", "sparse", "bamboo", "meadow", 
    "grove", "snow", "peak", "hill", "plains", "sunflower", "desert", 
    "savanna", "bad", "mushroom", "ice", "spikes", "swamp", "void", 
    "river", "frozen", "beach", "shore", "ocean", "deep", "lush", 
    "drip", "cave", "nether", "crimson", "warped", "basalt", "end"
]
edlTitle = "sayBiome"
inputFilePath = "CLEAN_AUDIO.srt"
outputFilePath = "output.edl"
fps = 60
markingColors = {"swear": "Red", "keyword": "Yellow"}
markers = []
swearCount = 0
keywordCount = 0

def getDuration(tIn, tOut):
    hours = int(tOut[0:2]) - int(tIn[0:2])
    mins = int(tOut[3:5]) - int(tIn[3:5])
    secs = int(tOut[6:8]) - int(tIn[6:8])
    frames = (int(tOut[9:12])-int(tIn[9:12]))/1000*fps
    frames += (secs + mins*60 + hours*3600)*fps
    return round(frames)

def contains(list, content):
    for word in content.split(" "):
        for item in list:
            if item.lower() in word.lower():
                return True
    return False

def tcToTs(timecode):
    timestamp = timecode[:8]
    timestamp += f":{str(round(int(timecode[9:12])/1000*fps)).zfill(len(str(fps)))}"
    return timestamp

with open(inputFilePath) as f:
    file = f.read()
    captions = (file.split("\n\n"))[:-2]

for caption in captions:
    parts = caption.split("\n")
    # content = parts[2][3:-4]
    content = parts[2]
    if contains(swears, content):
        marking = "swear"
    elif contains(keywords, content):
        marking = "keyword"
    else:
        marking = None
    if marking != None:
        time = parts[1]
        timeParts = time.split(" ")
        timeIn = timeParts[0]
        timeOut = timeParts[2]
        marker = {"timeIn":timeIn, "timeOut":timeOut, "marking":marking, "content":content}
        markers.append(marker)

edlHeader = f"TITLE: {edlTitle}\nFCM: NON-DROP FRAME\n\n"
edlTxt = edlHeader

i = 0
for m in markers:
    i += 1
    if m["marking"] == "swear":
        swearCount += 1
        count = swearCount
    if m["marking"] == "keyword":
        keywordCount += 1
        count = keywordCount
    edlTxt += f"{str(i).zfill(3)}  001      V     C        {tcToTs(m["timeIn"])} {tcToTs(m["timeOut"])} {tcToTs(m["timeIn"])} {tcToTs(m["timeOut"])}\n"
    edlTxt += f" |C:ResolveColor{markingColors.get(m["marking"])} |M:{m["marking"]} {count} |D:{getDuration(m["timeIn"], m["timeOut"])}\n\n"

with open(outputFilePath, "w") as f:
    f.write(edlTxt)
    f.close()