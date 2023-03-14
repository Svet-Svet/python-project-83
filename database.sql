DROP TABLE IF EXISTS url;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE url (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date NOT NULL
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id int REFERENCES url (id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at date NOT NULL
);

SELECT * FROM url LEFT JOIN (
	SELECT DISTINCT ON (url_id) url_id, status_code, created_at
		FROM url_checks
		ORDER BY url_id, status_code, created_at DESC
) AS last_checks
ON url.id = last_checks.url_id;




SELECT * FROM (
    SELECT DISTINCT ON (url.name) url.id, url.name, status_code, url_checks.created_at AS created_at_url_checks
    FROM url JOIN url_checks ON url.id = url_checks.url_id
    ORDER BY url.name
    )
ORDER BY url.id DESC;


SELECT * FROM (
    SELECT DISTINCT ON (url.name) url.id, url.name, url_checks.status_code, url_checks.created_at AS created_at_url_checks
    FROM url LEFT JOIN url_checks ON url.id = url_checks.url_id
    ORDER BY url.name
    ) AS MYTable
ORDER BY MYTable.id DESC;
