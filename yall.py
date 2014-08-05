import re
import random
from helga.plugins import match
from helga import log, settings

logger = log.getLogger(__name__)

responses = {
    'good': {
        'verbose' : [
            (
                'is',
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
        ],

        'succinct' : [
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
        ],
    },
    'complain': {
        'verbose' : [
            (
                'is',
            ),
            (
               'sad', 'distressed', 'sorry', 'so heavyhearted', 'so heartsick',
               'forlorn', 'astonished', 'dejected', 'swamped', 'woebegone', 'weeping',
               'overthrown', 'troubled', 'hurting', 'pensive of sorts', 'in grief',
               'mournful', 'upset', 'dolent', 'heartbroken', 'tear-jerking', 'wretched',
               'dejected', 'dispirited', 'crestfallen', 'in the toilet', 'in a blue funk',
               'torn',
            ),
            (
                'by the',
            ),
            (
                'vehement', 'violent', 'strong', 'intense', 'concentrated', 'profound',
                'staturated', 'fierce', 'tearing', 'aggravated', 'exasperated',
                'maniacal', 'hefty', 'muscular', 'inflamed', 'sinewy', 'reinforced',
                'vicious', 'savage', 'enraged', 'multipotent', 'substantial',
                'ungovernable', 'berserk', 'riotous', 'insurrectionary', 'turbulent',
                'rampageous', 'out of control', 'mutinous', 'anarchic', 'rowdy',
                'obstreperous', 'rowdydowdy', 'rumbustious', 'uproarious', 'vociferous',
                'raucous',
            ),
            (
                'protestation', 'disapproval', 'gripe', 'remonstrance',
                'declaration', 'asseveration', 'expression', 'squawk',
                'intoxication', 'dislike', 'reverberation', 'disesteem', 'revilement',
                'disapprobation', 'proclamation', 'repugnancy', 'revilement',
            ),
            (
                'of',
            ),
            (
                'censure', 'denouncement', 'disapproval', 'proscription', 'reproach',
                'denunciation', 'judgement', 'blame', 'reprobation', 'damnation',
                'assistance', 'acumen', 'apprehension', 'foreboding', 'mistrust',
                'castigation', 'disparagement', 'ostracism'
            )
        ],

        'succinct' : [
            (
                '',
            ),
            (
                'oh noes...', 'errr', 'boooo!',
                'O_O', 'o_O', '', '', '', '', '',
            ),
            (
                'we have a problem now',
                'come on now', 'that was just terrible',
                'I feel like I should go now',
                'I should get a beer', 'so you do *not* appreciate me?',
                'never again I guess',
            ),
            (
                '!', ':(',
                '', '', '', '', '', '', '',
            )
        ],
    }
}


def is_getting_harassed(message, botnick=None):
    botnick = botnick or settings.NICK
    bad_adjectives = '|'.join([
        'bad',
        'terrible',
        'horrible',
        'uncool',
        'not cool',
        'the worst',
        'so stupid',
        'stupid',
        'suck',
        'blow',
        'broken',
        'so broken',
        ]
    )
    harass_regex = r'(((.*){botnick}:|(.*){botnick})+\s+(is|you|you are)+\s+({bad_adjectives})+|(.*)(is|you are|you)+\s+({bad_adjectives})+\s+(({botnick}:|{botnick}))+|^({bad_adjectives})+\s+({botnick})+|^({botnick}:|{botnick})+\s+({bad_adjectives})+)+'.format(
            bad_adjectives=bad_adjectives,
            botnick=botnick)
    harass_compiled = re.compile(harass_regex)
    return harass_compiled.match(message)


def is_getting_thanked(message, botnick=None):
    botnick = botnick or settings.NICK
    nice_adjectives = '|'.join([
        'great',
        'awesome',
        'fantastic',
        'cool',
        'da bomb',
        'the bomb',
        'the best',
        'stupendous',
        'impressive',
        'rock',
        'thanks',
        'thank you',
        ]
    )
    thanks_regex = r'(((.*){botnick}:|(.*){botnick})+\s+(is|you|you are)+\s+({nice_adjectives})+|(.*)(is|you are)+\s+({nice_adjectives})+\s+(({botnick}:|{botnick}))+|^({nice_adjectives})+\s+({botnick})+|^({botnick}:|{botnick})+\s+({nice_adjectives})+)+'.format(
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


def is_getting_pinged(message, botnick=None):
    return is_getting_thanked(message, botnick) or is_getting_harassed(message, botnick)


@match(is_getting_thanked, priority=50)
def yall(client, channel, nick, message, matches):
    """
    Match a user saying thanks to the bot, reply accordingly like a tamaulipan
    after getting a free burrito.
    """
    # this is really wasteful, should improve this later
    response_type = 'thanks' if is_getting_thanked(message, settings.NICK) else 'complain'
    verbose_response = responses[response_type]['verbose']
    succinct_response = responses[response_type]['succinct']
    use_nick = random.choice([True, False, False, False])
    if use_nick:
        return p_random_composer(succinct_response, nick)
    else:
        # do it like /me
        phrase = p_random_composer(verbose_response)
        return client.me(channel, phrase)
