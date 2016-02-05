#### djanky-form-validation
##### Sometimes, you just wanna skip the middle man. djanky's got you covered.
-----

#### Instructions (WIP)
- Single field validation
- Nested field(s) validation (for nested fields)

#### View usage
```
  # rules
  EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
  REQUIRED = ['baz', 'bang', 'users.last_name']
  PATTERNS = {"email": EMAIL_REGEX, "users.email": EMAIL_REGEX}
```

```
  # view logic
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

  cleaned = clean_post(POST, REQUIRED, PATTERNS)

  if is_valid(cleaned):
    # save all the things
```


#### Output
```
# print(cleaned)
{
  'bang': {'data': 'boom', 'invalid': [], 'required': []},
  'baz': {'data': 'bang', 'invalid': [], 'required': []},
  'email': {'data': 'bob@gmail.com', 'invalid': [], 'required': []},
  'foo': {'data': 'bar', 'invalid': [], 'required': []},
  'users': [
    {'data': {'email': 'capn@gmail.com', 'first_name': 'David', 'last_name': 'Boling', 'mi': 'daviddboling@gmail.com'}, 'invalid': [], 'required': []},
    {'data': {'email': 'capn@gmail.com', 'first_name': 'Captain', 'last_name': 'America', 'mi': "The Cap'n"}, 'invalid': [], 'required': []}
  ],
  'users.0.email': {'data': 'capn@gmail.com', 'invalid': [], 'required': []},
  'users.0.first_name': {'data': 'David', 'invalid': [], 'required': []},
  'users.0.last_name': {'data': 'Boling', 'invalid': [], 'required': []},
  'users.0.mi': {'data': 'daviddboling@gmail.com', 'invalid': [], 'required': []},
  'users.1.email': {'data': 'capn@gmail.com', 'invalid': [], 'required': []},
  'users.1.first_name': {'data': 'Captain', 'invalid': [], 'required': []},
  'users.1.last_name': {'data': 'America', 'invalid': [], 'required': []},
  'users.1.mi': {'data': "The Cap'n", 'invalid': [], 'required': []}
}
```

#### Example HTML (WIP)
```
```


#### Who's this for?
People who want full control over layouts and a better way to handle dynamic forms.

#### Why not Django forms?
To be honest, you should probably just use them. As a front-end developer, I desire full control over my markup in the classical ways rather than manually
modifying Django form layouts. Also just wanted to do it. It isn't called 'djanky-form-validation' for nothing!
