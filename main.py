import spacy
import pandas as pd
import time
from course_data.preprocessor import TextPreprocessor

class TextEmbedding:
    def __init__(self, spacy_model, courses_csv):
        self.nlp_model = spacy.load(spacy_model)
        self.courses_df = pd.read_csv(courses_csv)
        self.preprocessor = TextPreprocessor()
        self.title_weight = .75
        self.desc_weight = .25
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
            keyword = self.preprocessor.preprocess(keyword)

        # Find exact matches first
        keyword = keyword.lower()
        print("Finding similarities to keyword string: " + keyword)
        print("Exact matches:")
        contains_keyword = self.courses_df[self.courses_df["title"].str.lower().str.contains(keyword)]
        print(contains_keyword[["Course Code", "title", "desc"]].head(10))

        print("---------------------------------------------------------------")
        # Find relevant matches using embedding
        print("Relevant matches: ")
        nlp_keyword = self.nlp_model(keyword)
        self.courses_df["titleXkeyword"] = self.courses_df["nlp_title"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["titleXdesc"] = self.courses_df["nlp_desc"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["similarity"] = self.title_weight * self.courses_df["titleXkeyword"] + self.desc_weight * self.courses_df["titleXdesc"]
        self.courses_df = self.courses_df.sort_values(by="similarity", ascending=False)
        print(self.courses_df[["Course Code", "title", "desc", "similarity"]].head(10))

    def two_keyword_similarity(self, keyword1, keyword2):
        return self.nlp_model(keyword1).similarity(self.nlp_model(keyword2))

if __name__ == "__main__":
    spacy_model = "en_core_web_md"
    courses_csv = "cs_courses.csv"
    with_preprocessing = False
    textEmbedding = TextEmbedding(spacy_model, courses_csv)

    while True:
        keyword = input("Give me a keyword: ")
        textEmbedding.get_similar_course_titles(keyword, with_preprocessing)

    # keywords = ["vision", "neural networks", "probability", "systems", "SQL"]
    # for keyword in keywords:
    #     textEmbedding.get_similar_course_titles(keyword)
