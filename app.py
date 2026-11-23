# import io
# import re
# import html
# import hashlib
# from collections import defaultdict

# import streamlit as st
# from faster_whisper import WhisperModel
# from faster_whisper.audio import decode_audio


# st.set_page_config(
#     page_title="EchoTrace",
#     page_icon="🎙️",
#     layout="wide",
# )

# MAX_DURATION = 600
# SAMPLE_RATE = 16000


# # ---------- DESIGN ----------

# st.html("""
# <style>
# .stApp {
#     background: #F2ECFA !important;
#     color: #171B46;
# }

# .block-container {
#     max-width: 1400px;
#     padding-top: 2.5rem;
# }

# [data-testid="stHeader"] {
#     background: transparent;
# }

# h1, h2, h3 {
#     color: #171B46 !important;
# }

# .st-key-input_panel,
# .st-key-results_panel {
#     background: #FCFAFF !important;
#     border: 1px solid #B79ADB !important;
#     border-radius: 22px !important;
#     box-shadow: 0 10px 28px rgba(75, 45, 120, 0.12) !important;
#     padding: 10px;
#     padding-bottom: 24px !important;
# }

# [class*="st-key-repeat_card_"] {
#     background: linear-gradient(135deg, #F5F0FF, #FAF7FF);
#     border: 1px solid #EAE0FF !important;
#     border-radius: 18px !important;
#     padding: 8px;
#     box-shadow: 0 6px 18px rgba(93, 54, 170, 0.10);
# }

# button[kind="primary"] {
#     background: linear-gradient(110deg, #7945F8, #6030DF);
#     color: white;
#     border: none;
#     border-radius: 12px;
#     min-height: 48px;
#     transition: transform 0.2s, box-shadow 0.2s;
# }

# button[kind="primary"]:hover {
#     background: #6030DF;
#     color: white;
#     transform: translateY(-2px);
#     box-shadow: 0 6px 18px rgba(112, 57, 238, 0.22);
# }

# button[kind="primary"]:not(:disabled),
# button[kind="primary"]:not(:disabled) p {
#     color: #FFFFFF !important;
#     font-weight: 700;
# }

# button[kind="primary"]:disabled {
#     background: #E9E1F5 !important;
#     color: #80718F !important;
#     box-shadow: none;
#     transform: none;
# }

# button[kind="primary"]:disabled p {
#     color: #80718F !important;
# }

# button[kind="secondary"] {
#     background: #F2ECFF;
#     color: #513484;
#     border: 1px solid #E6DBFF;
#     border-radius: 12px;
#     min-height: 48px;
# }

# [data-testid="stFileUploaderDropzone"] {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     gap: 16px;
#     min-height: 220px;
#     padding: 24px;
#     text-align: center;
#     background: #F2ECFA !important;
#     border: 2px dashed #CDB8FF;
#     border-radius: 16px;
# }

# [data-testid="stFileUploaderDropzone"]::before {
#     content: "⇧";
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     width: 60px;
#     height: 60px;
#     border-radius: 18px;
#     background: #EEE5FF;
#     color: #8954EF;
#     font-size: 42px;
#     font-weight: 700;
# }

# [data-testid="stFileUploaderDropzone"] > div {
#     text-align: center;
#     justify-content: center;
# }

# [data-testid="stExpander"] {
#     border: 1px solid #EAE4F5;
#     border-radius: 16px;
#     box-shadow: 0 6px 18px rgba(93, 54, 170, 0.10);
# }

# [data-testid="stExpander"],
# [data-testid="stExpander"] details,
# [data-testid="stExpander"] summary,
# [data-testid="stExpanderDetails"],
# .transcript-row {
#     background: #F8F5FF !important;
# }

# .hero {
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#     gap: 24px;
#     margin-bottom: 30px;
# }

# .hero > div:first-child {
#     flex: 1;
#     min-width: 0;
# }

# .hero-title {
#     display: flex;
#     align-items: center;
#     gap: 16px;
# }

# .hero h1 {
#     margin: 0;
#     padding: 0;
#     font-size: clamp(36px, 4vw, 56px);
#     font-weight: 800;
#     letter-spacing: -1.5px;
#     white-space: nowrap;
# }

# .subtitle {
#     color: #777394;
#     font-size: 18px;
#     margin-top: 8px;
# }

# .logo {
#     display: flex;
#     align-items: center;
#     gap: 5px;
#     flex-shrink: 0;
# }

# .logo span {
#     width: 7px;
#     background: #7545F5;
#     border-radius: 10px;
#     transform-origin: center;
#     animation: logoPulse 1.4s ease-in-out infinite;
# }

# .logo span:nth-child(1) { animation-delay: -0.2s; }
# .logo span:nth-child(2) { animation-delay: -0.4s; }
# .logo span:nth-child(3) { animation-delay: -0.6s; }
# .logo span:nth-child(4) { animation-delay: -0.8s; }
# .logo span:nth-child(5) { animation-delay: -1.0s; }

# .audio-animation {
#     width: 350px;
#     max-width: 35%;
#     height: 100px;
#     position: relative;
#     overflow: hidden;
#     flex-shrink: 0;
# }

# .sound-bars {
#     position: absolute;
#     inset: 0;
#     display: flex;
#     justify-content: center;
#     align-items: center;
#     gap: 7px;
# }

# .sound-bars span {
#     width: 8px;
#     height: var(--height);
#     background: linear-gradient(
#         to bottom,
#         var(--color, #8B5CF6),
#         var(--bottom-color, #6D28D9)
#     );
#     border-radius: 8px;
#     transform-origin: center;
#     animation: soundpulse 1.8s ease-in-out infinite;
#     animation-delay: var(--delay);
#     box-shadow: 0 3px 8px rgba(139, 92, 246, 0.12);
# }

# @keyframes logoPulse {
#     0%, 100% { transform: scaleY(0.55); }
#     50% { transform: scaleY(1); }
# }

# @keyframes soundpulse {
#     0%, 100% {
#         transform: scaleY(0.45);
#         opacity: 0.85;
#     }
#     50% {
#         transform: scaleY(1);
#         opacity: 1;
#     }
# }

# .badge {
#     background: #FFE6E7;
#     color: #BC3546;
#     padding: 8px 14px;
#     border-radius: 12px;
#     display: inline-block;
#     margin-bottom: 16px;
#     font-weight: 600;
# }

# .repeat-heading {
#     display: inline-block;
#     color: #FFFFFF;
#     background: #8B5CF6;
#     padding: 6px 12px;
#     border-radius: 12px;
#     margin-bottom: 12px;
#     font-size: 13px;
#     font-weight: 600;
# }

# .repeat-text {
#     font-size: 23px;
#     font-weight: 700;
#     color: #171B46;
#     margin-bottom: 18px;
#     overflow-wrap: anywhere;
# }

# .take-label {
#     background: #EDE4FF;
#     color: #6637CE;
#     padding: 7px 11px;
#     border-radius: 12px;
#     display: inline-block;
#     margin-bottom: 8px;
#     font-size: 13px;
#     font-weight: 600;
# }

# .transcript-row {
#     display: flex;
#     align-items: flex-start;
#     gap: 14px;
#     padding: 14px;
#     margin-bottom: 8px;
#     border: 1px solid #EEE8F8;
#     border-radius: 12px;
#     box-shadow: 0 3px 10px rgba(93, 54, 170, 0.07);
# }

# .transcript-row.repeated {
#     background: #F0E8FF !important;
#     border-color: #E6D8FF;
# }

# .transcript-time {
#     color: #7751BC;
#     font-size: 13px;
#     min-width: 115px;
#     padding-top: 3px;
# }

# .transcript-text {
#     flex: 1;
#     color: #242044;
#     overflow-wrap: anywhere;
# }

# .repeat-tag {
#     color: #7040D7;
#     font-size: 12px;
#     white-space: nowrap;
#     background: #E6D8FF;
#     padding: 4px 8px;
#     border-radius: 8px;
# }

# .note {
#     background: #F6F1FF;
#     color: #716287;
#     padding: 14px;
#     border-radius: 12px;
#     margin-top: 12px;
#     margin-bottom: 0;
#     font-size: 14px;
# }

# .tip {
#     background: #FFF0EF;
#     color: #8A5555;
#     padding: 15px;
#     border-radius: 12px;
#     margin-top: 12px;
#     margin-bottom: 0;
#     font-size: 14px;
# }

# .empty-state {
#     text-align: center;
#     padding: 65px 20px;
#     border-radius: 16px;
#     background: #F2ECFA;
#     color: #827891;
# }

# .empty-state strong {
#     display: block;
#     font-size: 22px;
#     color: #4B3C66;
#     margin-bottom: 12px;
# }

# .empty-icon {
#     font-size: 36px;
#     margin-bottom: 14px;
# }

# @media (max-width: 700px) {
#     .audio-animation { display: none; }
#     .transcript-row { flex-wrap: wrap; }
#     .repeat-tag { white-space: normal; }
# }

# @media (prefers-reduced-motion: reduce) {
#     .logo span,
#     .sound-bars span {
#         animation: none;
#     }

#     button[kind="primary"] {
#         transition: none;
#         transform: none;
#     }
# }
# </style>
# """)


# # ---------- FUNCTIONS ----------

# @st.cache_resource
# def load_model():
#     return WhisperModel(
#         "base.en",
#         device="cpu",
#         compute_type="int8",
#     )


# def timestamp(seconds):
#     total_tenths = max(0, round(float(seconds) * 10))
#     minutes, remaining = divmod(total_tenths, 600)
#     return f"{minutes:02d}:{remaining / 10:04.1f}"


# def split_sentences(segments):
#     """Split the transcript for display only."""
#     sentences = []
#     current_words = []

#     def save_sentence():
#         if current_words:
#             sentences.append({
#                 "text": "".join(
#                     word["text"] for word in current_words
#                 ).strip(),
#                 "start": current_words[0]["start"],
#                 "end": current_words[-1]["end"],
#             })
#             current_words.clear()

#     for segment in segments:
#         for word in segment.get("words", []):
#             if current_words:
#                 gap = word["start"] - current_words[-1]["end"]

#                 if gap > 1.2:
#                     save_sentence()

#             current_words.append(word)

#             if re.search(r'[.!?]["\']?$', word["text"].strip()):
#                 save_sentence()

#     save_sentence()
#     return sentences


# @st.cache_data(show_spinner=False)
# def find_repeats(segments):
#     """
#     Search the full word sequence, independently of sentence boundaries.
#     Find exact repeated wording and consecutive single-word repeats.
#     """
#     words = []

#     for segment in segments:
#         for word in segment.get("words", []):
#             normalized_tokens = re.findall(
#                 r"\w+(?:['’]\w+)*",
#                 word["text"].lower(),
#             )

#             for token in normalized_tokens:
#                 words.append({
#                     "token": token.replace("’", "'"),
#                     "text": word["text"].strip(),
#                     "start": word["start"],
#                     "end": word["end"],
#                 })

#     tokens = [word["token"] for word in words]
#     positions = defaultdict(list)

#     for index, token in enumerate(tokens):
#         positions[token].append(index)

#     patterns = set()

#     # Discover repeated sequences with at least two words.
#     for indices in positions.values():
#         for offset, first in enumerate(indices):
#             for second in indices[offset + 1:]:
#                 if (
#                     first > 0
#                     and second > 0
#                     and tokens[first - 1] == tokens[second - 1]
#                 ):
#                     continue

#                 length = 0

#                 while (
#                     second + length < len(tokens)
#                     and first + length < second
#                     and tokens[first + length]
#                     == tokens[second + length]
#                 ):
#                     length += 1

#                 if length >= 2:
#                     patterns.add(
#                         tuple(tokens[first:first + length])
#                     )

#     groups = []
#     covered = []

#     # Prefer long phrases over smaller phrases within them.
#     ordered_patterns = sorted(
#         patterns,
#         key=lambda pattern: (-len(pattern), pattern),
#     )

#     for pattern in ordered_patterns:
#         size = len(pattern)
#         occurrences = []
#         next_free = 0

#         for start in positions[pattern[0]]:
#             end = start + size

#             if (
#                 start >= next_free
#                 and tuple(tokens[start:end]) == pattern
#             ):
#                 occurrences.append((start, end))
#                 next_free = end

#         if len(occurrences) < 2:
#             continue

#         already_covered = all(
#             any(
#                 old_start <= start and end <= old_end
#                 for old_start, old_end in covered
#             )
#             for start, end in occurrences
#         )

#         if already_covered:
#             continue

#         group = []

#         for start, end in occurrences:
#             group.append({
#                 "text": " ".join(
#                     word["text"] for word in words[start:end]
#                 ),
#                 "start": words[start]["start"],
#                 "end": words[end - 1]["end"],
#             })

#         groups.append(group)
#         covered.extend(occurrences)

#     # Single words are flagged only when consecutive.
#     # This avoids flagging every ordinary use of "the" or "I".
#     index = 0

#     while index < len(tokens):
#         end = index + 1

#         while (
#             end < len(tokens)
#             and tokens[end] == tokens[index]
#             and words[end]["start"] - words[end - 1]["end"] <= 2.0
#         ):
#             end += 1

#         if end - index >= 2:
#             already_covered = all(
#                 any(
#                     start <= word_index < stop
#                     for start, stop in covered
#                 )
#                 for word_index in range(index, end)
#             )

#             if not already_covered:
#                 groups.append([
#                     {
#                         "text": words[word_index]["text"],
#                         "start": words[word_index]["start"],
#                         "end": words[word_index]["end"],
#                     }
#                     for word_index in range(index, end)
#                 ])

#         index = end

#     return sorted(
#         groups,
#         key=lambda group: group[0]["start"],
#     )


# def set_source(source):
#     st.session_state["source"] = source


# # ---------- HEADER ----------

# bar_heights = [
#     18, 28, 45, 60, 35, 75, 48, 28, 55, 80,
#     40, 62, 30, 72, 48, 26, 56, 38, 68, 24,
# ]

# bar_colors = [
#     "#7945F8", "#8248F5", "#8B4BF1", "#974EEE",
#     "#A451EA", "#B454E5", "#C357DF", "#D25AD8",
#     "#DF5DD0", "#EA60C5", "#F163B8", "#F566AC",
#     "#F7699F", "#F96C92", "#FA7087", "#FB757D",
#     "#FC7A73", "#FD806A", "#FE8762", "#FF8F5A",
# ]

# bars = "".join(
#     f'<span style="'
#     f'--height:{height}px;'
#     f'--delay:-{index * 0.13:.2f}s;'
#     f'--color:{bar_colors[index]};'
#     f'--bottom-color:{bar_colors[max(0, index - 2)]};'
#     f'"></span>'
#     for index, height in enumerate(bar_heights)
# )

# st.html(f"""
# <div class="hero">
#     <div>
#         <div class="hero-title">
#             <div class="logo" aria-hidden="true">
#                 <span style="height:20px"></span>
#                 <span style="height:38px"></span>
#                 <span style="height:55px"></span>
#                 <span style="height:32px"></span>
#                 <span style="height:16px"></span>
#             </div>
#             <h1>EchoTrace</h1>
#         </div>
#         <div class="subtitle">
#             Find repeated words and phrases in your recordings.
#         </div>
#     </div>

#     <div class="audio-animation" aria-hidden="true">
#         <div class="sound-bars">{bars}</div>
#     </div>
# </div>
# """)


# # ---------- INPUT PANEL ----------

# st.session_state.setdefault("source", "Upload audio")

# left, right = st.columns([0.9, 1.3], gap="large")
# results = None

# with left:
#     with st.container(border=True, key="input_panel"):
#         st.subheader("Add your audio")

#         upload_column, record_column = st.columns(2)
#         source = st.session_state["source"]

#         with upload_column:
#             st.button(
#                 "↥ Upload audio",
#                 key="choose_upload",
#                 type=(
#                     "primary"
#                     if source == "Upload audio"
#                     else "secondary"
#                 ),
#                 use_container_width=True,
#                 on_click=set_source,
#                 args=("Upload audio",),
#             )

#         with record_column:
#             st.button(
#                 "🎙 Record voice",
#                 key="choose_record",
#                 type=(
#                     "primary"
#                     if source == "Record voice"
#                     else "secondary"
#                 ),
#                 use_container_width=True,
#                 on_click=set_source,
#                 args=("Record voice",),
#             )

#         if source == "Upload audio":
#             audio = st.file_uploader(
#                 "Drop your audio here",
#                 type=["wav", "mp3", "m4a", "ogg", "opus"],
#                 key="uploaded_audio",
#             )
#         else:
#             audio = st.audio_input(
#                 "Record your voice",
#                 key="recorded_audio",
#             )

#         st.caption("English · One speaker · Up to 10 minutes")

#         if audio is not None:
#             audio_bytes = audio.getvalue()
#             audio_id = hashlib.sha256(audio_bytes).hexdigest()

#             if st.session_state.get("audio_id") != audio_id:
#                 st.session_state["audio_id"] = audio_id
#                 st.session_state.pop("transcript", None)
#                 st.session_state.pop("waveform", None)
#                 st.session_state.pop("duration", None)

#             # Microphone recordings already have a player.
#             if source == "Upload audio":
#                 st.audio(audio)

#             if st.button(
#                 "✦ Analyze audio",
#                 type="primary",
#                 use_container_width=True,
#             ):
#                 st.session_state.pop("transcript", None)
#                 st.session_state.pop("waveform", None)
#                 st.session_state.pop("duration", None)

#                 try:
#                     with st.spinner("Reading your audio..."):
#                         waveform = decode_audio(
#                             io.BytesIO(audio_bytes),
#                             sampling_rate=SAMPLE_RATE,
#                         )

#                     duration = len(waveform) / SAMPLE_RATE

#                     if duration > MAX_DURATION:
#                         st.warning(
#                             "Please use a recording up to 10 minutes."
#                         )

#                     elif len(waveform) == 0:
#                         st.warning("This audio file is empty.")

#                     else:
#                         with st.spinner(
#                             "Preparing Whisper. "
#                             "First run downloads the model..."
#                         ):
#                             model = load_model()

#                         progress = st.progress(
#                             0,
#                             text="Transcribing your recording...",
#                         )

#                         try:
#                             segments, _ = model.transcribe(
#                                 waveform,
#                                 language="en",
#                                 word_timestamps=True,
#                                 condition_on_previous_text=False,
#                             )

#                             transcript = []

#                             for segment in segments:
#                                 transcript.append({
#                                     "start": segment.start,
#                                     "end": segment.end,
#                                     "text": segment.text.strip(),
#                                     "words": [
#                                         {
#                                             "start": word.start,
#                                             "end": word.end,
#                                             "text": word.word,
#                                         }
#                                         for word in (segment.words or [])
#                                     ],
#                                 })

#                                 fraction = min(
#                                     0.99,
#                                     segment.end / max(duration, 0.01),
#                                 )

#                                 progress.progress(
#                                     fraction,
#                                     text=(
#                                         "Transcribing: "
#                                         f"{timestamp(segment.end)} / "
#                                         f"{timestamp(duration)}"
#                                     ),
#                                 )

#                             progress.progress(
#                                 1.0,
#                                 text="Transcription complete.",
#                             )

#                         finally:
#                             progress.empty()

#                         st.session_state["transcript"] = transcript
#                         st.session_state["waveform"] = waveform
#                         st.session_state["duration"] = duration

#                 except Exception as error:
#                     st.error(f"Could not analyze the audio: {error}")

#             results = st.session_state.get("transcript")

#             if st.session_state.get("duration") is not None:
#                 st.caption(
#                     "Recording length: "
#                     f'{timestamp(st.session_state["duration"])}'
#                 )

#         else:
#             st.button(
#                 "✦ Analyze audio",
#                 type="primary",
#                 disabled=True,
#                 use_container_width=True,
#             )

#         st.html("""
#         <div class="note">
#             Record first. Analyze when you are ready.
#             You can speak continuously without deliberate pauses.
#         </div>
#         """)


# # ---------- RESULTS PANEL ----------

# with right:
#     with st.container(border=True, key="results_panel"):
#         st.subheader("Review your recording")

#         if results:
#             sentences = split_sentences(results)

#             with st.spinner("Finding repeated words and phrases..."):
#                 repeats = find_repeats(results)

#             waveform = st.session_state["waveform"]

#             label = (
#                 "1 possible repeat"
#                 if len(repeats) == 1
#                 else f"{len(repeats)} possible repeats"
#             )

#             st.html(
#                 f'<div class="badge">↻ {label}</div>'
#             )

#             if not repeats:
#                 st.info(
#                     "No matching repeated wording found. "
#                     "Changes in wording or transcription errors "
#                     "may hide repeats."
#                 )

#             repeated_times = {
#                 (occurrence["start"], occurrence["end"])
#                 for group in repeats
#                 for occurrence in group
#             }

#             for number, group in enumerate(repeats, start=1):
#                 with st.container(
#                     border=True,
#                     key=f"repeat_card_{number}",
#                 ):
#                     text = html.escape(group[0]["text"])

#                     st.html(
#                         f'<div class="repeat-heading">'
#                         f'Possible repeated wording · {number}</div>'
#                         f'<div class="repeat-text">{text}</div>'
#                     )

#                     st.caption(
#                         f"{len(group)} occurrences · "
#                         "Listen to compare each attempt."
#                     )

#                     for row_start in range(0, len(group), 2):
#                         row = group[row_start:row_start + 2]
#                         columns = st.columns(len(row))

#                         for offset, (column, occurrence) in enumerate(
#                             zip(columns, row)
#                         ):
#                             take = row_start + offset + 1

#                             with column:
#                                 start = timestamp(occurrence["start"])
#                                 end = timestamp(occurrence["end"])

#                                 st.html(
#                                     f'<div class="take-label">'
#                                     f'Take {take} · {start}–{end}'
#                                     f'</div>'
#                                 )

#                                 if occurrence["text"] != group[0]["text"]:
#                                     st.write(occurrence["text"])

#                                 clip_start = max(
#                                     0,
#                                     int(
#                                         (occurrence["start"] - 0.15)
#                                         * SAMPLE_RATE
#                                     ),
#                                 )

#                                 clip_end = min(
#                                     len(waveform),
#                                     int(
#                                         (occurrence["end"] + 0.15)
#                                         * SAMPLE_RATE
#                                     ),
#                                 )

#                                 clip = waveform[clip_start:clip_end]

#                                 if len(clip) > 0:
#                                     st.audio(
#                                         clip,
#                                         sample_rate=SAMPLE_RATE,
#                                     )
#                                 else:
#                                     st.caption(
#                                         "This occurrence has no usable "
#                                         "audio duration in the transcript."
#                                     )

#             with st.expander("Full transcript", expanded=True):
#                 display_rows = sentences or results

#                 for sentence in display_rows:
#                     start = timestamp(sentence["start"])
#                     end = timestamp(sentence["end"])
#                     text = html.escape(sentence["text"])

#                     is_repeated = any(
#                         sentence["start"] < repeat_end
#                         and sentence["end"] > repeat_start
#                         for repeat_start, repeat_end in repeated_times
#                     )

#                     row_class = (
#                         "transcript-row repeated"
#                         if is_repeated
#                         else "transcript-row"
#                     )

#                     tag = (
#                         '<span class="repeat-tag">'
#                         'Contains repeat</span>'
#                         if is_repeated
#                         else ""
#                     )

#                     st.html(
#                         f'<div class="{row_class}">'
#                         f'<span class="transcript-time">'
#                         f'{start}–{end}</span>'
#                         f'<span class="transcript-text">{text}</span>'
#                         f'{tag}</div>'
#                     )

#             st.caption(
#                 "Matches use exact transcribed wording, ignoring "
#                 "capitalization and punctuation. Single words are "
#                 "flagged when consecutive. Timestamps are approximate; "
#                 "clips include a little extra context."
#             )

#         elif results == []:
#             st.info("No speech detected. Try a clearer recording.")

#         else:
#             st.html("""
#             <div class="empty-state">
#                 <div class="empty-icon">🎧</div>
#                 <strong>Your results will appear here</strong>
#                 Upload audio or record your voice,
#                 then click Analyze audio.
#             </div>
#             """)

#         st.html("""
#         <div class="tip">
#             💡 Listen to each attempt and decide which to keep.
#             Intentional repetitions may also be highlighted.
#             Your original audio remains unchanged.
#         </div>
#         """)





import io
import re
import html
import math
import wave
import hashlib
from collections import defaultdict

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio


st.set_page_config(
    page_title="EchoTrace",
    page_icon="🎙️",
    layout="wide",
)

SAMPLE_RATE = 16000
MAX_DURATION = 600


# ---------- ECHOTRACE WELCOME SCREEN ----------

st.session_state.setdefault("echotrace_started", False)


def start_echotrace():
    st.session_state["echotrace_started"] = True


if not st.session_state["echotrace_started"]:
    st.html("""
    <style>
    .stApp {
        background:
            radial-gradient(
                ellipse at 50% 40%,
                #251A48 0%,
                #17112E 55%,
                #110D22 100%
            ) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 7vh;
        padding-bottom: 3rem;
    }

    .welcome-screen {
        text-align: center;
        padding: 50px 16px 20px;
    }

    .welcome-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 9px;
        height: 110px;
        margin-bottom: 28px;
    }

    .welcome-wave span {
        display: block;
        width: 11px;
        height: var(--height);
        border-radius: 20px;
        background: linear-gradient(180deg, #D879E7, #A46BF5);
        animation: welcomePulse 1.6s ease-in-out infinite;
        animation-delay: var(--delay);
        box-shadow: 0 0 20px rgba(180, 110, 245, 0.18);
    }

    @keyframes welcomePulse {
        0%, 100% { transform: scaleY(0.55); }
        50% { transform: scaleY(1); }
    }

    .welcome-title {
        margin: 0;
        color: #FFFFFF !important;
        font-size: clamp(54px, 9vw, 100px);
        font-weight: 800;
        letter-spacing: -3px;
        line-height: 1.15;
    }

    .welcome-description {
        color: #D9CDEC;
        font-size: clamp(17px, 2.5vw, 25px);
        line-height: 1.6;
        margin-top: 24px;
    }

    .welcome-steps {
        color: #BA9BFA;
        font-size: 16px;
        letter-spacing: 4px;
        margin-top: 48px;
        margin-bottom: 24px;
    }

    .st-key-welcome_action button {
        background: linear-gradient(110deg, #8950F8, #6935DF) !important;
        border: 1px solid #A77AF5 !important;
        border-radius: 14px !important;
        min-height: 54px;
        box-shadow: 0 8px 30px rgba(126, 69, 238, 0.25);
    }

    .st-key-welcome_action button,
    .st-key-welcome_action button p {
        color: #FFFFFF !important;
        font-size: 17px;
        font-weight: 600;
    }

    .st-key-welcome_action button:hover {
        border-color: #D4B8FF !important;
        box-shadow: 0 8px 35px rgba(126, 69, 238, 0.4);
    }

    .welcome-footer {
        text-align: center;
        color: #A99DBF;
        font-size: 13px;
        margin-top: 24px;
    }

    @media (prefers-reduced-motion: reduce) {
        .welcome-wave span {
            animation: none;
        }
    }
    </style>

    <div class="welcome-screen">
        <div class="welcome-wave" aria-hidden="true">
            <span style="--height:24px; --delay:-0.2s"></span>
            <span style="--height:44px; --delay:-0.4s"></span>
            <span style="--height:68px; --delay:-0.6s"></span>
            <span style="--height:92px; --delay:-0.8s"></span>
            <span style="--height:52px; --delay:-1.0s"></span>
            <span style="--height:108px; --delay:-1.2s"></span>
            <span style="--height:72px; --delay:-1.4s"></span>
            <span style="--height:38px; --delay:-1.6s"></span>
            <span style="--height:58px; --delay:-1.8s"></span>
        </div>

        <h1 class="welcome-title">EchoTrace</h1>

        <div class="welcome-description">
            Find repeated sentences in your recordings.
        </div>

        <div class="welcome-steps">
            REVIEW &nbsp; | &nbsp; EDIT &nbsp; | &nbsp; DOWNLOAD
        </div>
    </div>
    """)

    _, welcome_column, _ = st.columns([1, 1.2, 1])

    with welcome_column:
        with st.container(key="welcome_action"):
            st.button(
                "Start reviewing →",
                type="primary",
                use_container_width=True,
                on_click=start_echotrace,
            )

    st.html("""
    <div class="welcome-footer">
        Your recording. Your choice of what to keep.
    </div>
    """)

    st.stop()


# ---------- DESIGN ----------

st.html("""
<style>
.stApp {
    background: #F2ECFA !important;
    color: #171B46;
}
.block-container {
    max-width: 1400px;
    padding-top: 2.5rem;
}
[data-testid="stHeader"] {
    background: transparent;
}
h1, h2, h3 {
    color: #171B46 !important;
}
.st-key-input_panel,
.st-key-results_panel {
    background: #FCFAFF !important;
    border: 1px solid #B79ADB !important;
    border-radius: 22px !important;
    box-shadow: 0 10px 28px rgba(75,45,120,0.12) !important;
    padding: 10px;
    padding-bottom: 24px !important;
}
[class*="st-key-repeat_card_"] {
    background: linear-gradient(135deg,#F5F0FF,#FAF7FF);
    border: 1px solid #EAE0FF !important;
    border-radius: 18px !important;
    padding: 8px;
    box-shadow: 0 6px 18px rgba(93,54,170,0.10);
}
button[kind="primary"] {
    background: linear-gradient(110deg,#7945F8,#6030DF);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    transition: transform 0.2s, box-shadow 0.2s;
}
button[kind="primary"]:hover {
    background: #6030DF;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(112,57,238,0.22);
}
button[kind="primary"]:not(:disabled),
button[kind="primary"]:not(:disabled) p {
    color: white !important;
    font-weight: 700;
}
button[kind="primary"]:disabled {
    background: #E9E1F5 !important;
    box-shadow: none;
    transform: none;
}
button[kind="primary"]:disabled p {
    color: #80718F !important;
}
button[kind="secondary"] {
    background: #F2ECFF;
    color: #513484;
    border: 1px solid #E6DBFF;
    border-radius: 12px;
    min-height: 44px;
}
[data-testid="stFileUploaderDropzone"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    min-height: 220px;
    padding: 24px;
    text-align: center;
    background: #F2ECFA !important;
    border: 2px dashed #CDB8FF;
    border-radius: 16px;
}
[data-testid="stFileUploaderDropzone"]::before {
    content: "⇧";
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 18px;
    background: #EEE5FF;
    color: #8954EF;
    font-size: 42px;
    font-weight: 700;
}
.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 24px;
    margin-bottom: 30px;
}
.hero > div:first-child {
    flex: 1;
    min-width: 0;
}
.hero-title {
    display: flex;
    align-items: center;
    gap: 16px;
}
.hero h1 {
    margin: 0;
    padding: 0;
    font-size: clamp(36px,4vw,56px);
    font-weight: 800;
    letter-spacing: -1.5px;
}
.subtitle {
    color: #777394;
    font-size: 18px;
    margin-top: 8px;
}
.logo {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
}
.logo span {
    width: 7px;
    background: #7545F5;
    border-radius: 10px;
    transform-origin: center;
    animation: logoPulse 1.4s ease-in-out infinite;
}
.logo span:nth-child(1) { animation-delay: -0.2s; }
.logo span:nth-child(2) { animation-delay: -0.4s; }
.logo span:nth-child(3) { animation-delay: -0.6s; }
.logo span:nth-child(4) { animation-delay: -0.8s; }
.logo span:nth-child(5) { animation-delay: -1s; }

.audio-animation {
    width: 350px;
    max-width: 35%;
    height: 100px;
    position: relative;
    overflow: hidden;
    flex-shrink: 0;
}
.sound-bars {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 7px;
}
.sound-bars span {
    width: 8px;
    height: var(--height);
    background: linear-gradient(
        to bottom,var(--color),var(--bottom-color)
    );
    border-radius: 8px;
    transform-origin: center;
    animation: soundpulse 1.8s ease-in-out infinite;
    animation-delay: var(--delay);
}
@keyframes logoPulse {
    0%,100% { transform: scaleY(0.55); }
    50% { transform: scaleY(1); }
}
@keyframes soundpulse {
    0%,100% { transform: scaleY(0.45); opacity: 0.85; }
    50% { transform: scaleY(1); opacity: 1; }
}
.badge {
    background: #FFE6E7;
    color: #BC3546;
    padding: 8px 14px;
    border-radius: 12px;
    display: inline-block;
    margin-bottom: 16px;
    font-weight: 600;
}
.repeat-heading {
    display: inline-block;
    color: white;
    background: #8B5CF6;
    padding: 6px 12px;
    border-radius: 12px;
    margin-bottom: 12px;
    font-size: 13px;
    font-weight: 600;
}
.repeat-text {
    font-size: 22px;
    font-weight: 700;
    color: #171B46;
    margin-bottom: 18px;
    overflow-wrap: anywhere;
}
.take-label {
    background: #EDE4FF;
    color: #6637CE;
    padding: 7px 11px;
    border-radius: 12px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 600;
}
.transcript-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px;
    margin-bottom: 8px;
    border: 1px solid #EEE8F8;
    border-radius: 12px;
    background: #F8F5FF;
}
.transcript-time {
    color: #7751BC;
    font-size: 13px;
    min-width: 115px;
    padding-top: 3px;
}
.transcript-text {
    flex: 1;
    color: #242044;
    overflow-wrap: anywhere;
    white-space: pre-wrap;
}
.transcript-text mark {
    background: #E6D8FF;
    color: #513484;
    border-radius: 4px;
    padding: 2px 0;
}
.note, .tip {
    padding: 14px;
    border-radius: 12px;
    margin-top: 12px;
    font-size: 14px;
}
.note {
    background: #F6F1FF;
    color: #716287;
}
.tip {
    background: #FFF0EF;
    color: #8A5555;
}
.empty-state {
    text-align: center;
    padding: 65px 20px;
    border-radius: 16px;
    background: #F2ECFA;
    color: #827891;
}
.empty-state strong {
    display: block;
    font-size: 22px;
    color: #4B3C66;
    margin-bottom: 12px;
}
.empty-icon {
    font-size: 36px;
    margin-bottom: 14px;
}
@media (max-width: 700px) {
    .audio-animation { display: none; }
    .transcript-row { flex-wrap: wrap; }
}
@media (prefers-reduced-motion: reduce) {
    .logo span, .sound-bars span { animation: none; }
    button[kind="primary"] {
        transition: none;
        transform: none;
    }
}
</style>
""")


# ---------- MODEL AND DETECTION ----------

@st.cache_resource
def load_model():
    return WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8",
    )


def timestamp(seconds):
    total_tenths = max(0, round(float(seconds) * 10))
    minutes, remaining = divmod(total_tenths, 600)
    return f"{minutes:02d}:{remaining / 10:04.1f}"


@st.cache_data(show_spinner=False)
def find_repeats(segments):
    words = []

    for segment in segments:
        for word in segment.get("words", []):
            normalized_tokens = re.findall(
                r"\w+(?:['’]\w+)*",
                word["text"].lower(),
            )

            for token in normalized_tokens:
                words.append({
                    "token": token.replace("’", "'"),
                    "text": word["text"].strip(),
                    "start": word["start"],
                    "end": word["end"],
                })

    tokens = [word["token"] for word in words]
    positions = defaultdict(list)

    for index, token in enumerate(tokens):
        positions[token].append(index)

    patterns = set()

    # Search inside continuous speech, across sentence boundaries.
    for indices in positions.values():
        for offset, first in enumerate(indices):
            for second in indices[offset + 1:]:
                if (
                    first > 0
                    and second > 0
                    and tokens[first - 1] == tokens[second - 1]
                ):
                    continue

                length = 0

                while (
                    second + length < len(tokens)
                    and first + length < second
                    and tokens[first + length]
                    == tokens[second + length]
                ):
                    length += 1

                if length >= 2:
                    patterns.add(
                        tuple(tokens[first:first + length])
                    )

    groups = []
    covered = []

    for pattern in sorted(
        patterns,
        key=lambda item: (-len(item), item),
    ):
        size = len(pattern)
        occurrences = []
        next_free = 0

        for start in positions[pattern[0]]:
            end = start + size

            if (
                start >= next_free
                and tuple(tokens[start:end]) == pattern
            ):
                occurrences.append((start, end))
                next_free = end

        if len(occurrences) < 2:
            continue

        if all(
            any(a <= start and end <= b for a, b in covered)
            for start, end in occurrences
        ):
            continue

        groups.append([
            {
                "text": " ".join(
                    word["text"] for word in words[start:end]
                ),
                "start": words[start]["start"],
                "end": words[end - 1]["end"],
            }
            for start, end in occurrences
        ])

        covered.extend(occurrences)

    # Only consecutive single-word repetitions are flagged.
    index = 0

    while index < len(tokens):
        end = index + 1

        while (
            end < len(tokens)
            and tokens[end] == tokens[index]
            and words[end]["start"] - words[end - 1]["end"] <= 2.0
        ):
            end += 1

        if end - index >= 2:
            already_covered = all(
                any(a <= k < b for a, b in covered)
                for k in range(index, end)
            )

            if not already_covered:
                groups.append([
                    {
                        "text": words[k]["text"],
                        "start": words[k]["start"],
                        "end": words[k]["end"],
                    }
                    for k in range(index, end)
                ])

        index = end

    return sorted(groups, key=lambda group: group[0]["start"])


# ---------- AUDIO EDITING ----------

def make_wav_bytes(samples):
    buffer = io.BytesIO()
    pcm = (np.clip(samples, -1, 1) * 32767).astype("<i2")

    with wave.open(buffer, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(pcm.tobytes())

    return buffer.getvalue()


def merge_cut_intervals(cuts, audio_length):
    intervals = []

    for start, end in cuts:
        first = max(
            0, min(audio_length, math.floor(start * SAMPLE_RATE))
        )
        last = max(
            0, min(audio_length, math.ceil(end * SAMPLE_RATE))
        )

        if last > first:
            intervals.append((first, last))

    merged = []

    for first, last in sorted(intervals):
        if merged and first <= merged[-1][1]:
            merged[-1] = (
                merged[-1][0],
                max(last, merged[-1][1]),
            )
        else:
            merged.append((first, last))

    return merged


def remove_audio_sections(samples, intervals):
    parts = []
    cursor = 0

    for first, last in intervals:
        if first > cursor:
            parts.append(samples[cursor:first])

        cursor = last

    if cursor < len(samples):
        parts.append(samples[cursor:])

    if not parts:
        return np.empty(0, dtype=samples.dtype)

    return np.concatenate(parts)


def play_clip(samples, start, end, padding=0.15):
    first = max(0, math.floor((start - padding) * SAMPLE_RATE))
    last = min(
        len(samples),
        math.ceil((end + padding) * SAMPLE_RATE),
    )

    if last > first:
        st.audio(
            samples[first:last],
            sample_rate=SAMPLE_RATE,
        )
    else:
        st.caption("No usable audio duration for this occurrence.")


# ---------- VISUALS ----------

def show_waveform(samples, repeat_intervals, cut_intervals):
    block_size = max(1, int(np.ceil(len(samples) / 3000)))
    starts = np.arange(0, len(samples), block_size)

    minimum = np.minimum.reduceat(samples, starts)
    maximum = np.maximum.reduceat(samples, starts)

    times = np.repeat(starts / SAMPLE_RATE, 2)
    amplitudes = np.column_stack((minimum, maximum)).ravel()

    figure = go.Figure(
        go.Scatter(
            x=times,
            y=amplitudes,
            mode="lines",
            line=dict(color="#7545F5", width=1),
            hovertemplate=(
                "Time: %{x:.2f}s"
                "<br>Amplitude: %{y:.3f}<extra></extra>"
            ),
        )
    )

    for start, end in repeat_intervals:
        figure.add_vrect(
            x0=start,
            x1=end,
            fillcolor="#A78BFA",
            opacity=0.22,
            line_width=0,
            layer="below",
        )

    for first, last in cut_intervals:
        figure.add_vrect(
            x0=first / SAMPLE_RATE,
            x1=last / SAMPLE_RATE,
            fillcolor="#F97316",
            opacity=0.35,
            line_width=0,
        )

    figure.update_layout(
        height=260,
        margin=dict(l=15, r=15, t=15, b=35),
        paper_bgcolor="#FCFAFF",
        plot_bgcolor="#FCFAFF",
        font=dict(color="#171B46"),
        xaxis_title="Original recording time (seconds)",
        yaxis_title="Amplitude",
        showlegend=False,
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        key="review_waveform",
    )

    st.caption(
        "Purple: possible repeats · Orange: selected for removal. "
        "Drag to zoom; double-click to reset."
    )


def highlighted_transcript(words, repeat_intervals):
    fragments = []

    for word in words:
        safe_text = html.escape(word["text"])

        repeated = any(
            word["start"] < end and word["end"] > start
            for start, end in repeat_intervals
        )

        fragments.append(
            f"<mark>{safe_text}</mark>"
            if repeated
            else safe_text
        )

    return "".join(fragments)


def set_source(source):
    st.session_state["source"] = source


def clear_analysis():
    for key in (
        "transcript",
        "waveform",
        "duration",
        "edited_wav",
        "edit_signature",
    ):
        st.session_state.pop(key, None)


# ---------- HEADER ----------

bar_heights = [
    18, 28, 45, 60, 35, 75, 48, 28, 55, 80,
    40, 62, 30, 72, 48, 26, 56, 38, 68, 24,
]

bar_colors = [
    "#7945F8", "#8248F5", "#8B4BF1", "#974EEE",
    "#A451EA", "#B454E5", "#C357DF", "#D25AD8",
    "#DF5DD0", "#EA60C5", "#F163B8", "#F566AC",
    "#F7699F", "#F96C92", "#FA7087", "#FB757D",
    "#FC7A73", "#FD806A", "#FE8762", "#FF8F5A",
]

bars = "".join(
    f'<span style="'
    f'--height:{height}px;'
    f'--delay:-{index * 0.13:.2f}s;'
    f'--color:{bar_colors[index]};'
    f'--bottom-color:{bar_colors[max(0, index - 2)]};'
    f'"></span>'
    for index, height in enumerate(bar_heights)
)

st.html(f"""
<div class="hero">
    <div>
        <div class="hero-title">
            <div class="logo" aria-hidden="true">
                <span style="height:20px"></span>
                <span style="height:38px"></span>
                <span style="height:55px"></span>
                <span style="height:32px"></span>
                <span style="height:16px"></span>
            </div>
            <h1>EchoTrace</h1>
        </div>
        <div class="subtitle">
            Find repeated attempts. Review, edit, and download.
        </div>
    </div>
    <div class="audio-animation" aria-hidden="true">
        <div class="sound-bars">{bars}</div>
    </div>
</div>
""")


# ---------- INPUT PANEL ----------

st.session_state.setdefault("source", "Upload audio")

left, right = st.columns([0.9, 1.3], gap="large")
results = None

with left:
    with st.container(border=True, key="input_panel"):
        st.subheader("Add your audio")

        upload_column, record_column = st.columns(2)
        source = st.session_state["source"]

        with upload_column:
            st.button(
                "↥ Upload audio",
                key="choose_upload",
                type=(
                    "primary"
                    if source == "Upload audio"
                    else "secondary"
                ),
                use_container_width=True,
                on_click=set_source,
                args=("Upload audio",),
            )

        with record_column:
            st.button(
                "🎙 Record voice",
                key="choose_record",
                type=(
                    "primary"
                    if source == "Record voice"
                    else "secondary"
                ),
                use_container_width=True,
                on_click=set_source,
                args=("Record voice",),
            )

        if source == "Upload audio":
            audio = st.file_uploader(
                "Drop your audio here",
                type=["wav", "mp3", "m4a", "ogg", "opus"],
                key="uploaded_audio",
            )
        else:
            audio = st.audio_input(
                "Record your voice",
                key="recorded_audio",
            )

        st.caption("English · One speaker · Up to 10 minutes")

        if audio is not None:
            audio_bytes = audio.getvalue()
            audio_id = hashlib.sha256(audio_bytes).hexdigest()

            if st.session_state.get("audio_id") != audio_id:
                clear_analysis()
                st.session_state["audio_id"] = audio_id

            # Recorded audio already has playback in its widget.
            if source == "Upload audio":
                st.audio(audio)

            if st.button(
                "✦ Analyze audio",
                type="primary",
                use_container_width=True,
            ):
                clear_analysis()

                try:
                    with st.spinner("Reading your audio..."):
                        waveform = decode_audio(
                            io.BytesIO(audio_bytes),
                            sampling_rate=SAMPLE_RATE,
                        )

                    duration = len(waveform) / SAMPLE_RATE

                    if len(waveform) == 0:
                        st.warning("This audio file is empty.")

                    elif not np.isfinite(waveform).all():
                        st.warning("The audio contains invalid samples.")

                    elif duration > MAX_DURATION:
                        st.warning(
                            "Please use a recording up to 10 minutes."
                        )

                    else:
                        with st.spinner(
                            "Preparing Whisper. "
                            "First run downloads the model..."
                        ):
                            model = load_model()

                        progress = st.progress(
                            0,
                            text="Transcribing your recording...",
                        )

                        try:
                            segments, _ = model.transcribe(
                                waveform,
                                language="en",
                                word_timestamps=True,
                                condition_on_previous_text=False,
                            )

                            transcript = []

                            for segment in segments:
                                transcript.append({
                                    "start": segment.start,
                                    "end": segment.end,
                                    "text": segment.text.strip(),
                                    "words": [
                                        {
                                            "start": word.start,
                                            "end": word.end,
                                            "text": word.word,
                                        }
                                        for word in (segment.words or [])
                                    ],
                                })

                                progress.progress(
                                    min(
                                        0.99,
                                        segment.end / max(duration, 0.01),
                                    ),
                                    text=(
                                        "Transcribing: "
                                        f"{timestamp(segment.end)} / "
                                        f"{timestamp(duration)}"
                                    ),
                                )

                        finally:
                            progress.empty()

                        st.session_state["transcript"] = transcript
                        st.session_state["waveform"] = waveform
                        st.session_state["duration"] = duration

                except Exception as error:
                    st.error(f"Could not analyze the audio: {error}")

            results = st.session_state.get("transcript")

            if st.session_state.get("duration") is not None:
                st.caption(
                    "Recording length: "
                    f'{timestamp(st.session_state["duration"])}'
                )

        else:
            st.button(
                "✦ Analyze audio",
                type="primary",
                disabled=True,
                use_container_width=True,
            )

        st.html("""
        <div class="note">
            Record first, then analyze.
            You can speak continuously without deliberate pauses.
        </div>
        """)


# ---------- RESULTS PANEL ----------

with right:
    with st.container(border=True, key="results_panel"):
        st.subheader("Review your recording")

        if results:
            with st.spinner("Finding repeated wording..."):
                repeats = find_repeats(results)

            waveform = st.session_state["waveform"]
            duration = len(waveform) / SAMPLE_RATE
            audio_id = st.session_state["audio_id"]

            repeat_intervals = sorted({
                (item["start"], item["end"])
                for group in repeats
                for item in group
            })

            label = (
                "1 possible repeat"
                if len(repeats) == 1
                else f"{len(repeats)} possible repeats"
            )

            st.html(f'<div class="badge">↻ {label}</div>')

            # Avoid duplicate removal controls for the same interval.
            occurrence_lookup = {}

            for group_number, group in enumerate(repeats, start=1):
                for take_number, item in enumerate(group, start=1):
                    occurrence_key = (item["start"], item["end"])

                    if occurrence_key not in occurrence_lookup:
                        occurrence_lookup[occurrence_key] = {
                            **item,
                            "group": group_number,
                            "take": take_number,
                        }

            occurrences = sorted(
                occurrence_lookup.values(),
                key=lambda item: item["start"],
            )

            repeat_tab, transcript_tab, edit_tab = st.tabs([
                "🔁 Repeated attempts",
                "📝 Transcript",
                "✂️ Edit & download",
            ])

            # ---------- REPEATED ATTEMPTS ----------

            with repeat_tab:
                if not repeats:
                    st.info(
                        "No matching repeated wording found. "
                        "Changes in wording or transcription errors "
                        "may hide repeats."
                    )

                for number, group in enumerate(repeats, start=1):
                    with st.container(
                        border=True,
                        key=f"repeat_card_{number}",
                    ):
                        text = html.escape(group[0]["text"])

                        st.html(
                            '<div class="repeat-heading">'
                            f'Possible repeat · {number}</div>'
                            f'<div class="repeat-text">{text}</div>'
                        )

                        st.caption(
                            f"{len(group)} occurrences. "
                            "Listen to compare the attempts."
                        )

                        for take_number, occurrence in enumerate(
                            group,
                            start=1,
                        ):
                            start = occurrence["start"]
                            end = occurrence["end"]

                            st.html(
                                '<div class="take-label">'
                                f'Take {take_number} · '
                                f'{timestamp(start)}–{timestamp(end)}'
                                '</div>'
                            )

                            if occurrence["text"] != group[0]["text"]:
                                st.write(occurrence["text"])

                            play_clip(waveform, start, end)

                st.caption(
                    "Playback clips include extra context. "
                    "Open Edit & download to remove an attempt."
                )

            # ---------- TRANSCRIPT ----------

            with transcript_tab:
                st.caption(
                    "Highlighted words belong to possible repeats. "
                    "Timestamps refer to the original recording."
                )

                for segment in results:
                    words = segment.get("words", [])

                    text = (
                        highlighted_transcript(
                            words,
                            repeat_intervals,
                        )
                        if words
                        else html.escape(segment["text"])
                    )

                    st.html(
                        '<div class="transcript-row">'
                        '<span class="transcript-time">'
                        f'{timestamp(segment["start"])}–'
                        f'{timestamp(segment["end"])}'
                        '</span>'
                        f'<span class="transcript-text">{text}</span>'
                        '</div>'
                    )

                transcript_text = "\n".join(
                    f'{timestamp(segment["start"])}–'
                    f'{timestamp(segment["end"])}  '
                    f'{segment["text"]}'
                    for segment in results
                )

                st.download_button(
                    "Download transcript",
                    data=transcript_text,
                    file_name="echotrace_transcript.txt",
                    mime="text/plain",
                    key=f"transcript_download_{audio_id}",
                )

            # ---------- EDITING ----------

            cuts = []
            invalid_cut = False

            with edit_tab:
                st.write(
                    "Select the attempts to remove. "
                    "Everything else will stay in the recording."
                )

                st.caption(
                    "Cut times are approximate. Adjust the boundaries "
                    "and listen to the edited preview."
                )

                if not occurrences:
                    st.info(
                        "No repeated attempts are available to remove."
                    )

                for index, occurrence in enumerate(occurrences):
                    widget_key = f"{audio_id}_{index}"

                    start = float(
                        max(0, min(duration, occurrence["start"]))
                    )
                    end = float(
                        max(0, min(duration, occurrence["end"]))
                    )

                    with st.container(border=True):
                        selected = st.checkbox(
                            (
                                f'Remove repeat {occurrence["group"]}, '
                                f'take {occurrence["take"]} '
                                f'({timestamp(start)}–{timestamp(end)})'
                            ),
                            key=f"remove_{widget_key}",
                            value=False,
                        )

                        st.write(occurrence["text"])

                        if selected:
                            start_column, end_column = st.columns(2)

                            with start_column:
                                cut_start = st.number_input(
                                    "Remove from (seconds)",
                                    min_value=0.0,
                                    max_value=float(duration),
                                    value=start,
                                    step=0.01,
                                    format="%.2f",
                                    key=f"cut_start_{widget_key}",
                                )

                            with end_column:
                                cut_end = st.number_input(
                                    "Remove until (seconds)",
                                    min_value=0.0,
                                    max_value=float(duration),
                                    value=end,
                                    step=0.01,
                                    format="%.2f",
                                    key=f"cut_end_{widget_key}",
                                )

                            if cut_end <= cut_start:
                                invalid_cut = True
                                st.warning(
                                    "The end must be after the start."
                                )
                            else:
                                cuts.append((cut_start, cut_end))

                                st.caption(
                                    "This exact section will be removed:"
                                )

                                play_clip(
                                    waveform,
                                    cut_start,
                                    cut_end,
                                    padding=0,
                                )

                cut_intervals = merge_cut_intervals(
                    cuts,
                    len(waveform),
                )

                removed_samples = sum(
                    last - first
                    for first, last in cut_intervals
                )

                remaining_samples = (
                    len(waveform) - removed_samples
                )

                if cuts:
                    first_metric, second_metric = st.columns(2)

                    first_metric.metric(
                        "Selected for removal",
                        f"{removed_samples / SAMPLE_RATE:.1f} seconds",
                    )

                    second_metric.metric(
                        "Edited duration",
                        timestamp(remaining_samples / SAMPLE_RATE),
                    )

                if remaining_samples == 0:
                    st.warning(
                        "These selections remove the entire recording. "
                        "Keep at least one section."
                    )

                preview_signature = (
                    audio_id,
                    tuple(cut_intervals),
                )

                # Never offer an outdated edited download.
                if (
                    st.session_state.get("edit_signature")
                    != preview_signature
                ):
                    st.session_state.pop("edited_wav", None)
                    st.session_state.pop("edit_signature", None)

                can_preview = (
                    bool(cut_intervals)
                    and not invalid_cut
                    and remaining_samples > 0
                )

                if st.button(
                    "✂️ Create edited preview",
                    type="primary",
                    disabled=not can_preview,
                    use_container_width=True,
                    key=f"create_preview_{audio_id}",
                ):
                    edited = remove_audio_sections(
                        waveform,
                        cut_intervals,
                    )

                    st.session_state["edited_wav"] = make_wav_bytes(
                        edited
                    )

                    st.session_state["edit_signature"] = (
                        preview_signature
                    )

                if (
                    not invalid_cut
                    and st.session_state.get("edit_signature")
                    == preview_signature
                    and st.session_state.get("edited_wav")
                ):
                    st.subheader("Edited preview")

                    st.audio(
                        st.session_state["edited_wav"],
                        format="audio/wav",
                    )

                    st.download_button(
                        "⬇ Download edited audio",
                        data=st.session_state["edited_wav"],
                        file_name="echotrace_edited.wav",
                        mime="audio/wav",
                        use_container_width=True,
                        key=f"edited_download_{audio_id}",
                    )

                    st.caption(
                        "The edited player's timeline starts at zero. "
                        "The transcript and overview still show "
                        "the original recording's timestamps."
                    )

                elif cut_intervals and not invalid_cut:
                    st.caption(
                        "Click Create edited preview after "
                        "changing your selections."
                    )

            # ---------- WAVEFORM ----------

            st.subheader("Recording overview")

            show_waveform(
                waveform,
                repeat_intervals,
                cut_intervals,
            )

            st.caption(
                "Matches use exact transcribed wording, ignoring "
                "capitalization and punctuation. Single words are "
                "flagged when consecutive. Your original audio is "
                "unchanged; edited downloads are separate mono WAV files."
            )

        elif results == []:
            st.info(
                "No speech detected. Try a clearer recording."
            )

        else:
            st.html("""
            <div class="empty-state">
                <div class="empty-icon">🎧</div>
                <strong>Your results will appear here</strong>
                Upload audio or record your voice,
                then click Analyze audio.
            </div>
            """)

        st.html("""
        <div class="tip">
            💡 Find → compare → select removals →
            preview → download.
            Repeated wording may be intentional; you decide what to keep.
        </div>
        """)