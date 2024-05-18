import unittest

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from books.models import Book, Profile, ProfileLibrary
from books.models.profile_library import BookReadingWorkflow
from books.tests.models.test_book import make_book


class TestProfileLibrary(TestCase):
    def test_with_valid_values(self):
        book1 = Book.objects.create(**make_book(title="Iron Flame"))
        book2 = Book.objects.create(**make_book(title="Fourth Wing"))
        user = User.objects.create(username="user", password="password")
        profile = Profile.objects.create(user=user)
        profile_library_args = make_profile_library()
        user1 = ProfileLibrary.objects.create(
            profile=profile, book=book1, **profile_library_args
        )
        user2 = ProfileLibrary.objects.create(
            profile=profile, book=book2, **profile_library_args
        )

        self.assertEqual(set(profile.books.all()), {book1, book2})
        self.assertEqual(user1.state, BookReadingWorkflow.to_be_read.value)

    def test_allows_notes_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        profile = Profile.objects.create(user=user)
        profile_library_args = make_profile_library(notes=None)
        profile_library = ProfileLibrary.objects.create(
            profile=profile, book=book, **profile_library_args
        )
        self.assertIsNotNone(profile_library)

    def test_allows_price_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        profile = Profile.objects.create(user=user)
        profile_library_args = make_profile_library(price=None)
        profile_library = ProfileLibrary.objects.create(
            profile=profile, book=book, **profile_library_args
        )
        self.assertIsNotNone(profile_library)

    def test_does_not_allows_ownership_type_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        profile = Profile.objects.create(user=user)
        profile_library_args = make_profile_library(ownership_type=None)
        with self.assertRaisesMessage(
            IntegrityError, 'null value in column "ownership_type"'
        ):
            ProfileLibrary.objects.create(
                profile=profile, book=book, **profile_library_args
            )

    def test_state_value_changes_as_per_state_machine_workflow(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        profile = Profile.objects.create(user=user)
        profile_library_args = make_profile_library()
        profile_library = ProfileLibrary.objects.create(
            profile=profile, book=book, **profile_library_args
        )
        profile_library.sm.start()
        self.assertEqual(
            profile_library.state, BookReadingWorkflow.currently_reading.value
        )


class TestBookReadingWorkflow(unittest.TestCase):
    def test_start_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.to_be_read
        sm.start()
        self.assertEqual(sm.current_state, BookReadingWorkflow.currently_reading)

    def test_pause_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.currently_reading
        sm.pause()
        self.assertEqual(sm.current_state, BookReadingWorkflow.paused_reading)

    def test_archive_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.read
        sm.archive()
        self.assertEqual(sm.current_state, BookReadingWorkflow.archived)

        sm.current_state = BookReadingWorkflow.paused_reading
        sm.archive()
        self.assertEqual(sm.current_state, BookReadingWorkflow.archived)

    def test_finish_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.currently_reading
        sm.finish()
        self.assertEqual(sm.current_state, BookReadingWorkflow.read)

    def test_restart_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.read
        sm.restart()
        self.assertEqual(sm.current_state, BookReadingWorkflow.currently_reading)

    def test_resume_event(self):
        sm = BookReadingWorkflow()
        sm.current_state = BookReadingWorkflow.paused_reading
        sm.resume()
        self.assertEqual(sm.current_state, BookReadingWorkflow.currently_reading)

        sm.current_state = BookReadingWorkflow.archived
        sm.resume()
        self.assertEqual(sm.current_state, BookReadingWorkflow.currently_reading)


def make_profile_library(**kwargs):

    default_profile_library = {
        "price": 1500,
        "notes": "it is a fantasy fiction about dragons",
        "ownership_type": "Audio Book",
    }

    return default_profile_library | dict(kwargs)
