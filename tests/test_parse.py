from terrapin.parser import Parser


def check_equal(template, context, expected):

    terrapin = Parser()
    result = terrapin.parse(template, context)

    assert result == expected


def test_variable():

    template = "{{var}}"
    context = {
        "var": "test"
    }
    expected = "test"

    check_equal(template, context, expected)
