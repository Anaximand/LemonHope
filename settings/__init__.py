modules = dict()

TABLE_NAME = 'settings'

def registerModule(module, settingNames) -> None:
    """
    Register a setting module
    """
    modules[module] = ['enabled'] + settingNames
