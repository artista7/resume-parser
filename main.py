import fire
import spacy

from modules.spellchecker import SpellChecker
from modules.parser.pdf_parser import PDFParser

def main(resume_file):
    parser = PDFParser(resume_file)
    spell_checker = SpellChecker()
    possible_spelling_errors = spell_checker.check_misspelled(parser.text)
    parsed_dict = {"email": parser.email,
                   "name": parser.name,
                   "phone_no": parser.phone,
                   "sections": parser.sections,
                   "possible_spelling_errors":possible_spelling_errors}
    return parsed_dict



if __name__ == '__main__':
    fire.Fire(main)
    # parsed_info = main("test/sample-resume.pdf")
    # pprint(parsed_info)
