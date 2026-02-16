from unittest import TestCase

from business_object.utilisateur import Utilisateur


class TestUtilisateur(TestCase):
    def test_validation_ok(self):
        self.assertEqual(Utilisateur.valider_nom_utilisateur("john"), "john")

    def test_validation_ko(self):
        with self.assertRaises(ValueError):
            Utilisateur.valider_nom_utilisateur("a")
