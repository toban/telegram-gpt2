# telegram-gpt2

## Requirements

- python 3.7 ([pyenv](https://github.com/pyenv/pyenv-installer) is great)
- `apt-get install libffi-dev libssl-dev`
- `pip install -r requirements.txt`
- `apt-get install vorbis-tools espeak`

Create an input.txt file like such and run gpt2simple.py

```
username1: Im talking about this
username2: Im responding to that
```

after training

you can run gpt2read.py to get some more samples otherwise they are found in demo.tx from training

Create a copy of config.py and fill in the fields as config.py.template

chat_id is the telegram chat where the discussion is happening and all the bots are invited to. They probably need to be administrators aswell.

```
class Setup:
	config = {
		"chat_id": 0, 
		"manager_bot": '<TOKEN>',
		"manager_bot_name": 'manager_botname',
		"rss_feeds": [],


		"user_to_bot": {
			"<@username>": '<botname>'
		},

		"tokens": {
			"botname": '<token>',
		},
		"names": {
			"botname": 'Bot name',
		},
		"voice_pitch": {
			"botname": 40,
		}
	}
```

then run main.py

Currently the bots just start talking, and responds to any input but it might take a while if no GPU.
