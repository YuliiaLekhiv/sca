import requests
from django.core.exceptions import ValidationError

def validate_breed(value):
    response = requests.get('https://api.thecatapi.com/v1/breeds')
    if response.status_code == 200:
        breeds = [breed['name'] for breed in response.json()]
        if value not in breeds:
            raise ValidationError(f"{value} is not a valid breed.")
    else:
        raise ValidationError("Could not validate breed at this time.")