from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

    def test_use_home_template(self):
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

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')

