-----------------------------------------------------
-- Insertion des utilisateurs
-----------------------------------------------------
INSERT INTO utilisateur (nom_utilisateur)
VALUES 
    ('dupont'),
    ('martin');

-----------------------------------------------------
-- Insertion des credentials (identifiants)
-- Les hashs et sels seront remplacés dynamiquement par reset_database.py
-----------------------------------------------------
INSERT INTO credentials (id, mot_de_passe_hash, sel)
VALUES
    (1, 'mdp1', ''),
    (2, 'mdp2', '');
