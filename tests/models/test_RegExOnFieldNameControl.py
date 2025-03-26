import json
from unittest.mock import MagicMock
from internal.models.RegExOnFieldNameControl import RegExOnFieldNameControl
from internal.models.DataTypeTag import DataTypeTag

def testInitialization(control, regex):
    assert control.name == "Test Control"
    assert json.loads(control.raw_data)["regex"] == regex

def testGetData(control, regex):
    data = control.getData()

    assert data == {"regex": regex}

def testGetRegEx(control, regex):
    assert control.getRegEx() == regex

def testConditionMatches_with_match(control):
    mock_field = MagicMock()
    mock_field.getName.return_value = "user_email"

    assert control._Control__conditionMatches(mock_field)
    mock_field.getName.assert_called_once()

def testConditionMatches_without_match(control):
    mock_field = MagicMock()
    mock_field.getName.return_value = "username"

    assert not control._Control__conditionMatches(mock_field)
    mock_field.getName.assert_called_once()

def testExecuteOn_with_match(control, emailDataTypeTag):
    mock_field = MagicMock()
    mock_field.getName.return_value = "user_email"

    control.executeOn(mock_field)

    mock_field.updateTag.assert_called_once_with(emailDataTypeTag, 10)

def testExecuteOn_without_match(control):
    mock_field = MagicMock()
    mock_field.getName.return_value = "username"

    control.executeOn(mock_field)

    mock_field.updateTag.assert_not_called()