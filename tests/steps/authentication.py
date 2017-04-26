"""
Authentication unit tests.
"""

from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.authentication import AuthenticationManager
from aaa_manager.authentication import USER_COLLECTION, APP_KEY, USER_ITEM, SECRET
from aaa_manager.basedb import BaseDB
import bcrypt
import json
import datetime
import base64
                
@given('I have user information and application identification')
def step_impl(context):
    context.user_info = {
            'username': 'unitteste', 
            'password': 'Un1ttpwd', 
            'fname': 'unitfname', 
            'lname': 'unitlname',
            'email': 'unit@test.com'
            }
    context.app_id = 1

@when('I user is not repeated')
def step_impl(context):
    pass
    

@then('User is successfully created')
def step_impl(context):
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=True) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert mck_insert.called
            assert mck_unique.called
                
@when('I user is repeated')
def step_impl(context):
    pass

@then("User is not created and user string is returned")
def step_impl(context):
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=False) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert not mck_insert.called
            assert mck_unique.called
            print(result)
            assert len(result) == 2
            assert result[0] == None
            assert result[1] == 'users'

@when('I user is admin')
def step_impl(context):
    pass

@then("User is not created and admin string is returned")
def step_impl(context):
    context.user_info['username'] = 'admin'
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=False) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert not mck_insert.called
            assert not mck_unique.called
            print(result)
            assert len(result) == 2
            assert result[0] == None
            assert result[1] == 'admin'

@given('I have username and password')
def step_impl(context):
    context.username = 'teste'
    context.password = 'pwd'

@when('I access application')
def step_impl(context):
    authentication = AuthenticationManager()
    hashed = authentication._hashpwd('pwd')
    context.info = {'username': 'teste', 'password': hashed}
    ret = [{'auth': [context.info]}]
    with patch.object(BaseDB, 'get', 
        return_value=ret) as mck_get:
            context.result = authentication.access_app(1,
                context.username, context.password)
            assert mck_get.called

@then('I get user information')
def step_impl(context):
    assert context.result == context.info
                
@given('I have valid application ID and user information')
def step_impl(context):
    context.app_id = 1
    context.user_info = {'username': 'teste', 'password': 'pwd'}

@when('I consult token')
def step_impl(context):
    context.token = 'abababab'
    ret = [{
            'data': [{
                'app_id': context.app_id, 
                'user': context.user_info
            }],
            'token': context.token
        }]
    with patch.object(BaseDB, 'get_all', return_value=ret) as mck_get:
        authentication = AuthenticationManager()
        context.result = authentication.get_token(context.app_id, context.user_info)
        

@then('I get valid token')
def step_impl(context):
    assert context.result == context.token
                
@given('I have valid application ID and token')
def step_impl(context):
    context.app_id = 1
    context.username = 'teste'
    context.user_info = {'username': context.username, 'password': 'pwd'}
    context.token = 'ababab'
    ret = [{
            'data': [{
                'app_id': context.app_id, 
                'created': datetime.datetime.now(),
                'user': context.user_info
            }],
            'token': context.token
        }]
    with patch.object(BaseDB, 'get', return_value=ret) as mck_get:
        authentication = AuthenticationManager()
        context.result = authentication.verify_token(context.app_id,
                context.token)
        assert mck_get.called
        
@when('I verify token')
def step_impl(context):
    pass

@then('I get corresponding username')
def step_impl(context):
    assert context.result == context.username
                
@given('I have valid application ID, user information and token')
def step_impl(context):
    context.app_id = 1
    context.username = 'teste'
    context.user_info = {'username': context.username, 'password': 'pwd'}
    context.token = 'ababab'
    context.data = {
            'app_id': context.app_id, 
            'created': datetime.datetime.now(),
            'user': context.user_info
            }
    with patch.object(BaseDB, 'insert') as mck_insert:
        authentication = AuthenticationManager()
        context.result = authentication.insert_token(context.app_id,
                context.user_info,
                context.token)
        assert mck_insert.called

@when('I insert token')
def step_impl(context):
    pass

@then('I get database response')
def step_impl(context):
    assert context.result is not None
                
@given('I have valid token')
def step_impl(context):
    context.token = 'ababab'
    with patch.object(BaseDB, 'remove') as mck_remove:
        authentication = AuthenticationManager()
        context.result = authentication.remove_token(context.token)
        assert mck_remove.called
        assert mck_remove.called_with('Token', 'token', context.token)


@when('I remove token')
def step_impl(context):
    pass

@then('I remove token from database')
def step_impl(context):
    assert context.result is not None

@given('I have user information')
def step_impl(context):
    context.username = 'teste'
    context.user_info = {'username': context.username, 'password': 'pwd'}

@when('I generate token')
def step_impl(context):
    pass

@then('I generate token successfully')
def step_impl(context):
    authentication = AuthenticationManager()
    context.result = authentication.generate_token(context.user_info).encode('utf-8')
    hashed = bcrypt.hashpw((SECRET+json.dumps(context.user_info)).encode('utf-8'), base64.b64decode(context.result))
    assert base64.b64encode(hashed) == context.result
                
@given('I have application ID')
def step_impl(context):
    context.app_id = 1

@when('I remove application')
def step_impl(context):
    pass

@then('I remove application successfully')
def step_impl(context):
    with patch.object(BaseDB, 'remove') as mck_remove:
        authentication = AuthenticationManager()
        context.result = authentication.remove_app(context.app_id)
        assert mck_remove.called
        assert mck_remove.called_with(USER_COLLECTION, APP_KEY, context.app_id)
                
@given('I have application ID and user information')
def step_impl(context):
    context.app_id = 1
    context.username = 'teste'
    context.token = 'abababa'
    context.user_info = {'username': context.username, 'token':
            context.token}

@when('I delete user')
def step_impl(context):
    pass

@then('I delete user successfully')
def step_impl(context):
    with patch.object(BaseDB, 'remove_list_item') as mck_remove:
        authentication = AuthenticationManager()
        context.result = authentication.delete_user(context.app_id,
                context.user_info)
        assert mck_remove.called_with(
                USER_COLLECTION, 
                APP_KEY, 
                context.app_id,
                USER_ITEM, 
                context.user_info)

@when('I update user')
def step_impl(context):
    context.user_info['fname'] = 'teste'
    context.user_info['lname'] = 'teste'
    context.user_info['email'] = 'new@email.com'

@then('I update user successfully')
def step_impl(context):
    context.usernew = {
            'token': 'abababab', 
            'username': context.username, 
            'email': 'm@n.com', 
            'fname': 'teste',
            'lname': 'teste'}
    context.userold = {'username': context.username}
    with patch.object(BaseDB, 'get') as mck_get:
        with patch.object(AuthenticationManager, 'verify_token', return_value=True) as mck_verify:
            with patch.object(AuthenticationManager, 'delete_user', return_value=1) as mck_delete:
                with patch.object(BaseDB, 'insert', return_value=1) as mck_insert:
                    authentication = AuthenticationManager()
                    result = authentication.update_user(context.app_id,
                        context.usernew)
                    assert mck_get.called
                    assert mck_verify.called
                    assert mck_delete.called
                    assert mck_insert.called
                    assert result > 0

@given('I have chosen and invalid password')
def step_impl(context):
    context.invalid_passwords = [
            'abcd', 
            'abcdefgh',
            'Abcdefgh',
            '@bcdefgh',
            '@bC1',
            '1abCD',
            '@bcD1234'
            ]


@when('I create user')
def step_impl(context):
    authentication = AuthenticationManager()
    for item in context.invalid_passwords:
        if not authentication.validate_pwd({
            'username': 'teste',
            'password': item,
            'fname': 'teste',
            'lname': 'teste',
            'email': 'teste@aaa.com'
            }):
            context.result = False
            context.value =  item + ' is invalid'
    context.result = True
    context.value =  'valid'

@then('User is not created and invalid password is returned')
def step_impl(context):
    assert context.result, context.value
