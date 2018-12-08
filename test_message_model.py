"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Remove the session entity"""
        db.session.remove()

    def signup_user(self, username, email):
        """Creates a user for testing in the database"""

        self.testuser3 = User.signup(
            username=username,
            email=email,
            password="123456",
            image_url="/test.jpg")

        db.session.commit()

    def test_message_create(self):
        """Message instance should be created properly"""

        self.signup_user(username="blah", email="123@123.com")

        new_msg = Message(text="A new message", user_id=self.testuser3.id)

        self.assertEqual(new_msg.text, "A new message")
        self.assertEqual(new_msg.user_id, self.testuser3.id)

    def test_message_liked(self):
        """Test if a user has successfully liked a message and unliked the same message"""

        testuser2 = User.signup(
            username="bleggh",
            email='123123@gmail.com',
            password="123456",
            image_url="/test.jpg")

        self.signup_user(username='blah', email='123@123.com')

        new_msg = Message(text="A new message", user_id=self.testuser3.id)
        db.session.add(new_msg)
        db.session.commit()

        likes = Like(user_id=testuser2.id, message_id=new_msg.id)
        db.session.add(likes)
        db.session.commit()

        self.assertEqual(new_msg.is_liked_by(testuser2), True)
        db.session.delete(likes)
        db.session.commit()
        self.assertEqual(new_msg.is_liked_by(testuser2), False)
