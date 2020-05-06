# Argparse Subparser Filter

Python library to make it easy to add an argument to any of many recursive [argparse](https://docs.python.org/3.8/library/argparse.html) subparsers based on properties.

## Use

The utilities in this library make it easier to modify complex argparse trees to add similar commands.
This helps to avoid boilerplate and duplication when specifying parsers since options and arguments can be added to entire 
sets of parsers at the same time.

```python
# This should return an argparse.ArgumentParser
p = generate_parser()

# Get all parser objects in this argparse tree
# You can set "maxdepth" to limit recursion
parsers = get_parsers(p)

# Filter
metadata_parsers = (p for p in with_option(parsers, "metadata")
keys_command_metadata_parsers = (p for p in matching(metadata_parsers, "keys"))

# Modify
for p in keys_command_metadata_parsers:
    # Add additional options
```

## Why

I really like argparse and I end up using it in most of my Python command line tools. Since I can use argparse and not require any additional imports or dependencies, as well as get support for some awesome tooling like [sphinx autoprogram](https://github.com/sphinx-contrib/autoprogram), I have't really looked at other CLI libraries for python even though I know there are many great ones out there.

I originally created this because I wanted to add a `--loglevel" option to every command in an argparse tree with >100 subcommands. The straightforward solution was to add the option to the root parser, like this.

```python
p = argparse.ArgumentParser()
p.add_argument(
    "--loglevel", dest="loglevel", action="store_true", help="Set the logging level for the application."
)
# Add other subparsers, options, etc.
```

But this resulted a CLI API like this.

```bash
cli --loglevel debug cmd1 --flaga --flagb
```

The global flags always had to come before the subcommand-specific options, and you would only see the "help" information for these global options when calling `cli -h`, not when calling `cli cmd1 -h`. This context-dependent behavior was non-intuitive to me, and it was causing me to make frequent mistakes when working with my own tools.  I wanted the output of `-h` for a command to contain all the options for that command, even if some of those were global / parent parser options.

Other cli libraries I had worked with in the past had the concept of ["persistent"](https://github.com/spf13/cobra#persistent-flags) or "global" flags for this very purpose. The argparse library *does* allow you avoid repeating yourself via [parent parsers](https://docs.python.org/3.8/library/argparse.html#parents) ([stackoverflow](https://stackoverflow.com/questions/7498595/python-argparse-add-argument-to-multiple-subparsers)). But if you have a set of arguments you want to add to 10s or hundreds of subparsers, that still means adding a `parents=[shared_args]` argument to every parser and subparser.

With this library, it's easy to add the `--loglevel` flag to every single subcommand on a parser.

```python
p = argparse.ArgumentParser()
# Add other subparsers, options, etc.
for p in argparse_subparser_filter.get_parsers(p):
    p.add_argument(
        "--loglevel", dest="loglevel", action="store_true", help="Set the logging level for the application."
    )
```

Which gives us the CLI syntax we're looking for.

```bash
cli cmd1 --flaga --flagb --loglevel debug
```

## Status

I haven't bothered to put this on pypi yet since it's so small. If there is interest let me know. If I do that, I'll also set up CI and tests.

## Credits

The argparse tree walking code borrows heavily from the `scan_programs` function in the ["sphinxcontrib/autoprogram"](https://github.com/sphinx-contrib/autoprogram/blob/master/sphinxcontrib/autoprogram.py) library.

## License

MIT
