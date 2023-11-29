import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure the necessary NLTK components are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        custom_stop_words = ['This', 'this', 'Introduction', 'introduction', 'These', 'these',
                             'Topic', 'topic', 'Department', 'department',
                             'How', 'how', 'The', 'the', 'Course', 'course',
                             'Students', 'students', 'student', 'Student', 'Including', 'including', 
                             'Faculty', 'faculty', 'Instructor', 'instructor', 'Instructors', 'instructors', 
                             'A', 'We', 'It', 'In', 'also', 'use', 'An', 'Topics']
        self.stop_words.update(custom_stop_words)

    def preprocess(self, text):
        # Check if the text is a string
        if not isinstance(text, str):
            return ''
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in self.stop_words]
        return ' '.join(tokens)

# Example usage
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    example_text = "This is an example sentence demonstrating text preprocessing course."
    processed_text = preprocessor.preprocess(example_text)
    print(processed_text)
