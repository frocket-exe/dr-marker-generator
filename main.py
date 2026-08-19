swears = ["fuck", "shit"]
keywords = ["max", "video"]
markers = []

with open("Subtitle 1.srt") as f:
    file = f.read()
    captions = file.split("\n\n")

for caption in captions:
    parts = caption.split("\n")
    content = parts[2][3:-4]
    for word in content.split(" "):
        if word in swears:
            marking = "swear"
        elif word in keywords:
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

for m in markers:
    print(m)