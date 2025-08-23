CREATE TABLE  IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    role VARCHAR(20) NOT NULL
);

-- CREATE TABLE problems (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(100) NOT NULL,
--     description TEXT NOT NULL,
--     input_format TEXT NOT NULL,
--     output_format TEXT NOT NULL,
--     sample_input TEXT NOT NULL,
--     sample_output TEXT NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW(),
--     author_id INTEGER REFERENCES users(id)
-- );

-- CREATE TABLE submissions (
--     id SERIAL PRIMARY KEY,
--     problem_id INTEGER REFERENCES problems(id),
--     user_id INTEGER REFERENCES users(id),
--     code TEXT NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW(),
--     score INTEGER NOT NULL,
--     status VARCHAR(20) NOT NULL
-- );
