import yall


class TestIsGettingThanked(object):

    def setup(self):
        self.nick = 'alf'

    def test_matches_nick(self):
        message = 'alf you are awesome'
        assert yall.is_getting_thanked(message, self.nick)

    def test_matches_nick_with_colon(self):
        message = 'alf: you are awesome'
        assert yall.is_getting_thanked(message, self.nick)

    def test_match_adjective_first_extra_words(self):
        message = 'you are awesome alf'
        assert yall.is_getting_thanked(message, self.nick)

    def test_match_adjective_first(self):
        message = 'awesome alf'
        assert yall.is_getting_thanked(message, self.nick)

    def test_match_adjective_first_extra_chars(self):
        message = 'awesome alf! the world is coming to and end son'
        assert yall.is_getting_thanked(message, self.nick)


class TestIsNotGettingThanked(object):

    def setup(self):
        self.nick = 'alf'

    def test_does_not_match_adjective_first(self):
        message = 'you are not awesome alf'
        assert yall.is_getting_thanked(message, self.nick) is None

    def test_doesn_not_match_negatives(self):
        message = 'alf you are not awesome'
        assert yall.is_getting_thanked(message, self.nick) is None

    def test_doesn_not_match_negatives_botnick_colon(self):
        message = 'alf: you are not awesome'
        assert yall.is_getting_thanked(message, self.nick) is None


def test_random_composer_succinct():
    # Really just excercising the code here. We rely on random() calls
    for i in range(29):
        assert yall.p_random_composer(yall.succinct, 'alfredo') is not ''
    #assert False


def test_random_composer_verbose():
    # Really just excercising the code here. We rely on random() calls
    for i in range(29):
        assert yall.p_random_composer(yall.verbose, '') is not ''
    #assert False
