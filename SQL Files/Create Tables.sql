
CREATE TABLE UserInfo (
UserID int PRIMARY KEY IDENTITY NOT NULL,
Username varchar(30) NOT NULL,
Email varchar(320) NOT NULL,
Passw varchar(256) NOT NULL);

CREATE TABLE UserSavedLists (
ListID int PRIMARY KEY IDENTITY NOT NULL,
ListName varchar(50) NOT NULL,
DateLastSaved smalldatetime NOT NULL,
PublicOrPrivate int NOT NULL,
ListDescr varchar(1000),
UserID int FOREIGN KEY REFERENCES UserInfo(UserID) NOT NULL);

CREATE TABLE Categories(
CategoryID int PRIMARY KEY NOT NULL,
CategoryName varchar(50) NOT NULL);

CREATE TABLE BikeParts (
PartID int PRIMARY KEY NOT NULL,
PartName varchar(100) NOT NULL,
PartDescr varchar(1000),
PartMainCategory int FOREIGN KEY REFERENCES Categories(CategoryID) NOT NULL);

CREATE TABLE CompatibleCategories (
PartCategoryID int PRIMARY KEY IDENTITY NOT NULL,
PartID int FOREIGN KEY REFERENCES BikeParts(PartID) NOT NULL,
CategoryID int FOREIGN KEY REFERENCES Categories(CategoryID) NOT NULL);

CREATE TABLE PartLists (
PartListID int PRIMARY KEY IDENTITY NOT NULL,
PartID int FOREIGN KEY REFERENCES BikeParts(PartID) NOT NULL,
ListID int FOREIGN KEY REFERENCES UserSavedLists(ListID) NOT NULL);

CREATE TABLE PriceChanges (
PriceID int PRIMARY KEY IDENTITY NOT NULL,
Price decimal(7,2) NOT NULL,
PriceDate smalldatetime NOT NULL,
Retailer varchar(50) NOT NULL,
WebsiteURL varchar(2048) NOT NULL,
PartID int FOREIGN KEY REFERENCES BikeParts(PartID) NOT NULL);


INSERT INTO Categories VALUES ('1', 'Frameset');
INSERT INTO Categories VALUES ('2', 'Frame');
INSERT INTO Categories VALUES ('3', 'Fork');
INSERT INTO Categories VALUES ('4', 'Stem');
INSERT INTO Categories VALUES ('5', 'Handlebar');
INSERT INTO Categories VALUES ('6', 'Handlebar Tape');
INSERT INTO Categories VALUES ('7', 'Wheels');
INSERT INTO Categories VALUES ('8', 'Tyres');
INSERT INTO Categories VALUES ('9', 'Inner Tubes');
INSERT INTO Categories VALUES ('10', 'Rim Tape');
INSERT INTO Categories VALUES ('11', 'Tubeless Wheels');
INSERT INTO Categories VALUES ('12', 'Tubeless Tyres');
INSERT INTO Categories VALUES ('13', 'Tubeless Sealant');
INSERT INTO Categories VALUES ('14', 'Tubeless Rim Tape');
INSERT INTO Categories VALUES ('15', 'Front Caliper');
INSERT INTO Categories VALUES ('16', 'Rear Caliper');
INSERT INTO Categories VALUES ('17', 'Brake Cable');
INSERT INTO Categories VALUES ('18', 'Brake Cable Housing');
INSERT INTO Categories VALUES ('19', 'Hydraulic Front Caliper');
INSERT INTO Categories VALUES ('20', 'Hydraulic Rear Caliper');
INSERT INTO Categories VALUES ('21', 'Hydraulic Brake Lines');
INSERT INTO Categories VALUES ('22', 'Hydraulic Brake Fluid');
INSERT INTO Categories VALUES ('23', 'Left Shifter');
INSERT INTO Categories VALUES ('24', 'Right Shifter');
INSERT INTO Categories VALUES ('25', 'Front Derailleur');
INSERT INTO Categories VALUES ('26', 'Rear Derailleur');
INSERT INTO Categories VALUES ('27', 'Crankset');
INSERT INTO Categories VALUES ('28', 'Cassette');
INSERT INTO Categories VALUES ('29', 'Bottom Bracket');
INSERT INTO Categories VALUES ('30', 'Chain');
INSERT INTO Categories VALUES ('31', 'Gear Cable');
INSERT INTO Categories VALUES ('23', 'Gear Cable Housing');
