import re
from datetime import datetime

from bson import ObjectId
from handle_data import Person, Conversation, Sentence, people
from sentiment import analyze_sentiment, analyze_conversation
def parse_srt_time(time_str: str) -> datetime:
    """Parse SRT time format 'HH:MM:SS,ms' into a datetime object."""
    h, m, s_ms = time_str.split(":")
    s, ms = s_ms.split(",")
    return datetime.now()

def srt_to_conversation_rnbrad(srt_text: str) -> Conversation:
    """
    Converts an SRT transcript to a Conversation object,
    mapping Speaker 0 -> Ryan, Speaker 1 -> Brad.
    """
    # Fetch Person documents from MongoDB
    ryan_doc = people.find_one({"name": "Ryan"})
    brad_doc = people.find_one({"name": "Brad"})
    if not ryan_doc or not brad_doc:
        raise ValueError("Ryan or Brad not found in MongoDB People collection.")

    speaker_map = {
        "Speaker 0": ryan_doc["_id"],
        "Speaker 1": brad_doc["_id"]
    }

    sentences = []
    flags = []
    participants_set = set([ryan_doc["_id"], brad_doc["_id"]])

    blocks = srt_text.strip().split("\n\n")
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue  # Skip malformed blocks
        
        # Lines: [index, time_range, text...]
        time_range = lines[1]
        text_lines = lines[2:]
        start_str, end_str = time_range.split(" --> ")
        start_time = parse_srt_time(start_str)
        end_time = parse_srt_time(end_str)
        total_seconds = int((end_time - start_time).total_seconds())

        # Extract speaker and text
        match = re.match(r"(Speaker \d+): (.*)", text_lines[0])
        if match:
            speaker_id, text = match.groups()
        else:
            speaker_id, text = "Unknown", " ".join(text_lines)

        # Map to Person ObjectId
        speaker_oid = speaker_map.get(speaker_id, ObjectId())

        sentence = Sentence(
            speaker=speaker_oid,
            text=text,
            sentiment=analyze_sentiment(text),
            start_time=start_time,
            total_time=total_seconds
        )

        sentences.append(sentence)
        if(sentence.sentiment['compound'] <= -0.):  # Flag very negative sentences
            flags.append(sentences.index(sentence))
    # Conversation metadata
    conversation_start = sentences[0].start_time if sentences else datetime.now()
    total_time = sum(s.total_time for s in sentences)

    convo = Conversation(
        participants=list(participants_set),
        start_time=conversation_start,
        total_time=total_time,
        sentences=sentences,
        sentiment= analyze_conversation(sentences),
        flags=flags
    )

    return convo

# -------------------------
# Example usage
# -------------------------
srt_text = """
1
00:00:00,780 --> 00:00:02,320
Speaker 0: Hey Bradley, how are you doing today?

2
00:00:04,080 --> 00:00:04,720
Speaker 1: I'm doing great.

3
00:00:04,840 --> 00:00:05,180
Speaker 1: How are you?

4
00:00:06,100 --> 00:00:06,960
Speaker 0: I'm doing pretty good.

5
00:00:07,240 --> 00:00:10,440
Speaker 0: I mean it's 2 37 a.m.

6
00:00:10,800 --> 00:00:12,880
Speaker 0: And how many hours do we have left?

7
00:00:13,120 --> 00:00:13,700
Speaker 0: I'm so tired.

8
00:00:13,800 --> 00:00:14,800
Speaker 0: I can't even do the math.

9
00:00:15,500 --> 00:00:18,020
Speaker 1: We have like seven or eight hours left, I believe.

10
00:00:18,680 --> 00:00:21,060
Speaker 0: Do you think we're gonna be able to finish the project in time?

11
00:00:23,000 --> 00:00:23,660
Speaker 1: I think we will.

12
00:00:24,000 --> 00:00:26,500
Speaker 1: If this test right here works, I think we will.

13
00:00:27,800 --> 00:00:35,160
Speaker 0: Yeah, this test would be a pretty big leap because then we can start implementing the other functions and squirt in our program.

14
00:00:35,880 --> 00:00:39,860
Speaker 1: Yeah, if we don't finish that then I think I'm just going to squirt myself.

15
00:00:40,660 --> 00:00:44,060
Speaker 0: Yeah, I'd probably squirt squirt my brains out if I don't finish.

16
00:00:44,120 --> 00:00:46,780
Speaker 0: this like this would probably be one of the biggest.

17
00:00:47,340 --> 00:00:48,760
Speaker 1: Let me cut you off right there Ryan.

18
00:00:49,540 --> 00:00:50,120
Speaker 1: I have a gun.

19
00:00:50,440 --> 00:00:51,880
Speaker 1: I'm going to squirt you right now.

20
00:00:52,960 --> 00:00:56,180
Speaker 0: If you squirt me, I'll be glad I'll squirt with a smile.

21
00:00:57,620 --> 00:01:01,800
Speaker 1: That is a good thing good boy.
"""

conversation = srt_to_conversation_rnbrad(srt_text)
