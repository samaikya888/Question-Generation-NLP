from flask import Flask, request, jsonify, json
from flask_cors import CORS

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import random
from typing import Dict, List
import spacy
from sense2vec import Sense2Vec 
from spacy.lang.en import English
import json
import regex as re
import pdfplumber



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def parse_pdf(pdf_data):
    output_string = BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    pdf_file = BytesIO(pdf_data)
    for page in PDFPage.get_pages(pdf_file, check_extractable=True):
        interpreter.process_page(page)

    converter.close()
    text = output_string.getvalue()
    output_string.close()

    return text.decode('utf-8')

@app.route('/api/endpoint', methods=['POST'])
def process_data():
    nlp = spacy.load('en_core_web_sm')
    #print(request.form.get('text'))

    is_text_mode = request.form.get('isTextMode')
    if is_text_mode == 'true':
        text_data = request.form.get('text')
        text=text_data
        print(text)
    else:
        pdf_file = request.files['pdfFile']
        pdf_data = pdf_file.read()  # Read the PDF data

        text = parse_pdf(pdf_data)
        print(text)


    # Tokenize text into words
    tokens = word_tokenize(text)

    # Remove punctuation marks and lowercase the tokens
    tokens = [token.lower() for token in tokens if token not in string.punctuation]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join the preprocessed tokens back into a string
    preprocessed_text = ' '.join(tokens)

    # Print the preprocessed text
    print(preprocessed_text)

    mcqs = []

    doc = nlp(preprocessed_text)
    key_concepts=[]

    for entity in doc.ents:
        if entity.label_ == 'PERSON' or entity.label_ == 'ORG' or entity.label_ == 'NORP' or entity.label_ == 'FAC' or entity.label_ == 'LOC':
            key_concepts.append(entity.text)
    for token in doc:
        if token.pos_ == 'NOUN' and token.dep_ != 'punct':
            key_concepts.append(token.text)
        elif token.pos_ == 'VERB' and token.dep_ != 'aux':
            key_concepts.append(token.lemma_)
    key_concepts = list(set(key_concepts))

    print(key_concepts)

    for concept in key_concepts:
        # Identify sentences that contain the concept
        print("current concept: ", concept)
        sentences = sent_tokenize(text)
        concept_sentences = []
        for sentence in sentences:
            if concept.lower() in sentence.lower():
                print("adding sentence:", sentence)
                concept_sentences.append(sentence)

        # Choose a sentence at random and generate the MCQ
        if concept_sentences:
            sentence = random.choice(concept_sentences)
            print("selected sentence: ", sentence)
            answer = concept.capitalize()
            answer_options = [answer]
            for i in range(3):
                random_word = random.choice(key_concepts)
                if random_word != answer:
                    answer_options.append(random_word.capitalize())
            random.shuffle(answer_options)
            print("answers:", answer_options)
            pattern = re.compile(r'\b' + re.escape(answer.lower()) + r'\b')
            question = pattern.sub('_____', sentence)
            #question = sentence.replace(answer.lower(), '_____')
            mcq = {'question': question, 'options': answer_options, 'answer': answer}
            mcqs.append(mcq)



    # Randomize the order of the MCQs
    random.shuffle(mcqs)
    
    print(len(mcqs))

    # Print the MCQs
    for i, mcq in enumerate(mcqs):
        print(f'{i+1}. {mcq["question"]}')
    for j, option in enumerate(mcq["options"]):
        print(f'{chr(97+j)}. {option}')
    print(f'Answer: {mcq["answer"]}')
    print()

    data = mcqs[:15]
    # print(data)
    return json.dumps(data)

if __name__ == '__main__':
    app.run()
