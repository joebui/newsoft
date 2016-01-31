create table Category (
	id int identity(1,1) primary key,
	name varchar(100) not null
);

create table Subcategory (
	id int identity(1,1) primary key,
	categoryID int references category(id) not null,
	name varchar(100) not null
);

create table News (
	id int identity(1,1) primary key,
	subcategoryID int references subcategory(id) not null,
	title varchar(200) not null,
	shortdesc varchar(500),
	content text not null
);

drop table category;
drop table subcategory;
drop table news;

alter table News add created datetime not null, updated datetime not null;