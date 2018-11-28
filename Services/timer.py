from .managed_service import ManagedService
from Services.class_utils import exposify

@exposify
class Timer(ManagedService):
    pass

_default = Timer