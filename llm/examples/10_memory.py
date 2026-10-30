"""Persistent storage within a temporary demo directory; no permanent file by default."""
from pathlib import Path
from tempfile import TemporaryDirectory
from memory_store import MemoryStore

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "memory.sqlite"
        with MemoryStore(path) as store:
            store.append("alice", "chat1", "問題一")
            store.set_preference("alice", "language", "zh-TW")
        with MemoryStore(path) as reopened:
            print("恢復歷史：", reopened.history("alice", "chat1"))
            print("另一個人：", reopened.history("bob", "chat1"))
            print("跨對話偏好：", reopened.preference("alice", "language"))
