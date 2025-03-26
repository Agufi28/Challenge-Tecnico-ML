import pytest
from internal.models.FieldTag import FieldTag
from internal.models.DatabaseTable import DatabaseTable
from internal.models.DataTypeTag import DataTypeTag
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def test_fieldtag_creation(makeField, emailDataTypeTag):
	field = makeField()
	mock_certanty_score = 85
	field_tag = FieldTag(field=field, tag=emailDataTypeTag, certanty_score=mock_certanty_score)

	assert field_tag.field == field
	assert field_tag.tag == emailDataTypeTag
	assert field_tag.certanty_score == mock_certanty_score

def test_fieldtag_persistence(session, makeTable, makeField, emailDataTypeTag):
	field = makeField()
	mock_certanty_score = 85
	field_tag = FieldTag(field=field, tag=emailDataTypeTag, certanty_score=mock_certanty_score)

	session.add(field_tag)
	session.commit()

	persisted_field_tag = session.query(FieldTag).first()
	assert persisted_field_tag is not None
	assert persisted_field_tag.field == field
	assert persisted_field_tag.certanty_score == mock_certanty_score