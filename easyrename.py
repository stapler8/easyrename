import getopt
import os
import sys
import re
from operator import indexOf

# get arguments
args = sys.argv[1:]

options = 'hd:f:e:l:vy'
long_options = ['help', 'delimiter', 'fields', 'extension', 'filter', 'verbose', 'yes']

parameters = {
    'directory': b'',
    'delimiter': ' ',
    'fields': [1],
    'extension': '*',
    'filter': '*',
    'verbose': False,
    'yes': False
}

help_string = '''
    Usage: python3 easyrename.py OPTION... [FILE]...
    
    Arguments:
        -h, --help:      Show this help message and exit
        -d, --delimiter: Specify character(s) to delimit fields with
        -f, --fields:    Specify field(s) to include in renamed file
                           Separate fields with comma
                           Denote ranges with hyphen
        -e, --extension: Specify extension of files to be renamed
        -l, --filter:    Filter files to rename with regular expression
        -v, --verbose:   List files as they are renamed
        -y, --yes:       Do not confirm before renaming files
'''

def process_arguments():
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        parameters['directory'] = os.fsencode(values[0])

        # ensure directory is valid
        if not os.path.exists(parameters['directory']):
            raise FileNotFoundError(f'Error: directory {parameters["directory"]} does not exist')

        for argument in arguments:
            if argument[0] in ('-h', '--help'):
                print(help_string)
                sys.exit(0)

            elif argument[0] in ('-d', '--delimiter'):
                parameters['delimiter'] = argument[1]

            elif argument[0] in ('-f', '--fields'):
                get_fields(argument[1])

            elif argument[0] in ('-e', '--extension'):
                parameters['extension'] = argument[1]

            elif argument[0] in ('-l', '--filter'):
                parameters['filter'] = argument[1]

            elif argument[0] in ('-v', '--verbose'):
                parameters['verbose'] = True

            elif argument[0] in ('-y', '--yes'):
                parameters['yes'] = True

    except (getopt.error, FileNotFoundError) as err:
        print("Error: " + str(err))
        sys.exit(1)


def get_fields(fields: str):
    parameters['fields'] = []

    try:
        field_value = ''
        i = -1

        #loop using walrus operator to allow continue statements and modifying the value of i
        #effectively for i in range(len(fields))
        while (i := i + 1) < len(fields):

            # catch invalid fields
            if fields[i] not in ',' '-' and not fields[i].isnumeric():
                raise ValueError(f'Invalid field {fields[i]}')

            # catch improper use of field separators at beginning of string
            if i == 0 and fields[i] in ',' '-':
                raise ValueError(f'Invalid field string {fields}')

            if fields[i].isnumeric():
                field_value += fields[i]
                continue

            if fields[i] == ',':
                parameters['fields'].append(int(field_value))
                field_value = ''
                continue

            # handle ranges
            if fields[i] == '-':
                temp_field = fields[i+1:]

                # catch improper use of range separators
                if temp_field.count(',') > 0 and temp_field.count('-') > 0:
                    if temp_field.index('-') < temp_field.index(','):
                        raise ValueError(f'Invalid field string {fields}')

                # add range to next comma
                if temp_field.count(',') > 0:
                    print(int(temp_field[0:temp_field.index(',')]))
                    for j in range(int(field_value), int(temp_field[0:temp_field.index(',')]) + 1):
                        parameters['fields'].append(j)

                    # move iterator to after the range
                    i = temp_field.index(',') + len(fields) - len(temp_field)
                    field_value = ''
                    continue

                # handle ranges at end of string
                for j in range(int(field_value), int(temp_field[0:])):
                    parameters['fields'].append(j)
                    field_value = ''

        # add final field_value to field parameter
        if field_value != '':
            parameters['fields'].append(int(field_value))

    except ValueError as err:
        print(f"Error: " + str(err))
        sys.exit(1)

def rename():

    try:
        # process files in directory
        for file in os.listdir(parameters['directory']):
            filename = os.fsdecode(file)
            basename, extension = os.path.splitext(filename)

            # don't rename files not matching extension
            if (parameters['extension'] != '*'
                    and not extension.endswith(parameters['extension'])):
                continue

            # don't rename files not matching filter
            if (parameters['filter'] != '*'
                    and not re.search(parameters['filter'], filename)):
                continue

            # split filename into parts
            fields = basename.split(parameters['delimiter'])

            #
            # rename files
            #
            new_filename = ''.join([fields[i - 1] + parameters['delimiter'] for i in parameters['fields']])[:-1] + extension

            # confirm rename
            if not parameters['yes']:
                print(f'Old File: {filename}')
                print(f'New File: {new_filename}')
                print(f'Proceed with rename? [(Y)es/(n)o/(a)ll] ', end='')
                selection = input('')

                if selection.lower() in 'n' 'no':
                    print('abort.')
                    sys.exit(0)

                if selection.lower() in 'a' 'all':
                    parameters['yes'] = True

            os.rename(os.fsdecode(parameters['directory']) + filename,
                      os.fsdecode(parameters['directory']) + new_filename)
            if parameters['verbose']:
                print(f'Renamed File: {new_filename}')


    except IndexError as err:
        print(f'Error: {str(err)}')
        sys.exit(1)



process_arguments()
rename()
