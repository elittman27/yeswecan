from flask import Flask, jsonify, render_template, request
from main import TextEmbedding

app = Flask(__name__)

spacy_model = "en_core_web_lg"
courses_csv = "combined_courses_preprocessed.csv"
with_preprocessing = True
load_embeddings = True
textEmbedding = TextEmbedding(spacy_model, courses_csv, load_embeddings=load_embeddings)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    user_input = request.form['userInput']
    if user_input == '':
        return 'Please enter some valid text'

    class_list = textEmbedding.get_similar_course_titles(user_input, True)
    return jsonify(class_list)

if __name__ == '__main__':
    app.run(debug=True)
