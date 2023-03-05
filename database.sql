DROP TABLE IF EXISTS url;
DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE url (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date NOT NULL
);

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    answer bigint,
    created_at date NOT NULL
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id int REFERENCES url (id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at timestamp NOT NULL
);

