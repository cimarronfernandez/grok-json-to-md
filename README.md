# Grok JSON → Clean Markdown Converter

**Turn Grok's giant unreadable export JSON into actually nice, readable Markdown chat files. Entirely vibe coded by grok, including this README.md. All I did was REMOVE a few lines from this README**

## The problem this script solves

Most existing methods could only export separate grok chats to md files.
After oversharing too much personal information with grok, I panicked and decided to take everything down after exporting them (Then I will have a detailed journal of my thoughts), I am embarrassed to admit how careless I was with my privacy when talking to LLMs :(

However, when you export **all your Grok conversations** (via grok.x.ai → Settings → Data → Export), you get one massive JSON file that looks like this:

- deeply nested structure
- tons of internal metadata
- Grok's thinking steps / chain-of-thought blocks
- redundant fields repeated in almost every message
- no clean separation between conversations
- basically impossible to read or search nicely in a text editor

Most people just want:

- one markdown file per conversation
- clean back-and-forth between User and Grok
- readable titles

This little script does exactly that.

## Features

- Creates one `.md` file per conversation
- Nice heading + conversation ID
- Alternating ### User / ### Grok sections (only shows header when speaker changes)
- Sanitized, filesystem-safe filenames (title + short ID)
- Skips empty / useless conversations
- Generates a simple `_index.md` with clickable list of all chats
- Zero dependencies beyond standard library + `argparse`

## Usage

```bash
# Basic usage
python grok_export_json_to_md.py

# With custom paths
python grok_export_json_to_md.py --input prod-grok-backend.json --output clean-chats

# See all options
python grok_export_json_to_md.py --help
```

## Output structure example:
```Plaintext

clean-chats/
├── _index.md
├── how-to-fine-tune-llms_abc12345.md
├── funny-cat-stories_4f8d9012.md
├── physics-homework-help_9b2e67c1.md
└── …
```
## Installation

Just download the single file:
```Bash
# easiest way
curl -O https://raw.githubusercontent.com/cimarronfernandez/grok-json-to-md/master/grok_export_json_to_md.py

# or git clone the repo
git clone https://github.com/cimarronfernandez/grok-json-to-md.git
```

No pip install needed — it uses only built-in Python modules.

Requirements

    Python 3.8 or newer

That's literally it.

## How this project was created

100% vibe-coded by Grok

If the code feels a bit quirky… that's probably why. 😄

## Contributing

Found a bug? 

Conversation title turned into garbage filename? 

Want --dry-run or --since 2025-01-01?

Feel free to open an issue or a pull request — everything is very welcome, I will ask Grok to vibe code a new commit when I see them.

Even small things like better filename sanitization, emoji support in titles, or color-coded markdown are appreciated.

## License

MIT License — do whatever you want with it.

Just don't blame me if your 14 GB export takes 20 minutes to process and your laptop sounds like a jet engine. 🚀

Made with Carelessness + laziness + Grok 

Last updated: March 2026
