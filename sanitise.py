import re

keepCap = ["I", "Kohl", "I'm", "I've", "I'd"]
puncToRemove = r'[.!",;]'
unsanitisedPath = "proof_of_concept.srt"

with open(unsanitisedPath) as f:
    file = f.read()

file = file[:-2]
lines = file.split("\n\n")
newLines = ""
for line in lines:
    content = line.split("\n")[2]
    content = re.sub(puncToRemove, '', content)
    content = content.split(" ")
    words = []
    for word in content:
        if word.capitalize() in keepCap:
            words.append(word.capitalize())
        else:
            words.append(word.lower())
    content = " ".join(words)
    line = f"{line.split("\n")[0]}\n{line.split("\n")[1]}\n{content}"
    newLines += (line)
    newLines += ("\n\n")

san = newLines[:-2]

with open("SANITISED.srt", "w") as f:
    f.write(san)
    f.close()