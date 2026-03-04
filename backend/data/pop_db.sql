-----------------------------------------------------
-- Insertion des utilisateurs (ids auto-générés)
-----------------------------------------------------
INSERT INTO utilisateur (nom_utilisateur, role)
VALUES 
    ('admin', 'admin'),
    ('dupont', 'user'),
    ('martin', 'user');

-----------------------------------------------------
-- Insertion des credentials (identifiants)
-- Les hashs et sels seront remplacés dynamiquement par reset_database.py
-----------------------------------------------------
INSERT INTO credentials (id, mot_de_passe_hash, sel)
VALUES
    (1, 'nutriplan', ''),
    (2, 'mdp123', ''),
    (3, 'mdp123', '');
