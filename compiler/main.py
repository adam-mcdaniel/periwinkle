import click
from os import mkdir, system
from constants import CABLELANG_PRELUDE
from parser import compile_file



@click.group()
def main():
    """
    The compiler for the periwinkle programming language.
    """
    pass


@main.command()
def info():
    "Displays info on the periwinkle compiler"
    custom_info('Periwinkle compiler v{}'.format(__version__))
    for improvement in __improvements__:
        custom_info(improvement)


@main.command()
@click.argument('input_file')
def compile(input_file):
    "Compile a periwinkle script in debug mode"

    output_dir = "out"
    try:
        system("wire new " + output_dir)
        mkdir(output_dir + "/include/external")
    except: pass

    script = compile_file(input_file)
    open(
        "out/src/main.cb", "w"
    ).write(CABLELANG_PRELUDE + script)

    system("cd out; wire run")


if __name__ == "__main__":
    main()