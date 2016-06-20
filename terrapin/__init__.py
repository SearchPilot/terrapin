import re

from terrapin.parser import Parser
from terrapin.lexer import word_regex


parser = Parser()


def render(template, context):
    """ Choose which rendering strategy to use and execute """

    if '{%' in template:
        return render_full(template, context)
    else:
        return render_simple(template, context)


def render_full(template, context):
    """ Render with fully featured template engine """

    return parser.parse(template, context)


def render_simple(template, context):
    """ Render a template by replacing variables """

    return replace_variables(template, context)


def replace_variables(string, variables):
    """ Format a templated value """

    found_variables = find_variables(string)
    for variable in found_variables:
        value = str(variables.get(variable, ''))
        string = string.replace('{{' + variable + '}}', value)
    return string


def find_variables(template):
    """ Find all the used variables

    This is any string that looks like {{var}}
    """

    capture_variable_regex = r'\{\{(' + word_regex + r')\}\}'
    found_variables = re.findall(capture_variable_regex, template)
    return list(found_variables)


class ObservingContext(dict):
    """ Keep a record of which keys have tried to be accessed """

    def __init__(self, *args, **kwargs):

        self.keys_seen = set()

    def get(self, key, *args, **kwargs):

        self.keys_seen.add(key)
        return super(ObservingContext, self).get(key, *args, **kwargs)


def used_variables(template):
    """ Return a set of used variables in the template """

    context = ObservingContext()
    parser.parse(template, context)
    return context.keys_seen
