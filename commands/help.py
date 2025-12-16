from twitch.commands import handler, PREFIX


@handler.command(name="help", aliases=["cmds"], cooldown=5)
def help_command(ctx):
    ctx.reply(f"Commands: {', '.join(PREFIX + c for c in handler.get_all())}")
