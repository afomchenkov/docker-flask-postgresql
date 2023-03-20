import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('simpleuser', 'simpleuser@test.com', 'testpassword')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'simpleuser')
        self.assertEqual(user.email, 'simpleuser@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('simpleuser', 'simpleuser@test.com', 'testpassword')
        duplicate_user = User(
            username='simpleuser',
            email='simpleuser@test2.com',
            password='testpassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('simpleuser', 'simpleuser@test.com', 'testpassword')
        duplicate_user = User(
            username='simpleusertest',
            email='simpleuser@test.com',
            password='testpassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('simpleuser', 'simpleuser@test.com', 'testpassword')
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('test', 'test@test.com', 'testpassword')
        user_two = add_user('test2', 'test@test2.com', 'testpassword')
        self.assertNotEqual(user_one.password, user_two.password)


if __name__ == '__main__':
    unittest.main()
