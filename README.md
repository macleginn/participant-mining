participant-mining
==================

Two Python 3 scripts for extracting open profiles of all participants of an event on Facebook or Vkontakte

The Facebook script uses the Facepy library. Get it [here](https://github.com/jgorset/facepy) or with
```pip3 install facepy```. It also needs an Access Token, which is available at
https://developers.facebook.com/tools/explorer (it should be obtained again for the next session). The Access Token goes into line 17. Facebook event ids go into the list ```facebook_events``` on line 19.

The Vkontakte script takes a list of type string of event_ids, which should be names or ids
(event4534523 -> '4534523').

Both scripts produce .txt report files in the working directory.
