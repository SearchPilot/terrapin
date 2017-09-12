
class TemplateError(Exception):
    """Exception raised during parsing of a template

    Attributes:
        line_number: line number of the error
        position: position of the error
        value: value when the error occured
    """

    def __init__(self, template, line_number=0, position=0, value=None, message=None):

        if not message:
            if line_number != 0:
                error_mask = "Template `{ts}` gives error at line {ln}, position {p} at: {v}"
            else:
                error_mask = "Template `{ts}` gives unknown error."

            message = error_mask.format(ts=template[:50],
                                        ln=line_number,
                                        p=position,
                                        v=value)

        super(TemplateError, self).__init__(message)
