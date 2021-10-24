word = input("Enter word: ")


def test_short_word():
    assert len(word) < 15, "Entered word is more than 15 symbols"
