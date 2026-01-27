"""Voice profile sync hook module."""


def mount(coordinator, config: dict):
    """Mount function called by amplifier-core module loader."""
    from .hook import MyVoiceSyncHook

    return MyVoiceSyncHook(config)
