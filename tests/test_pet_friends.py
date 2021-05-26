import sys

sys.path.insert(0, '..')
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data_and_photo(name="Пушистик", animal_type="Racoon",
                                               age='4', pet_photo="../images/animal.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)  # auth_key replaced
    assert status == 200
    assert result['name'] == "Пушистик"
    assert result['age'] == '4'


def test_update_information_about_pet_with_valid_data(name='Полосатик', animal_type="Енот", age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['animal_type'] == 'Енот'


def test_delete_pet_valid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_without_photo_valid_data(name="Продам гитару", animal_type="Аккустика",
                                              age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # auth_key replaced
    assert status == 200
    assert result['name'] == "Продам гитару"
    assert result['age'] == '4'

def test_add_photo_of_pet_valid_data(pet_photo="../images/guitar.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo']
    # pf.delete_pet(auth_key, pet_id)


def test_add_photo_of_pet_no_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet_without_photo(auth_key, pet_id)
    assert status == 400


def test_add_new_pet_without_photo_empty_name(name="", animal_type="Аккустика",
                                              age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # auth_key replaced
    assert status == 400
    assert result['name'] is not ""


def test_add_new_pet_without_photo_empty_animal_type(name="Гитара", animal_type='',
                                              age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # auth_key replaced
    # assert status == 400
    assert result['animal_type'] is not ""

def test_add_new_pet_without_photo_age_is_letter(name="Гитара", animal_type="Аккустика",
                                              age='w'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # auth_key replaced
    # assert status == 400
    assert result['age'] is not "w"


def test_get_api_for_user_empty_password(email=valid_email, password=None):
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_for_user_invalid_password(email=valid_email, password='11111'):
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_for_user_none_password_field(email=valid_email):
    status, result = pf.get_api_key_none_password_param(email)

    assert status == 200


def test_get_list_of_pets_invalid_key(filter=''):
    auth_key = {"key": "123"}

    status, result = pf.list_of_pets(auth_key, filter)
    assert status == 200


def test_add_photo_of_pet_invalid_photo_format(pet_photo="../images/text_file.txt"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 400


def test_add_photo_of_pet_large_photo(pet_photo="../images/50mb_sample.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
        _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 400


def test_add_new_pet_without_photo_name_long(name= f'{10000*"a"}', animal_type="кот",
                                              age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # auth_key replaced
    assert status == 400




