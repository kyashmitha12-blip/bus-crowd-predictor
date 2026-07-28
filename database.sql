-- database.sql
-- Run this file in MySQL to set up the Bus Crowd Predictor database
-- It creates the database, all tables, and fills in real bus route data

CREATE DATABASE IF NOT EXISTS bus_crowd_db;
USE bus_crowd_db;

-- Table 1: stores each bus route and its total seat count
CREATE TABLE IF NOT EXISTS bus_capacity (
    bus_number VARCHAR(10) PRIMARY KEY,
    route_name VARCHAR(50),
    total_seats INT DEFAULT 55
);

-- Table 2: stores each boarding confirmation made by a student/teacher
CREATE TABLE IF NOT EXISTS bus_boarding (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    bus_number VARCHAR(10),
    boarding_point VARCHAR(50),
    travel_date DATE,
    travel_time TIME
);

-- Insert all real bus routes (from college transport website), 55 seats each
INSERT INTO bus_capacity (bus_number, route_name, total_seats) VALUES
('R01', 'Ennore', 55),
('R01A', 'Tondiarpet', 55),
('R01B', 'Kasimedu', 55),
('R02', 'Triplicane', 55),
('R03', 'Choolai', 55),
('R03A', 'Collector Nagar', 55),
('R03B', 'Water Tank', 55),
('R04', 'East Mogappair', 55),
('R05', 'CIT Nagar', 55),
('R05A', 'Loyola College', 55),
('R06', 'Chinmayanagar', 55),
('R07', 'Santhome', 55),
('R08', 'Kovilambakkam', 55),
('R08A', 'Adambakkam', 55),
('R09', 'MKB Nagar', 55),
('R10', 'Thachoor', 55),
('R11', 'Chengalpattu', 55),
('R11A', 'Guduvanchery', 55),
('R12', 'Minjur', 55),
('R13', 'Vyasarpadi', 55),
('R13A', 'ICF', 55),
('R14', 'Thiruvallur', 55),
('R14B', 'Kakkalur', 55),
('R15', 'Cheyyar', 55),
('R15A', 'Orikkai', 55),
('R15B', 'Kancheepuram', 55),
('R16', 'Neelangkarai', 55),
('R16B', 'Sholinganallur', 55),
('R17', 'Valluvarkottam', 55),
('R17A', 'Valasaravakkam', 55),
('R18', 'Pallikaranai', 55),
('R18A', 'Sembakkam', 55),
('R18B', 'Kelambakkam', 55),
('R19', 'Poombukar', 55),
('R19A', 'Vinayagapuram', 55),
('R20', 'Vepampattu', 55),
('R20A', 'Pattabiram', 55),
('R21', 'Ayyapakkam', 55),
('R22', 'Thiruthani', 55),
('R22A', 'SR Gate', 55),
('R23', 'K4 Police Station', 55),
('R24', 'Arcot', 55),
('R25', 'Kallikuppam', 55),
('R25A', 'Pudur', 55),
('R26', 'Andarkuppam', 55),
('R27', 'Avadi', 55),
('R27A', 'Kollumedu', 55),
('R28', 'Agaram', 55),
('R29', 'Velachery', 55),
('R29A', 'Pammal', 55),
('R29B', 'Sivanthangal', 55);
