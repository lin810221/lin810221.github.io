"""Run from the extracted examples directory. Tokens print only at provisioning."""
import argparse
import asyncio
from gateway.settings import Settings
from gateway.store import Store
from gateway.worker import run_once


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['migrate', 'provision', 'revoke', 'work-once', 'work'])
    parser.add_argument('--tenant', default='demo')
    parser.add_argument('--role', choices=['reader', 'editor'], default='editor')
    args = parser.parse_args()
    store = Store(Settings().database_path)
    try:
        store.migrate()
        if args.command == 'provision':
            print(store.provision(args.tenant, args.role))
        elif args.command == 'revoke':
            import getpass
            store.revoke(getpass.getpass('Token to revoke (hidden): '))
            print('credential removed if present')
        elif args.command == 'work-once':
            print(asyncio.run(run_once(store)))
        elif args.command == 'work':
            async def work():
                while True:
                    try:
                        await run_once(store)
                    except Exception:
                        print('job failed; inspect persisted safe event codes')
                    await asyncio.sleep(.5)
            try:
                asyncio.run(work())
            except KeyboardInterrupt:
                pass
        else:
            print('schema at revision 0001')
    finally:
        store.engine.dispose()


if __name__ == '__main__':
    main()
