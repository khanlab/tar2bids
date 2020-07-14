from io import StringIO
import numpy as np


def reformat(data):
    """
    Convert data into integer or floating point data

    :param data:
    :return:
    """
    try:
        data = data.decode('utf-8')
    except AttributeError:
        pass

    if data.isdecimal():
        return int(data)
    else:
        try:
            return float(data)
        except ValueError:
            # not a float
            pass

        if data.startswith('(') and data.endswith(')'):
            data = [reformat(x.strip()) for x in data.lstrip('(').rstrip(')').split(',')]
        elif data == 'Yes':
            return True
        elif data == 'No':
            return False

    return data


def jcamp_parse(data):
    jcamp_dict = dict()
    variable = None

    for line in data:
        check = line.lstrip()

        # Skip comment lines
        if check.startswith('$$'):
            pass
        # Line starts a new variable
        elif check.startswith('##'):
            lhs, _, rhs = check.strip('##').partition('=')

            # Stop reading when end is found
            if lhs.lower() == 'end':
                break

            variable = [rhs.rstrip('\n')]
            jcamp_dict[lhs] = variable
        # Line is a data line to append to the previous variable
        elif variable:
            variable.append(line.rstrip('\n'))

    # All variables have now been read

    # Parse the contents of the variables
    for key, value in jcamp_dict.items():

        # If the variable starts with ( then combine all the lines until the first one that ends with )
        # TODO:
        # Edge case when variable is a struct of structs. A contained struct might end a line and therefore exit
        # prematurely before the containing struct is complete. Fixing requires parsing the entire contents because
        # the struct could contain strings with parenthesis. This requires a char by char parser which is considerably
        # more difficult for an extremely unlikely occurrence.
        has_struct = False
        if value[0].lstrip().startswith('('):
            has_struct = True
            first_line = ''
            line = value[0]

            # Concatenate lines until one that ends in ) is reached
            for line in value:
                first_line += line
                if line.rstrip().endswith(')'):
                    break

            # Combine all the rest of the lines into one long data string
            data = ''.join(value[value.index(line)+1:])
            if data:
                value = [first_line, data]
            else:
                value = [first_line]

        if len(value) == 1:
            # Only one line in data so just parse the data
            jcamp_dict[key] = reformat(value[0])
        elif has_struct:
            # Data has multiple lines, so the first line is the dimensions of the array of data
            # Read the dimensions
            dim = [int(x.strip()) for x in value[0].lstrip('(').rstrip(')').split(',')]

            data = value[1]
            if data.lstrip().startswith('('):
                # Second line starts with ( so there is an array of structs
                data = [[reformat(y.strip()) for y in x.lstrip('(').rstrip(')').split(',')] for x in data.split(') (')]
            elif len(dim) == 1 and data.lstrip().startswith('<'):
                # Second line start with < so it is a string and the dimensions are the maximum length
                jcamp_dict[key] = {'maximum_length': dim[0], 'value': data}
                continue
            else:
                # Second line is an array of data. Split on whitespace and reformat each entry.
                data = [reformat(x) for x in data.split()]

            jcamp_dict[key] = {'dim': dim, 'value': data}

    return jcamp_dict


def jcamp_read(data):

    if not isinstance(data, bytes) or isinstance(data, str):
        # Try to use data as a filename
        try:
            with open(data, 'r') as fh:
                return jcamp_parse(fh)
        except IOError:
            pass
        except (TypeError, ValueError):
            # Was not a valid filename, so continue trying other options
            pass
        except OSError as err:
            if err.errno != 63:
                raise

    # It was not a filename, so it should be a string
    # Make sure that data is str and not bytes
    try:
        data = data.decode('utf-8')
    except AttributeError:
        # Was not a bytes so it did not have decode attribute
        pass

    # Convert to IO object which permits iterating through string on linebreaks
    try:
        handle = StringIO(data)
    except TypeError:
        # Was not a str object so assume it is a list of lines
        handle = data

    # Parse the data
    return jcamp_parse(handle)


class JCAMPData(dict):
    def __init__(self, data, *args, **kwargs):
        super(JCAMPData, self).__init__(*args, **kwargs)
        self.update(jcamp_read(data))

    def __str__(self):
        return '\n'.join(['{key} = {value}'.format(key=key, value=value) for key, value in self.items()])

    def format(self, variable):
        data = self[variable]
        if 'dim' in data:
            a = np.empty((len(data['value']), 1))
            for counter, value in enumerate(data['value']):
                a[counter] = value
            data = np.reshape(a, data['dim'])
        elif 'maximum_length' in data:
            data = str(data['value'])

        return data
