"""Abstract ODM with shared functionalityfor other MongoDB Collections."""

import datetime

import mongoengine


class BaseDocument(mongoengine.Document):
    meta = {
        "abstract": True,
    }

    def _update_last_mod_date(self) -> int:
        """
        Updates the document's "last_updated_date" attribute in the DB.

        document._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        result = self.update(last_modified_date=datetime.datetime.utcnow())
        self.reload()
        return result

    def save(self) -> int:
        """
        Save the document's current state in the DB.  First refreshes the last
        modified date if it's already a DB instance, before delegating to the
        built-in/inherited save() method.

        document.save()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        if self.id:
            self._update_last_mod_date()
        return super().save()
