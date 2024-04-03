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

class UserModelTestCase(TestCase):
    """Test views for messages."""
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
        
    def test_is_following_model(self):
        """ 
        Does is_following successfully detect when user1 is following user2? 
        Does is_following successfully detect when user1 is not following user2?
        Does is_followed_by successfully detect when user1 is followed by user2
        Does is_followed_by successfully detect when user1 is not followed by user2?
        """

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        u1.following.append(u2)
        db.session.commit()
        # User1 should have no followers
        self.assertEqual(len(u1.followers), 0)
        # User2 should have 1 followers
        self.assertEqual(len(u2.followers), 1)
        # Check if user1 is following user2
        self.assertTrue(u1.is_following(u2))
        # Check if user2 is not following user1
        self.assertFalse(u2.is_following(u1))
        # Check if user2 is follow by user1
        self.assertTrue(u2.is_followed_by(u1))
        # Check if user1 is follow by user2
        self.assertFalse(u1.is_followed_by(u2))
        
    def test_authenticate_model(self):
        """ 
        Does User.signup successfully create a new user given valid credentials?
        Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
        Does User.authenticate successfully return a user when given a valid username and password?        Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
        Does User.authenticate fail to return a user when the username is invalid?
        Does User.authenticate fail to return a user when the password is invalid?
        """

        u = User.signup(
            username="testuser",
            password="HASHED_PASSWORD",
            email="test@test.com",
            image_url=User.image_url.default.arg
        )
        db.session.commit()
        
        # Attempt to create another user with the same username and email
        try:  
            User.signup(
                username="testuser",  
                email="test@test.com",
                password="anotherpassword",
                image_url=User.image_url.default.arg
                
            )
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            
        # User count 1 
        users_count = User.query.count()
        self.assertEqual(users_count, 1)

        # Test successful authentication with correct credentials
        auth_user = User.authenticate('testuser', 'HASHED_PASSWORD')
        self.assertEqual(auth_user, u)
        
        # Test unsuccessful authentication with incorrect username
        auth_user_invalid_username = User.authenticate('wrongusername', 'HASHED_PASSWORD')
        self.assertFalse(auth_user_invalid_username)
        
        # Test unsuccessful authentication with incorrect password
        auth_user_invalid_password = User.authenticate('testuser', 'wrongpassword')
        self.assertFalse(auth_user_invalid_password)


        
        
if __name__ == "__main__":
    import unittest
    unittest.main()