from clixon.clixon import Clixon

c = Clixon(source='running', ncclient=True)

xml = c.get_root()

c.__exit__()
