"""Validate supplied DNS snapshots without making a network request."""
from integration_core import endpoint_policy


if __name__ == "__main__":
    hosts = {"tools.example.invalid"}
    print(endpoint_policy("https://tools.example.invalid/mcp", hosts, ["93.184.216.34"]))
    for addresses in (["127.0.0.1"], ["169.254.169.254"], ["93.184.216.34", "::1"]):
        try:
            endpoint_policy("https://tools.example.invalid/mcp", hosts, addresses)
        except ValueError:
            print("blocked non-public resolution")
    print("Production: bind the validated DNS result to the actual connection; disable cross-origin redirects.")
