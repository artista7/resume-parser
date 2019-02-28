"""
    Module for parsing PDFs
"""
import fire
from utils import pdf_utils

def parse_pdf_to_lines(pdf_file_path):
    """
        Extract text for PDF

        :param:
            - pdf_file_path: Path of file

        :output:
            - A list containing text for each line
    """
    text_lines = pdf_utils.extract_text(pdf_file_path)
    print(type(text_lines))
    return text_lines

def extract_segments(text_lines):
    """
        Extracts meaningful segments from extracted text
    """
    pass

if __name__ == '__main__':
    fire.Fire(parse_pdf_to_lines)
