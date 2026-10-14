-- Lista projektowa nr 1 - PostgreSQL 18
-- ALTER TABLE resolves the Bandy <-> Kocury referential cycle.

DROP TABLE IF EXISTS wrogowie_kocurow;
DROP TABLE IF EXISTS wrogowie;
-- Bandy has a foreign key to Kocury, while Kocury has one to Bandy.
-- Dropping Bandy first with CASCADE removes only that dependent FK.
DROP TABLE IF EXISTS bandy CASCADE;
DROP TABLE IF EXISTS kocury;
DROP TABLE IF EXISTS funkcje;

CREATE TABLE funkcje (
    funkcja    varchar(10) PRIMARY KEY,
    min_myszy  numeric(3) CHECK (min_myszy > 5),
    max_myszy  numeric(3) CHECK (max_myszy >= min_myszy AND max_myszy < 200)
);

CREATE TABLE bandy (
    nr_bandy   numeric(2) PRIMARY KEY,
    nazwa      varchar(20) NOT NULL,
    teren      varchar(15) UNIQUE,
    szef_bandy varchar(15) UNIQUE
);

CREATE TABLE kocury (
    imie             varchar(15) NOT NULL,
    plec             varchar(1) CHECK (plec IN ('M', 'D')),
    pseudo           varchar(15) PRIMARY KEY,
    funkcja          varchar(10) REFERENCES funkcje(funkcja),
    szef             varchar(15) REFERENCES kocury(pseudo),
    w_stadku_od      date DEFAULT CURRENT_DATE,
    przydzial_myszy  numeric(3),
    myszy_extra      numeric(3),
    nr_bandy         numeric(2) REFERENCES bandy(nr_bandy)
);

ALTER TABLE bandy
    ADD CONSTRAINT bandy_szef_bandy_fk
    FOREIGN KEY (szef_bandy) REFERENCES kocury(pseudo);

CREATE TABLE wrogowie (
    imie_wroga       varchar(15) PRIMARY KEY,
    stopien_wrogosci numeric(2) CHECK (stopien_wrogosci BETWEEN 1 AND 10),
    gatunek          varchar(15),
    lapowka          varchar(20)
);

CREATE TABLE wrogowie_kocurow (
    pseudo           varchar(15) REFERENCES kocury(pseudo),
    imie_wroga       varchar(15) REFERENCES wrogowie(imie_wroga),
    data_incydentu   date NOT NULL,
    opis_incydentu   varchar(50),
    PRIMARY KEY (pseudo, imie_wroga)
);
