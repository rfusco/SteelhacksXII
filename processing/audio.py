import whisper, os
import models



model = whisper.load_model("base")
result = model.transcribe("../files/audio/Recording.mp3")
print(result["text"])




