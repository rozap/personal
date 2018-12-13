import os
from os import listdir
from os.path import isfile, join
from jinja2 import Environment, FileSystemLoader
import markdown
from time import sleep
from sh import git

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(
    loader=FileSystemLoader(THIS_DIR),
    trim_blocks=True
)

def ls(place):
    return [f for f in listdir(place) if isfile(join(place, f))]

def posts():
    posts = 'posts'

    ugh = []
    chronological = sorted([
        (p, [int(d) for d in p.split('.')[0].split('-')]) 
        for p in ls(posts)
    ], key=lambda t: t[1])
    chronological.reverse()

    print(chronological)

    for (file, _) in chronological:
        with open(join(posts, file), 'r') as f:
            ugh.append(markdown.markdown(f.read()))
    return ugh

def htmls():
    templates = 'templates'
    dist = 'dist'
    rendered_posts = posts()

    for file in ls(templates):
        print("Rendering", file)
        rendered = j2_env.get_template(join(templates, file)).render(
            posts=rendered_posts
        )

        out = join(dist, file)
        with open(out, 'w+') as f:
            print('wrote', out)
            f.write(rendered)

while True:
    git('pull', 'origin', 'master')
    htmls()
    sleep(60 * 60 * 8)