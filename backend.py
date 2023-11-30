from flask import Flask, jsonify, render_template, request
from main import TextEmbedding

app = Flask(__name__)

spacy_model = "en_core_web_lg"
courses_csv = "combined_courses_preprocessed.csv"
with_preprocessing = True
load_embeddings = True
save_embeddings = False
textEmbedding = TextEmbedding(spacy_model, courses_csv, load_embeddings=load_embeddings, save_embeddings=save_embeddings)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    user_input = request.form['userInput']
    # Process the received data
    if user_input == '':
        return 'Please enter some valid text'

    class_list = textEmbedding.get_similar_course_titles(user_input, True)
    # Send the processed data back as a response
    return jsonify(class_list)

if __name__ == '__main__':
    app.run(debug=True)
