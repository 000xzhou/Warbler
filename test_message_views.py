"""Message View tests."""

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


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment for the class once before all tests."""
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL_TEST']
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

    def test_add_message(self):
        """Can you add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
            self.assertEqual(msg.user_id, self.testuser.id)
            
            
    def test_delete_message(self):
        """Can you delete a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            resp = c.post("/messages/new", data={"text": "Hello"})
            msg = Message.query.one()

            delete_resp = c.post(f"/messages/{msg.id}/delete")

            # Make sure it redirects
            self.assertEqual(delete_resp.status_code, 302)

            msg_in_db = Message.query.filter_by(id=msg.id).first()
            # Check msg don't exist
            self.assertIsNone(msg_in_db)
            
    def test_add_message_logout(self):
        """Can you add a message when logged out?"""

        with self.client as c:
            # Attempt to post a message without being logged in
            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            
            # Check the final URL
            self.assertEqual(resp.request.path, "/")
            # Check for the flash message in the response data
            self.assertIn("Access unauthorized.", resp.get_data(as_text=True))
            # Verify that no messages were created in the database
            self.assertEqual(Message.query.count(), 0)

    def test_delete_message_logout(self):
        """Can you delete a message when logged out?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
            
            with c.session_transaction() as sess:
                del sess[CURR_USER_KEY]
                
            # Attempt to delete a message without being logged in
            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)            
            
            # Check the final URL
            self.assertEqual(resp.request.path, "/")
            # Check for the flash message in the response data
            self.assertIn("Access unauthorized.", resp.get_data(as_text=True))
            # Verify that messages still exist in the database
            self.assertEqual(Message.query.count(), 1)
            
            
            
if __name__ == "__main__":
    import unittest
    unittest.main()