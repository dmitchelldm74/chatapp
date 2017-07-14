CREATE TABLE "messages" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`_from`	TEXT,
	`_to`	TEXT,
	`content`	TEXT,
	`timestamp`	TEXT
);
CREATE TABLE "sessions" (
	`key`	TEXT,
	`now`	TEXT,
	`expiration`	TEXT,
	`user`	TEXT
);
CREATE TABLE "users" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`username`	TEXT NOT NULL,
	`password`	TEXT NOT NULL
);
