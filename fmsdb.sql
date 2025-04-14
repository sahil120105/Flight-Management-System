create database flight_management_system;
use flight_management_system;

-- Create Passenger table with auto-incrementing integer ID
CREATE TABLE Passenger (
    Ps_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Age INT NOT NULL,
    Sex ENUM('M', 'F', 'Other') NOT NULL,
    Contacts VARCHAR(50) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE, 
    Password VARCHAR(255) NOT NULL);

-- Passengers (Ps_ID will be auto-generated)
INSERT INTO Passenger (Name, Address, Age, Sex, Contacts, Email, Password) VALUES
('John Smith', '123 Main St, New York, NY', 35, 'M', '+1-555-123-4567', 'john.smith@example.com', 'password123'),
('Mary Johnson', '456 Oak Ave, Los Angeles, CA', 42, 'F', '+1-555-234-5678', 'mary.johnson@example.com', 'password123'),
('Raj Patel', '789 Park Rd, New Delhi, India', 28, 'M', '+91-98765-43210', 'raj.patel@example.com', 'password123'),
('Sarah Williams', '101 Queen St, London, UK', 31, 'F', '+44-7700-900123', 'sarah.williams@example.com', 'password123'),
('Takashi Yamamoto', '202 Sakura St, Tokyo, Japan', 45, 'M', '+81-90-1234-5678', 'takashi.yamamoto@example.com', 'password123'),
('Emma Brown', '303 Beach Rd, Sydney, Australia', 29, 'F', '+61-4-1234-5678', 'emma.brown@example.com', 'password123'),
('Michael Davis', '404 Maple Ave, Toronto, Canada', 37, 'M', '+1-416-555-1234', 'michael.davis@example.com', 'password123'),
('Sophie Martin', '505 Champs-Élysées, Paris, France', 33, 'F', '+33-6-12-34-56-78', 'sophie.martin@example.com', 'password123'),
('Hans Mueller', '606 Rhine St, Frankfurt, Germany', 50, 'M', '+49-170-1234567', 'hans.mueller@example.com', 'password123'),
('Li Wei', '707 Pudong Rd, Shanghai, China', 26, 'M', '+86-13912345678', 'li.wei@example.com', 'password123'),
('Isabella Rossi', '808 Roman Way, Rome, Italy', 39, 'F', '+39-312-345-6789', 'isabella.rossi@example.com', 'password123'),
('Robert Wilson', '909 Pine St, Chicago, IL', 41, 'M', '+1-555-987-6543', 'robert.wilson@example.com', 'password123'),
('Priya Sharma', '111 Gandhi Rd, Mumbai, India', 32, 'F', '+91-99876-54321', 'priya.sharma@example.com', 'password123'),
('James Taylor', '222 Elizabeth St, London, UK', 38, 'M', '+44-7700-900456', 'james.taylor@example.com', 'password123'),
('Yuki Tanaka', '333 Tokyo St, Tokyo, Japan', 27, 'F', '+81-90-8765-4321', 'yuki.tanaka@example.com', 'password123');




-- Create Countries table
CREATE TABLE Countries (
    Country_code VARCHAR(3) PRIMARY KEY,
    Country_Name VARCHAR(100) NOT NULL
);

-- Countries
INSERT INTO Countries (Country_code, Country_Name) VALUES
('USA', 'United States'),
('IND', 'India'),
('GBR', 'United Kingdom'),
('CAN', 'Canada'),
('AUS', 'Australia'),
('JPN', 'Japan'),
('DEU', 'Germany'),
('FRA', 'France'),
('ITA', 'Italy'),
('CHN', 'China');


-- Create Airplane_Type table
CREATE TABLE Airplane_Type (
    A_ID VARCHAR(10) PRIMARY KEY,
    Capacity INT NOT NULL,
    A_weight DECIMAL(10, 2) NOT NULL,
    Company VARCHAR(100) NOT NULL
);

-- Airplane Types
INSERT INTO Airplane_Type (A_ID, Capacity, A_weight, Company) VALUES
('B737', 189, 41413.00, 'Boeing'),
('B747', 467, 183520.00, 'Boeing'),
('B777', 396, 167829.00, 'Boeing'),
('B787', 330, 119950.00, 'Boeing'),
('A320', 186, 42400.00, 'Airbus'),
('A330', 335, 119600.00, 'Airbus'),
('A350', 440, 140000.00, 'Airbus'),
('A380', 853, 276800.00, 'Airbus'),
('E190', 114, 29476.00, 'Embraer'),
('CRJ9', 90, 23133.00, 'Bombardier');


-- Create Airport table
CREATE TABLE Airport (
    Air_Code VARCHAR(5) PRIMARY KEY,
    Air_Name VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Country_code VARCHAR(3) NOT NULL,
    FOREIGN KEY (Country_code) REFERENCES Countries(Country_code)
);

-- Airports
INSERT INTO Airport (Air_Code, Air_Name, City, Country_code) VALUES
('JFK', 'John F. Kennedy International Airport', 'New York', 'USA'),
('LAX', 'Los Angeles International Airport', 'Los Angeles', 'USA'),
('ORD', 'Hare International Airport', 'Chicago', 'USA'),
('DEL', 'Indira Gandhi International Airport', 'New Delhi', 'IND'),
('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'IND'),
('LHR', 'Heathrow Airport', 'London', 'GBR'),
('YYZ', 'Toronto Pearson International Airport', 'Toronto', 'CAN'),
('SYD', 'Sydney Airport', 'Sydney', 'AUS'),
('NRT', 'Narita International Airport', 'Tokyo', 'JPN'),
('FRA', 'Frankfurt Airport', 'Frankfurt', 'DEU'),
('CDG', 'Charles de Gaulle Airport', 'Paris', 'FRA'),
('FCO', 'Leonardo da Vinci International Airport', 'Rome', 'ITA'),
('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'CHN');


-- Create Flight table
CREATE TABLE Flight (
    Flight_ID INT AUTO_INCREMENT PRIMARY KEY,
    Departure DATETIME NOT NULL,
    Arrival DATETIME NOT NULL,
    Fare_Amount DECIMAL(10, 2) NOT NULL,
    A_ID VARCHAR(10) NOT NULL,
    Starting_Airport VARCHAR(5) NOT NULL,
    Ending_Airport VARCHAR(5) NOT NULL,
    Remaining_Seats INT NOT NULL,
    FOREIGN KEY (A_ID) REFERENCES Airplane_Type(A_ID),
    FOREIGN KEY (Starting_Airport) REFERENCES Airport(Air_Code),
    FOREIGN KEY (Ending_Airport) REFERENCES Airport(Air_Code)
);

-- Flights
INSERT INTO Flight (Departure, Arrival, Fare_Amount, A_ID, Starting_Airport, Ending_Airport, Remaining_Seats) VALUES
('2025-04-10 08:00:00', '2025-04-10 11:30:00', 325.00, 'B737', 'LAX', 'JFK', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B737')),
('2025-04-10 10:00:00', '2025-04-10 12:00:00', 255.00, 'A320', 'JFK', 'ORD', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'A320')),
('2025-04-11 14:00:00', '2025-04-11 16:30:00', 175.00, 'B737', 'DEL', 'BOM', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B737')),
('2025-04-12 22:00:00', '2025-04-13 10:30:00', 750.00, 'B777', 'JFK', 'LHR', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B777')),
('2025-04-13 12:00:00', '2025-04-14 16:30:00', 950.00, 'B787', 'LAX', 'NRT', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B787')),
('2025-04-14 20:00:00', '2025-04-16 06:30:00', 1200.00, 'A350', 'LAX', 'SYD', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'A350')),
('2025-04-15 18:00:00', '2025-04-16 07:30:00', 675.00, 'A330', 'JFK', 'CDG', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'A330')),
('2025-04-16 09:00:00', '2025-04-16 11:30:00', 375.00, 'A320', 'LHR', 'FRA', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'A320')),
('2025-04-17 11:00:00', '2025-04-17 14:30:00', 500.00, 'B737', 'NRT', 'PVG', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B737')),
('2025-04-18 07:00:00', '2025-04-18 09:30:00', 385.00, 'CRJ9', 'JFK', 'YYZ', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'CRJ9')),
('2025-04-18 15:00:00', '2025-04-18 18:30:00', 325.00, 'B737', 'LAX', 'JFK', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B737')),
('2025-04-19 10:00:00', '2025-04-19 12:00:00', 255.00, 'A320', 'JFK', 'ORD', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'A320')),
('2025-04-19 13:00:00', '2025-04-19 15:30:00', 175.00, 'B737', 'DEL', 'BOM', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B737')),
('2025-04-20 22:00:00', '2025-04-21 10:30:00', 750.00, 'B777', 'JFK', 'LHR', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B777')),
('2025-04-21 12:00:00', '2025-04-22 16:30:00', 950.00, 'B787', 'LAX', 'NRT', (SELECT Capacity FROM Airplane_Type WHERE A_ID = 'B787'));


-- Create transaction table
CREATE TABLE Transactions (
    TS_ID INT AUTO_INCREMENT PRIMARY KEY,
    Transaction_Date DATETIME NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Ps_ID INT NOT NULL,
    Flight_ID INT NOT NULL,
    FOREIGN KEY (Ps_ID) REFERENCES Passenger(Ps_ID),
    FOREIGN KEY (Flight_ID) REFERENCES Flight(Flight_ID)
);


--Trigger
DELIMITER //

CREATE TRIGGER AfterTransactionInsert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
        UPDATE Flight
        SET Remaining_Seats = Remaining_Seats - 1
        WHERE Flight_ID = NEW.Flight_ID AND Remaining_Seats > 0;
END //

DELIMITER ;


-- Create Admins table
CREATE TABLE Admins (
    Admin_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Is_SuperAdmin BOOLEAN NOT NULL DEFAULT FALSE
);


INSERT INTO Admins (Name, Email, Password, Is_SuperAdmin)
VALUES ('Sahil Ranadive', 'admin@gmail.com', 'qwerty', TRUE);