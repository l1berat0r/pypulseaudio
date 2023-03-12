************
pypulseaudio
************

This is a fork of a repository that had it's last update in 2014 and the author didn't have any activity in the last 2 years on github.
I needed a simple python wrapper that will allow me to interact with a pulseadio server including ability to record and playback samples,
so I decided to adopt this project and expand it's functionality.
If the original author answers, I'll be happy to merge my changes to his repository. If not, I will think what to do with it.

For now I'm beginning my work on the `dev` branch.

- `Original repository: <https://github.com/liamw9534/pypulseaudio>`_

Installation
============

Install the python library by running::

    pip install pypulseaudio


Documentation
=============

Documentation is hosted at https://pythonhosted.org/pypulseaudio


Project resources
=================

- `Source code <https://github.com/liamw9534/pypulseaudio>`_
- `Issue tracker <https://github.com/liamw9534/pypulseaudio/issues>`_
- `Download development snapshot <https://github.com/liamw9534/pypulseaudio/archive/master.tar.gz#egg=pypulseaudio-dev>`_


Changelog
=========

v0.1.0
------

Initial release supporting:

- Get server information with ``get_server_info()``
- Connection management with ``connect()`` and ``disconnect()``
- Enumerate installed audio cards using ``get_card_info_list()``, ``get_card_info_by_name()`` and ``get_card_info_by_index()``
- Enumerate available audio sources using ``get_source_info_list()``, ``get_source_info_by_name()`` and ``get_source_info_by_index()``
- Enumerate available audio sinks using ``get_sink_info_list()``, ``get_sink_info_by_name()`` and ``get_sink_info_by_index()``
- Enumerate installed modules using ``get_module_info_list()`` and ``get_module_info()``
- Set default sources and sinks with ``set_default_source()`` and ``set_default_sink()``
- Module management with ``load_module()`` and ``unload_module()``
- Set a card's profile with ``set_card_profile_by_index()`` or ``set_card_profile_by_name()``

This release is intended to provide the main audio management functions only, rather than
audio streaming or sound sampling functions.
