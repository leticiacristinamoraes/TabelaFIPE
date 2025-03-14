
CREATE TABLE Users (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)

);
CREATE TABLE Roles (
    id UUID PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Permissions (
    id UUID PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE Cars (
    id UUID PRIMARY KEY,
    brand VARCHAR(255),
    model VARCHAR(255),
    model_year VARCHAR(255)
);

CREATE TABLE Shops (
    id UUID PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Users_roles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES Users(id),
    role_id UUID REFERENCES Roles(id)
);

CREATE TABLE Roles_permissions (
    id UUID PRIMARY KEY,
    role_id UUID REFERENCES Roles(id),
    permission_id UUID REFERENCES Permissions(id)
);

CREATE TABLE Registers (
    id UUID PRIMARY KEY,
    shop_id UUID REFERENCES Shops(id),
    car_id UUID REFERENCES Cars(id),
    created_date DATE,
    price VARCHAR(255)
);


CREATE TABLE Avg_price (
    id UUID PRIMARY KEY,
    car_id UUID REFERENCES Cars(id),
    avg_price VARCHAR(255)
);
