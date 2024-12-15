import glob
import re

def get_between(line, start, end):
    index1 = line.index(start)
    index2 = line.index(end)

    return line[index1 + len(start): index2]

def get_image_slug(path):
    # get the filename from the path
    parts = path.split('/')
    filename = parts[-1]
    # remove the suffix
    location = filename.rfind('.')
    name = filename[:location]
    return name.replace('-','_').replace('.','_')


def process_file(file):
    with open(file) as f: 
        # go through every line in the file looking for an image and replace with new syntax
        lines = []
        images = []
        modified = False
        for line in f.readlines():
            if not line.startswith('!'):
                lines.append(line)
                continue
            alt_text = get_between(line, '[',']')
            image_path = get_between(line, '(', ')')
            if not alt_text or not image_path:
                print("Error in image markdown: ", file)
                print("Line: ", line)
                exit()
            slug = get_image_slug(image_path)
            images.append((image_path, slug))
            lines.append(f'<Image alt="{alt_text}" src={{{slug}}} />\n')
            modified = True

        if not modified:
            return lines, modified
        
        # put the imports after the mdx frontmatter
        newlines = []
        first = True
        for line in lines:
            if line.startswith('---') and first:
                first = False
                newlines.append(line)
            elif line.startswith('---') and not first:
                # insert the imports
                newlines.append(line)
                newlines.append("\n")
                newlines.append('import { Image } from "astro:assets";\n')
                for image_path, slug in images:
                    newlines.append(f'import {slug} from "@{image_path}";\n')
                newlines.append("\n")
            else:
                newlines.append(line)
    
    return newlines, modified


def rewrite_file(file, lines):
    f = open(file, 'w')
    f.writelines(lines)
    f.close()

def process_files():
    # loop through the files in this directory and process each of them
    for file in glob.glob('*.mdx'):
        lines, modified = process_file(file)
        if modified:
            # rewrite file
            rewrite_file(file, lines)



if __name__ == "__main__":
    process_files()