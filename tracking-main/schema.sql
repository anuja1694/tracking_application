create table users( id integer primary key AUTOINCREMENT, name text not null, password text not null, admin boolean not null DEFAULT '0');

create table trk ( trkid integer primary key AUTOINCREMENT, route text not null, vehicle text, team text,
status text, trk_date timestamp DEFAULT CURRENT_TIMESTAMP );

