from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

user_commands = [BotCommand(command="info", description="information"),
                 BotCommand(command="current_order", description="your current order"),
                 BotCommand(command="help", description="ofc we help you!")]

async def setup_bot_commands(bot):
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(user_commands)