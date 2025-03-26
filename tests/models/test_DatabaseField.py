import pytest
from unittest.mock import MagicMock
from internal.models.DatabaseField import DatabaseField
from internal.models.DataTypeTag import DataTypeTag
from internal.models.FieldDataTypes import FieldDataTypes
from internal.models.FieldTag import FieldTag

def testInitialization():
	field = DatabaseField(name="test_field", type=FieldDataTypes.STRING)
	assert field.name == "test_field"
	assert field.type == FieldDataTypes.STRING
	assert len(field.tags) == 0

def testGetName(makeField):
    field = makeField()
    assert field.getName() == "test_field"

def testGetOrAddTagAddNewTag(makeField, emailDataTypeTag):
    field = makeField()
    assert len(field.tags) == 0
    new_tag = field.getOrAddTag(emailDataTypeTag)
    assert len(field.tags) == 1
    assert new_tag.tag == emailDataTypeTag
    assert isinstance(new_tag, FieldTag)

def testGetOrAddTagExistingTag(makeField, emailDataTypeTag):
    field = makeField()
    existing_tag = field.getOrAddTag(emailDataTypeTag)
    retrieved_tag = field.getOrAddTag(emailDataTypeTag)
    assert len(field.tags) == 1
    assert existing_tag == retrieved_tag

def testUpdateTagAddNewTag(makeField, emailDataTypeTag):
    field = makeField()
    assert len(field.tags) == 0
    field.updateTag(emailDataTypeTag, 10)
    assert len(field.tags) == 1
    assert field.tags[0].tag == emailDataTypeTag
    assert field.tags[0].certanty_score == 10

def testUpdateTagUpdateExistingTag(makeField, emailDataTypeTag):
    field = makeField()
    field.updateTag(emailDataTypeTag, 10)
    field.updateTag(emailDataTypeTag, 5)
    assert len(field.tags) == 1
    assert field.tags[0].tag == emailDataTypeTag
    assert field.tags[0].certanty_score == 15
    
def testUpdateTagAdd2Tags(makeField, emailDataTypeTag, usernameTag):
    field = makeField()
    field.updateTag(emailDataTypeTag, 10)
    field.updateTag(usernameTag, 5)
    assert len(field.tags) == 2
    assert field.tags[0].tag == emailDataTypeTag
    assert field.tags[0].certanty_score == 10
    assert field.tags[1].tag == usernameTag
    assert field.tags[1].certanty_score == 5

def testRunCallsExecuteOn(makeField):
    field = makeField()
    mock_control_1 = MagicMock()
    mock_control_2 = MagicMock()
    controls = [mock_control_1, mock_control_2]

    field.run(controls)

    mock_control_1.executeOn.assert_called_once_with(field)
    mock_control_2.executeOn.assert_called_once_with(field)