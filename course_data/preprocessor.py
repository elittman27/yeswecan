import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure the necessary NLTK components are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        custom_stop_words = ['This', 'Introduction', 'These', 'Topic', 'Department', 'How', 'The', 'Course']
        self.stop_words.update(custom_stop_words)

    def preprocess(self, text):
        # Check if the text is a string
        if not isinstance(text, str):
            return ''
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in self.stop_words]
        return ' '.join(tokens)

# Example usage
preprocessor = TextPreprocessor()
example_text = "this is an example sentence demonstrating text preprocessing."
processed_text = preprocessor.preprocess(example_text)
print(processed_text)
