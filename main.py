from typing import List, Set

from discord import Role, Member, Embed, Color, Guild
from discord.ext import commands
from discord.ext.commands import Bot, Context as CommandContext, Paginator

from config import Config

config = Config.load('config.yaml')

bot = Bot(
    command_prefix=commands.when_mentioned_or('!'),
)


def check_is_mentor(author: Member, role: Role):
    role_name: str = role.name.lower()
    if not role_name.endswith(' lernender'):
        return False
    mentor_role_name = role_name.replace(' lernender', ' mentor')
    return len([role for role in author.roles if role.name.lower() == mentor_role_name]) > 0


def get_members_with_role(role: Role):
    guild: Guild = role.guild
    members: List[Member] = guild.members
    return [member for member in members if role in member.roles]


@bot.command(name='listusers', pass_context=True)
async def list_users(ctx: CommandContext, *, role: Role):
    author: Member = ctx.author
    roles: List[Role] = author.roles
    role_ids: Set[int] = set([role.id for role in roles])
    admin: bool = len(role_ids.intersection(config.admin_roles))
    if not admin and not check_is_mentor(author, role):
        return await ctx.send(
            embed=Embed(
                title='Missing permissions',
                color=Color.red(),
                description='You are neither an admin nor a mentor for this role.'))
    paginator = Paginator(prefix='', suffix='')
    for user in get_members_with_role(role):
        paginator.add_line(f'{user} - {user.mention}')
    for page in paginator.pages:
        await ctx.send(
            embed=Embed(
                title=f'Users with the role @{role.name}',
                description=page))
    if len(paginator.pages) == 0:
        await ctx.send(
            embed=Embed(
                title=f'Users with the role @{role.name}',
                description='No users found.'))


if __name__ == '__main__':
    bot.run(config.token)
