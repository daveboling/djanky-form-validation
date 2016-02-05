from collections import defaultdict
from pprint import pprint

#example data
POST = {
    'owners.0.first_name': 'David',
    'owners.0.last_name': 'asdf',
    'owners.0.mi': 'D',
    'owners.1.first_name': 'Adam',
    'owners.1.last_name': 'Solesby',
    'owners.1.mi': 'G',
    'baz': 'a',
    'bang': 'a',
    'foo': 'bar',
}

REQUIRED = ['baz', 'bang', 'owners.last_name']
PATTERNS = {}


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
            re = patterns[validator]
            if re.match(val):
                validated_data['invalid'].append(key)
    return validated_data


def format_field_errors(key, value, required, patterns):
    validated_data = {"data": value, "required": [], "invalid": []}
    if key in required:

        # check missing
        if not value:
            validated_data['required'].append(key)

        # check invalid
        elif key in patterns:
            re = patterns[key]
            if re.match(value):
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
pprint(is_valid(cleaned))
