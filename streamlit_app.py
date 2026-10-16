import streamlit as st
import requests

st.set_page_config(page_title="Miguel's language site", page_icon="🌍", layout="wide")

LESSONS = {
    "Italian": {"phrase": "Ciao, come stai?", "pronunciation": "chow, KOH-meh stye", "meaning": "Hi, how are you?", "words": [("grazie", "thank you"), ("buongiorno", "good morning"), ("amico", "friend"), ("per favore", "please"), ("acqua", "water"), ("casa", "home")]},
    "Spanish": {"phrase": "Hola, ¿cómo estás?", "pronunciation": "OH-lah, KOH-moh es-TAHS", "meaning": "Hi, how are you?", "words": [("gracias", "thank you"), ("buenos días", "good morning"), ("amigo", "friend"), ("por favor", "please"), ("agua", "water"), ("casa", "home")]},
    "French": {"phrase": "Bonjour, comment ça va ?", "pronunciation": "bohn-ZHOOR, koh-MAHN sah vah", "meaning": "Hello, how are you?", "words": [("merci", "thank you"), ("bonjour", "hello"), ("ami", "friend"), ("s’il vous plaît", "please"), ("eau", "water"), ("maison", "home")]},
    "German": {"phrase": "Hallo, wie geht es dir?", "pronunciation": "HAH-loh, vee gate ess deer", "meaning": "Hello, how are you?", "words": [("danke", "thank you"), ("Guten Morgen", "good morning"), ("Freund", "friend"), ("bitte", "please"), ("Wasser", "water"), ("Haus", "home")]},
    "Japanese": {"phrase": "こんにちは、元気ですか？", "pronunciation": "kon-ni-chi-wa, gen-ki des-ka", "meaning": "Hello, how are you?", "words": [("ありがとう", "thank you"), ("おはよう", "good morning"), ("友達", "friend"), ("お願いします", "please"), ("水", "water"), ("家", "home")]},
}

for name, value in {"saved": [], "repetitions": 0, "word_offset": 0}.items():
    if name not in st.session_state:
        st.session_state[name] = value

@st.cache_data(ttl=3600, show_spinner=False)
def wikipedia_summary(language):
    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{language}_language",
            timeout=8,
            headers={"User-Agent": "MiguelsLanguageSite/1.0"},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("title", f"{language} language"), data.get("extract"), data.get("content_urls", {}).get("desktop", {}).get("page")
    except requests.RequestException:
        return f"About {language}", "Live language context is unavailable right now. Your lesson is still ready to use.", None

def save_item(word, meaning, language):
    item = {"word": word, "meaning": meaning, "language": language}
    if item not in st.session_state.saved:
        st.session_state.saved.append(item)

st.title("🌍 Miguel's language site")
st.caption("A simple place to explore a language, one useful phrase at a time.")

language = st.selectbox("I want to learn", list(LESSONS), key="language")
lesson = LESSONS[language]

main, mission = st.columns([3, 2])
with main:
    st.subheader("Today's phrase")
    st.markdown(f"## {lesson['phrase']}")
    st.caption(lesson["pronunciation"])
    st.write(f"**“{lesson['meaning']}”**")
    if st.button("Save phrase", type="primary"):
        save_item(lesson["phrase"], lesson["meaning"], language)
        st.toast("Phrase saved")

with mission:
    st.subheader("Small mission")
    st.write("Say today’s phrase aloud three times.")
    st.progress(st.session_state.repetitions / 3)
    st.caption(f"{st.session_state.repetitions} of 3 repetitions")
    label = "Start again" if st.session_state.repetitions == 3 else "I said it once"
    if st.button(label):
        st.session_state.repetitions = 0 if st.session_state.repetitions == 3 else st.session_state.repetitions + 1
        st.rerun()

st.divider()
st.subheader("From the web")
with st.spinner("Finding fresh context from Wikipedia…"):
    title, summary, source = wikipedia_summary(language)
st.markdown(f"**{title}**")
st.write(summary)
if source:
    st.link_button("Read on Wikipedia ↗", source)

st.divider()
left, right = st.columns([4, 1])
with left:
    st.subheader("Build your word bank")
with right:
    if st.button("Refresh words ↻"):
        st.session_state.word_offset = (st.session_state.word_offset + 3) % len(lesson["words"])
        st.rerun()

words = lesson["words"]
offset = st.session_state.word_offset
selection = (words + words)[offset:offset + 3]
word_columns = st.columns(3)
for column, (word, meaning) in zip(word_columns, selection):
    with column:
        st.markdown(f"### {word}")
        st.write(meaning)
        if st.button("+ Save", key=f"save-{language}-{word}"):
            save_item(word, meaning, language)
            st.toast(f"Saved {word}")

st.divider()
st.subheader("Saved words & phrases")
if not st.session_state.saved:
    st.info("Nothing saved yet. Add words and phrases from your lesson.")
for index, item in enumerate(st.session_state.saved):
    item_col, remove_col = st.columns([6, 1])
    with item_col:
        st.write(f"**{item['word']}** — {item['meaning']}  ")
        st.caption(item["language"])
    with remove_col:
        if st.button("Remove", key=f"remove-{index}"):
            st.session_state.saved.pop(index)
            st.rerun()
