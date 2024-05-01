import string
from typing import Optional
from fastapi import FastAPI

from model import Resource
from model import resource as resource_obj

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/test')
async def test():
    return {'data': output(input())}


def output(mapping: dict[str, str]) -> str:
    template = string.Template('''
        Project Name: $project_name
        UR Number: $ur_number
        Request Name: $request_name
        Request Email: $request_email
        Request Phone: $request_phone
        Department: $department
        System Name: $system_name
        System Owner: $system_owner
        System Phone: $system_phone
        Create Date: $create_date
        Project Launch Date: $project_launch_date
        Action By: $action_by
    ''')
    return template.substitute(mapping)


def input() -> dict[str, str]:
    placeholders = ('project_name', 'ur_number', 'request_name', 'request_email', 'request_phone', 'department', 'system_name', 'system_owner', 'system_phone', 'create_date', 'project_launch_date', 'action_by')

    # Set default value for each placeholder to '-'.
    mapping = dict(zip(placeholders, ['-' for _ in placeholders]))

    # Set value for each placeholder.
    mapping['project_name'] = query_project_name_by_resource(resource_obj)
    mapping |= get_request_details(resource_obj)

    return mapping


# Utility function
def query_project_name_by_resource(resource: Resource) -> str:
    return resource.project.name


def query_request_creator_by_resource(resource: Resource, key: str) -> Optional[str]:
    creator = resource.request.creator

    try:
        return getattr(creator, key)
    except AttributeError:
        return None


# Function in main.py
def get_request_details(resource: Resource) -> dict[str, str]:
    """
    Fetch following attributes from 'Resource.request.creator':
    - first_name
    - last_name
    - email
    - phone_number

    and return new dictionary with keys that match with the placeholders.
    """

    # Define target attributes to fetch.
    fetch_attrs = ('first_name', 'last_name', 'email', 'phone_number')

    # Fetch value for each attribute.
    fetch_values = tuple(query_request_creator_by_resource(resource, key) for key in fetch_attrs)

    # Merge values with attributes.
    fetch_items = dict(zip(fetch_attrs, fetch_values))

    # Assemble new dictionary.
    result = {}
    if fetch_items[fetch_attrs[0]] and fetch_items[fetch_attrs[1]] is not None:
        result |= {'request_name': f'{fetch_items.pop(fetch_attrs[0])} {fetch_items.pop(fetch_attrs[1])}'}
    else:
        del fetch_items[fetch_attrs[0]]
        del fetch_items[fetch_attrs[1]]

    if fetch_items[fetch_attrs[2]] is not None:
        result |= {'request_email': fetch_items.pop(fetch_attrs[2])}
    else:
        del fetch_items[fetch_attrs[2]]

    if fetch_items[fetch_attrs[3]] is not None:
        result |= {'request_phone': fetch_items.pop(fetch_attrs[3])}
    else:
        del fetch_items[fetch_attrs[3]]

    return result
