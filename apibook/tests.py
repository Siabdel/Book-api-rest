from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User

from apibook import models as api_models

class BookTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # add auteur
        aa,dd  = api_models.Author.objects.update_or_create(
            firstname='f_name', 
            lastname='l_name')

        # add book
        test_book = api_models.Book.objects.create(
            title='book_title', description='book_desc'
        )
        # raise Exception(aa)
        test_book.author.add(aa.id)
        ## 
        test_book.save()
        
        
        return super().setUpTestData()
    def test_book_content(self):
        book = api_models.Book.objects.get(id=1)
        expected_author = f'{book.author}'
        expected_title = f'{book.title}'
        expected_description = f'{book.description}'

        # test equal
        # self.assertEqual(expected_author, 'f_name')
        self.assertEqual(expected_title, 'book_title')
        self.assertEqual(expected_description, 'book_desc')
        
