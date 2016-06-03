from hypothesis import given, assume
from hypothesis.strategies import text, integers
import pytest

from terrapin.exceptions import TemplateError
from terrapin import render


def check_equal(template, context, expected):

    result = render(template, context)

    assert result == expected


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

    template = "{% if var == \"" + s + "\" %}equal{% endif %}"
    context = {
        "var": s,
    }
    expected = "equal"

    check_equal(template, context, expected)


@given(s=text())
def test_non_equality_if(s):

    assume('\n' not in s)
    assume('"' not in s)

    template = "{% if var != \"" + s + "\" %}unequal{% else %}equal{% endif %}"
    context = {
        "var": s + '.',  # modify so not equal
    }
    expected = "unequal"

    check_equal(template, context, expected)


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
