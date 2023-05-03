Parse Config from .py-Files.

#Usage
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



#Todo:
[ ] parse more filetypes
    [ ] json
    [ ] toml
    [ ] ini
