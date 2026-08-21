import whisperx

AUDIO = "srt test.wav"

device = "cuda"
compute_type = "float16"

print("Loading WhisperX...")
model = whisperx.load_model(
    "large-v2",
    device,
    compute_type=compute_type,
)

print("Transcribing...")
result = model.transcribe(
    AUDIO,
    language="en",
    batch_size=4,
)

print("\nBefore alignment:")
for segment in result["segments"]:
    print(segment)

print("\nLoading alignment model...")
align_model, metadata = whisperx.load_align_model(
    language_code=result["language"],
    device=device,
)

print("Aligning...")
result = whisperx.align(
    result["segments"],
    align_model,
    metadata,
    AUDIO,
    device,
    return_char_alignments=False,
)

print("\nAFTER ALIGNMENT:")

for segment in result["segments"]:
    for word in segment.get("words", []):
        print(
            f"{word['start']:.3f} -> "
            f"{word['end']:.3f}  "
            f"{word['word']}"
        )


def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = round((seconds - int(seconds)) * 1000)

    if milliseconds == 1000:
        milliseconds = 0
        secs += 1

    if secs == 60:
        secs = 0
        minutes += 1

    if minutes == 60:
        minutes = 0
        hours += 1

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def make_captions(segments):

    captions = []
    current_words = []

    MAX_WORDS = 8
    PAUSE_THRESHOLD = 0.5

    for segment in segments:

        words = segment.get("words", [])

        for word in words:

            if "start" not in word or "end" not in word:
                continue

            current_words.append(word)

            if len(current_words) == 1:
                continue

            previous_word = current_words[-2]

            gap = word["start"] - previous_word["end"]

            previous_text = previous_word["word"].strip()

            # Strong sentence boundary
            sentence_finished = previous_text.endswith((".", "?", "!"))

            # Long silence
            long_pause = gap >= PAUSE_THRESHOLD

            # Hard maximum
            maximum_reached = len(current_words) >= MAX_WORDS

            if sentence_finished or long_pause or maximum_reached:

                captions.append(current_words[:-1])
                current_words = [word]

    if current_words:
        captions.append(current_words)

    return captions


captions = make_captions(result["segments"])


with open("proof_of_concept.srt", "w", encoding="utf-8") as srt:

    for number, caption in enumerate(captions, start=1):

        start = caption[0]["start"]
        end = caption[-1]["end"]

        text = " ".join(
            word["word"].strip()
            for word in caption
        )

        srt.write(
            f"{number}\n"
            f"{format_srt_time(start)} --> {format_srt_time(end)}\n"
            f"{text}\n\n"
        )


print(f"Generated {len(captions)} captions.")