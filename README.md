This repository holds the source code for the [substratestack demo][app] on
Google App Engine.

[Ace][ace] is embedded to offer a nice syntax-highlighed editor for the Python 
script. Prior to executing the script, `open()` is replaced with `FakeFile`.
This class writes newly created files to in-memory buffers. These are then 
stored in a ZIP stream which is offered for download.

[ace]: http://ace.ajax.org/
[app]: https://substratestack.appspot.com/
