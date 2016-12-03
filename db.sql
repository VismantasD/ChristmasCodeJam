drop table if exists teams;
drop table if exists entries;

create table teams (
    teamid integer primary key autoincrement,
    name text not null unique
);

create table entries (
    entryid integer primary key autoincrement,
    teamid integer,
    entry text not null,
    created datetime default(datetime()),
    foreign key( teamid ) references teams(teamid)
);

insert into teams (name) values ('Happy Feet');
insert into teams (name) values ('Blade Runner');
insert into teams (name) values ('Neuromancer');
insert into teams (name) values ('Stalker');

insert into entries (teamid, entry) values (1, 'entry1');
insert into entries (teamid, entry) values (2, 'entry2');
insert into entries (teamid, entry) values (3, 'entry3');
insert into entries (teamid, entry) values (3, 'entry4');
