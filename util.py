import re

illegal_character_replacements = {
    '~': '-',
    '#': 'Num.',
    '%': 'Pct.',
    '&': 'And',
    '*': '-',
    '{': '[',
    '}': ']',
    '\\': '_',
    ':': '-',
    '<': '[',
    '>': ']',
    '?': '',
    '/': '_',
    '+': 'Plus',
    '|': '_',
    '"': '\'',
}

common_censoring_replacements = {
    'f__k': 'fuck',
    'F__k': 'Fuck',
    'F__K': 'FUCK'
}


def replace_illegal_characters(raw_string):
    cleansed_string = ''
    chars = list(raw_string)
    for char in chars:
        if char in illegal_character_replacements.keys():
            cleansed_string = cleansed_string + illegal_character_replacements[char]
        else:
            cleansed_string = cleansed_string + char
    return cleansed_string


def strip_explicit_text(raw_string):
    return raw_string.replace(' [Explicit]', '').replace(' (Explicit)', '')


def clean_file_name(name):
    pattern = re.compile('(\d+\s-\s)(.+)(\.mp3)')
    return replace_common_censoring(strip_explicit_text(pattern.sub('', ' '.join(name.strip('.mp3').split()[2:]))))


def replace_common_censoring(censored_string):
    uncensored_string = censored_string
    for censored_word in common_censoring_replacements:
        if censored_word in uncensored_string:
            uncensored_string = uncensored_string.replace(censored_word, common_censoring_replacements[censored_word])
    return uncensored_string


def is_string_not_blank(raw_string):
    if raw_string and raw_string.strip():
        # raw_string is not None AND raw_string is not empty or blank
        return True
    # raw_string is None OR raw_string is empty or blank
    return False


def clean_title_starting_with_the(raw_title):
    if raw_title is None:
        return None
    else:
        if raw_title.endswith(", The"):
            return "The " + raw_title.replace(", The", "")
        else:
            return raw_title


def get_track_number_from_file_name(file_name):
    m = re.search('(\d+).+', file_name)
    if m:
        return m.group(1)
    else:
        return ''
