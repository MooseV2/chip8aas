def exposify(cls):
    # cls.__dict__ does not include inherited members, so we can't use that.
    for key in dir(cls):
        val = getattr(cls, key)
        if callable(val) and not key.startswith("_"):
            setattr(cls, "exposed_%s" % (key,), val)
    return cls

# class Singleton(object):
#     def __new__(cls, *args, **kw):
#         if not hasattr(cls, '_instance'):
#             orig = super(Singleton, cls)
#             cls._instance = orig.__new__(cls, *args, **kw)
#         return cls._instance

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
