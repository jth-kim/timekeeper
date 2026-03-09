"""Investigation: ...
Generated: 20260308_113449 UTC
"""

from supabase_helper import query_entries


def main():
    entries = query_entries(days=30)
    all_tags = set()
    for entry in entries:
        tags = entry.get('tags', [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
        elif isinstance(tags, list):
            tags = tags
        else:
            tags = []
        for tag in tags:
            all_tags.add(tag)
    
    print("Unique tags used in the last 30 days:")
    for tag in sorted(all_tags):
        print(f'- {tag}')

if __name__ == "__main__":
    main()