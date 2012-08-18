from django.db import models
from cms.models import CMSPlugin

class Article(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=30)
    length = 500

    def __unicode__(self):
        return self.name

    def get_absolute_url(self): 
        return reverse('article_view', args=[self.pk])

    class Meta:
        verbose_name_plural = 'article'


class ArticleChunk(models.Model):
    article = models.ForeignKey(Article)
    link = [] #names of links this chunk maps to


class ArticlePlugin(CMSPlugin):
    article = models.ForeignKey(Article)
