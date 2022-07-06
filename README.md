# winget-lib

This is highly experimental, I might change the interfaces or throw away the project at any time.

This is a Python replacement for my wingethelpers PowerShell library. 
Why the change in language? I can easily generate Python types for the JSON Schemas provided by the winget team, which makes coding utilities for the repo waaaaay easier. Also, I like Python more.


The first thing I'm building is a replacement for the updating and testing workflow (so update a manifest and run in windows sandbox), since that's what I use most often.