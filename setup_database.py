import psycopg2


"""
Description:
    Create all database tables
    and insert default admin.

Args:
    None

Returns:
    None
"""


connection = psycopg2.connect(

    host="localhost",

    database="face_recognition_db",

    user="postgres",

    password="1234"

)

cursor = connection.cursor()


"""
Description:
    Create people table
"""


cursor.execute(
"""

CREATE TABLE IF NOT EXISTS people_master(

    id SERIAL PRIMARY KEY,

    name VARCHAR(100) UNIQUE,

    employee_id VARCHAR(30),

    email VARCHAR(100),

    department VARCHAR(100),

    embedding JSONB,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

);

"""
)


"""
Description:
    Create attendance table
"""


cursor.execute(
"""

CREATE TABLE IF NOT EXISTS attendance_logs(

    id SERIAL PRIMARY KEY,

    employee_id VARCHAR(30),

    name VARCHAR(100),

    event_type VARCHAR(10),

    log_time TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    attendance_date DATE
    DEFAULT CURRENT_DATE

);

"""
)


"""
Description:
    Create admin table
"""


cursor.execute(
"""

CREATE TABLE IF NOT EXISTS admin_users(

    id SERIAL PRIMARY KEY,

    username VARCHAR(50)
    UNIQUE,

    password VARCHAR(255)

);

"""
)


"""
Description:
    Insert default admin.

Args:
    username=admin
    password=admin123

Returns:
    row
"""


cursor.execute(
"""

INSERT INTO admin_users(

    username,
    password

)

VALUES(

    'admin',
    'admin123'

)

ON CONFLICT(username)

DO NOTHING

"""
)

cursor.execute(
"""

CREATE TABLE IF NOT EXISTS unknown_faces(

    id SERIAL PRIMARY KEY,

    image_path VARCHAR(255),

    detected_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

);

"""
)

connection.commit()

cursor.close()

connection.close()


print(

    "Database setup complete"

)