from aiogram.fsm.storage.memory import MemoryStorage


def get_storage() -> MemoryStorage:
    return MemoryStorage()
