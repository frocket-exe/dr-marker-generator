import whisper

model = whisper.load_model("large-v2", device="cuda")

result = model.transcribe(
    "srt test.wav",
    language="en",
    word_timestamps=True,
    beam_size=5,
    temperature=0,
    condition_on_previous_text=False
)

for segment in result["segments"]:
    print("\nSEGMENT:")
    print(segment["start"], segment["end"], segment["text"])

    for word in segment.get("words", []):
        print(
            f"  {word['start']:.2f} -> {word['end']:.2f}  {word['word']}"
        )