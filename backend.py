from flask import Flask, render_template, request
from main import TextEmbedding

app = Flask(__name__)

spacy_model = "en_core_web_lg"
courses_csv = "combined_courses_preprocessed.csv"
# courses_csv = "combined_courses_preprocessed.csv"
textEmbedding = TextEmbedding(spacy_model, courses_csv)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    user_input = request.form['userInput']
    # Process the received data
    if user_input == '':
        return 'Please enter some valid text'

    df = textEmbedding.get_similar_course_titles(user_input, True)
    # Send the processed data back as a response
    response = ''
    for ind in df.index:
        response += df['Course Code'][ind] + ':  ' + df['Course Title'][ind] + '\n'

    return response

if __name__ == '__main__':
    app.run(debug=True)
