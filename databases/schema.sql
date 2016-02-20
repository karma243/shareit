drop table if exists entries;
drop table if exists authentication;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

create table authentication (
    username text primary key not null,
    password text not null
);