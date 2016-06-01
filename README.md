
# Terrapin is a lightweight template language

## Release a new version

To release a new version making it available to pip install. NB. This doesn't make it public, and only allows installation from people with access to the terrapin repository

1. Bump version in `setup.py`
2. `git push origin branch`
3. Create pull request & merge into master
4. `git checkout master`
5. `git pull origin master`
6. `git tag -a vx.x.x -m "Tag Message"`
7. `git push origin vx.x.x`

## To pip install

`pip install git+ssh://git@github.com/DistilledLtd/terrapin.git@vx.x.x`

## Usage

```
from terrapin.parser import Parser

template = 'Hello {{name}}'
context = {
	"name" : "bob"
}

terrapin = Parser()
output = terrapin.parse(template, context)
print(output)
```

## Syntax

Terrapin supports the following

- Variables from the context: `{{variable}}`
- Truthy if `{% if variable %}I'm alive{% endif %}`
- Equality if `{% if variable == "String" %}I'm alive{% endif %}`
- Non Equality if `{% if variable != "String" %}I'm alive{% endif %}`
- Else `{% if variable %}foo{% else %}bar{% endif %}`