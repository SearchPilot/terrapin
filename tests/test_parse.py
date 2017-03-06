from hypothesis import given, assume
from hypothesis.strategies import text, integers
import pytest

from terrapin.exceptions import TemplateError
from terrapin.used_variables import used_variables
from tests.utils import check_equal

@given(s=text())
def test_variable(s):

    template = "testing {{var}}"
    context = {
        "var": s
    }
    expected = "testing " + s

    check_equal(template, context, expected)


@given(s=text())
def test_truthy_if(s):

    assume(not s == '')

    template = "{% if var %}hello{% endif %}"
    context = {
        "var": s,

    }
    expected = "hello"

    check_equal(template, context, expected)


@given(s=text())
def test_output_if(s):

    assume(not s == '')
    assume('{' not in s)
    assume('}' not in s)

    template = "{% if var %}==" + s + "{% endif %}"
    context = {
        "var": "on",

    }
    expected = '==' + s

    check_equal(template, context, expected)


@given(s=text())
def test_nested_truthy_if(s):

    assume(not s == '')

    template = "{% if var %}hello {% if var %}{{var}}{% endif %}{% endif %}"
    context = {
        "var": s,

    }
    expected = "hello " + s

    check_equal(template, context, expected)


@given(s=text(), t=text())
def test_if_else(s, t):

    template = "{% if var %}s: {{s}}{% else %}t: {{t}}{% endif %}"
    context = {
        "var": True,
        "s": s,
        "t": t
    }
    expected = "s: " + s

    check_equal(template, context, expected)

    context = {
        "var": False,
        "s": s,
        "t": t
    }
    expected = "t: " + t

    check_equal(template, context, expected)


@given(s=text())
def test_equality_if(s):

    assume('\n' not in s)
    assume('"' not in s)
    assume("'" not in s)

    template = "{% if var == \"" + s + "\" %}equal{% endif %}"
    context = {
        "var": s,
    }
    expected = "equal"

    check_equal(template, context, expected)

    # Repeat with single quoted string
    template = "{% if var == '" + s + "' %}equal{% endif %}"
    check_equal(template, context, expected)


@given(s=text())
def test_non_equality_if(s):

    assume('\n' not in s)
    assume('"' not in s)
    assume("'" not in s)

    template = "{% if var != \"" + s + "\" %}unequal{% else %}equal{% endif %}"
    context = {
        "var": s + '.',  # modify so not equal
    }
    expected = "unequal"

    check_equal(template, context, expected)

    # Repeat with single quoted string
    template = "{% if var != '" + s + "' %}unequal{% else %}equal{% endif %}"
    check_equal(template, context, expected)


def test_length_gt():

    template = '{% if var.len > 10 %}greater than{% else %}less than{% endif %}'
    context = {
        "var": 'long string with more than 10 characters'
    }
    expected = 'greater than'

    check_equal(template, context, expected)

    # Repeat with short string
    context = {
        "var": 'short'
    }
    expected = 'less than'
    check_equal(template, context, expected)


def test_length_lt():

    template = '{% if var.len < 10 %}less than{% else %}greater than{% endif %}'
    context = {
        "var": 'long string with more than 10 characters'
    }
    expected = 'greater than'
    check_equal(template, context, expected)

    # Repeat with short string
    context = {
        "var": 'short'
    }
    expected = 'less than'
    check_equal(template, context, expected)


def test_length_equality():

    template = '{% if var.len == 12 %}equal{% else %}not equal{% endif %}'
    context = {
        "var": '12characters'
    }
    expected = 'equal'
    check_equal(template, context, expected)

    # Repeat with short string
    context = {
        "var": 'short'
    }
    expected = 'not equal'
    check_equal(template, context, expected)


def test_length_non_equality():

    template = '{% if var.len != 12 %}not equal{% else %}equal{% endif %}'
    context = {
        "var": '12characters'
    }
    expected = 'equal'
    check_equal(template, context, expected)

    # Repeat with short string
    context = {
        "var": 'short'
    }
    expected = 'not equal'
    check_equal(template, context, expected)


def test_invalid_len():

    template = '{% if var.len > string %}less than{% endif %}'
    with pytest.raises(TemplateError) as te:
        check_equal(template, {}, '')
        assert("Template error at line 1" in str(te))

    template = '{% if var.len < string %}less than{% endif %}'
    with pytest.raises(TemplateError) as te:
        check_equal(template, {}, '')
        assert("Template error at line 1" in str(te))

    template = '{% if var.len > "string" %}less than{% endif %}'
    with pytest.raises(TemplateError) as te:
        check_equal(template, {}, '')
        assert("Template error at line 1" in str(te))

    template = '{% if var.len < "string" %}less than{% endif %}'
    with pytest.raises(TemplateError) as te:
        check_equal(template, {}, '')
        assert("Template error at line 1" in str(te))


@given(s=text(), t=text())
def test_compund(s, t):

    assume('\n' not in s)
    assume('"' not in s)

    template = """Hello {{s}},
{% if b %}
    You are true. Have a string: {{t}}
{% else %}
    You are false. No string :( '87675675^^^8 £$$£@$(*&'')
{% endif %}
Thanks,
Terrapin
    """

    context = {
        "s": s,
        "t": t,
        "b": True
    }

    expected = """Hello """ + s + """,

    You are true. Have a string: """ + t + """

Thanks,
Terrapin
    """

    check_equal(template, context, expected)

    context = {
        "s": s,
        "t": t,
        "b": False
    }

    expected = """Hello """ + s + """,

    You are false. No string :( '87675675^^^8 £$$£@$(*&'')

Thanks,
Terrapin
    """

    check_equal(template, context, expected)


@given(n=integers(min_value=0, max_value=128))
def test_many_nested_if(n):

    def make_nested(m):

        if m == 0:
            return " HELLO "
        else:
            return "{% if var %}" + make_nested(m - 1) + "{% endif %}"

    template = make_nested(n)

    context = {
        "var": True,

    }
    expected = " HELLO "

    check_equal(template, context, expected)


@given(s=text())
def test_template_error(s):

    invalid_template = "{% if var %}s: {{s}}{% end %}"

    with pytest.raises(TemplateError) as te:
        check_equal(invalid_template, {}, '')
        assert("Template error at line 1" in str(te))

    invalid_template = "{% if var %}s: {{s}}"

    with pytest.raises(TemplateError) as te:
        check_equal(invalid_template, {}, '')
        assert("Unknown template error" in str(te))


def test_quoty_string():

    template = """<li itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="{{level_up}}" title="{{initial_title}}" itemprop="url"><span itemprop="title">{{initial_title}}</span></a></li>"""
    context = {}
    expected = """<li itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="" title="" itemprop="url"><span itemprop="title"></span></a></li>"""
    check_equal(template, context, expected)


def test_used_variables_simple():

    template = "{{var1}} test {{var2}}"
    used = used_variables(template)
    expected = {"var1", "var2"}
    assert used == expected

    template = "{{var1}}{{var2}}{{  }}"
    used = used_variables(template)
    expected = {"var1", "var2"}
    assert used == expected

    template = "{{var1}}{{var2}}{{var2}}"
    used = used_variables(template)
    expected = {"var1", "var2"}
    assert used == expected


def test_used_variables_full():

    template = "{{var1}} test {{var2}} {% if var3 == 'hello' %}{{var4}}{% else %}{{var5}}{% endif %}"
    used = used_variables(template)
    expected = {"var1", "var2", "var3", "var4", "var5"}
    assert used == expected

    template = "{{var1}} test {{var2}} {% if var3 != 'hello' %}{{var4}}{% else %}{{var5}}{% endif %}"
    used = used_variables(template)
    expected = {"var1", "var2", "var3", "var4", "var5"}
    assert used == expected
