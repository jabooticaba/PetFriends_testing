import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
  def __init__(self):
    self.base_url = 'https://petfriends1.herokuapp.com/'

  def get_api_key(self, email: str, password: str) -> json:
    """This method allows to get API key which should be used for other API methods and a status of request
    in JSON format"""

    headers = {
      'email': email,
      'password': password,
    }

    res = requests.get(self.base_url+'api/key', headers=headers)
    status = res.status_code
    result = ''

    try:
      result = res.json()
    except:
      result = res.text

    return status, result

  def list_of_pets(self, auth_key: json, filter:str = '') -> json:
    """This method allows to get the status of the request and list of pets,
    which must match the filter and retured in json format."""

    # headers = {"auth_key": auth_key['key']}
    headers = {"auth_key": auth_key}
    filter = {'filter': filter}

    res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
    status = res.status_code
    result = ''

    try:
      result = res.json()
    except:
      result = res.text

    return status, result

  def add_new_pet(self, auth_key:json, name:str, animal_type:str, age:str, pet_photo) -> json:
    """This method allows to add information about new pet."""

    data = MultipartEncoder(
    fields={
       'name': name,
       'animal_type': animal_type,
       'age': age,
       'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
    })
    headers = {'auth_key': auth_key, 'Content-Type': data.content_type} # ['key'] deleted from auth_key

    res = requests.post(self.base_url+'api/pets', data = data, headers = headers)
    status = res.status_code
    result = ''

    try:
      result = res.json()
    except:
      result = res.text

    return status, result

  def update_pet_info(self, auth_key:json, pet_id, name: str, animal_type: str, age: str) -> json:

    data = MultipartEncoder(
    fields={
       'name': name,
       'animal_type': animal_type,
       'age': age       
    })
    headers = {'auth_key': auth_key, 'Content-Type': data.content_type} # ['key'] deleted from auth_key

    res = requests.put(self.base_url+ f'/api/pets/{pet_id}', data = data, headers = headers)
    status = res.status_code
    result = ''

    try:
      result = res.json()
    except:
      result = res.text

    return status, result

  def delete_pet(self, auth_key:json, pet_id) -> json:
    """Delete pet with {pet_id}, returns status code"""

    headers = {'auth_key': auth_key} # ['key'] deleted from auth_key

    res = requests.delete(self.base_url+ f'/api/pets/{pet_id}', headers = headers)
    status = res.status_code
    
    return status
