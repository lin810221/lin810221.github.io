"""Default prints a bound query plan; --live runs SELECT on your own database."""
import argparse
from engine_clients import PG_QUERY,pg_parameters

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live",action="store_true")
    if parser.parse_args().live:
        from pg_driver import query_existing
        print(query_existing("alpha","usb hub",3))
    else:
        print("OFFLINE SQL",PG_QUERY)
        print("Parameter types",[type(v).__name__ for v in pg_parameters("alpha","usb hub",3)])
        print("No PostgreSQL service or query plan was executed.")
