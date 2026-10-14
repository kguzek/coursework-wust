-- Lista projektowa nr 1 - Oracle Database Free.
-- The Compose startup mount runs this file during first Oracle initialization.
-- ALTER TABLE resolves the Bandy <-> Kocury referential cycle.

CREATE TABLE funkcje (
    funkcja    VARCHAR2(10) PRIMARY KEY,
    min_myszy  NUMBER(3) CHECK (min_myszy > 5),
    max_myszy  NUMBER(3) CHECK (max_myszy >= min_myszy AND max_myszy < 200)
);

CREATE TABLE bandy (
    nr_bandy   NUMBER(2) PRIMARY KEY,
    nazwa      VARCHAR2(20) NOT NULL,
    teren      VARCHAR2(15) UNIQUE,
    szef_bandy VARCHAR2(15) UNIQUE
);

CREATE TABLE kocury (
    imie             VARCHAR2(15) NOT NULL,
    plec             VARCHAR2(1) CHECK (plec IN ('M', 'D')),
    pseudo           VARCHAR2(15) PRIMARY KEY,
    funkcja          VARCHAR2(10) REFERENCES funkcje(funkcja),
    szef             VARCHAR2(15) REFERENCES kocury(pseudo),
    w_stadku_od      DATE DEFAULT SYSDATE,
    przydzial_myszy  NUMBER(3),
    myszy_extra      NUMBER(3),
    nr_bandy         NUMBER(2) REFERENCES bandy(nr_bandy)
);

ALTER TABLE bandy
    ADD CONSTRAINT bandy_szef_bandy_fk
    FOREIGN KEY (szef_bandy) REFERENCES kocury(pseudo);

CREATE TABLE wrogowie (
    imie_wroga       VARCHAR2(15) PRIMARY KEY,
    stopien_wrogosci NUMBER(2) CHECK (stopien_wrogosci BETWEEN 1 AND 10),
    gatunek          VARCHAR2(15),
    lapowka          VARCHAR2(20)
);

CREATE TABLE wrogowie_kocurow (
    pseudo           VARCHAR2(15) REFERENCES kocury(pseudo),
    imie_wroga       VARCHAR2(15) REFERENCES wrogowie(imie_wroga),
    data_incydentu   DATE NOT NULL,
    opis_incydentu   VARCHAR2(50),
    PRIMARY KEY (pseudo, imie_wroga)
);
