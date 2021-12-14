from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='anonymous')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание 2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.user)
        self.author = User.objects.create_user(username='Author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/anonymous/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',

        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_pages(self):
        """Страницы доступны любому пользователю"""
        pages_status = {
            '/': HTTPStatus.OK,
            '/group/test-slug/': HTTPStatus.OK,
            '/profile/anonymous/': HTTPStatus.OK,
            '/posts/1/': HTTPStatus.OK,
            '/error_page/': HTTPStatus.NOT_FOUND,
        }
        for page, status in pages_status.items():
            with self.subTest(page=page, status=status):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, status)

    def test_post_create(self):
        """Страница /create/ доступна авторизованому."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """Страница /posts/<int:post_id>/create/ доступна автору."""
        response = self.author_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_follow(self):
        response = self.authorized_client.get(
            f'/{self.author.username}/follow/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_unfollow(self):
        response = self.authorized_client.get(
            f'/{self.author.username}/unfollow/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
