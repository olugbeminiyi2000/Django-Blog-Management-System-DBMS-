from django.db import models

# Create your models here.
class BlogUser(models.Model):
    user_id = models.PositiveIntegerField(null=False, unique=True)
    
    
    def __str__(self):
        return "{}".format(self.user_id)

class Comment(models.Model):
    comment = models.TextField(null=False)
    comment_to_user = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        null=False,
        related_name="user_comments",
    )

    def __str__(self):
        return "{}".format(self.comment)

class BlogCategory(models.Model):
    CATEGORIES = [
        ("Tech", "Technology"),
        ("Fash", "Fashion"),
        ("Trav", "Travel"),
        ("Food", "Food"),
        ("Fit", "Fitness"),
        ("Life", "Lifestyle"), 
    ]
    category = models.CharField(
        max_length=100,
        choices=CATEGORIES,
        null=False,
    )

    
    def __str__(self):
        return "{}".format(self.category)

class BlogPost(models.Model):
    blog_title = models.CharField(max_length=300, null=False, unique=True)
    blog = models.TextField(null=False)
    blog_user = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        null=False,
        related_name="user_blogs",
    )
    blog_category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_blogs",
    )

    def __str__(self):
        return "{}".format(self.blog)
