# easyrename
Easily batch rename files to remove unnecessary fields

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

