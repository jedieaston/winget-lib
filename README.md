# winget-lib

This is highly experimental, I might change the interfaces or throw away the project at any time.

This is a Python replacement for my wingethelpers PowerShell library. 
Why the change in language? I can easily generate Python types for the JSON Schemas provided by the winget team, which makes coding utilities for the repo waaaaay easier. Also, I like Python more.

It mostly is just a library at this stage, I've experimented with creating CLI utilities using the bindings but 
haven't messed with that as much. I usually just make one off scripts or notebooks to use the bindings with. 