import psycopg2
from faker import Faker
import random

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="haraka_data",
    user="admin",
    password="admin"
)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    location_id INT REFERENCES locations(id),
    content TEXT
);
''')

conn.commit()

# Populate tables
faker = Faker()

# Users
user_ids = []
for _ in range(50):
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;', (faker.name(), faker.email()))
    user_ids.append(cursor.fetchone()[0])

# Locations
location_ids = []
for _ in range(50):
    cursor.execute('INSERT INTO locations (latitude, longitude, description) VALUES (%s, %s, %s) RETURNING id;',
                   (faker.latitude(), faker.longitude(), faker.text()))
    location_ids.append(cursor.fetchone()[0])

# Comments
for _ in range(200):
    cursor.execute('INSERT INTO comments (user_id, location_id, content) VALUES (%s, %s, %s);',
                   (random.choice(user_ids), random.choice(location_ids), faker.sentence()))

conn.commit()
cursor.close()
conn.close()

print("Database populated with fake data!")
