import asyncio
import pytest
pytest_plugins = ('pytest_asyncio',)

from unittest.mock import AsyncMock, MagicMock, patch


# --- Helper to Import Main Safely ---
def import_main_safely():
    with patch("main.discord.Intents") as MockIntents:
        mock_intents = MagicMock()
        mock_intents.message_content = True
        MockIntents.default.return_value = mock_intents
        import main
        return main


@pytest.mark.asyncio
async def test_secret_command():
    main = import_main_safely()
    mock_ctx = MagicMock()
    mock_ctx.send = AsyncMock()

    await main.secret(mock_ctx)

    mock_ctx.send.assert_called_with("Welcome to the club!")


# # --- Blacklist Tests ---
# @pytest.mark.parametrize("message", [
#     "this is shit", "hello bitch", "what the fuck", "heil hitler"
# ])
# def test_blacklisted_words(message):
#     main = import_main_safely()
#     assert main.blacklist_pattern.search(message)
#
#
# @pytest.mark.parametrize("message", [
#     "this is fine", "hello friend", "nice to meet you"
# ])
# def test_non_blacklisted_words(message):
#     main = import_main_safely()
#     assert not main.blacklist_pattern.search(message)
#
#
# # --- Command Tests ---
# @pytest.mark.asyncio
# async def test_assign_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_role = MagicMock()
#     mock_role.name = main.SECRET_ROLE
#     mock_ctx.guild.roles = [mock_role]
#     mock_ctx.author.add_roles = AsyncMock()
#     mock_ctx.send = AsyncMock()
#     mock_ctx.author.mention = "@User"
#
#     await main.assign(mock_ctx)
#
#     mock_ctx.author.add_roles.assert_called_with(mock_role)
#     mock_ctx.send.assert_called_with("@User is now assigned to Bot Tester Group 1.")
#
#
# @pytest.mark.asyncio
# async def test_remove_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_role = MagicMock()
#     mock_role.name = main.SECRET_ROLE
#     mock_ctx.guild.roles = [mock_role]
#     mock_ctx.author.remove_roles = AsyncMock()
#     mock_ctx.send = AsyncMock()
#     mock_ctx.author.mention = "@User"
#
#     await main.remove(mock_ctx)
#
#     mock_ctx.author.remove_roles.assert_called_with(mock_role)
#     mock_ctx.send.assert_called_with("@User has had Bot Tester Group 1 removed.")
#
#
# @pytest.mark.asyncio
# async def test_dm_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_ctx.author.send = AsyncMock()
#
#     await main.dm(mock_ctx, msg="test message")
#
#     mock_ctx.author.send.assert_called_with("You said test message")
#
#
# @pytest.mark.asyncio
# async def test_reply_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_ctx.reply = AsyncMock()
#
#     await main.reply(mock_ctx)
#
#     mock_ctx.reply.assert_called_with("This is a reply to your message!")
#
#
# @pytest.mark.asyncio
# async def test_poll_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_message = MagicMock()
#     mock_ctx.send = AsyncMock(return_value=mock_message)
#     mock_message.add_reaction = AsyncMock()
#
#     await main.poll(mock_ctx, question="Is this a test?")
#
#     mock_ctx.send.assert_called()
#     mock_message.add_reaction.assert_any_call("👍")
#     mock_message.add_reaction.assert_any_call("👎")
#
#
# @pytest.mark.asyncio
# async def test_secret_command():
#     main = import_main_safely()
#     mock_ctx = MagicMock()
#     mock_ctx.send = AsyncMock()
#
#     await main.secret(mock_ctx)
#
#     mock_ctx.send.assert_called_with("Welcome to the club!")
#
#
# @pytest.mark.asyncio
# async def test_secret_error_missing_role():
#     main = import_main_safely()
#     from discord.ext import commands
#
#     mock_ctx = MagicMock()
#     mock_ctx.send = AsyncMock()
#     error = commands.MissingRole(main.SECRET_ROLE)
#
#     await main.secret_error(mock_ctx, error)
#     mock_ctx.send.assert_called_with("You do not have the permission to do that!")
#
#
# # --- Event Test: on_message ---
# @pytest.mark.asyncio
# async def test_on_message_blacklisted():
#     main = import_main_safely()
#
#     mock_message = MagicMock()
#     mock_message.content = "you bitch"
#     mock_message.author = MagicMock()
#     mock_message.delete = AsyncMock()
#     mock_message.channel.send = AsyncMock()
#     main.bot.user = MagicMock()
#     mock_message.author != main.bot.user
#
#     await main.on_message(mock_message)
#
#     mock_message.delete.assert_called_once()
#     mock_message.channel.send.assert_called_once()
#
#
# @pytest.mark.asyncio
# async def test_on_message_clean():
#     main = import_main_safely()
#
#     mock_message = MagicMock()
#     mock_message.content = "Hello friend"
#     mock_message.author = MagicMock()
#     mock_message.delete = AsyncMock()
#     mock_message.channel.send = AsyncMock()
#     main.bot.user = MagicMock()
#     mock_message.author != main.bot.user
#
#     with patch.object(main.bot, 'process_commands', new_callable=AsyncMock) as mock_process:
#         await main.on_message(mock_message)
#         mock_process.assert_called_once_with(mock_message)
#         mock_message.delete.assert_not_called()
#         mock_message.channel.send.assert_not_called()
