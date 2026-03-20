# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.book import Book  # noqa: E501
from swagger_server.models.book_input import BookInput  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_books_book_id_delete(self):
        """Test case for books_book_id_delete

        Xóa sách
        """
        response = self.client.open(
            '/v1/books/{bookId}'.format(book_id='book_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_book_id_get(self):
        """Test case for books_book_id_get

        Lấy chi tiết một cuốn sách
        """
        response = self.client.open(
            '/v1/books/{bookId}'.format(book_id='book_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_book_id_patch(self):
        """Test case for books_book_id_patch

        Cập nhật một phần thông tin sách
        """
        body = BookInput()
        response = self.client.open(
            '/v1/books/{bookId}'.format(book_id='book_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_get(self):
        """Test case for books_get

        Liệt kê danh sách sách
        """
        query_string = [('page_size', 10)]
        response = self.client.open(
            '/v1/books',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Tạo mới một cuốn sách
        """
        body = BookInput()
        response = self.client.open(
            '/v1/books',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
