drop database if exists e_gramateia;
create database if not exists e_grammateia;
use e_grammateia; 

create table Professor(
	Prof_no int primary key not null unique auto_increment,
    Prof_name nvarchar(100) not null,
    id_tomea int ,
    Phone char(10) ,
    email varchar(50) ,
    Office_location nvarchar(300),
    Office_hours varchar(150),
    Gender enum('M','F') not null default 'M',
    School enum('ECE','OTHER') default 'ECE'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

create table Tomeis(
	ID_Tomea int primary key not null auto_increment,
    Name_Tomea nvarchar(150) not null,
    Director_ID int ,
    foreign key(Director_ID) references Professor(Prof_no) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table Professor 
add foreign key(id_tomea) references Tomeis(ID_Tomea) on delete cascade;

create table Roes(
	id_Rohs int primary key not null auto_increment,
    name_rohs nvarchar(150)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;


create table Courses(
	Course_Code nvarchar(10) primary key not null,
    Course_name nvarchar(250) not null,
    ects int not null,
    Lab char(1),
    Semester int not null,
    Course_Type enum('O','C','T') not null default 'O'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

create table Teaches(
	Prof_id int not null,
    Course_code nvarchar(10) not null,
    primary key(Prof_id,Course_code),
    foreign key(Prof_id) references Professor(Prof_no),
    foreign key(Course_Code) references Courses(Course_Code) on delete cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;

create table c_belongs_r(
	Course_code nvarchar(10) not null,
    id_Rohs int not null,
    Semester int,
    Omada char(1),
    primary key(Course_code,id_Rohs),
    foreign key(Course_Code) references Courses(Course_Code) on delete cascade,
    foreign key(id_Rohs) references Roes(id_Rohs) on delete cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;



