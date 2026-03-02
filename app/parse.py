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
00:00:00,000 --> 00:00:02,200
Speaker 0: Good morning, Mrs. Thompson — how are you feeling today?

2
00:00:02,400 --> 00:00:04,200
Speaker 1: Good morning, Doctor. I'm feeling pretty well, thank you.

3
00:00:04,400 --> 00:00:06,000
Speaker 0: That's wonderful to hear. Any new aches or concerns since our last visit?

4
00:00:06,200 --> 00:00:08,400
Speaker 1: Just a little stiffness in my knees in the morning, but it eases after I move around.

5
00:00:08,600 --> 00:00:11,000
Speaker 0: Okay — morning stiffness that improves with activity can be normal. Are you walking as much as before?

6
00:00:11,200 --> 00:00:13,100
Speaker 1: Not as much lately; I worry about falling, so I've been careful.

7
00:00:13,300 --> 00:00:15,600
Speaker 0: That's understandable. We can talk about simple balance exercises and a safe walking plan to build confidence.

8
00:00:15,800 --> 00:00:18,200
Speaker 1: I would like that. I miss my walks to the park.

9
00:00:18,400 --> 00:00:20,500
Speaker 0: We'll make a plan so you can return safely. How have you been sleeping?

10
00:00:20,700 --> 00:00:22,300
Speaker 1: Sleep's been okay — I wake a few times, but I usually doze back off.

11
00:00:22,500 --> 00:00:24,800
Speaker 0: That sounds normal for your age. Any new medications or side effects to report?

12
00:00:25,000 --> 00:00:27,200
Speaker 1: No new ones. The heart medicine seems to agree with me.

13
00:00:27,400 --> 00:00:29,600
Speaker 0: Great — your blood pressure readings in the chart look stable. Have you had any dizziness or lightheadedness?

14
00:00:29,800 --> 00:00:31,400
Speaker 1: Only once last week when I stood up quickly. It passed after a moment.

15
00:00:31,600 --> 00:00:34,000
Speaker 0: We'll note that. I'll review your blood pressure and adjust if needed, and suggest standing up slowly.

16
00:00:34,200 --> 00:00:36,200
Speaker 1: Thank you, Doctor. I appreciate you listening.

17
00:00:36,400 --> 00:00:38,600
Speaker 0: Of course — that's my job. Are you getting enough to eat and drink during the day?

18
00:00:38,800 --> 00:00:40,600
Speaker 1: I try to. My daughter brings soup and we share lunch most afternoons.

19
00:00:40,800 --> 00:00:43,200
Speaker 0: That's excellent social support. Keep up the fluids — dehydration can cause dizziness too.

20
00:00:43,400 --> 00:00:45,800
Speaker 1: I'll make sure to sip more water during the day.

21
00:00:46,000 --> 00:00:48,200
Speaker 0: One more thing — would you like a referral to a gentle exercise group for balance and strength?

22
00:00:48,400 --> 00:00:50,200
Speaker 1: Yes, please. That sounds lovely and social.

23
00:00:50,400 --> 00:00:53,000
Speaker 0: I'll arrange it and we'll follow up in a month to see how you're doing. Anything else on your mind?

24
00:00:53,200 --> 00:00:54,800
Speaker 1: No, Doctor — I'm grateful. Thank you for your help.

25
00:00:55,000 --> 00:00:57,000
Speaker 0: You're very welcome, Mrs. Thompson. Take care, and call if anything changes.
"""
conversation = srt_to_conversation_rnbrad(srt_text)
