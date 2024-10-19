from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()  # Create the database schema
            # Add a cupcake for testing
            cupcake = Cupcake(flavor='TestFlavor', size='TestSize', rating=5, image='http://test.com/cupcake.jpg')
            db.session.add(cupcake)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop the database schema

    def test_create_cupcake(self):
        with self.app.app_context():
            response = self.client.post('/api/cupcakes', json={
                'flavor': 'TestFlavor2',
                'size': 'TestSize2',
                'rating': 10,
                'image': 'http://test.com/cupcake2.jpg'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('cupcake', response.json)

    def test_get_cupcake(self):
        with self.app.app_context():
            cupcake = Cupcake.query.first()  # This should now work without issues
            response = self.client.get(f"/api/cupcakes/{cupcake.id}")
            self.assertEqual(response.status_code, 200)

    def test_list_cupcakes(self):
        with self.app.app_context():
            response = self.client.get('/api/cupcakes')
            self.assertEqual(response.status_code, 200)
            self.assertIn('cupcakes', response.json)

    def test_update_cupcake_info(self):
        with self.app.app_context():
            cupcake = Cupcake.query.first() 
            response = self.client.patch(f"/api/cupcakes/{cupcake.id}", json=CUPCAKE_DATA_2)
            self.assertEqual(response.status_code, 200)

    
    def test_delete_cupcake(self):
        with self.app.app_context():
            cupcake = Cupcake.query.first()
            self.assertIsNotNone(cupcake)
            response = self.client.delete(f"/api/cupcakes/{cupcake.id}")                         
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data, {"message": "Deleted"})
            