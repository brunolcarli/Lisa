from django.test import TestCase
from lisa_processing.util.pipelines import Normalizer


class TextNormalizerTests(TestCase):
    """
    Testes de validação do normalizador de texto utilizado no processamento
    dos pipelines.
    """
    def setUp(self):
        self.refresh = Normalizer()

    def test_convert_string_to_list(self):
        """
        Verifica que o normalizador converte string em lista de tokens.
        """
        text = 'o rato roeu a roupa do rei de Roma.'
        tokens = self.refresh.string_to_list(text)

        # agora deve ser uma lista
        self.assertTrue(isinstance(tokens, list))
        # deve haver 9 tokens, um para cada termo na frase.
        self.assertEqual(len(tokens), 10)
        # todos os tokens são string
        self.assertTrue(all([isinstance(token, str) for token in tokens]))

    def test_covert_list_to_string(self):
        """
        verifica que o normalizador converte uma lista de tokens em uma bela
        string.
        """
        tokens = ['o', 'rato', 'roeu', 'a', 'roupa', 'do', 'rei', 'de', 'Roma', '.']
        text = self.refresh.list_to_string(tokens)

        # agora deve ser uma string
        self.assertTrue(isinstance(text, str))
        # como a saída deve se parecer
        self.assertEqual(text, 'o rato roeu a roupa do rei de Roma.')
