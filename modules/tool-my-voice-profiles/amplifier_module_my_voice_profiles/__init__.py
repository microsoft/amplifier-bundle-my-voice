"""Voice profile management tool module."""


def mount(coordinator, config: dict):
    """Mount function called by amplifier-core module loader."""
    from .tool import MyVoiceProfilesTool

    return MyVoiceProfilesTool(config)
