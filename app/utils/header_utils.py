from app.conf.page_response import PageResponse


def create_list_header(page_response: PageResponse):
    """
    Create list header from page response.

    :param page_response: Page response.
    :return: List header.
    """
    return {
        "X-Page": str(page_response.page),
        "X-Size": str(page_response.size),
        "X-Total-Count": str(page_response.total)
    }
