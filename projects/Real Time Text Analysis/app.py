import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

def process_text(text):
    """
    Process the given text and return the word count, character count, word frequency,
    and top 5 most frequent words.

    Parameters
    ----------
    text : str
        The input text to process

    Returns
    -------
    tuple
        A tuple of (word_count, char_count, word_freq, top_words)

    Notes
    -----
    The word frequency is a dictionary where the keys are the words and the
    values are the frequencies of the words. The top 5 most frequent words are
    returned as a list of tuples, where the first element of each tuple is the
    word and the second element is the frequency of the word.

    """
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    char_count = len(text)
    word_freq = Counter(words)
    top_words = word_freq.most_common(5)
    return word_count, char_count, word_freq, top_words

def generate_wordcloud(word_freq):
    """
    Generates and displays a word cloud from a given word frequency dictionary.

    Parameters
    ----------
    word_freq : dict
        A dictionary where the keys are words and the values are their frequencies.

    Notes
    -----
    The word cloud is displayed using Streamlit's pyplot method, and it visualizes 
    the frequency of words with their size in the cloud. Words with higher frequencies 
    appear larger.
    """

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def show():
    """
    Displays a Streamlit app with a text area for the user to enter their text.
    The app then displays statistics about the text, including the number of words and characters.
    It also displays a table of the top 5 most frequent words and a word cloud visualization of the text.
    """
    st.title("📊 Real-Time Text Analysis")
    text = st.text_area("Enter your text here:")
    
    if text:
        word_count, char_count, word_freq, top_words = process_text(text)
        
        st.subheader("📌 Statistics")
        st.write(f"Words: {word_count}")
        st.write(f"Characters: {char_count}")
        
        st.subheader("🔝 Top 5 Most Frequent Words")
        df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
        st.table(df)
        
        st.subheader("☁️ Word Cloud")
        generate_wordcloud(word_freq)
    else:
        st.info("Enter some text to start the analysis!")

