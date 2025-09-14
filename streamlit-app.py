# file: pos_app.py
import streamlit as st
# import nltk
import pandas as pd
import os

# Siapkan resource NLTK (sekali saja, jangan taruh di loop)
# nltk.download("punkt")

# ========== Fungsi Dummy POS Tagger ==========
def pos_tag_dictionary(tokens):
    # contoh sederhana: semua kata jadi NOUN
    return [(t, "NOUN") for t in tokens]

def pos_tag_rule_based(tokens):
    # rule base dummy
    result = []
    for t in tokens:
        if t.endswith("ing"):
            result.append((t, "VERB"))
        else:
            result.append((t, "NOUN"))
    return result

def pos_tag_hmm(tokens):
    # sementara pakai NLTK default HMM atau dummy
    return [(t, "HMM_TAG") for t in tokens]

def pos_tag_crf(tokens):
    # dummy CRF, nanti bisa ganti dengan model CRF asli
    return [(t, "CRF_TAG") for t in tokens]

# ========== Streamlit App ==========
st.set_page_config(page_title="POS Tagging Dashboard", layout="wide")

st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Navigasi",
    ["Dashboard", "Upload Corpus", "POS Tagging", "Interactive Demo"]
)

# ---------- Dashboard ----------
if menu == "Dashboard":
    st.title("📊 POS Tagging Dashboard")
    st.write("Statistik token dan POS tag dari corpus.")

    if os.path.exists("uploaded_corpus.txt"):
        with open("uploaded_corpus.txt", "r", encoding="utf-8") as f:
            text = f.read()

        tokens = nltk.word_tokenize(text)
        df = pd.DataFrame(tokens, columns=["Token"])
        st.metric("Jumlah Token", len(tokens))

        st.subheader("Sample Token")
        st.dataframe(df.head(20))
    else:
        st.info("Belum ada corpus di-upload. Silakan upload di menu *Upload Corpus*.")

# ---------- Upload Corpus ----------
elif menu == "Upload Corpus":
    st.title("📂 Upload Corpus")
    uploaded_file = st.file_uploader("Upload file TXT", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        with open("uploaded_corpus.txt", "w", encoding="utf-8") as f:
            f.write(text)
        st.success("Corpus berhasil diupload!")

# ---------- POS Tagging ----------
elif menu == "POS Tagging":
    st.title("⚙️ Proses POS Tagging")
    method = st.selectbox(
        "Pilih Metode:",
        ["Dictionary", "Rule-based", "HMM", "CRF"]
    )

    if os.path.exists("uploaded_corpus.txt"):
        with open("uploaded_corpus.txt", "r", encoding="utf-8") as f:
            text = f.read()

        tokens = nltk.word_tokenize(text)

        if method == "Dictionary":
            tagged = pos_tag_dictionary(tokens)
        elif method == "Rule-based":
            tagged = pos_tag_rule_based(tokens)
        elif method == "HMM":
            tagged = pos_tag_hmm(tokens)
        else:
            tagged = pos_tag_crf(tokens)

        df = pd.DataFrame(tagged, columns=["Token", "POS Tag"])
        st.dataframe(df.head(50))
    else:
        st.info("Belum ada corpus di-upload.")

# ---------- Interactive Input/Output ----------
elif menu == "Interactive Demo":
    st.title("💬 Interactive POS Tagging")
    sentence = st.text_area("Masukkan kalimat:", "Saya sedang belajar pemrograman.")

    method = st.radio(
        "Pilih Metode:",
        ["Dictionary", "Rule-based", "HMM", "CRF"],
        horizontal=True
    )

    if st.button("Proses"):
        tokens = nltk.word_tokenize(sentence)

        if method == "Dictionary":
            tagged = pos_tag_dictionary(tokens)
        elif method == "Rule-based":
            tagged = pos_tag_rule_based(tokens)
        elif method == "HMM":
            tagged = pos_tag_hmm(tokens)
        else:
            tagged = pos_tag_crf(tokens)

        st.subheader("Hasil POS Tagging")
        for word, tag in tagged:
            st.markdown(f"🔹 **{word}** → `{tag}`")
