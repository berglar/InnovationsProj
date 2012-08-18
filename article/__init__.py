class Article(models.Model):
    def __init__(self):
        name = models.CharField(max_length=30)
        length = 500 #numWords

class ArticleChunks(models.Model):
    #would ordinarily put this section in __init__, 
    #but we don't want to override __init__ of models.Model
    def __init__(self):
        #use ForeignKey for many-to-one relation
        self.article = models.ForeignKey(Article) 
        self.length = self.article.length #default to length of article
        self.links = [] #set of links this chunk relates to


    
    
