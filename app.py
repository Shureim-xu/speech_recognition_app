import streamlit as st
import speech_recognition as sr
import time


# SPEECH TRANSCRIPTION FUNCTION
def transcribe_speech(api_choice, language, pause_duration=0.8):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Listening... (Speak now)")
        r.pause_threshold = pause_duration   # Allows pause/continue speaking

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            st.info("Transcribing...")
        except sr.WaitTimeoutError:
            return "No speech detected. Try speaking louder or closer to the mic."
        except Exception as e:
            return f"Microphone error: {str(e)}"

        # API SELECTION
        try:
            if api_choice == "Google":
                return r.recognize_google(audio, language=language)

            elif api_choice == "Sphinx (Offline)":
                return r.recognize_sphinx(audio, language=language)

            else:
                return "Unknown API selected."

        except sr.UnknownValueError:
            return "Sorry, the audio was unclear. Try speaking again."

        except sr.RequestError:
            return "API request failed. Check your internet or API service."

        except Exception as e:
            return f"Unexpected error: {str(e)}"


# MAIN STREAMLIT APP
def main():
    st.title("🎤 Improved Speech Recognition App")
    st.write("Enhancements: API Selection • Language Choice • Pause/Resume • Save to File")

    # API SELECTION
    api_choice = st.selectbox(
        "Choose Speech Recognition API:",
        ["Google", "Sphinx (Offline)"]
    )

    # LANGUAGE SELECTION
    language = st.selectbox(
        "Choose Language:",
        [
            ("English (US)", "en-US"),
            ("English (UK)", "en-GB"),
            ("French", "fr-FR"),
            ("Spanish", "es-ES"),
            ("Swahili", "sw-KE"),
        ],
        format_func=lambda x: x[0]
    )[1]

    # PAUSE/RESUME FEATURE
    pause_duration = st.slider(
        "Pause Threshold (control pause & resume)",
        min_value=0.5,
        max_value=2.0,
        value=0.8,
        step=0.1,
        help="Lower = stops faster, Higher = lets you pause while talking"
    )

    st.write("---")

    # BUTTON TO START RECORDING
    if st.button("🎙 Start Recording"):
        text = transcribe_speech(api_choice, language, pause_duration)
        st.success("Transcription Complete:")
        st.write(text)

        # SAVE TO FILE OPTION
        if text and "Sorry" not in text:
            if st.button("💾 Save Transcription to File"):
                filename = f"transcription_{int(time.time())}.txt"

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)

                st.success(f"Saved successfully as: {filename}")


if __name__ == "__main__":
    main()
