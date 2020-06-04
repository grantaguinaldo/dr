from flask import Flask, jsonify, request, render_template
import pandas as pd
from gensim import corpora, similarities, models
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import requests as r
stop = set(stopwords.words('english'))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def main():
    
    POST_DATA = request.get_json()
    
    INPUT_QUERY = POST_DATA['input_query']
    
    df = pd.read_csv('train.csv')
    df['text'] = df['request'].apply(lambda row: [word for word in simple_preprocess(row) if word not in stop and len(word)>1])
    stop.update(['image','jpg','png','i','ii','iii','iv','v','vi','vii','viii','ix','x'])
    dictionary = corpora.Dictionary(df.text)

    corpus = [dictionary.doc2bow(text) for text in df.text]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=17)
    dictionary = corpora.Dictionary(df['text'])
    corpus = [dictionary.doc2bow(text) for text in df['text']]
    index = similarities.MatrixSimilarity(lsi[corpus], num_features=17)

    vec_bow = dictionary.doc2bow([word for word in simple_preprocess(INPUT_QUERY) if word not in stop and len(word)>1])
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]

    df['sim'] = sims
    return jsonify(df[['sim', 'request', 'url']].sort_values(by='sim', ascending=False).to_dict())

if __name__ == "__main__":
    app.run(debug=True)
