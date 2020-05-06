import argparse
import re

"""
Tools for modifying complex argparse objects in python, usually to add new options.
"""

def get_subparser_action(parser):
    """
    FIXME: Is the order here important? Can we scan front to back or back to front and avoid this logic?
    """
    neg1_action = parser._actions[-1]

    if isinstance(neg1_action, argparse._SubParsersAction):
        return neg1_action

    for a in parser._actions:
        if isinstance(a, argparse._SubParsersAction):
            return a

def get_parsers(parser, maxdepth=0, depth=0):
    """
    Yields all "argparse.ArgumentParser" objects in an argparse tree.
    """
    if maxdepth and depth >= maxdepth:
        return

    # Current parser
    yield parser

    # Subparsers
    if parser._subparsers:
        choices = ()

        subp_action = get_subparser_action(parser)
        if subp_action:
            choices = subp_action.choices.items()
        
        for _, sub in choices:
            if isinstance(sub, argparse.ArgumentParser):
                for p in get_parsers(
                    sub, maxdepth, depth + 1
                ):
                    yield p

def matching(parsers, pattern, negate=False):
    """
    Return all parsers with command matching a regular expression "pattern".
    Set "negate" to only return parsers *not* matching this command pattern.
    """
    if type(pattern) == re.Pattern:
        matcher = pattern
    else:
        matcher = re.compile(pattern)
    for parser in parsers:
        parser_cmd = " ".join(parser.prog.split()[1:])
        match = bool(matcher.match(parser_cmd))
        if negate:
            match = not match
        if match:
            yield parser

def with_option(parsers, option_name_pattern, negate=False):
    """
    Return parsers having an option with a name matching the given regular expression.
    Works with "help", "-h", "--help".
    Set "negate" to only return parsers *without* a matching option statement.
    """
    if type(option_name_pattern) == re.Pattern:
        matcher = option_name_pattern
    else:
        matcher = re.compile(option_name_pattern)
    for parser in parsers:
        match = False
        for action in parser._actions:
            if matcher.match(action.dest):
                # Check option destination variable name
                match = True
            else:
                # Check option strings
                for option_string in action.option_strings:
                    if matcher.match(option_string):
                        match = True
        if negate:
            match = not match
        if match:
            yield parser
