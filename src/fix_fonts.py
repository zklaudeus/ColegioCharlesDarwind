import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove inline font-family
    content = re.sub(r'font-family:\s*[\'\"].*?[\'\"]\s*,\s*sans-serif;?', '', content)
    content = re.sub(r'font-family:\s*[\'\"].*?[\'\"]\s*,\s*system-ui\s*,\s*sans-serif;?', '', content)
    
    # Optional: cleanup empty styles left behind
    content = re.sub(r'style=\"\s*\"', '', content)
    # Also clean up cases where there's only whitespace before the style closing quote
    content = re.sub(r'style=\"(.*?)\s+\"', r'style="\1"', content)

    # 2. Add trykker classes based on existing classes
    def replace_class(match):
        cls_str = match.group(1)
        
        # Determine target trykker class
        target_class = None
        if re.search(r'\b(text-xs|text-sm|text-\[1[0-4]px\]|sm:text-xs|md:text-sm)\b', cls_str):
            target_class = 'trykker-small'
            cls_str = re.sub(r'\b(text-xs|text-sm|text-\[1[0-4]px\]|sm:text-xs|md:text-sm|font-bold|font-semibold|font-medium|font-light|font-sans|font-inter|font-poppins)\b', '', cls_str)
        elif re.search(r'\b(text-base|text-lg|sm:text-lg|md:text-xl)\b', cls_str):
            target_class = 'trykker-body'
            cls_str = re.sub(r'\b(text-base|text-lg|sm:text-lg|md:text-xl|font-bold|font-semibold|font-medium|font-light|font-sans|font-inter|font-poppins)\b', '', cls_str)
        elif re.search(r'\b(text-xl|text-2xl|text-3xl|sm:text-2xl|md:text-3xl|sm:text-3xl|md:text-4xl)\b', cls_str):
            target_class = 'trykker-subtitle'
            cls_str = re.sub(r'\b(text-xl|text-2xl|text-3xl|sm:text-2xl|md:text-3xl|sm:text-3xl|md:text-4xl|font-bold|font-semibold|font-medium|font-light|font-sans|font-inter|font-poppins)\b', '', cls_str)
        elif re.search(r'\b(text-4xl|text-5xl|sm:text-4xl|sm:text-5xl|md:text-5xl|md:text-6xl|lg:text-6xl)\b', cls_str):
            target_class = 'trykker-title'
            cls_str = re.sub(r'\b(text-4xl|text-5xl|sm:text-4xl|sm:text-5xl|md:text-5xl|md:text-6xl|lg:text-6xl|font-bold|font-semibold|font-medium|font-light|font-sans|font-inter|font-poppins)\b', '', cls_str)
        elif re.search(r'\b(text-6xl|text-7xl|sm:text-6xl|sm:text-7xl|md:text-6xl|md:text-7xl|lg:text-7xl)\b', cls_str):
            target_class = 'trykker-hero'
            cls_str = re.sub(r'\b(text-6xl|text-7xl|sm:text-6xl|sm:text-7xl|md:text-6xl|md:text-7xl|lg:text-7xl|font-bold|font-semibold|font-medium|font-light|font-sans|font-inter|font-poppins)\b', '', cls_str)

        # Remove 'font-bold', 'font-medium' everywhere if we already decided it's trykker, wait, 
        # let's just always strip font-bold/font-medium if we are replacing it, because trykker handles weight (it's only 400).
        if target_class and target_class not in cls_str:
            cls_str = f'{target_class} {cls_str}'
            
        cls_str = re.sub(r'\s+', ' ', cls_str).strip()
        return f'class="{cls_str}"'

    # Apply class replacement
    content = re.sub(r'class=\"(.*?)\"', replace_class, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

if __name__ == "__main__":
    for root, dirs, files in os.walk('c:/Users/claud/Desktop/CharlesDarwin/src'):
        for file in files:
            if file.endswith('.astro'):
                filepath = os.path.join(root, file)
                # Skip layout.astro since we already defined our base there
                if 'Layout.astro' not in filepath and 'Conocenos.astro' not in filepath and 'Hero.astro' not in filepath and 'Identity.astro' not in filepath and 'Navbar.astro' not in filepath and 'Footer.astro' not in filepath:
                    process_file(filepath)
