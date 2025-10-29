import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question


# Create your tests here
class QuestionModelTests(TestCase):
    def test_was_published_recently_not_with_future_question(self):
        # was_published_recently() should return False for questions with pub_date in the future
        time = timezone.now() + datetime.timedelta(days=30)
        q = Question(pub_date=time)
        self.assertIs(q.was_published_recently(), False)

    def test_was_published_recently_not_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        q = Question(pub_date=time)
        self.assertIs(q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        q = Question(pub_date=time)
        self.assertIs(q.was_published_recently(), True)