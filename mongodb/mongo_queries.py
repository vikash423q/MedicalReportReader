from typing import Dict

from pymongo.collection import Collection


def find_document(collection: Collection, query: Dict, projection=None, multiple=False, sort_by=None, order_by=None,
                  size=0):
    """ Function to retrieve a single or multiple documents from a provided
    collection using a dictionary containing a document's elements.
    """

    if multiple:
        if sort_by and order_by:
            results = collection.find(filter=query, projection=projection).sort(sort_by, order_by).limit(size)
        else:
            results = collection.find(query, projection).limit(size)
        return [r for r in results]
    else:
        return collection.find_one(filter=query, projection=projection)
