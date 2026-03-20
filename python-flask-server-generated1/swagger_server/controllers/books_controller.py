import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.models.book_input import BookInput  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server import util


def books_book_id_delete(book_id):  # noqa: E501
    """Xóa sách

     # noqa: E501

    :param book_id: ID duy nhất của cuốn sách (định dạng UUID hoặc string)
    :type book_id: str

    :rtype: None
    """
    return 'do some magic!'


def books_book_id_get(book_id):  # noqa: E501
    """Lấy chi tiết một cuốn sách

     # noqa: E501

    :param book_id: ID duy nhất của cuốn sách (định dạng UUID hoặc string)
    :type book_id: str

    :rtype: Book
    """
    return 'do some magic!'


def books_book_id_patch(book_id, body=None):  # noqa: E501
    """Cập nhật một phần thông tin sách

    Chỉ gửi lên những trường cần thay đổi (theo mẫu thiết kế Partial Update của JJ Geewax). # noqa: E501

    :param book_id: ID duy nhất của cuốn sách (định dạng UUID hoặc string)
    :type book_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_get(page_size=None):  # noqa: E501
    """Liệt kê danh sách sách

    Trả về danh sách tất cả các sách có trong hệ thống. Hỗ trợ phân trang (Pagination). # noqa: E501

    :param page_size: Số lượng sách trên một trang
    :type page_size: int

    :rtype: List[Book]
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Tạo mới một cuốn sách

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
