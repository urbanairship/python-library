class Constant(object):
    KEY_CLASS=None

    @classmethod
    def validate(cls, item, allow_private=False):
        if allow_private:
            underscores = '__'
        else:
            underscores = '_'

        class_dict = {
            (cls.__name__ + '.' + attr): val for
            attr, val in cls.__dict__.iteritems() if
            not callable(attr) and not attr.startswith(underscores)
            and not attr == 'KEY_CLASS'
        }

        if item not in class_dict.values():
            raise ValueError(
                "Unrecognized option '{}'. {}".format(
                    item,
                    cls._build_error_string(class_dict)
                )
             )

    @classmethod
    def _build_error_string(cls, class_dict):
            col1 = max([len(attr) for attr in class_dict.keys()])
            col2 = max([len(str(val)) for val in class_dict.values()])
            table = ""
            if not cls.KEY_CLASS:
                row_format = '{:<' + str(col1) + '}  {:<' + str(col2) + '}\n'
                table += row_format.format('Enum', 'Corresponding String')
                table += row_format.format(
                    '-' * max(col1, 4),
                    '-' * max(col2, 20)
                )
                for key, val in class_dict.iteritems():
                    table += row_format.format(key, val)
                return "Valid options for '{}' are:\n\n{}".format(cls.__name__, table)
            row_format = '{:<' + str(col1) + '}\n'
            table += row_format.format('Keys')
            table += row_format.format('-' * max(col2, 4))
            for val in class_dict.values():
                table += row_format.format(val)
            return "Valid keys for '{}' are:\n\n{}".format(cls.KEY_CLASS, table)


def check_multiple(item, *args):
    errors = []
    for enum in args:
        try:
            enum.validate(item, allow_private=True)
        except ValueError as e:
            errors.append(str(e))
    if len(errors) == len(args):
        raise ValueError('\n'.join(errors))


def rgb(red, green, blue):
    """Helper function that returns rgb strings to be used
    by color-specification headers.

    Arguments:
        red (int): Red color value.
        green (int): Green color value.
        blue (int): Blue color value.

    Returns:
        A string representing the specified color.

    Example:
        >>> rgb(23, 167, 42)
        'rgb(23, 167, 42)'
    """
    return 'rgb({0:d},{1:d},{2:d})'.format(red, green, blue)
