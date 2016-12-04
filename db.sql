drop table if exists teams;
drop table if exists entries;

create table teams (
    teamid integer primary key autoincrement,
    name text not null unique,
    secret integer not null
);

create table entries (
    entryid integer primary key autoincrement,
    teamid integer,
    entry text not null,
    created datetime default(datetime()),
    foreign key( teamid ) references teams(teamid)
);

insert into teams (name, secret) values ('Happy Feet', 1);
insert into teams (name, secret) values ('Deep Thought', 2);
insert into teams (name, secret) values ('Dark Side of the Moon', 3);
insert into teams (name, secret) values ('Shallow', 4);

insert into entries (teamid, entry) values (1, 'entry1');
insert into entries (teamid, entry) values (2, 'entry2');
insert into entries (teamid, entry) values (3, 'entry3');
insert into entries (teamid, entry) values (3, 'entry4');
