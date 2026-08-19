import re

with open("CLEAN_AUDIO.srt") as f:
    file = f.read()

file = file[:-2]
lines = file.split("\n\n")
newLines = ""
for line in lines:
    content = line.split("\n")[2]
    if content.lower() in ["i", "kohl", "i'm", "i've", "i'd"]:
        content = content.capitalize()
    else:
        content = content.lower()
    content = re.sub(r'[.!",;]', '', content)
    line = f"{line.split("\n")[0]}\n{line.split("\n")[1]}\n{content}"
    newLines += (line)
    newLines += ("\n\n")

san = newLines[:-2]

with open("SANITISED.srt", "w") as f:
    f.write(san)
    f.close()