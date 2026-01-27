"""Voice profile management tool module."""


def mount(config: dict):
    """Mount function called by amplifier-core module loader."""
    from .tool import MyVoiceProfilesTool

    return MyVoiceProfilesTool(config)
