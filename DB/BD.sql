CREATE DATABASE IF NOT EXISTS bd_projet_AIS;

USE bd_projet_AIS;

-- Création de la table "Role"
CREATE TABLE IF NOT EXISTS Role (
    IDRole INT PRIMARY KEY,
    Role VARCHAR(255) NOT NULL
);

-- Création de la table "Country"
CREATE TABLE IF NOT EXISTS Country (
    IDCountry INT PRIMARY KEY,
    NameCountry VARCHAR(255) NOT NULL
);


-- Création de la table "Company"
CREATE TABLE IF NOT EXISTS Company (
    IDCompany INT PRIMARY KEY,
    NameCompany VARCHAR(255) NOT NULL,
    IDCountry INT
);

-- Création de la table "VesselType"
CREATE TABLE IF NOT EXISTS VesselType (
    IDVesselType INT  PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

-- Création de la table "NavigationStatus"
CREATE TABLE IF NOT EXISTS NavigationStatus (
    Status INT PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

-- création de la table Vessel
CREATE TABLE IF NOT EXISTS Vessel (
    MMSI VARCHAR(255) PRIMARY KEY,
    IMO VARCHAR(255),
    CallSign VARCHAR(255) NOT NULL,
    IDVesselType INT,
    VesselName VARCHAR(255) NOT NULL,
    Length FLOAT(10,5),
    Width FLOAT(10,5),
    Draft FLOAT(10,5),
    Cargo VARCHAR(255),
    IDCountry INT NOT NULL,
    TransceiverClass VARCHAR(255) NOT NULL,
    IDCompany INT,
    FOREIGN KEY (IDCountry) REFERENCES Country(IDCountry) ON DELETE CASCADE,
    FOREIGN KEY (IDCompany) REFERENCES Company(IDCompany) ON DELETE CASCADE,
    FOREIGN KEY (IDVesselType) REFERENCES VesselType(IDVesselType) ON DELETE CASCADE
);


-- création de la table Position
CREATE TABLE IF NOT EXISTS Position (
    MMSI VARCHAR(255),
    BaseDateTime DATETIME,
    LAT FLOAT(15,10),
    LON FLOAT(15,10),
    SOG FLOAT(15,10),
    COG FLOAT(15,10),
    Heading FLOAT(15,10),
    Status INT,
    Region VARCHAR(255),
    PRIMARY KEY (MMSI, BaseDateTime),
    FOREIGN KEY (MMSI) REFERENCES Vessel(MMSI) ON DELETE CASCADE,
    FOREIGN KEY (Status) REFERENCES NavigationStatus(Status)
);

-- création de la table User
CREATE TABLE IF NOT EXISTS User (
    IDUser INT AUTO_INCREMENT PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    Login VARCHAR(255) NOT NULL
);

-- création de la table UserHasRole
CREATE TABLE IF NOT EXISTS UserHasRole (
    IDUser INT,
    IDRole INT,
    PRIMARY KEY (IDUser, IDRole),
    FOREIGN KEY (IDUser) REFERENCES User(IDUser) ON DELETE CASCADE,
    FOREIGN KEY (IDRole) REFERENCES Role(IDRole) ON DELETE CASCADE
);

-- création de la table UserHasVessel
CREATE TABLE IF NOT EXISTS UserHasVessel (
    IDUser INT,
    MMSI VARCHAR(255),
    IsCaptain BOOLEAN,
    PRIMARY KEY (IDUser, MMSI),
    FOREIGN KEY (IDUser) REFERENCES User(IDUser) ON DELETE CASCADE,
    FOREIGN KEY (MMSI) REFERENCES Vessel(MMSI) ON DELETE CASCADE
);
