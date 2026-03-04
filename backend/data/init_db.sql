-----------------------------------------------------
-- Utilisateur 
-----------------------------------------------------
DROP TABLE IF EXISTS utilisateur CASCADE ;

CREATE TABLE utilisateur (
    id                      SERIAL PRIMARY KEY,
    nom_utilisateur         VARCHAR(30) UNIQUE NOT NULL,
    role                    VARCHAR(20) DEFAULT 'user'
);

-----------------------------------------------------
-- Credentials (authentification)
-----------------------------------------------------
DROP TABLE IF EXISTS credentials CASCADE;

CREATE TABLE credentials (
    id                      INTEGER PRIMARY KEY REFERENCES utilisateur(id) ON DELETE CASCADE,
    mot_de_passe_hash       VARCHAR(256) NOT NULL,
    sel                     VARCHAR(64) NOT NULL
);