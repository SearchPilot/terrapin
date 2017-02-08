
from terrapin import render


def check_equal(template, context, expected):

    result = render(template, context)

    assert result == expected