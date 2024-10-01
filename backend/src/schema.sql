DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS user;

-- Create the stations table
CREATE TABLE stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    uic_id CHAR(9) NOT NULL
);

-- Insert test data into the stations table
INSERT INTO stations (name, uic_id) VALUES ('Bern', '8507000');
INSERT INTO stations (name, uic_id) VALUES ('Zürich', '8503000');
INSERT INTO stations (name, uic_id) VALUES ('Spiez', '8508350');