from twitch.message_handler import commands, PREFIX


@commands.add(name="help", aliases=["cmds"], cooldown=5)
def help_command(ctx):
    ctx.reply(f"Commands: {', '.join(PREFIX + c for c in commands.list())}")
