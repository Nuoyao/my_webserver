
-- Database Schema

Stock(Stock_Ticker INT NOT NULL, 
Market_Cap REAL, 
Profile_ID INT 
NOT NULL 
UNIQUE, 
PRIMARY KEY(Stock_Ticker),
FK(Stock_Ticker) REFERENCES Company_Profile(Profile_ID)
ON UPDATE NO ACTION
ON DELETE NO ACTION)

Historical_Data(Stock_Ticker INT NOT NULL, 
Date DATETIME NOT NULL, 
Close Real, 
Adjusted_Close Real, 
Open Real, 
Low Real, 
High Real, 
Volume Real,
PRIMARY KEY(Stock_Ticker, Date), 
FOREIGN KEY (Stock_Ticker) REFERENCES Stock (Stock_Ticker)
ON UPDATE CASCADE
ON DELETE NO ACTION) 

Fundamental_Financial_Data(Stock_Ticker INT NOT NULL, 
Release_Season DATETIME NOT NULL,
Revenue Real, 
Cost Real, 
Profit Real, 
PRIMARY KEY(Stock_Ticker, Release_Season), 
FOREIGN KEY (Stock_Ticker) REFERENCES Stock (Stock_Ticker)
ON UPDATE CASCADE
    ON DELETE NO ACTION) 

Company_Profile(Profile_ID INT NOT NULL,
Sector VARCHAR(255) NOT NULL, 
Address VARCHAR(255) NOT NULL,
Number_of_Employees INT, 
PRIMARY KEY(Profile_ID),
FOREIGN KEY (Stock_Ticker) REFERENCES Stock (Stock_Ticker))

Key_Executives(Title VARCHAR(255) NOT NULL, 
Pay Real, 
Name VARCHAR(255) NOT NULL, 
Year_Born INT, 
PRIMARY KEY(Name), 
FOREIGN KEY (Profile_ID) REFERENCES Company_Profile (Profile_ID)
	ON UPDATE NO ACTION
    ON DELETE NO ACTION) 

-- Advanced Features
-- Composite types

Create TYPE addr AS (
    unit_number  integer,
    street  character varying(255) ,
	city character varying(255) ,
	state_abbr character varying(255), 
	zip_code integer	
);

ALTER TABLE company_profile
ADD COLUMN address addr;

—- Arrays
CREATE TABLE forecast (
	stock_ticker character varying(255),
    revenue   real[],
	earnings real[]
);

-- Trigger

ALTER TABLE stock
ADD COLUMN price_change real;

CREATE OR REPLACE FUNCTION price_change() 
	RETURNS trigger AS $$
	BEGIN
		UPDATE stock SET price_change = NEW.adj_close/
(SELECT h.adj_close 
FROM historical h												
WHERE h.date < NEW.date AND h.stock_ticker = NEW.stock_ticker
ORDER BY h.date DESC											  	
LIMIT 1)*100-100
		WHERE stock.stock_ticker = NEW.stock_ticker;
		RETURN OLD;
	END; 
	$$
	LANGUAGE PLPGSQL;

CREATE TRIGGER calculate_change
    AFTER INSERT ON historical
    FOR EACH ROW
EXECUTE FUNCTION price_change(); 
