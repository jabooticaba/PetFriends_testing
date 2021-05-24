import sys

sys.path.insert(0, '..')
from api import PetFriends
from settings import valid_email, valid_password


class StoreStuff:
    """Используется для хранения переменных тест-рана, auth_key, pet_id и т.д."""
    auth_key = None
    pet_id = None
    # first_pet_id = None  # Используется в цикле удаления питомцев


pf = PetFriends()
store_stuff = StoreStuff


def test_get_api_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    store_stuff.auth_key = result['key']
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter='my_pets'):
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = store_stuff.auth_key
    status, result = pf.list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    # store_stuff.first_pet_id = result['pets'][0]['id']  # Используется для очистки списка питомцев в цикле
    # print(store_stuff.first_pet_id)


def test_add_new_pet_with_valid_data_and_photo(name="Пушистик", animal_type="Racoon",
                                               age='4', pet_photo="../images/animal.jpg"):
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(store_stuff.auth_key, name, animal_type, age, pet_photo)  # auth_key replaced
    assert status == 200
    assert result['name'] == "Пушистик"
    assert result['age'] == '4'
    store_stuff.pet_id = result['id']


def test_update_information_about_pet_with_valid_data(name='Полосатик', animal_type="Енот", age='4'):
    status, result = pf.update_pet_info(store_stuff.auth_key, store_stuff.pet_id, name, animal_type, age)
    assert status == 200
    assert result['animal_type'] == 'Енот'


#   def test_delete_pet_valid_id():  # Удалить 10 питомцев в цикле pytest --repeat-scope=session --count=10,
#  закомментить тесты 3, 4
#   status = pf.delete_pet(store_stuff.auth_key, store_stuff.first_pet_id)
#   assert status == 200


def test_delete_pet_valid_id():
    status = pf.delete_pet(store_stuff.auth_key, store_stuff.pet_id)
    assert status == 200
