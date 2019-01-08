"""Fixtures for various test modules."""

import datetime

import pytest
import mongoengine


##############################################################################
# test_storage_*.py fixtures
##############################################################################

@pytest.fixture(scope='function')
def mongodb(request):
    """
    Create and yield a test MongoDB collection for each test.  Destroy the
    collection upon test completion.
    """
    db = mongoengine.connect(db='test_db', alias='core', host='mongodb://localhost')
    yield db
    db.drop_database('test_db')
    db.close()



##############################################################################
# test_cookbook_*.py fixtures
##############################################################################

class Fake_User:
    """Fake storage.User for testing."""
    def __init__(self, _id=123, name='Tester', email='tester@here.com',
        created_date=datetime.datetime.utcnow(), last_modified_date=datetime.datetime.utcnow(),
        recipes=[], view='list', page_size=100, email_distros={}):
        self.id = _id
        self._id = _id
        self.name = name
        self.email = email
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.recipe_ids = recipes
        self.shared_recipe_ids = []
        self.view = view
        self.page_size = page_size
        self.email_distros = email_distros

    def save(self):
        pass

    def update(self, add_to_set__recipes=None, last_modified_date=None):
        if add_to_set__recipes == 'good' or isinstance(last_modified_date, datetime.datetime):
            return 1
        else:
            return 0


@pytest.fixture(scope='function')
def get_user():
    """Return an instance of Fake_User for testing."""
    return Fake_User()
