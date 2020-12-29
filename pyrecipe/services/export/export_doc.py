"""
PDF file writer for selected recipes to export.

Noteable Classes/Functions:
1.  FileWriter - class that uses the reportlab third-party package to contruct
    PDFs.  This will create the main PDF content.
2.  _write_metadata - function that uses the pikepdf third-party package to
    write the metadata into the PDF created by the FileWriter class.  The
    metadata will be used to write in all the recipe data, so that a file
    previously exported by PyRecipe can be imported to another instance of the
    PyRecipe system (i.e. sharing with family/friends), writing all the shared
    recipes into the local database.

Usage:
1.  export_to_pdf - an all-encompassing function that will both create the
    PDF, using the FileWriter, as well as write the metadata, using the
    _write_metadata function.  Unless specified by the user/system admin, files
    will be writting to the source directory: pyrecipe/tradingpost/exports/
"""

import datetime
import pathlib
from typing import List

from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from pyrecipe import __version__ as VERSION
from pyrecipe.files import FILESDIR
from pyrecipe.storage.shared.recipe_model import RecipeModel


class FileWriter:
    """
    Class that will export a list of given recipes to a PDF for download.
    Each recipe will be separated by a pagebreak.
    Bookmarks will be added in the PDF.
    The Header/Footer will indicate PyRecipe version.

    PARAMS:
    :param filename: (str) optional arg, defaults to "PyRecipe_" + datetime string.

    USES:
    * FileWriter().create_doc(recipes:List['Recipe']), where recipes is a list of
      one or more Recipe instances.

    TODO:
    * Add bookmarks
    """

    EXPORT_DIR = FILESDIR.joinpath("exports/")
    PARENT_DIR = pathlib.Path(__file__).absolute().parent
    PDF_LOGO_PATH = PARENT_DIR.joinpath("images/pyrecipe_pdf_logo.png")

    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir()

    def __init__(self, filename=None):
        self.filename = str(pathlib.Path(FileWriter.EXPORT_DIR).joinpath(filename))
        self.doc = SimpleDocTemplate(self.filename, pagesize=letter)
        self.styles = getSampleStyleSheet()

    def create_doc(self, recipe: RecipeModel) -> int:
        """
        Create a PDF of all given recipes.
        Each recipe is separated by a pagebreak.

        :param recipe: (RecipeModel) a pyrecipe.storage.shared.recipe_model.RecipeModel instances.
        :returns: (int) the number of recipes successfully written to the file.
        """
        recipes_written = 0
        flowables = []

        flowables.append(self._add_section(recipe.name, "Title"))

        timing = "<para align=center>prep time: {:.0f} minutes  |  cook time: {:.0f} minutes</para>".format(
            recipe.prep_time, recipe.cook_time
        )
        flowables.append(Paragraph(timing, style=self.styles["Normal"]))

        servings = "<para align=center>servings: {}</para>".format(recipe.servings)
        flowables.append(Paragraph(servings, style=self.styles["Normal"]))

        flowables.append(self._add_section("Ingredients", "Heading2"))
        for ingredient in recipe.ingredients:
            flowables.append(self._add_bullet(ingredient))

        flowables.append(self._add_section("Directions", "Heading2"))
        for direction in recipe.directions:
            flowables.append(self._add_sequence(recipe.id, direction))
            flowables.append(Spacer(0, 5))

        if recipe.notes:
            flowables.append(self._add_section("Notes", "Heading2"))
            for note in recipe.notes:
                flowables.append(self._add_bullet(note))

        recipes_written += 1
        flowables.append(PageBreak())

        self.doc.build(
            flowables,
            onFirstPage=self._add_header_footer,
            onLaterPages=self._add_header_footer,
        )
        return recipes_written

    def _add_header_footer(self, canvas, doc) -> None:
        """
        Adds the header and footer to the document.

        This function is only meant to be passed to SimpleDocTemplate.build().
        The params are a required signature for the function.

        :param canvas: (reportlab.pdfgen.Canvas) internal param necessary to
            pass to the 'doc.build' method.
        :param doc: (reportlab.platypus.SimpleDocTemplate) internal param necessary to
            pass to the 'doc.build' method.
        """
        width, height = doc.pagesize

        img = Image(FileWriter.PDF_LOGO_PATH, width=76.2, height=20)
        img.wrapOn(canvas, width, height)
        img.drawOn(canvas, 0.5 * inch, 0.5 * inch)

        lower_left = "<font size=8 color=#777777>version: {}</font>".format(VERSION)
        p = Paragraph(lower_left, self.styles["Normal"])
        p.wrapOn(canvas, width, height)
        p.drawOn(canvas, 1.75 * inch, 0.5 * inch)

        lower_right = "<font size=8 color=#777777>{}</font>".format(doc.page)
        p = Paragraph(lower_right, self.styles["Normal"])
        p.wrapOn(canvas, width, height)
        p.drawOn(canvas, 7.0 * inch, 0.5 * inch)

    def _add_section(self, title: str, style: str = "Heading1") -> "flowable":
        """
        Adds a new section/title, such as a Header1.

        :param title: (str) the title for that section.
        :param style: (str) what style/hierarchy to create.
            i.e. Heading1, Heading2, Normal, etc.
        :returns: (flowable) the reportlab flowable to append to the document.
        """
        text = "{}".format(title)
        return Paragraph(text, style=self.styles[style])

    def _add_bullet(self, item: str, style: str = "Normal") -> "flowable":
        """
        Adds the given item as a bullet.

        :param item: (str) a single str to add as a bullet.
        :param style: (str) what style/hierarchy to create.
            i.e. Heading1, Heading2, Normal, etc.
        :returns: (flowable) the reportlab flowable to append to the document.
        """
        text = "<bullet>&bull</bullet>{}".format(item)
        return Paragraph(text, style=self.styles[style])

    def _add_sequence(self, _id: str, item: str, style: str = "Normal") -> "flowable":
        """
        Adds a recipe direction as a numbered sequence.

        :param _id: (str) the sequence _id so the sequence can be tied to that specific
            list/sequence and start over the numbering for a new sequence _id.
        :param item: (str) a single item to add in the sequence.
        :param style: (str) what style/hierarchy to create.
            i.e. Heading1, Heading2, Normal, etc.
        :returns: (flowable) the reportlab flowable to append to the document.
        """
        text = '<seq id="{}">.  {}'.format(_id, item)
        return Paragraph(text, style=self.styles[style])


def export_to_pdf(recipe:RecipeModel, filename:str=None) -> pathlib.Path:
    """
    Function that will delegate to the FileWriter class and build the
    pdf from the given recipes.

    :param recipe: (RecipeModel) a pyrecipe.storage.shared.recipe_model.RecipeModel instances.
    :param filename: (str) filename of file to write.  Defaults to None, which will allow the
        FileWriter to automatically handle filename creation.
    :returns: (pathlib.Path) the absolute file path of the file just written.
    """
    fw = FileWriter(filename)
    num_written = fw.create_doc(recipe)
    return fw.filename
