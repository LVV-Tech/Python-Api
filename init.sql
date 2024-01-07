CREATE TABLE promo (
	id integer PRIMARY KEY AUTOINCREMENT,
	key string,
	discount integer,
	amount integer,
	deadline date,
	active boolean
);

CREATE TABLE service (
	id integer PRIMARY KEY AUTOINCREMENT,
	name string,
	description string,
	price decimal
);

CREATE TABLE action (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	service_id integer,
	promo_id integer,
	cost decimal,
	transaction_time date
);

CREATE TABLE user (
	id integer PRIMARY KEY AUTOINCREMENT,
	role integer,
	phone string,
	full_name string,
	passport string,
	passport_from string,
	address string,
	bank_props string,
	birth_date date,
	ref_counter integer,
	--нахуя?: ,
	ref_from string,
	login string,
	password string,
	vk_id integer,
	tg_id integer
);





