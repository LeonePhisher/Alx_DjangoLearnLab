from django.db import models

class Author(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title=models.CharField(max_length=100)
    publication_year=models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
     related_name="books")

def __str__(self):
    return self.title
