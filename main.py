import spacy
import pandas as pd
import time
import pickle
import os
from course_data.preprocessor import TextPreprocessor

class TextEmbedding:
    def __init__(self, spacy_model, courses_csv, load_embeddings=True, save_embeddings=True):
        self.nlp_model = spacy.load(spacy_model)
        self.courses_df = pd.read_csv(courses_csv)
        self.preprocessor = TextPreprocessor()
        self.title_weight = .75
        self.desc_weight = .25
        self.courses_df["title"] = self.courses_df["Course Title Preprocessed"]
        self.courses_df["desc"] = self.courses_df["Description Preprocessed"]

        embeddings_file = 'courses_embeddings.pkl'

        t0 = time.time()
        if load_embeddings and os.path.exists(embeddings_file):
            with open(embeddings_file, 'rb') as f:
                self.courses_df = pickle.load(f)
            t1 = time.time()
            print("Loaded embeddings from file in: %.4f seconds" % (t1-t0))
        else:
            self.courses_df["nlp_title"] = self.courses_df["title"].apply(lambda title: self.nlp_model(str(title).lower()))
            self.courses_df["nlp_desc"] = self.courses_df["desc"].apply(lambda desc: self.nlp_model(str(desc).lower()))
            t1 = time.time()
            print("Finished setup in: %.4f seconds" % (t1-t0))

            if save_embeddings:
                with open(embeddings_file, 'wb') as f:
                    pickle.dump(self.courses_df, f)

    def get_similar_course_titles(self, keyword, with_preprocessing=False):
        """ Given a keyword string, return the list of most relevant course titles"""
        if with_preprocessing:
            keyword = self.preprocessor.preprocess(keyword)

        # Find exact matches first
        keyword = keyword.lower()
        print("Finding similarities to keyword string: " + keyword)
        print("Exact matches:")
        copy_df = self.courses_df.copy()
        contains_keyword = copy_df[copy_df["title"].str.lower().fillna("").str.contains(keyword)]
        print(contains_keyword[["Course Code", "Course Title", "Description"]].head(10))

        print("---------------------------------------------------------------")
        # Find relevant matches using embedding
        print("Relevant matches: ")
        nlp_keyword = self.nlp_model(keyword)
        copy_df["titleXkeyword"] = copy_df["nlp_title"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        copy_df["titleXdesc"] = copy_df["nlp_desc"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        copy_df["similarity"] = self.title_weight * copy_df["titleXkeyword"] + self.desc_weight * copy_df["titleXdesc"]
        copy_df = copy_df.sort_values(by="similarity", ascending=False).head(10)
        
        courses_list = copy_df.to_dict(orient='records')
        formatted_courses = []
        for course in courses_list:
            formatted_course = {
                "course_code": course["Course Code"],
                "title": course["Course Title"],
                "description": course["Description"],
                "similarity": course["similarity"]
            }
            formatted_courses.append(formatted_course)
        return formatted_courses

    def two_keyword_similarity(self, keyword1, keyword2):
        return self.nlp_model(keyword1).similarity(self.nlp_model(keyword2))

# if __name__ == "__main__":
#     spacy_model = "en_core_web_lg"
#     courses_csv = "cs_courses_preprocessed.csv"
#     with_preprocessing = True
#     load_embeddings = False
#     textEmbedding = TextEmbedding(spacy_model, courses_csv, load_embeddings=load_embeddings)

#     while True:
#         keyword = input("Give me a keyword: ")
#         textEmbedding.get_similar_course_titles(keyword, with_preprocessing)
