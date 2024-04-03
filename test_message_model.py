"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

class MessagerModelTestCase(TestCase):
    """Test model for messages."""
    @classmethod
    def setUpClass(cls):
        """Set up test environment for the class once before all tests."""
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL']
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment for the class after all tests."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    def tearDown(self):
        """Clean up after each test."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        
        msg = Message(text="Some Text")
        u.messages.append(msg)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(u.messages), 1)
        self.assertEqual(msg.text, "Some Text")

        

        
        
if __name__ == "__main__":
    import unittest
    unittest.main()