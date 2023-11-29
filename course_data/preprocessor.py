import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word.isalpha()]
        tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stop_words]

        return ' '.join(tokens)

# Example usage
preprocessor = TextPreprocessor()
example_text = "This is an example sentence demonstrating text preprocessing."
processed_text = preprocessor.preprocess(example_text)
print(processed_text)
