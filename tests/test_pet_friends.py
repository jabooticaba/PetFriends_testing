import sys
import pytest

sys.path.insert(0, '..')
from api import PetFriends
from settings import valid_email, valid_password
from test_data_generators import chinese_chars, russian_chars, special_chars, generate_string
import os

pf = PetFriends()


class TestFunctions:

    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.parametrize("email", [valid_email, 'None'], ids=['valid', 'empty'])
    @pytest.mark.parametrize("password", [valid_password, 'None'], ids=['valid', 'empty'])
    def test_get_api_key_negative(self, email, password):
        if email != valid_email or password != valid_password:
            status, result = pf.get_api_key(email, password)
            assert status == 403

    # @pytest.fixture(autouse=True)
    # def logging(self, request):
    #     ''' Функция логирования для задания 21.6.4,
    #     реализовано: создание файла, внесение кода ответа, тела ответа
    #     не реализовано: перечислены заголовки запроса, параметры пути, параметры строки и тело запроса
    #     '''
    #     yield
    #
    #     with open('log.txt', 'at', encoding='utf8') as log_file:
    #         log_file.write(f'\n============Test::{request.node.name}================\n')
    #         # log_file.write(f'Test name: {request.function.__name__}\n')
    #         log_file.write(f'Status code: {str(self.status)}\n')
    #         log_file.write(f'Body: {self.result}\n')
    #         log_file.write(f'Exp: {request.response}\n')

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_get_all_pets_with_valid_key(self, filter):  # filter available values : my_pets
        self.status, self.result = pf.list_of_pets(self.key, filter)
        assert len(self.result['pets']) > 0
        assert self.status == 200

    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.xfail
    @pytest.mark.parametrize("filter",
                             [generate_string(255),
                              generate_string(1001),
                              russian_chars(),
                              russian_chars().upper(),
                              chinese_chars(),
                              special_chars(),
                              123
                              ]
        , ids=['255 symbols'
            , 'more than 1000 symbols'
            , 'russian'
            , 'RUSSIAN'
            , 'chinese'
            , 'specials'
            , 'digit'])
    def test_get_all_pets_with_valid_key(self, filter):
        self.status, self.result = pf.list_of_pets(self.key, filter)
        assert self.status == 400

    #     def test_get_list_of_pets_invalid_api_key(filter=''):
    #         auth_key = {"key": "123"}
    #         self.status, result = pf.list_of_pets(self.key, filter)
    #         assert self.status == 200

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("name"
        , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
           special_chars(), '123']
        , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("animal_type"
        , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
           special_chars(), '123']
        , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("age", ['1'], ids=['min'])
    def test_add_new_pet_without_photo_positive(self, name, animal_type, age):
        self.status, result = self.pf.add_new_pet_without_photo(self.key, name, animal_type, age)
        assert self.status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type

    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.parametrize("name", [''], ids=['empty'])
    @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
    @pytest.mark.parametrize("age"
        , ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), \
           russian_chars(), russian_chars().upper(), chinese_chars()]
        , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', \
               'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
    def test_add_new_pet_without_photo_negative(self, name, animal_type, age):
        self.status, result = self.pf.add_new_pet_without_photo(self.key, name, animal_type, age)
        assert self.status == 400

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("pet_photo", ['../images/guitar.jpg'], ids=['valid'])
    def test_add_photo_of_pet_valid_data(self, pet_photo):
        _, my_pets = pf.list_of_pets(self.key, 'my_pets')

        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(self.key, "Тест-кот", "кот", "2")
            _, my_pets = pf.list_of_pets(self.key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        self.status, result = self.pf.add_photo_of_pet(self.key, pet_id, pet_photo)
        assert result['pet_photo']
        assert self.status == 200

    @pytest.mark.negative
    @pytest.mark.parametrize("pet_photo", ['../images/text_file.txt', '../images/50mb_sample.jpg'],
                             ids=['text_format', 'large_photo'])  # TODO Add all negative parameters
    def test_add_photo_of_pet_file_negative(self, pet_photo):
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(auth_key, "Тест-кот", "кот", "2")
            _, my_pets = pf.list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 400

    '''
    ==========================Work in progress below this line (parameterizing)==================
    '''

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_add_new_pet_with_valid_data_and_photo(self, name="Пушистик", animal_type="Racoon",
                                                   age='4', pet_photo="../images/animal.jpg"):
        self.status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)
        assert result['name'] == "Пушистик"
        assert result['age'] == '4'
        assert self.status == 200

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_update_information_about_pet_with_valid_data(self, name='Полосатик', animal_type="Енот", age='4'):

        _, my_pets = self.pf.list_of_pets(self.key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet_without_photo(self.key, "Тест-кот", "кот", "2")
            _, my_pets = self.pf.list_of_pets(self.key, "my_pets")

        self.status, result = self.pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert result['animal_type'] == 'Енот'
        assert self.status == 200

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_delete_pet_valid_id(self):
        _, my_pets = self.pf.list_of_pets(self.key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet_without_photo(self.key, "Тест-кот", "кот", "2")
            _, my_pets = self.pf.list_of_pets(self.key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        self.status = self.pf.delete_pet(self.key, pet_id)
        _, my_pets = self.pf.list_of_pets(self.key, "my_pets")

        assert pet_id not in my_pets.values()
        assert self.status == 200

    @pytest.mark.smoke
    @pytest.mark.negative
    def test_add_photo_of_pet_no_photo(self):
        _, my_pets = pf.list_of_pets(self.key, 'my_pets')

        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(self.key, "Тест-кот", "кот", "2")
            _, my_pets = pf.list_of_pets(self.key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        self.status, result = pf.add_photo_of_pet_without_photo(self.key, pet_id)
        assert self.status == 400

    def test_get_api_for_user_none_password_field(email=valid_email):
        status, result = pf.get_api_key_none_password_param(email)

        assert status == 200

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.delete
    def test_delete_pet_valid_id(self):
        _, my_pets = self.pf.list_of_pets(self.key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        self.status = self.pf.delete_pet(self.key, pet_id)
        _, my_pets = self.pf.list_of_pets(self.key, "my_pets")

        assert self.status == 200