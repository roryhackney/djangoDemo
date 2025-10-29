import datetime
from django.test import TestCase
from django.urls import reverse
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

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions are available.")
        self.assertQuerySetEqual(response.context["recentPosts"], [])

    def test_past_question(self):
        q = create_question(question_text="Past question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["recentPosts"], [q])

    def test_future_question(self):
        create_question(question_text="future question", days=4)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # should not load a question not yet published
        q = create_question(question_text="Future", days=5)
        url = reverse("polls:detail", args=(q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        q = create_question(question_text="Past", days=-1)
        url=reverse("polls:detail", args=(q.id,))
        res = self.client.get(url)
        self.assertContains(res, q.question_text)