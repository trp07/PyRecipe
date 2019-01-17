import pathlib

PARENT_DIR = pathlib.Path(__file__).absolute().parent
PDF_LOGO_PATH = str(PARENT_DIR.joinpath('pyrecipe_pdf_logo.png'))
