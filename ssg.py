import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader

POSTS = {}
for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)
    
    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])
        POSTS = {
            post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d %H:%M'), reverse=True)
        }
        
        env = Environment(loader=PackageLoader('ssg', 'templates'))
        index_template = env.get_template('index.html')
        post_template = env.get_template('post-detail.html')
        
        index_posts_metadata = [POSTS[post].metadata for post in POSTS]
        index_html_content = index_template.render(posts=index_posts_metadata)
        
        with open('output/index.html', 'w') as file:
            file.write(index_html_content)
            
for post in POSTS:
    post_metadata = POSTS[post].metadata
    
    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
    }
    
    post_html_content = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}/index.html'.format(slug=post_metadata['slug'])
    
    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html_content)