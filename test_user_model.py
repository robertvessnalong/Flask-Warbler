"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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
        Follows.query.delete()
        db.drop_all()
        db.create_all()

        self.userOne = User.signup(username="testOne", email="testOne@gmail.com",password="password", image_url=None)
        self.userOne_id = 5555
        self.userOne.id = self.userOne_id
        self.userTwo = User.signup(username="testTwo", email="testTwo@gmail.com", password="password", image_url=None)
        self.userTwo_id = 6666
        self.userTwo.id = self.userTwo_id



        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_follows(self):
        self.userOne.following.append(self.userTwo)
        db.session.commit()

        self.assertEqual(len(self.userTwo.followers), 1)
        self.assertEqual(len(self.userOne.following), 1)

    def test_following(self):
        self.userOne.following.append(self.userTwo)
        db.session.commit()

        self.assertTrue(self.userOne.is_following(self.userTwo))

    def test_follower(self):
        self.userOne.following.append(self.userTwo)
        db.session.commit()

        self.assertTrue(self.userOne.is_followed_by(self.userTwo))

    def test_login(self):
        user = User.authenticate(self.userOne.username, "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.userOne_id)