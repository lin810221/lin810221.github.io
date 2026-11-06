"""Estimate payload plus graph, with total copies and explicit exclusions."""
from search_core import capacity

if __name__ == "__main__":
    for bits,originals in ((32,False),(8,False),(8,True),(1,True)):
        print("bits",bits,"retain originals",originals,
              capacity(1000000,1536,bits=bits,neighbors=16,replicas=2,keep_original=originals))
    print("Not a complete RSS/disk estimate: metadata, WAL, cache, backups and graph levels are excluded.")
