from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import ArticlePlugin
from django.utils.translation import ugettext as _

class CMSArticlePlugin(CMSPluginBase):
    model = ArticlePlugin
    name = _("Article")
    render_template = "article/article.html"

    def render(self, context, instance, placeholder):
        context.update({
            'article':instance.article,
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(CMSArticlePlugin)from cms.models import CMSPlugin
