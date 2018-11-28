import rpyc


c = rpyc.connect_by_service("TIME")
print( "server's time is", c.root.get_time())

c = rpyc.connect_by_service("DATE")
print( "server's time is", c.root.get_date())