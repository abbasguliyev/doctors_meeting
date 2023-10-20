from django.utils.text import slugify

def generate_random_slug(name: str, query_list) -> str:
    """
    This method about for the generate new unique slug . 
    If any data have same slug , this method add also index of last data to slug for be unique
    """
    slug = slugify(name)
    instances = query_list.filter(slug=slug)
    if instances.exists():
        slug_index = query_list.last().pk
        slug = slugify(f"{name}-{slug_index}")

    return slug