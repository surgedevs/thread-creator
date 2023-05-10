"""
:author @Surge
:contributors @Surge

Creates threads via a button click.
"""

import discord

TOKEN = 'DISCORD_BOT_TOKEN_HERE'

intents = discord.Intents.none()
bot = discord.Bot(intents=intents)


class ThreadButtonView(discord.ui.View):
    """
    View for the thread creation button.
    """

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label='Create',
        style=discord.ButtonStyle.primary,
        emoji='➕',
        custom_id='thread-create'
    )
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        channel: discord.abc.GuildChannel = await bot.fetch_channel(interaction.channel_id)

        thread: discord.Thread = await channel.create_thread(
            name=interaction.user.name + '\'s Clyde thread',
            message=None,
            auto_archive_duration=60,
            type=None,
            invitable=True,
            reason='Clyde thread creation'
        )

        await thread.add_user(interaction.user)
        await thread.send(embed=discord.Embed(
            title='👋 This is your private thread!',
            description='Mention Clyde to convert your thread into a Clyde thread!',
            color=0x5964f0
        ))

        embed = discord.Embed(
            title='✅ Done!',
            description='Thread created.',
            color=0x00ff00
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


@bot.slash_command()
@discord.default_permissions(manage_guild=True)
@discord.commands.guild_only()
async def send_thread_creator(ctx: discord.ApplicationContext) -> None:
    """
    Creates a command to send an embed with a button to create threads.

    :param ctx: discord.ext.commands.Context
    :returns: None
    """

    embed = discord.Embed(
        title='💬 Create a thread',
        description='Click the button below to create a new thread!',
        color=0x5964f0,
    )

    await ctx.send(embed=embed, view=ThreadButtonView())
    await ctx.respond(ephemeral=True, embed=discord.Embed(
        title='✅ Done!',
        description=discord.Embed.Empty,
        color=0x00ff00
    ))


@bot.event
async def on_ready() -> None:
    """
    Prints a logging on message.

    :return: None
    """

    print('Logged in as: {}'.format(bot.user))

    bot.add_view(ThreadButtonView())


bot.run(TOKEN)
