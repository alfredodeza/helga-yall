import re
import random
from helga.plugins import match
from helga import log, settings

logger = log.getLogger(__name__)

verbose = [
    (
        '/me is',
    ),
    (
       'overwhelmed', 'overpowered', 'swept over', 'overcomed', 'overtaken',
       'astonished', 'flabbergasted', 'swamped', 'engulfed', 'inundated',
       'overthrown',
    ),
    (
        'by the',
    ),
    (
        'vehement', 'violent', 'strong', 'intense', 'concentrated', 'profound',
        'staturated', 'fierce', 'tearing', 'aggravated', 'exasperated',
        'fortified', 'hefty', 'muscular', 'powerful', 'sinewy', 'reinforced',
        'strengthened', 'brawny', 'equipotent', 'multipotent', 'substantial',
        'ironlike', 'respectable', 'sizable', 'sizeable', 'emphatic'
    ),
    (
        'protestation', 'affirmation', 'verification', 'assertion',
        'declaration', 'asseveration', 'expression', 'exaltation',
        'intoxication', 'elation', 'reverberation', 'elevation', 'inebriation',
        'glorification', 'proclamation',
    ),
    (
        'of',
    ),
    (
        'gratitude', 'thankfulness', 'appreciation', 'divinity', 'goodness',
        'admiration', 'contribution', 'gratefulness', 'generosity', 'worthy',
        'assistance', 'esteem',
    )
]

succinct = [
    (
        '',
    ),
    (
        'awwww...', '\o/', 'weeeeeeee!',
        '', '', '', '', '', '', '',
        # the phrase that started the verbose section :)
        # 'overwhelmed by your vehement protestations of gratitude'
    ),
    (
        'no problem',
        'you got it', 'anything you say',
        'sure thing',
        '**hugs**', '**kisses**', '*hugs and kisses*', 'anytime',
        'roger roger', 'de nada', 'certainly',
        'por supuesto', 'of course my horse', 'so you *do* appreciate me',
        'absolutely',
    ),
    (
        '!', ':)', ';)',
        '', '', '', '', '', '', '',
    )
]


def is_getting_thanked(message, botnick=None):
    botnick = botnick or settings.NICK
    nice_adjectives = '|'.join([
        'great',
        'awesome',
        'fantastic',
        'cool',
        'da bomb',
        'stupendous',
        'impressive',
        ]
    )
    thanks_regex = r'(({botnick}:|{botnick})+\s+(is|you are)+\s+({nice_adjectives})+|(.*)(is|you are)+\s+({nice_adjectives})+\s+({botnick})+|^({nice_adjectives})+\s+({botnick})+)'.format(
            nice_adjectives=nice_adjectives,
            botnick=botnick)
    thanks_compiled = re.compile(thanks_regex)
    return thanks_compiled.match(message)


def p_random_composer(phrases, nick=''):
    """
    :param phrases: an iterable of iterables with phrases.
    """
    if nick:
        phrase = '%s:' % nick
    else:
        phrase = ''
    for item in phrases:
        phrase += random.choice(item) + ' '
    print phrase
    return phrase


@match(is_getting_thanked, priority=0)
def yall(client, channel, nick, message, matches):
    """
    Match a user saying thanks to the bot, reply accordingly like a tamaulipan
    after getting a free burrito.
    """
    use_nick = random.choice([True, False, False, False])
    if use_nick:
        phrase = p_random_composer(succinct, nick)
    else:
        phrase = p_random_composer(verbose)
    return phrase
