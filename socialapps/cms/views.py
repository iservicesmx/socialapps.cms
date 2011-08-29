
def get_slug(path):
    """
    Return the object's slug

        >>> get_slug('/foo/bar/')
        bar
    """
    if path.endswith('/'):
        path = path[:-1]
    return path.split("/")[-1]


def get_object(path):
    pass
    
    
class BaseView(object):
    pass