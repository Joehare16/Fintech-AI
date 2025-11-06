from news_cleaner.cleaner import clean_text, clean_dataframe

import pandas as pd

class Test_clean_text:

    def test_whitespace_valid(self):

        #takes in a string input and should return it with no white space

        whiteSpaceString = " This  is    a   test   string   "

        whiteSpaceRes = clean_text(whiteSpaceString)

        assert whiteSpaceRes == "This is a test string"

    def test_removeHtml_valid(self):

        htmlStr = "<h> This is a test heading </h>"

        htmlStrRes = clean_text(htmlStr)

        assert htmlStrRes == "This is a test heading"



class Test_clean_dataframe:

    # takes in a data frame

    def test_dropdupes_valid(self):

        df = pd.DataFrame({
            "title": ["This is a dupe", None, "This is a dupe"]
        })

        dfcleaned = clean_dataframe(df)

        assert len(dfcleaned) == 1
        assert dfcleaned["title"].tolist() == ["this is a dupe"]
    

    def test_dropdupes_boundary(self):

        df = pd.DataFrame({
            "title": ["t1", "t2"],
            "content": ["This is almost the same", "ThIs IS aLmost The saME"] 
        })

        dfcleaned = clean_dataframe(df)

        assert len(dfcleaned) == 1
        assert dfcleaned["content"].tolist() == ["this is almost the same"]

    def test_dropempty(self):

        df = pd.DataFrame({
            "title": ["Valid Title", None, ""],
            "content": ["Valid Content", None, ""]
        })

        dfcleaned = clean_dataframe(df)

        assert dfcleaned["title"].tolist() == ["valid title"]
        assert dfcleaned["content"].tolist() == ["valid content"]

    def test_all_valid(self):

        df = pd.DataFrame({
            "title": ["  <h1>Title One</h1>  ", "Title Two", None, "Title One"],
            "content": ["  <p>Content One</p>  ", "Content Two", "Content Three", "  <p>Content One</p>  "],
            "description": [None, "<div>Description Two</div>", "<div>Description Three</div>", None]
        })

        dfcleaned = clean_dataframe(df)

        assert dfcleaned["title"].tolist() == ["title one", "title two", pd.NA]
        assert dfcleaned["content"].tolist() == ["content one", "content two","content three"]
        assert dfcleaned["description"].tolist() == [pd.NA, "description two","description three"]
    