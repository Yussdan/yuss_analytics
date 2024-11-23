import pytest
from unittest.mock import AsyncMock, patch
from bot.bot import start, button_handler


@pytest.mark.asyncio
async def test_start_command():
    mock_update = AsyncMock()
    mock_context = AsyncMock()

    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.edit_message_text = AsyncMock()

    mock_update.message = AsyncMock()
    mock_update.message.reply_text = AsyncMock()

    with patch("bot.bot.InlineKeyboardMarkup") as mock_markup, \
         patch("bot.bot.InlineKeyboardButton") as mock_button:
        mock_markup.return_value = "mock_markup"
        mock_button.return_value = "mock_button"

        await start(mock_update, mock_context)

        mock_update.callback_query.edit_message_text.assert_called_once_with(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup="mock_markup"
        )

        mock_update.callback_query = None
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup="mock_markup"
        )

@pytest.mark.asyncio
async def test_button_handler():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    
    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.answer = AsyncMock()

    with patch("bot.bot.handle_start", new_callable=AsyncMock) as mock_handle_start:
        mock_update.callback_query.data = "start"
        await button_handler(mock_update, mock_context)
        mock_handle_start.assert_called_once_with(mock_update.callback_query)

    with patch("bot.bot.handle_back", new_callable=AsyncMock) as mock_handle_back:
        mock_update.callback_query.data = "back"
        await button_handler(mock_update, mock_context)
        mock_handle_back.assert_called_once_with(mock_update.callback_query)

    with patch("bot.bot.handle_cripto_selection", new_callable=AsyncMock) as mock_handle_cripto_selection:
        mock_update.callback_query.data = "BTC"
        await button_handler(mock_update, mock_context)
        mock_handle_cripto_selection.assert_called_once_with(mock_update.callback_query, mock_update.callback_query.data)

    with patch("bot.bot.cripto_value", new_callable=AsyncMock) as mock_cripto_value:
        mock_update.callback_query.data = "BTC_history"
        await button_handler(mock_update, mock_context)
        mock_cripto_value.assert_called_once_with('history', mock_update.callback_query, 'BTC')

    with patch("bot.bot.handle_callback", new_callable=AsyncMock) as mock_handle_callback:
        mock_update.callback_query.data = "BTC_callback"
        await button_handler(mock_update, mock_context)
        mock_handle_callback.assert_called_once_with(mock_update.callback_query, "BTC_callback")

