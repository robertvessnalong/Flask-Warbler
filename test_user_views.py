import os
from unittest import TestCase
from models import db, connect_db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

class UserViewTest(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        self.userOne = User.signup(username="testOne", email="testOne@gmail.com",password="password", image_url=None)
        self.userOne_id = 5555
        self.userOne.id = self.userOne_id
        self.userTwo = User.signup(username="testTwo", email="testTwo@gmail.com", password="password", image_url=None)
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@testOne", str(resp.data))
            self.assertIn("@testTwo", str(resp.data))

    def test_show_user(self):
        with self.client as c:
            resp = c.get(f"/users/{self.userOne_id}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testOne", str(resp.data))