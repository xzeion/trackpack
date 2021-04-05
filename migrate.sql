CREATE TABLE IF NOT EXISTS packages (
  id UUID PRIMARY KEY,
  created_at timestamp DEFAULT CURRENT_DATE(),
  updated_at timestamp DEFAULT CURRENT_DATE(),
  delivered boolean DEFAULT FALSE,
  eta timestamp NOT NULL,
  shipper UUID NOT NULL,
  reciever UUID NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
  id UUID PRIMARY KEY,
  package_id UUID NOT NULL,
  arrival timestamp DEFAULT CURRENT_DATE(),
  location decimal[][]
);

CREATE TABLE IF NOT EXISTS shipper (
  id UUID PRIMARY KEY,
  name text NOT NULL,
  address text NOT NULL
);

CREATE TABLE IF NOT EXISTS reciever (
  id UUID PRIMARY KEY,
  name text NOT NULL,
  address text NOT NULL
);
