from collections import defaultdict
import re
from pprint import pprint

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

POST = {
    'users.0.first_name': 'David',
    'users.0.last_name': 'Boling',
    'users.0.mi': 'daviddboling@gmail.com',
    'users.0.email': 'capn@gmail.com',
    'users.1.first_name': 'Captain',
    'users.1.last_name': 'America',
    'users.1.mi': 'The Cap\'n',
    'users.1.email': 'capn@gmail',
    'baz': 'bang',
    'bang': 'boom',
    'foo': 'bar',
    'email': 'bob@gmail.com'
}

REQUIRED = ['baz', 'bang', 'users.last_name']
PATTERNS = {"email": EMAIL_REGEX, "users.email": EMAIL_REGEX}

def clean_post(posted, required, patterns={}):
    cleaned = { k: v.strip() for k, v in posted.items() if not None }
    nested = []

    ## split cleaned data into nested dicts
    for k in list(cleaned):
        prefix, index, name = ('%s...' % k).split('.')[:3]

        if index and name:
            if prefix not in cleaned:
                cleaned[prefix] = defaultdict(lambda: defaultdict(lambda: None))
                nested.append(prefix)

            cleaned[prefix][index][name] = cleaned[k]

    validated_data = format_data(cleaned, nested, required, patterns)
    return validated_data


def format_data(cleaned, nested, required, patterns):
    # turn nested dictionaries into list of dict
    new_cleaned = {}
    for nested_field in nested:
        formatted_list = []

        # create list of dicts
        for val in cleaned[nested_field].items():
            validated_data = format_nested_field_errors(nested_field, val[1], required, patterns)

            formatted_list.append(validated_data)

        # assign to new cleaned dict
        new_cleaned[nested_field] = formatted_list

        # remove key from cleaned
        cleaned.pop(nested_field, None)

    # bring over remaining field and values that aren't nested
    for key in cleaned:
        validated_data = format_field_errors(key, cleaned[key], required, patterns)
        new_cleaned[key] = validated_data

    return new_cleaned


def format_nested_field_errors(prefix, fields, required, patterns):
    validated_data = {"data": fields, "required": [], "invalid": []}
    for key, val in fields.items():
        validator = '{}.{}'.format(prefix, key)

        # check missing fields
        if validator in required:
            if not fields[key]:
                validated_data['required'].append(key)

        # check invalid fields
        elif validator in patterns:
            if not patterns[validator].match(val):
                validated_data['invalid'].append(key)
    return validated_data


def format_field_errors(key, value, required, patterns):
    validated_data = {"data": value, "required": [], "invalid": []}

    # check missing
    if key in required:
        if not value:
            validated_data['required'].append(key)

    # check invalid
    elif key in patterns:
        if not patterns[key].match(value):
            validated_data['invalid'].append(key)

    return validated_data


def is_valid(cleaned):
    for field in list(cleaned):

        # check nested fields
        if isinstance(cleaned[field], list):
            for nested_field in cleaned[field]:
                if nested_field['required'] or nested_field['invalid']:
                    return False

        # check normal fields
        elif cleaned[field]['required'] or cleaned[field]['invalid']:
                return False

    return True


cleaned = clean_post(POST, REQUIRED, PATTERNS)
pprint(cleaned)
pprint(is_valid(cleaned))
