import click






@click.command()
@click.option('--name', prompt='Your name please')
def hello(name):
    click.echo(f"Hello {name}!")

hello()
