from reviews import preprocess as pp


class TestTextCleaning:
    def test_urls(self):
        res = pp.remove_urls(
            "https://www.amazon.it/Zotac-GAMING-GEFORCE-3090-ZT-A30910B-10P/dp/B09X3N1W96/ref=sr_1_1"
            "?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1O7FAD1QSAMN1&keywords=3090+ti&qid"
            "=1666970846&qu=eyJxc2MiOiI1LjU1IiwicXNhIjoiNC40NiIsInFzcCI6IjMuMzQifQ%3D%3D&sprefix"
            "=3090+ti%2Caps%2C122&sr=8-1"
        )
        assert res == ""

        res = pp.remove_urls("https://www.amazon.it/ref=nav_logo")
        assert res == ""

        res = pp.remove_urls("www.amazon.it")
        assert res == ""

        res = pp.remove_urls("amazon.it")
        assert res == "amazon.it"

    def test_spaces(self):
        res = pp.remove_spaces("A  text with     some  spaces.")
        assert res == "A text with some spaces."

        res = pp.remove_spaces("    ")
        assert res == " "

        res = pp.remove_spaces("")
        assert res == ""

    def test_punctuation(self):
        # commas

        res = pp.fix_punctuation("A,B")
        assert res == "A, B"

        res = pp.fix_punctuation("A,B,")
        assert res == "A, B, "

        res = pp.fix_punctuation("A,,B")
        assert res == "A, , B"

        # dots

        res = pp.fix_punctuation("A.B.")
        assert res == "A.B."

        res = pp.fix_punctuation("AA.B")
        assert res == "AA. B"

        res = pp.fix_punctuation("file.txt")
        assert res == "file.txt"

        res = pp.fix_punctuation("file.1.txt")
        assert res == "file.1.txt"

        res = pp.fix_punctuation("one file.two folders")
        assert res == "one file. two folders"

    def test_special_chars(self):
        res = pp.space_special_chars("a+b")
        assert res == "a b"

        res = pp.space_special_chars("10/11/12")
        assert res == "10 11 12"

        res = pp.space_special_chars("a-b-c")
        assert res == "a b c"

        res = pp.space_special_chars("a-b-")
        assert res == "a b "

        res = pp.space_special_chars("a..b")
        assert res == "a b"

        res = pp.space_special_chars("a.....b")
        assert res == "a b"

    def test_repetitions(self):
        res = pp.remove_repetitions("a wooord")
        assert res == "a woord"

        res = pp.remove_repetitions("   ")
        assert res == "   "
