from blogengine.celery import app
from blog.models import Post


@app.task
def print_str(pk):
    print(Post.objects.all())
