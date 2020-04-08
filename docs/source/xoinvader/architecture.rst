.. architecture

Architecture of XOInvader
-------------------------

**XOInvader** has Application class, that allows to register, deregister and manage State objects.
Only one State object can be current (Application.state property), only it's logic can be evaluated.
