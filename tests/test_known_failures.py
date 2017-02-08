import pytest

from tests.utils import check_equal
from terrapin.used_variables import used_variables


@pytest.mark.xfail(reason="Render Full can't handle variable inside single quotes")
def test_single_quote_either_side_var():

    template = "{% if var1 %}This won't {{var2}} work. '{% endif %}"
    context = {
        "var1": 'True',
        "var2": 'actually'
    }
    expected = "This won't actually work. '"

    check_equal(template, context, expected)


@pytest.mark.xfail(reason="Render Full can't handle variable inside double quotes")
def test_double_quote_either_side_var():

    template = '{% if var1 %} My var is "{{var2}}" {% endif %}'
    context = {
        "var1": 'True',
        "var2": 'actually'
    }
    expected = 'My var is "actually"'

    check_equal(template, context, expected)


@pytest.mark.xfail(reason="Render Full can't handle variable inside single quotes")
def test_used_variables_single_quote_either_side_var():

    template = "'{{var1}}' {% if var2 %}{{var2}}{% endif %}"
    used = used_variables(template)
    expected = {"var1", "var2"}
    assert used == expected


@pytest.mark.xfail(reason="Render Full can't handle variable inside double quotes")
def test_used_variables_double_quote_either_side_var():

    template = '"{{var1}}"" {% if var2 %}{{var2}}{% endif %}'
    used = used_variables(template)
    expected = {"var1", "var2"}
    assert used == expected


@pytest.mark.xfail(reason="Render Full can't handle }}")
def test_js_style_double_end_brace_full():

    template = "{% if var %}{{var}}{% endif %}Hello}}"
    context = {}
    expected = "Hello}}"
    check_equal(template, context, expected)
