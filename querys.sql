-- hacer al inicio de cada agregacion de filas, para reiniciar en limpio
-- TRUNCATE superheroes.tindanime_superhero * RESTART IDENTITY CASCADE

CREATE TABLE superheroes.tindanime_superhero(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    height DOUBLE PRECISION,
    weight DOUBLE PRECISION
);

CREATE TABLE superheroes.tindanime_character(
    id SERIAL,
    superhero_id SERIAL,
    biography_name VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (superhero_id) REFERENCES superheroes.tindanime_superhero(id)
);

CREATE TABLE superheroes.tindanime_alterego(
    id SERIAL,
    superhero_id SERIAL,
    name VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (superhero_id) REFERENCES superheroes.tindanime_superhero(id)
);

CREATE TABLE superheroes.tindanime_workOcupation(
    id SERIAL,
    superhero_id SERIAL,
    name VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (superhero_id) REFERENCES superheroes.tindanime_superhero(id)
);
