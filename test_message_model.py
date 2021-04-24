import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class UserTest(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.uid = 5555
        user = User.signup("Test", "test@gmail.com", "password", None)
        user.id = self.uid
        db.session.commit()
        self.user = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message(self):
        mess = Message(text="Hello World!", user_id=self.uid)

        db.session.add(mess)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "Hello World!")
