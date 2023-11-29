import spacy
import pandas as pd
import time
from course_data.preprocessor import TextPreprocessor

# nlp = spacy.load('en_core_web_lg')
# classes =  ["architecture", "security", "AI", "ML", "algorithms", "data science", "databases", "graphics", "operating systems"]
# nlp_classes = [nlp(c) for c in classes]
# nlp_keyword = nlp("design")

# for c in nlp_classes:
#     similarity = nlp_keyword.similarity(c)
#     print("Similarity between %s and %s is %.4f" % (nlp_keyword, c, similarity))

class TextEmbedding:
    def __init__(self, spacy_model, courses_csv):
        self.nlp_model = spacy.load(spacy_model)
        self.courses_df = pd.read_csv(courses_csv)
        self.preprocessor = TextPreprocessor()
        self.title_weight = .8
        self.desc_weight = .2
        self.courses_df["title"] = self.courses_df["Course Title"]
        self.courses_df["desc"] = self.courses_df["Description"]
        t0 = time.time()
        self.courses_df["nlp_title"] = self.courses_df["title"].apply(lambda title: self.nlp_model(str(title).lower()))
        t1 = time.time()
        print("Finished titles in: %.4f seconds" % (t1-t0))
        self.courses_df["nlp_desc"] = self.courses_df["desc"].apply(lambda desc: self.nlp_model(str(desc).lower()))
        t1 = time.time()
        print("Finished setup in: %.4f seconds" % (t1-t0))

    def get_similar_course_titles(self, keyword, with_preprocessing=False):
        """ Given a keyword string, return the list of most relevant course titles"""
        # Start by processing the input word
        if with_preprocessing:
            processed_text = self.preprocessor.preprocess(keyword)

        print("Finding similarities to keyword string: " + keyword)
        t = time.time()
        nlp_keyword = self.nlp_model(keyword.lower())
        self.courses_df["titleXkeyword"] = self.courses_df["nlp_title"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["titleXdesc"] = self.courses_df["nlp_desc"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["similarity"] = self.title_weight * self.courses_df["titleXkeyword"] + self.desc_weight * self.courses_df["titleXdesc"]
        self.courses_df = self.courses_df.sort_values(by="similarity", ascending=False)
        print(self.courses_df[["Course Code", "title", "desc", "similarity"]].head(25))
        print("Time to find similarity between %s and catalog: %.4f" % (keyword, time.time() - t))

spacy_model = "en_core_web_lg"
courses_csv = "cs_courses.csv"
textEmbedding = TextEmbedding(spacy_model, courses_csv)
while True:
    keyword = input("Give me a keyword: ")
    textEmbedding.get_similar_course_titles(keyword, with_preprocessing=True)

# keywords = ["vision", "neural networks", "probability", "systems", "SQL"]
# for keyword in keywords:
#     textEmbedding.get_similar_course_titles(keyword)
