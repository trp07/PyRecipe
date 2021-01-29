"""Module that handles importing user-generated images into recipe records."""

import hashlib
import pathlib
import typing

from PIL import Image, ExifTags


def process_image(image: pathlib.Path) -> str:
    """The main interface to this module, handles calls to other
    functions and executes the required business logic.

    :param image: (pathlib.Path) the filepath of the image to process
    :returns filename: (str) the filename (not filepath) of the processed image
    """
    processed_image = ImageImporter(image).process_image()
    return processed_image


############ Internal Functions ##############################################

class ImageImporter:
    """The class that will do all the image processing."""
    MAX_SIZE = (400, 400)

    def __init__(self, image: pathlib.Path):
        self._image = Image.open(image)
        self._path = image
        self.filetype = image.name.rsplit(".")[-1].lower()

    def process_image(self) -> typing.Optional[str]:
        """First checks if the file exists, then renames it.
        If the file was previously imported via a different recipe, then
        reference the already-existing file and return it.  Otherwise, resize
        it to a thumbnail of MAX_SIZE, delete the original file, and return the
        new filename.
        """
        if self._path.is_file():
            new_filename = self._rename_image()

            if self._check_if_image_already_exists(new_filename):
                self._path.unlink()
                return new_filename
            else:
                self._resize_image()
                self._image.save(self._path.parent.joinpath(new_filename))
                self._path.unlink()
                return new_filename

        else:
            return None

    def _rename_image(self) -> str:
        """Returns the md5sum of the original file as the new filename."""
        with open(self._path, "rb") as fp:
            hashed = hashlib.md5()
            hashed.update(fp.read())
        return hashed.hexdigest() + "." + self.filetype

    def _resize_image(self) -> None:
        """Resize the image into a thumbnail of MAX_SIZE pixels."""
        if hasattr(self._image, "getexif"):
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            e = self._image.getexif()
            if e is not None:
                if e[orientation] == 3:
                    self._image = self._image.transpose(Image.ROTATE_180)
                if e[orientation] == 6:
                    self._image = self._image.transpose(Image.ROTATE_270)
                if e[orientation] == 8:
                    self._image = self._image.transpose(Image.ROTATE_90)

        self._image.thumbnail(self.MAX_SIZE, Image.ANTIALIAS)

    def _check_if_image_already_exists(self, filename: str) -> bool:
        """Checks if the file already exists and returns True if so."""
        if pathlib.Path(self._path.parent.joinpath(filename)).is_file():
            return True
        else:
            return False
