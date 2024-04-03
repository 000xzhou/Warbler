"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

# app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test user for messages."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment for the class once before all tests."""
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL']
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
        app.config['WTF_CSRF_ENABLED'] = False
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

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_following_follower_page(self):
        """When you're logged in, can you see the follower / following pages for any user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
        testuser2 = User.signup(username="testuser2",
                        email="test2@test.com",
                        password="HASHED_PASSWORD",
                        image_url=None)
        db.session.commit()

        # checking testuser2 followers
        resp_followers = c.get(f"/users/{testuser2.id}/followers")
        self.assertEqual(resp_followers.status_code, 200)
        # checking testuser2 following
        resp_following = c.get(f"/users/{testuser2.id}/following")
        self.assertEqual(resp_following.status_code, 200)
            
    def test_following_follower_page_logout(self):
        """When you're logged out, are you disallowed from visiting a user's follower / following pages?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            # checking testuser followers
            resp_followers = c.get(f"/users/{self.testuser.id}/followers")
            self.assertEqual(resp_followers.status_code, 302)
            resresp_followers_follow = c.get(f"/users/{self.testuser.id}/followers", follow_redirects=True)            
            self.assertEqual(resresp_followers_follow.request.path, "/")
            # checking testuser following
            resp_following = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp_following.status_code, 302)
            resresp_following_follow = c.get(f"/users/{self.testuser.id}/following", follow_redirects=True)            
            self.assertEqual(resresp_following_follow.request.path, "/")


if __name__ == "__main__":
    import unittest
    unittest.main()