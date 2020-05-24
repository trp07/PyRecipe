import pytest

from pyrecipe.security import auth


###### Globals ######

PASSWORD = "password"

###### Tests ######


def test_password_knownGood():
    hashed = auth.hash_password(PASSWORD)
    verified = auth.verify_password(PASSWORD, hashed)
    assert verified == True


def test_password_knownBad():
    hashed = auth.hash_password(PASSWORD)
    verified = auth.verify_password("badpassword", hashed)
    assert verified == False
