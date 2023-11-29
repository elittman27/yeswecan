import spacy
import pandas as pd
import time

# nlp = spacy.load('en_core_web_lg')
# classes =  ["architecture", "security", "AI", "ML", "algorithms", "data science", "databases", "graphics", "operating systems"]
# nlp_classes = [nlp(c) for c in classes]
# nlp_keyword = nlp("design")

# for c in nlp_classes:
#     similarity = nlp_keyword.similarity(c)
#     print("Similarity between %s and %s is %.4f" % (nlp_keyword, c, similarity))

class TextEmbedding:
    def __init__(self):
        self.nlp_model = spacy.load('en_core_web_lg')
        self.courses_df = pd.read_csv("combined_courses.csv")
        self.title_weight = .8
        self.desc_weight = .2
        self.courses_df["title"] = self.courses_df["Course Title"]
        self.courses_df["desc"] = self.courses_df["Description"]
        t0 = time.time()
        self.courses_df["nlp_title"] = self.courses_df["title"].apply(lambda title: self.nlp_model(title))
        self.courses_df["nlp_desc"] = self.courses_df["desc"].apply(lambda desc: self.nlp_model(desc))
        t1 = time.time()
        print("Time to vectorize all the titles and descriptions: %.4f" % (t1-t0))
        print("Time per title and desc: %.4f" % ((t1 - t0) / len(self.courses_df)))

    def get_similar_course_titles(self, keyword):
        """ Given a keyword string, return the list of most relevant course titles"""
        print("Finding similarities to keyword string: " + keyword)
        t = time.time()
        nlp_keyword = self.nlp_model(keyword)
        self.courses_df["titleXkeyword"] = self.courses_df["nlp_title"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["titleXdesc"] = self.courses_df["nlp_desc"].apply(lambda nlp_v: nlp_v.similarity(nlp_keyword))
        self.courses_df["similarity"] = self.title_weight * self.courses_df["titleXkeyword"] + self.desc_weight * self.courses_df["titleXdesc"]
        self.courses_df = self.courses_df.sort_values(by="similarity", ascending=False)
        print(self.courses_df[["Course Code", "title", "desc", "similarity"]].head(5))
        print("Time to find similarity between %s and catalog: %.4f" % (keyword, time.time() - t))

textEmbedding = TextEmbedding()
while True:
    keyword = input("Give me a keyword: ")
    textEmbedding.get_similar_course_titles(keyword)

# keywords = ["vision", "neural networks", "probability", "systems", "SQL"]
# for keyword in keywords:
#     textEmbedding.get_similar_course_titles(keyword)


