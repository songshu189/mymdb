import tempfile
from django.test import TestCase, override_settings
from django.test.client import \
    RequestFactory
from django.urls.base import reverse
from django.contrib.auth import get_user_model

from core.models import Movie, Vote, MovieImage
from core.views import MovieList, CreateVote

MEDIA_ROOT = tempfile.mkdtemp()

class MovieListPaginationTestCase(
    TestCase):
    ACTIVE_PAGINATION_HTML = """
    <li class="page-item active">
      <a href="{}?page={}" class="page-link">{}</a>
    </li>
    """

    def setUp(self):
        for n in range(15):
            Movie.objects.create(
                title='Title {}'.format(
                    n),
                year=1990 + n,
                runtime=100,
            )

    def testFirstPage(self):
        movie_list_path = reverse(
            'core:MovieList')
        request = RequestFactory().get(
            path=movie_list_path)
        response = MovieList.as_view()(
            request)
        self.assertEqual(
            200,
            response.status_code)
        self.assertTrue(
            response.context_data[
                'is_paginated'])
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(
                movie_list_path, 1, 1),
            response.rendered_content)


class VoteTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='user01',
            email='user01@...',
            password='top_secret'
        )
        self.objects = []
        for n in range(5):
            obj = Movie.objects.create(
                title='Title {}'.format(
                    n),
                year=1990 + n,
                runtime=100,
            )
            self.objects.append(obj)

    def tearDown(self):
        Movie.objects.all().delete()
        self.user.delete()

    def test_createvote_redirect(self):
        movie_id = self.objects[2].id
        create_vote_path = reverse(
            'core:CreateVote',
            kwargs={'movie_id':movie_id}
        )
        self.client.force_login(self.user)
        response = self.client.get(create_vote_path)
        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id}
        )
        self.assertRedirects(response, movie_detail_url)

    def test_movie_detail(self):
        movie_id = self.objects[2].id
        self.client.force_login(self.user)
        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id}
        )
        response = self.client.get(movie_detail_url)
        self.assertInHTML('<label for="id_value_0"><input type="radio" name="value"'
            ' value="1" required id="id_value_0">👍</label>',
            response.rendered_content)

    def test_createvote_post(self):
        movie_id = self.objects[2].id
        create_vote_path = reverse(
            'core:CreateVote',
            kwargs={'movie_id':movie_id}
        )
        self.client.force_login(self.user)
        response = self.client.post(create_vote_path,
            data={
                'user': self.user.id,
                'movie': movie_id,
                'value': 1,
            })

        vote = Vote.objects.get(
            user__id=self.user.id,
            movie__id=movie_id,
            )

        self.assertEqual(vote.value, 1)

        update_vote_path = reverse(
            'core:UpdateVote',
            kwargs={'movie_id':movie_id, 'pk': vote.id}
        )
        response = self.client.get(update_vote_path)

        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id})

        self.assertRedirects(response, movie_detail_url)

        response = self.client.get(movie_detail_url)

class ImageUploadTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='user01',
            email='user01@...',
            password='top_secret'
        )
        self.movie = Movie.objects.create(
                title='Title 123',
                year=2018,
                runtime=100,
            )
        self.image = self._create_image()

    def _create_image(self):
        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def tearDown(self):
        self.image.close()

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_upload_image(self):
        movie_id = self.movie.id
        image_upload_path = reverse(
            'core:MovieImageUpload',
            kwargs={'movie_id':movie_id}
        )
        self.client.force_login(self.user)
        response = self.client.get(image_upload_path)

        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id}
        )
        self.assertRedirects(response, movie_detail_url)
        response=self.client.get(movie_detail_url)

        response = self.client.post(image_upload_path,
            data={
                'user': self.user.id,
                'movie': movie_id,
                'image': self.image,
            })

        mimg = MovieImage.objects.filter(
            user__id=self.user.id,
            movie__id=movie_id,
        )

        self.assertEqual(mimg.count(), 1)
