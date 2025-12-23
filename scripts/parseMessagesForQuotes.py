#!/usr/bin/env python3
"""
Script to extract message content from Discord chat export JSON files.
Usage: python parseMessagesForQuotes.py <output.json> <file1.json> [file2.json ...]
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParsedQuote:
    name: str
    message: str
    number: int | None = None
    url: str | None = None


def parse_remembered_message(content: str) -> ParsedQuote | None:
    """
    Parse a 'Remembered' message into its components.
    
    Format: Remembered that <name> said "<message>" (#<number>) (<url>)
    The number and url are optional.
    """
    # Pattern breakdown:
    # - Remembered that (.+?) said " - captures the name (non-greedy)
    # - "(.*)" - captures the quoted message (handles escaped quotes inside)
    # - (?: \(#(\d+)\))? - optional: captures the quote number
    # - (?: \((https?://[^)]+)\))? - optional: captures the URL
    pattern = r'^Remembered that (.+?) said "(.*)"(?: \(#(\d+)\))?(?: \((https?://[^)]+)\))?$'
    
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None
    
    name, message, number, url = match.groups()
    
    return ParsedQuote(
        name=name,
        message=message,
        number=int(number) if number else None,
        url=url
    )


def parse_angle_bracket_message(content: str) -> ParsedQuote | None:
    """
    Parse a message in angle bracket format.
    
    Format: <name> message (#number) url
    The number and url are optional.
    
    Example: <mr.controll> Besides. I think we all know... (#500) https://discord.com/...
    """
    # Pattern breakdown:
    # - ^<([^>]+)> - captures the name in angle brackets
    # - (.+?) - captures the message (non-greedy)
    # - (?: \(#(\d+)\))? - optional: captures the quote number
    # - (?: (https?://\S+))? - optional: captures the URL (no parentheses around it)
    pattern = r'^<([^>]+)>\s+(.+?)(?: \(#(\d+)\))?(?: (https?://\S+))?$'
    
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None
    
    name, message, number, url = match.groups()
    
    return ParsedQuote(
        name=name,
        message=message.strip(),
        number=int(number) if number else None,
        url=url
    )


def parse_message(content: str) -> ParsedQuote | None:
    """Try all parsers and return the first successful match."""
    # Try "Remembered that..." format first
    result = parse_remembered_message(content)
    if result:
        return result
    
    # Try "<name> message" format
    result = parse_angle_bracket_message(content)
    if result:
        return result
    
    return None


def extract_messages(file_path: str) -> list[str]:
    """Extract all message content from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    messages = data.get('messages', [])
    results = []
    for msg in messages:
        content = msg.get('content', '')
        if content and (content.startswith('Remembered') or content.startswith('<')):
            results.append(content)
    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python parseMessagesForQuotes.py <output.json> <file1.json> [file2.json ...]")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    all_content = []
    parsed_quotes = []
    failed_parses = []
    
    for file_path in input_files:
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue
        
        try:
            content = extract_messages(file_path)
            all_content.extend(content)
            print(f"Extracted {len(content)} messages from {file_path}", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
    
    # Parse each message
    quotes_without_number = []
    for msg in all_content:
        parsed = parse_message(msg)
        if parsed:
            if parsed.number is not None:
                parsed_quotes.append({
                    'name': parsed.name,
                    'message': parsed.message,
                    'number': parsed.number,
                    'url': parsed.url
                })
            else:
                quotes_without_number.append({
                    'name': parsed.name,
                    'message': parsed.message,
                    'url': parsed.url
                })
        else:
            failed_parses.append(msg)
    
    if failed_parses:
        print(f"Warning: Failed to parse {len(failed_parses)} messages:", file=sys.stderr)
        for msg in failed_parses:  # Show first 5 failures
            print(f"  - {msg}", file=sys.stderr)
        # if len(failed_parses) > 5:
            # print(f"  ... and {len(failed_parses) - 5} more", file=sys.stderr)
    
    # Build map keyed by quote number
    quotes_map = {
        quote['number']: {
            'name': quote['name'],
            'message': quote['message'],
            'url': quote['url']
        }
        for quote in parsed_quotes
    }
    
    # Find missing numbers from 1 to max and fill with unnumbered quotes
    if quotes_map and quotes_without_number:
        max_number = max(quotes_map.keys())
        missing_numbers = [n for n in range(1, max_number + 1) if n not in quotes_map]
        
        print(f"Found {len(missing_numbers)} missing slots, {len(quotes_without_number)} unnumbered quotes", file=sys.stderr)
        
        # Assign unnumbered quotes to missing slots
        for i, quote in enumerate(quotes_without_number):
            if i < len(missing_numbers):
                quotes_map[missing_numbers[i]] = quote
                print(f"  Assigned unnumbered quote to #{missing_numbers[i]}", file=sys.stderr)
            else:
                print(f"  Warning: No slot available for unnumbered quote: {quote['message']}", file=sys.stderr)
    elif quotes_without_number:
        print(f"Warning: {len(quotes_without_number)} quotes have no number and no numbered quotes to reference", file=sys.stderr)
    
    # Write each quote to JSON file in the format: {"quote": {"<number>": {...}}}
    # Sort by quote number
    output = {
        "quote": {
            str(num): quotes_map[num] for num in sorted(quotes_map.keys())
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False)
    
    print(f"Wrote {len(quotes_map)} quotes to {output_file}", file=sys.stderr)
    print(sorted(list(quotes_map.keys())))
    print(len(list(quotes_map.keys())))


if __name__ == '__main__':
    main()

