import collections

Creator = collections.namedtuple('Creator', ('first_name', 'last_name', 'email'))
creator = Creator(first_name='John', last_name='Doe', email='jDqZz@example.com')

Request = collections.namedtuple('Request', ('creator',))
request = Request(creator=creator)

Project = collections.namedtuple('Project', ('name',))
project = Project(name='myproject')

Resource = collections.namedtuple('Resource', ('project', 'request'))
resource = Resource(project=project, request=request)
