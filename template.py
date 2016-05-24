
from terrapin.parser import Parser


class Terrapin(Parser):
    pass


if __name__ == '__main__':

    test_templates = [
        'Working',
        'Working working',
        '<body><h1>Working</h1></body>',
        '<body><h1>Working working</h1></body>',
        """
        This \t has \t some\n\n
        white space


        in it
        """,
        '{{in_context}}',
        '{{not_in_context}}',
        '{% if in_context %}Working{% endif %}',
        '{% if in_context == "Working" %}Working{% endif %}',
        '{% if in_context == "Working" %}Working {{in_context}}{% endif %}',
        '{% if in_context == "Working" %}Working {{not_in_context}}{% endif %}',
        '{% if in_context == "Not Working" %}Not Working{% else %}Working {{in_context}}{% endif %}',
        '{% if in_context == "Not Working" %}Not Working{% else %}Working {{not_in_context}}{% endif %}',
        """
        {% if in_context == "Not Working" %}
            Not Working
        {% else %}
            <body><h1 id="test " class= "testing">This is some html</h1></body>
            <a href="http://www.distilled.net/?test=foo;bob=bar">R&amp;D</a>
            Working {{in_context}}
        {% endif %}
        """
    ]

    context = {
        'in_context': 'Working',
    }

    terrapin = Terrapin()

    for i, template in enumerate(test_templates):

        print('----------------')
        print("Template {i}: {t}".format(i=i, t=template))
        for t in terrapin.show_tokens(template):
            print(t)

        result = terrapin.parse(template, context)
        print('Result: ', result)
        print('')

    import time
    n = 1000
    for i, template in enumerate(test_templates):
        start_time = time.time()
        for _ in range(n):
            result = terrapin.parse(template, context)
        end_time = time.time()
        ms = (end_time - start_time) * 1000
        a = ms / n
        print('Template {i} completed {n} loops in {ms}ms Avg ({a})'.format(i=i, n=n, ms=ms, a=a))
