Py-config is a tool to create a configuration for your applications.
store data in a dict-like obj from .py-files or json.

values can be retrieved via config[key] or config.KEY

# Usage
copy/clone into your project directory

example.py
```
EXAMPLE_VALUE = 'example'
```

app.py
```
from configparser import Config
app = YourApp()
config = Config()
config.from_pyfile('example.py')

app.config = config
```

output:
```
print(app.config.EXAMPLE_VALUE)
> 'example'
```



# Todo:
- [ ] parse more filetypes
    - [X] json
    - [ ] toml
    - [ ] ini
    - [ ] env vars
