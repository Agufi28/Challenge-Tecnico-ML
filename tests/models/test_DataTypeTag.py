import pytest
from sqlalchemy.exc import IntegrityError
from internal.models.DataTypeTag import DataTypeTag
from internal.models.User import User

def testDataTypeTagCreation(session):
    tag = DataTypeTag(name="EMAIL", description="Email data type")
    session.add(tag)
    session.commit()

    persistedTag = session.query(DataTypeTag).filter_by(name="EMAIL").first()
    assert persistedTag is not None
    assert persistedTag.name == "EMAIL"
    assert persistedTag.description == "Email data type"


def testDataTypeTagPersistence(session):
    tag = DataTypeTag(name="USERNAME")
    session.add(tag)
    session.commit()

    persistedTag = session.query(DataTypeTag).filter_by(name="USERNAME").first()
    assert persistedTag is not None
    assert persistedTag.name == "USERNAME"


def testDataTypeTagUniquenessConstraint(session):
    tag1 = DataTypeTag(name="EMAIL")
    tag2 = DataTypeTag(name="EMAIL")

    session.add(tag1)
    session.commit()

    session.add(tag2)
    with pytest.raises(IntegrityError):
        session.commit()


def testDataTypeTagOptionalFields(session, makeUser):
    user = makeUser()
    session.add(user)
    session.commit()

    tag = DataTypeTag(name="PHONE", createdBy=user)
    session.add(tag)
    session.commit()

    persistedTag = session.query(DataTypeTag).filter_by(name="PHONE").first()
    assert persistedTag is not None
    assert persistedTag.createdBy == user