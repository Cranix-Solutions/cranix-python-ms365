# -*- coding: utf-8 -*-

import string

import cranix_ms365
from cranix_ms365 import vars as ms365_vars


def test_version_is_exposed():
    assert cranix_ms365.__version__


def test_state_directories():
    assert ms365_vars.MS365_DIR == '/var/adm/cranix/ms365'
    assert ms365_vars.USERIDS_DIR == ms365_vars.MS365_DIR + '/userids'
    assert ms365_vars.GROUPIDS_DIR == ms365_vars.MS365_DIR + '/groupids'
    assert ms365_vars.FAILED_DIR == ms365_vars.MS365_DIR + '/failed'


def test_generate_password_length():
    assert len(cranix_ms365.generate_office365_password(length=16)) == 16


def test_generate_password_contains_required_classes():
    password = cranix_ms365.generate_office365_password(length=20)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in '#$!?' for c in password)


def test_generate_password_too_short():
    try:
        cranix_ms365.generate_office365_password(length=2)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_cranix_user_to_ms_students():
    user = {
        'role': 'students',
        'uid': 'jdoe',
        'givenname': 'John',
        'surname': 'Doe',
        'password': 'secret',
    }
    result = cranix_ms365.cranix_user_to_ms(user)
    assert result['mailnickname'] == 'jdoe'
    assert result['givenName'] == 'John'
    assert result['surName'] == 'Doe'
    assert result['displayName'] == 'John Doe'
    assert result['jobTitle'] == 'Schüler'
    assert result['passwordProfile']['password'] == 'secret'


def test_cranix_user_to_ms_teacher_uses_teacher_domain():
    user = {
        'role': 'teachers',
        'uid': 'jdoe',
        'givenname': 'John',
        'surname': 'Doe',
        'password': 'secret',
    }
    result = cranix_ms365.cranix_user_to_ms(user)
    assert result['jobTitle'] == 'Lehrer'
    assert result['userprincipalname'] == 'jdoe@'
