import re
import nltk
from constants import PHONE_PATTERN, EMAIL_PATTERN, NAME_GRAMMAR

def extract_name(text):
    # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
    # Note the correction to the rule. Change has been made later.
    chunkParser = nltk.RegexpParser(NAME_GRAMMAR)
    all_chunked_tokens = []
    nameHits = []
    lines = text.split('\n')
    for tagged_tokens in lines:
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(tagged_tokens))
        # Creates a parse tree
        if len(tagged_tokens) == 0: continue # Prevent it from printing warnings
        chunked_tokens = chunkParser.parse(tagged_tokens)
        all_chunked_tokens.append(chunked_tokens)
        for subtree in chunked_tokens.subtrees():
            #  or subtree.label() == 'S' include in if condition if required
            if subtree.label() == 'NAME':
                for ind, leaf in enumerate(subtree.leaves()):
                    if 'NN' in leaf[1]:
                        # Case insensitive matching, as indianNames have names in lowercase
                        # Take only noun-tagged tokens
                        # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                        # Pick upto 3 noun entities
                        hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                        # Check for the presence of commas, colons, digits - usually markers of non-named entities
                        nameHits.append(hit)
                        # Need to iterate through rest of the leaves because of possible mis-matches
    return nameHits[0].strip() if nameHits else None


def extract_phone_num(text):
    '''
    Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
    Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
    Modules required: clock from time, code.
    '''
    inputString = text
    number = None
    try:
        pattern = re.compile(PHONE_PATTERN)
        match = pattern.findall(inputString)
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
        match = [re.sub(r'\D$', '', el).strip() for el in match]
        match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
        try:
            for el in list(match):
                if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                for x in el.split("-"):
                    try:
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                match.remove(el)
                    except:
                        pass
        except:
            pass
        number = match
    except:
        pass
    return number

def extract_email(text):
    pattern = re.compile(EMAIL_PATTERN)
    match = pattern.findall(text)
    return match[0].strip() if match else None
