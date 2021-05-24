import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        """This method allows to get unique API key which should be used for other API methods
        and a status of request in JSON format.
        """
        headers = {
            'email': email,
            'password': password,
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Method allows to get the status of the request and list of pets,
        which must match the filter and returned in json format. Filter variants: 'my_pets' or ''.
        """
        headers = {"auth_key": auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo) -> json:
        """Method allows to add information about new pet. Takes API key and information about new pet (Name,
        animal type, age, path to photo). Response contains the status code and new pet data in json format
         (including a unique pet id).
         """
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', data=data, headers=headers)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def update_pet_info(self, auth_key, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """This method allows to update information about pet. Takes API key, pet id and information about
        new pet (name, animal type, age). Response contains the status code and new pet data in json format
        (including a unique pet id).
         """
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.put(self.base_url + f'/api/pets/{pet_id}', data=data, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Method removes pet with pet_id, returns status code"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + f'/api/pets/{pet_id}', headers=headers)
        status = res.status_code

        return status

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """This method allows to add information about new pet without photo. Takes API key, and information about
        new pet (name, animal type, age). Response contains the status code and new pet data in json format
        (including the unique pet id)."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', data=data, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo) -> json:
        """This method allows to add photo of a pet. Takes API key, pet id and path to pet photo.
        Response contains the status code and new pet data in json format.
        """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', data=data, headers=headers)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_photo_of_pet_without_photo(self, auth_key: json, pet_id: str) -> json:
        """This method allows to add photo of a pet. Takes API key, pet id and path to pet photo.
        Response contains the status code and new pet data in json format.
        """

        data = MultipartEncoder(
            fields={
                            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', data=data, headers=headers)
        status = res.status_code
        result = ''

        try:
            result = res.json()
        except:
            result = res.text

        return status, result
