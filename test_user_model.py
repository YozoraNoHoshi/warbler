"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.client = app.test_client()

        self.u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD")

        db.session.add(self.u)

        self.u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD")

        db.session.add(self.u2)
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)

    def test_repr(self):
        '''Testing for repr, using string from Models.py'''

        self.assertEqual(
            repr(self.u), f"<User #{self.u.id}: testuser, test@test.com>")

    def test_is_following(self):
        '''Added two users above, append the relationship, test using "following" '''

        self.u.following.append(self.u2)
        db.session.commit()

        self.assertEqual(self.u.is_following(self.u2), True)

    def test_is_not_following(self):
        '''Removed append'''

        self.assertEqual(self.u.is_following(self.u2), False)

    def test_is_followed_by(self):
        '''Added two users above, append the relationship, test using  "followed" '''

        self.u.followers.append(self.u2)
        db.session.commit()

        self.assertEqual(self.u.is_followed_by(self.u2), True)

    def test_is_not_followed_by(self):
        '''Removed append '''

        self.assertEqual(self.u.is_followed_by(self.u2), False)

    def test_create_User(self):
        '''Creating a new user and manually checking password hash'''

        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()

        sign_up_test = User.signup(
            username="test",
            password="test123",
            email="abc@abc.com",
            image_url="/test.jpg")

        db.session.commit()

        self.assertEqual(sign_up_test.username, 'test')
        self.assertEqual(
            bcrypt.check_password_hash(sign_up_test.password, "test123"), True)
        self.assertEqual(sign_up_test.email, 'abc@abc.com')
        self.assertEqual(sign_up_test.image_url, '/test.jpg')

    def test_create_User_fail(self):
        '''Checking if it raises ValueError when password is not passed. "as cm" should let you capture the type of error raised but we couldnt get it work'''

        with self.assertRaises(ValueError):
            User.signup(
                username="test",
                password="",
                email="abc@abc.com",
                image_url="/test.jpg")

            # the_exception = cm.exception
            # self.assertEqual(the_exception.error_code, 3)

    def test_user_authenticate(self):
        '''Tests if user is returned when authenticated, authenticate function accepts username and password'''

        testuser3 = User.signup(
            username="testuser3",
            email="abc@abc.com",
            password="123456",
            image_url="/test.jpg")

        db.session.commit()

        self.assertEqual(
            User.authenticate(username="testuser3", password="123456"),
            testuser3)

    def test_fail_user_authenticate(self):
        '''Tests if an error is returned if credentials dont match'''

        testuser3 = User.signup(
            username="testuser3",
            email="abc@abc.com",
            password="123456",
            image_url="/test.jpg")

        db.session.commit()

        self.assertEqual(
            User.authenticate(username="testuser3", password="123abc"), False)

        self.assertEqual(
            User.authenticate(username="testuser4", password="123456"), False)
