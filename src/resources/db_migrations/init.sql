CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL UNIQUE,
    last_name VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    role VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    input_format TEXT,
    output_format TEXT,
    extra_metadata JSONB,
    test_cases JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INT REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    problem_id INT NOT NULL REFERENCES problems(id),
    code TEXT NOT NULL,
    code_md5 CHAR(32) NOT NULL UNIQUE,
    language VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    passed_tests INT DEFAULT 0,
    total_tests INT DEFAULT 0,
    runtime_ms INT,
    submitted_at TIMESTAMP DEFAULT NOW(),
    extra_metadata JSONB,
    test_results JSONB
);

-- Optional index for fetching user submissions quickly
CREATE INDEX idx_submissions_problem_user_id ON submissions(problem_id, user_id);
CREATE UNIQUE INDEX idx_submissions_user_problem ON submissions(user_id, problem_id, code_md5),;