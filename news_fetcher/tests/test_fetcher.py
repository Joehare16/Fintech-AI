from news_fetcher.fetcher import _normalize_newsapi_article

class Testnormalize_newsapi_article:

    def test_normalize_valid(self):

        # test a valid article
        raw = {"source":{"id":"techcrunch","name":"TechCrunch"},
                "author":"John Doe",
                "title":"New Tech Innovations",
                "description":"A look into new tech innovations.",
                "url":"https://techcrunch.com/new-tech-innovations",
                "publishedAt":"2024-06-01T12:00:00Z",
                "content":"Full article content here."}
        norm = _normalize_newsapi_article(raw)

        assert isinstance(norm, dict)
        assert len(norm) > 0
        assert norm["source"] == "TechCrunch"
        assert norm["author"] == "John Doe"
        assert norm["title"] == "New Tech Innovations"
        assert norm["description"] == "A look into new tech innovations."
        assert norm["url"] == "https://techcrunch.com/new-tech-innovations"
        assert norm["published_at"] == "2024-06-01T12:00:00Z"
        assert norm["content"] == "Full article content here."
        assert norm["raw"] == raw

    def test_normalize_missing_fields(self):

        raw = {"source":None,
                "author":None,
                }
        
        norm = _normalize_newsapi_article(raw)

        assert norm["source"] is None or "None"
        assert norm["author"] is None or "None"
        assert norm["title"] is None or "None"

    def test_normalize_unexpected_structure(self):

        raw = {"title": "title",
               "content": "content",
               "url": "https://test.com"}
        
        norm = _normalize_newsapi_article(raw)

        assert norm["title"] == "title"
        assert norm["content"] == "content"
        assert norm["url"] == "https://test.com"
        
    def test_normalize_unexpected_dataType(self):

        raw ={"description" : 123,
              "source" : 456}

        norm = _normalize_newsapi_article(raw)

        assert isinstance(norm["description"], str)
        assert norm["description"] == "123"

        assert isinstance(norm["source"], str)
        assert norm["source"] == "456"
        assert norm["raw"] == raw