"""Messages API with an explicit version header. Offline unless --live is supplied."""
from provider_requests import run_cli

if __name__ == "__main__":
    run_cli("claude")
