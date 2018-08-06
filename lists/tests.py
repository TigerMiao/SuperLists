from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

    def test_home_page_return_correct_html(self):
        '''
        # 手动渲染模板进行测试
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')

        expected_html = render_to_string('lists/home.html')
        self.assertEqual(html, expected_html)
        '''
        # 使用 Django 测试客户端进行测试
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
