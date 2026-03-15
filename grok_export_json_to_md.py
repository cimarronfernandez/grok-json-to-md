import json
import sys
from pathlib import Path
import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Grok JSON export to clean markdown files")
    parser.add_argument("--input", default="prod-grok-backend.json",
                        help="Path to the input JSON file")
    parser.add_argument("--output", default="clean_chats_md",
                        help="Output directory for markdown files")
    return parser.parse_args()

def safe_filename(title: str, conv_id: str, index: int) -> str:
    """Create safe filename with basic collision avoidance"""
    # Keep alphanum + hyphen/underscore, collapse multiple separators
    slug = re.sub(r'[^a-zA-Z0-9_-]+', '_', title.lower()).strip('_')
    slug = re.sub(r'_+', '_', slug)
    
    short_id = conv_id[:8] if conv_id and conv_id != "no-id" else f"c{index:03d}"
    base = f"{slug[:55]}_{short_id}".strip('_')
    
    return base + ".md"

def main():
    args = parse_args()
    INPUT_FILE = args.input
    OUTPUT_DIR = Path(args.output)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Read input ───────────────────────────────────────
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {INPUT_FILE}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {INPUT_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    conversations = data.get("conversations", [])
    if not conversations:
        print("No conversations found in the JSON.", file=sys.stderr)
        sys.exit(0)

    index_lines = ["# Grok Conversations Export\n", f"Total conversations: {len(conversations)}\n\n"]

    for i, conv_block in enumerate(conversations, 1):
        conv = conv_block.get("conversation", {})
        title = conv.get("title", f"Conversation {i}")
        conv_id = conv.get("id", "no-id")

        # ── Start markdown content (no frontmatter) ────────────────
        md_lines = [
            f"# {title}\n",
            f"*Conversation ID: `{conv_id}`*\n\n",
        ]

        responses = conv_block.get("responses", [])
        prev_sender = None

        for resp_block in responses:
            resp = resp_block.get("response", {})
            sender = resp.get("sender")
            message = (resp.get("message") or "").strip()

            if not message:
                continue

            current_sender = "User" if sender == "human" else "Grok"

            if current_sender != prev_sender:
                if prev_sender is not None:
                    md_lines.append("\n")
                md_lines.append(f"### {current_sender}\n")

            md_lines.append(message + "\n\n")
            prev_sender = current_sender

        if len(md_lines) > 3:  # lowered threshold since we removed frontmatter lines
            filename = safe_filename(title, conv_id, i)
            out_path = OUTPUT_DIR / filename

            try:
                with open(out_path, "w", encoding="utf-8") as out:
                    out.write("".join(md_lines))
                print(f"Saved: {out_path}")

                index_lines.append(f"- [{title}]({filename})  \n  *{len(responses)} messages*\n")
            except Exception as e:
                print(f"Failed to write {out_path}: {e}", file=sys.stderr)

    # Create index file
    index_path = OUTPUT_DIR / "_index.md"
    try:
        with open(index_path, "w", encoding="utf-8") as idx:
            idx.write("".join(index_lines))
        print(f"\nAll clean Markdown files saved in: {OUTPUT_DIR}")
        print(f"Index file created: {index_path}")
    except Exception as e:
        print(f"Failed to write index file {index_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
