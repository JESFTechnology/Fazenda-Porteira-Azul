create database blueGateFarm;

use blueGateFarm;

create table crops(
	id_crop int not null auto_increment primary key,
    name varchar(50),
    area_hectares decimal(10,2),
    current_season int
);

create table employees(
	id_employee int not null auto_increment primary key,
    name varchar(100),
    cpf int not null,
    job varchar(100),
    base_salary decimal(10,2),
    weekly_hours int,
    hire_date date,
    id_crop_fk int,
    foreign key (id_crop_fk) references crops(id_crop) on delete no action on update cascade
);

create table userType(
	id_user_type int not null auto_increment primary key,
    description varchar(200)
);

create table users(
	id_user int not null auto_increment primary key,
    name varchar(100),
    email varchar(200),
    password varchar(255),
    activity boolean,
    id_user_type_fk int not null,
    id_employee_fk int,
    foreign key (id_user_type_fk) references userType(id_user_type) on delete no action on update cascade,
	foreign key (id_employee_fk) references employees(id_employee) on delete no action on update cascade
);

create table machineryType(
	id_machinery_type int not null auto_increment primary key,
    name varchar(50)
);

create table machineryBrand(
	id_machinery_brand int not null auto_increment primary key,
    name varchar(50)
);

create table machinery(
	id_machinery int not null auto_increment primary key,
    model varchar(100),
    year int,
    total_worked_hours int,
    total_fuel_consumption decimal(10,2),
    id_machinery_brand_fk int,
    id_machinery_type_fk int,
	foreign key (id_machinery_brand_fk) references machineryBrand(id_machinery_brand) on delete no action on update cascade,
	foreign key (id_machinery_type_fk) references machineryType(id_machinery_type) on delete no action on update cascade
);

create table machineryUsage(
	id_machinery_usage int not null auto_increment primary key,
    usage_date date,
    hours_usage decimal(10,2),
    fuel_consumed decimal(10,2),
    observation varchar(255),
    id_machinery_fk int,
    id_employee_fk int,
	foreign key (id_machinery_fk) references machinery(id_machinery) on delete cascade on update cascade,
	foreign key (id_employee_fk) references employees(id_employee) on delete no action on update cascade
);

create table grains(
	id_grain int not null auto_increment primary key,
    name varchar(50),
    type varchar(50)
);

create table storageLocations(
	id_storage_location int not null auto_increment primary key,
    name varchar(100)
);

create table storage(
	id_storage int not null auto_increment primary key,
    quantity_bags int,
    entry_date date,
    id_grain_fk int,
	id_location_fk int,
	foreign key (id_grain_fk) references grains(id_grain) on delete cascade on update cascade,
	foreign key (id_location_fk) references storageLocations(id_storage_location) on delete cascade on update cascade
);

create table costTypes(
	id_cost_type int not null auto_increment primary key,
    name varchar(50),
    cost_value decimal(10,2)
);

create table productionCosts(
	id_production_cost int not null auto_increment primary key,
    cost_date date,
	description varchar(255),
    id_cost_type_fk int,
	foreign key (id_cost_type_fk) references costTypes(id_cost_type) on delete no action on update cascade
);

create table marketQuotes(
	id_market_quotes int not null auto_increment primary key,
	price_per_bag decimal(10,2),
    quote_date date,
    observation varchar(200),
    id_grain_fk int,
	foreign key (id_grain_fk) references grains(id_grain) on delete cascade on update cascade
);
