import psycopg2


"""
    Description:
        Create database tables.

    Args:
        None

    Returns:
        None
"""


connection=psycopg2.connect(

    host="localhost",

    database="face_recognition_db",

    user="postgres",

    password="1234"

)

cursor=connection.cursor()

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

connection.commit()

cursor.close()

connection.close()

print(
    "Database setup complete"
)