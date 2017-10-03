from threading import Thread

from terrapin.render_full import render_full

def run_render(template, context, expected):

    result = render_full(template, context)
    assert result == expected

def test_threading():

    template_1 = """Hello {{var_1}}, this a template """
    context_1 = {"var_1": "person"}
    expected_1 = "Hello person, this is a template"

    template_2 = """If {% var_2 %}{{var_3}}{% endif %} test test """
    context_2 = {"var_2": True, "var_3": "value", "var_1": "other person"}
    expected_2 = "If value test test "

    N = 1000
    for i in range(N):
        if i % 2 == 0:
            template, context, expected = template_1, context_1, expected_1
        else:
            template, context, expected = template_2, context_2, expected_2
        t = Thread(target=render_full, args=(template, context))
        t.start()
