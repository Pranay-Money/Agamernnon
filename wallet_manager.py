from solders.keypair import Keypair
import base58

class InvalidPrivateKeyError(Exception):
    pass

def derive_keypair(private_key: str) -> Keypair:
    try:
        secret = base58.b58decode(private_key.strip())
    except Exception as exc:
        raise InvalidPrivateKeyError(f"could not decode base58: {exc}") from exc

    if len(secret) == 64:
        return Keypair.from_bytes(secret)
    if len(secret) == 32:
        return Keypair.from_seed(secret)
    raise InvalidPrivateKeyError(
        f"invalid key length: {len(secret)} bytes (expected 32 or 64)"
    )

def derive_address(private_key: str) -> str:
    return str(derive_keypair(private_key).pubkey())

def create_wallet() -> tuple[str, str]:
    kp = Keypair()
    secret_key = base58.b58encode(bytes(kp)).decode("utf-8")
    return str(kp.pubkey()), secret_key

def get_wallets(context) -> list:
    return context.user_data.setdefault("wallets", [])

def get_active_index(context) -> int:
    return context.user_data.get("active_wallet_index", 0)

def set_active_index(context, index: int) -> None:
    context.user_data["active_wallet_index"] = index

def add_wallet(context, address: str, secret_key: str) -> dict:
    wallets = get_wallets(context)
    label = f"W{len(wallets) + 1}"
    wallet = {"label": label, "address": address, "secret_key": secret_key}
    wallets.append(wallet)
    set_active_index(context, len(wallets) - 1)
    return wallet