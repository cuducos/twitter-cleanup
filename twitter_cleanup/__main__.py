import click
from twitter_cleanup import TwitterCleanup


@click.group()
@click.option("--yes", "-y", help="Yes to all prompts", default=False, is_flag=True)
@click.pass_context
def cli(context, yes):
    """Twitter Cleanup"""
    context.obj = {"cleanup": TwitterCleanup(assume_yes=yes)}


@cli.command()
@click.argument("days", type=int)
@click.pass_context
def inactive(context, days):
    """Unfollow accounts inactive for a given amount of days."""
    context.obj["cleanup"].unfollow_inactive_for(days=days)


@cli.command()
@click.option(
    "--threshold",
    "-t",
    help="Botometer threshold (form 0 to 100, default=75)",
    default=75,
    type=click.IntRange(0, 100),
)
@click.pass_context
def bots(context, threshold):
    """Soft-block bots following you."""
    context.obj["cleanup"].soft_block_bots(threshold=threshold / 100)


if __name__ == "__main__":
    cli()
