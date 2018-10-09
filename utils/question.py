from django.conf import settings

def make_question_url(id):
    url = ''.join(('http://', settings.SITE_URL, '/question/', str(id), '/'))
    link = '<a href="{}">{}</a>'.format(url, url)
    return url, link