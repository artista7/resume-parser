import fire
import spacy

from modules.spellchecker import SpellChecker
from modules.parser.pdf_parser import PDFParser

def main(resume_file):
    parser = PDFParser(resume_file)
    spell_checker = SpellChecker()
    parsed_dict = {"email": parser.email,
                   "name": parser.name,
                   "phone_no": parser.phone,
                   "sections": parser.sections}
    # for section in parsed_dict["sections"]:
    #     from pprint import pprint
    #     pprint(spell_checker.check_misspelled(section['text']))
    return parsed_dict



if __name__ == '__main__':
    from pprint import pprint
    pprint(fire.Fire(main))
    # parsed_info = main("test/sample-resume.pdf")
    # pprint(parsed_info)
