import click


@click.command()
def get():
    """Hello World Command"""
    pass


@click.group(name='mbnatafgi')
def mbnatafgi():
    pass


mbnatafgi.add_command(get)

if __name__ == '__main__':
    mbnatafgi()
