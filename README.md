# 🎙️ EchoTrace

**Find repeated attempts. Review your recording. Keep your best take.**

EchoTrace is an audio review and editing prototype that identifies possible repeated words, phrases, and sentences in uploaded audio or voice recordings.

It combines transcription, timestamps, waveform visualization, and editing controls to help users review repeated attempts and download an edited recording.

## 🎯 Why I Built This

When recording a presentation, tutorial, or voice-over, people often restart sentences or record multiple attempts. Finding those sections manually can require listening through the entire recording.

I built EchoTrace to bring detection, review, and basic editing into one interface, helping users locate possible repeats and decide which parts to keep.

Repeated speech can be intentional, so users stay in control of every removal.

## 🔄 How It Works

1. Upload an audio file or record your voice.
2. Click **Analyze** to transcribe the recording and identify possible repeats.
3. Review highlighted wording, timestamps, and the waveform.
4. Listen to the repeated attempts.
5. Select unwanted sections and adjust the cut boundaries.
6. Preview the edited recording.
7. Download the edited audio.

## ✨ Features

- Audio upload and microphone recording.
- English speech transcription.
- Detection of repeated transcribed wording within continuous speech.
- Highlighted repeated wording in the transcript.
- Timestamps and playback for reviewing attempts.
- Waveform visualization with repeat highlights.
- Selection and adjustment of sections to remove.
- Preview before downloading.
- Edited audio export as WAV.

## 🛠️ Tools and Models

| Technology | Purpose |
| --- | --- |
| **Python** | Application logic and audio editing. |
| **Streamlit** | Interactive web interface. |
| **Faster-Whisper — `base.en`** | Speech transcription and word timestamps. |
| **NumPy** | Audio processing and combining retained sections. |
| **Plotly** | Interactive waveform visualization. |

Faster-Whisper converts speech into text. Custom matching logic then compares transcribed word sequences to identify possible repetitions.

Detection depends on the transcription rather than a direct comparison of audio sounds.

## 💡 Use Cases

- Reviewing presentation rehearsals.
- Comparing voice-over attempts.
- Cleaning up tutorial recordings.
- Finding repeated sections in podcast narration.
- Reviewing personal voice recordings.

## 🚀 Run Locally

Use **Python 3.11**.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start EchoTrace:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

Allow microphone access to record your voice. An internet connection is required for the initial Whisper model download.

## ✂️ How Editing Works

EchoTrace flags possible repeats for review. Users select the sections they want to remove and can adjust the start and end times.

The app combines the remaining audio into a new recording for preview and download. The original recording remains unchanged.
