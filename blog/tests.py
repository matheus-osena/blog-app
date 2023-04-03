from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
from .models import Post

class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username ='testuser',
            email = 'test@email.com',
            password = 'secret',
        )

        self.post = Post.objects.create(
            title = 'A good title',
            body = 'A good text',
            author = self.user,
        )

    def test_string_representation(self):
        post = Post(title = "A sample title")
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', "A good title")
        self.assertEqual(f'{self.post.body}', 'A good text')
        self.assertEqual(f'{self.post.author}', 'testuser')

    def post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good text')
        self.assertTemplateUsed(response, 'home.html')
    
    def post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(repsonse, 'post_detail.html')
