"""PDF filewriter for selected recipes to export."""

import datetime
from typing import List

from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from pyrecipe import __version__ as VERSION


class FileWriter:
    """
    Class that will export a list of given recipes to a PDF for download.
    Each recipe will be separated by a pagebreak.
    Bookmarks will be added in the PDF.
    The Header will indicate PyRecipe version.

    PARAMS:
    :param filename: (str) optional arg, defaults to "PyRecipe_" + datetime string.

    USES:
    * FileWriter().create_doc(recipes:List['Recipe']), where recipes is a list of
      one or more Recipe instances.
    """

    def __init__(self, filename=None):
        self.filename = filename or (
            "PyRecipe_"
            + datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%d_%H:%M")
        )
        self.doc = SimpleDocTemplate(self.filename, pagesize=letter)
        self.styles = getSampleStyleSheet()

    def create_doc(self, recipes: List["Recipe"]) -> int:
        """
        Create a PDF of all given recipes.
        Each recipe is separated by a pagebreak.

        :param recipes: (List['Recipe']) a list of one or more pyrecipe.cookbook.Recipe instances.
        :returns: (int) the number of recipes successfully written to the file.

        TODO:
        * Add Logo in _add_header... but first, create a logo!
        """
        recipes_written = 0
        flowables = []

        for recipe in recipes:
            flowables.append(self._add_section(recipe.name, "Title"))

            timing = "<para align=center>prep time: {:.0f} minutes  |  cook time: {:.0f} minutes</para>".format(
                recipe.prep_time, recipe.cook_time
            )
            flowables.append(Paragraph(timing, style=self.styles["Normal"]))

            servings = "<para align=center>servings: {}</para>".format(recipe.servings)
            flowables.append(Paragraph(servings, style=self.styles["Normal"]))

            flowables.append(self._add_section("Ingredients", "Heading2"))
            for ingredient in recipe.ingredients:
                igr = "{} - {} {}".format(
                    ingredient.name, ingredient.quantity, ingredient.unit
                )
                flowables.append(self._add_bullet(igr))

            flowables.append(self._add_section("Directions", "Heading2"))
            for direction in recipe.directions:
                flowables.append(self._add_sequence(recipe._id, direction))
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

        # TODO Add PyRecipe logo in Upper Left

        lower_left = "<font size=8 color=#777777>PyRecipe, version: {}</font>".format(
            VERSION
        )
        p = Paragraph(lower_left, self.styles["Normal"])
        p.wrapOn(canvas, width, height)
        p.drawOn(canvas, 0.5 * inch, 0.5 * inch)

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


def export_to_pdf(recipes: List["Recipe"]) -> int:
    """
    Function that will delegate to the FileWriter class and build the
    pdf from the given recipes.

    :param recipes: (List['Recipe']) a list of one or more pyrecipe.cookbook.Recipe instances.
    :returns: (int) the number of recipes successfully written to the file.
    """
    fw = FileWriter()
    return fw.create_doc(recipes)
