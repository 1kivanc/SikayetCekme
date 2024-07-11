import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def temizle(text):
    text = re.sub(r'\W', ' ', text)  
    text = re.sub(r'\s+', ' ', text)  
    text = text.lower()  
    return text

def preprocess(text):
    stop_words = set(stopwords.words('turkish'))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return words

def analizEt(dosya_adi):
    with open(dosya_adi, 'r', encoding='utf-8') as file:
        sikayetler = file.readlines()
    
    temiz_sikayetler = [temizle(sikayet) for sikayet in sikayetler]
    islenmis_sikayetler = [preprocess(sikayet) for sikayet in temiz_sikayetler]

    tum_kelimeler = [kelime for sikayet in islenmis_sikayetler for kelime in sikayet]
    kelime_frekansi = Counter(tum_kelimeler)
    
    print("En çok geçen kelimeler:")
    for kelime, frekans in kelime_frekansi.most_common(10):
        print(f"{kelime}: {frekans}")
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(kelime_frekansi)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words=set(stopwords.words('turkish')))
    tfidf_matrix = tfidf_vectorizer.fit_transform(temiz_sikayetler)

    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    tfidf_ranking = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}

    sorted_tfidf_ranking = sorted(tfidf_ranking.items(), key=lambda x: x[1], reverse=True)
    print("\nTF-IDF ile en önemli terimler:")
    for terim, skor in sorted_tfidf_ranking[:10]:
        print(f"{terim}: {skor}")

if __name__ == "__main__":
    analizEt('sikayetler.txt')
