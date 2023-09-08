from .models import Category

def menu_links(request): #fetch all category from database
    links = Category.objects.all()
    return dict(links=links)