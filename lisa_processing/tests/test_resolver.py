from django.test import TestCase
from lisa_processing.resolvers import Resolver


class ResolverTests(TestCase):
    def setUp(self):
        self.resolver = Resolver()

    def test_resolve_sent_seg_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a fragmentação de
        sentenças quando receber uma entrada do tipo str
        """
        input_data = 'Fui a feira da fruta. Pra ver o que a feira da fruta tem.'
        output = self.resolver.resolve_sentence_segmentation(input_data)

        self.assertEqual(len(output), 2)
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output[0], 'Fui a feira da fruta.')
        self.assertEqual(output[1], 'Pra ver o que a feira da fruta tem.')

    def test_resolve_sent_seg_with_list_input(self):
        """
        Verifica que o resolver processa adequadamente a fragmentação de
        sentenças quando receber uma entrada do tipo list
        """
        input_data = [
            'Fui a feira da fruta. Pra ver o que a feira da fruta tem.',
            'O rato rói. O sistema destroi. Nós somos a causa.'
        ]
        output = self.resolver.resolve_sentence_segmentation(input_data)

        self.assertEqual(len(output), 5)
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output[0], 'Fui a feira da fruta.')
        self.assertEqual(output[1], 'Pra ver o que a feira da fruta tem.')
        self.assertEqual(output[2], 'O rato rói.')
        self.assertEqual(output[3], 'O sistema destroi.')
        self.assertEqual(output[4], 'Nós somos a causa.')

    def test_resolve_tokenize_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a atomização quando
        receber uma entrada do tipo str
        """
        input_data = 'Fui a feira da fruta. Pra ver o que a feira da fruta tem.'
        output = self.resolver.resolve_tokenize(input_data)

        expected_output = [
            'Fui', 'a', 'feira', 'da', 'fruta', '.', 'Pra', 'ver', 'o', 'que',
            'a', 'feira', 'da', 'fruta', 'tem', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_tokenize_with_list_input(self):
        """
        Verifica que o resolver processa adequadamente a atomização quando
        receber uma entrada do tipo list
        """
        input_data = [
            'Fui a feira da fruta.',
            'Pra ver o que a feira da fruta tem.'
        ]
        output = self.resolver.resolve_tokenize(input_data)

        expected_output = [
            'Fui', 'a', 'feira', 'da', 'fruta', '.', 'Pra', 'ver', 'o', 'que',
            'a', 'feira', 'da', 'fruta', 'tem', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_remove_stopwords_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a remoção de palávras
        vazias quando receber uma entrada do tipo str
        """
        input_data = 'Fui a feira da fruta. Pra ver o que a feira da fruta tem.'
        output = self.resolver.resolve_remove_stopwords(input_data)

        expected_output = [
            'Fui', 'feira', 'fruta', '.', 'Pra', 'ver', 'feira', 'fruta', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_remove_stopwords_with_list_input(self):
        """
        Verifica que o resolver processa adequadamente a remoção de palávras
        vazias quando receber uma entrada do tipo list
        """
        input_data = [
            'Fui a feira da fruta.',
            'Pra ver o que a feira da fruta tem.'
        ]
        output = self.resolver.resolve_remove_stopwords(input_data)

        expected_output = [
            'Fui', 'feira', 'fruta', '.', 'Pra', 'ver', 'feira', 'fruta', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_remove_puncts_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a remoção de pontuação
        quando receber uma entrada do tipo str
        """
        input_data = 'Fui a feira da fruta. Pra ver o que a feira da fruta tem.'

        output = self.resolver.resolve_remove_puncts(input_data)
        expected_output = [
            'Fui', 'a', 'feira', 'da', 'fruta', 'Pra', 'ver', 'o', 'que',
            'a', 'feira', 'da', 'fruta', 'tem'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_remove_puncts_with_list_input(self):
        """
        Verifica que o resolver processa adequadamente a remoção de pontuação
        quando receber uma entrada do tipo list
        """
        input_data = [
            'Fui a feira da fruta.',
            'Pra ver o que a feira da fruta tem.'
        ]

        output = self.resolver.resolve_remove_puncts(input_data)
        expected_output = [
            'Fui', 'a', 'feira', 'da', 'fruta', 'Pra', 'ver', 'o', 'que',
            'a', 'feira', 'da', 'fruta', 'tem'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_lemming_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a lematização
        quando receber uma entrada do tipo str
        """
        input_data = 'O rato roeu a roupa do rei de Roma.'

        output = self.resolver.resolve_lemming(input_data)
        expected_output = [
            'O', 'ratar', 'roer', 'o', 'roupar', 'do', 'rei', 'de', 'Roma', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_lemming_with_list_input(self):
        """
        Verifica que o resolver processa adequadamente a lematização
        quando receber uma entrada do tipo list
        """
        input_data = [
            'O rato roeu a',
            'roupa do rei de Roma.'
        ]

        output = self.resolver.resolve_lemming(input_data)
        expected_output = [
            'O', 'ratar', 'roer', 'o', 'roupar', 'do', 'rei', 'de', 'Roma', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_stemming_with_str_input(self):
        """
        Verifica que o resolver processa adequadamente a stemização
        quando receber uma entrada do tipo str
        """
        input_data = 'O rato roeu a roupa do rei de Roma.'

        output = self.resolver.resolve_lemming(input_data)
        expected_output = [
            'O', 'ratar', 'roer', 'o', 'roupar', 'do', 'rei', 'de', 'Roma', '.'
        ]

        self.assertEqual(len(output), len(expected_output))
        self.assertTrue(isinstance(output, list))
        self.assertEqual(output, expected_output)

    def test_resolve_negative_lexical_text_classify_with_str_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens negativas com
        input em forma de string.
        """
        # testarei 3 mensagens de texo, ainda julgo serem poucos exemplos
        text_1 = 'Fulano perdeu pontos!'
        text_2 = 'Não volto mais àquela loja. O atendimento é péssimo!'
        text_3 = 'A empresa possui péssima gestão. Além do mais os funcionários'\
                 ' não recebem a devida valorização que merecem.'

        output_text_1 = self.resolver.resolve_lexical_text_classifier(text_1)
        output_text_2 = self.resolver.resolve_lexical_text_classifier(text_2)
        output_text_3 = self.resolver.resolve_lexical_text_classifier(text_3)

        self.assertTrue(output_text_1 < 0)
        self.assertTrue(output_text_2 < 0)
        self.assertTrue(output_text_3 < 0)
        self.assertTrue(isinstance(output_text_1, float))

    def test_resolve_positive_lexical_text_classify_with_str_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens positivas com
        input em forma de string.
        """
        # testarei 3 mensagens de texo, ainda julgo serem poucos exemplos
        text_1 = 'Adorei seu perfume, é muito cheiroso!'
        text_2 = 'Obrigado pelo almoço, a comida estava deliciosa.'
        text_3 = 'Nota 10! Fui muito bem atendido e os preços são ótimos.'

        output_text_1 = self.resolver.resolve_lexical_text_classifier(text_1)
        output_text_2 = self.resolver.resolve_lexical_text_classifier(text_2)
        output_text_3 = self.resolver.resolve_lexical_text_classifier(text_3)

        self.assertTrue(output_text_1 > 0)
        self.assertTrue(output_text_2 > 0)
        self.assertTrue(output_text_3 > 0)
        self.assertTrue(isinstance(output_text_1, float))

    def test_resolve_neutral_lexical_text_classify_with_str_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens neutras com
        input em forma de string.
        """
        # testarei 3 mensagens de texo, ainda julgo serem poucos exemplos
        text_1 = 'O modelo do carro é um Fiat Uno!'
        text_2 = 'Fazemos entrega a domicilio através do aplicativo.'
        text_3 = 'Ontém fui ao teatro no centro da cidade.'

        output_text_1 = self.resolver.resolve_lexical_text_classifier(text_1)
        output_text_2 = self.resolver.resolve_lexical_text_classifier(text_2)
        output_text_3 = self.resolver.resolve_lexical_text_classifier(text_3)

        self.assertEqual(output_text_1, 0)
        self.assertEqual(output_text_2, 0)
        self.assertEqual(output_text_3, 0)
        self.assertTrue(isinstance(output_text_1, float))

    def test_resolve_negative_lexical_text_classify_with_list_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens negativas com
        input em forma de lista.
        """
        text_list = [
            'Você deveria cortar este cabelo, está riduculamente feio',
            'Com esse cabelo você não vai conseguir um emprego, parece um marginal'
        ]
        token_list = ['Eu', 'odeio', 'legumes', 'legumes', 'são', 'horríveis']

        output_1 = self.resolver.resolve_lexical_text_classifier(text_list)
        output_2 = self.resolver.resolve_lexical_text_classifier(token_list)

        self.assertTrue(output_1 < 0)
        self.assertTrue(output_2 < 0)
        self.assertTrue(isinstance(output_1, float))
        self.assertTrue(isinstance(output_2, float))

    def test_resolve_positive_lexical_text_classify_with_list_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens positivas com
        input em forma de lista.
        """
        text_list = [
            'O filme foi melhor do que eu esperava. Os efeitos especiais estavam bons,',
            'o roteiro estava coerente, a composição musica clássica deu toque divino.'
        ]
        token_list = ['Estes', 'doces', 'são', 'deliciosos']

        output_1 = self.resolver.resolve_lexical_text_classifier(text_list)
        output_2 = self.resolver.resolve_lexical_text_classifier(token_list)

        self.assertTrue(output_1 > 0)
        self.assertTrue(output_2 > 0)
        self.assertTrue(isinstance(output_1, float))
        self.assertTrue(isinstance(output_2, float))

    def test_resolve_neutral_lexical_text_classify_with_list_input(self):
        """
        Verifica que o algoritmo de classificação de texto retorna corretamente
        o valor para o sentimento do texto quando recebe mensagens neutras com
        input em forma de lista.
        """
        text_list = [
            'Quando pequeno eu assistia chaves.',
            ' Na hora do almoço dragon ball, digimon ou pokemon.'
        ]
        token_list = ['Sabia', 'que', 'o', 'sabiá', 'sabia', 'assobiar', '?']

        output_1 = self.resolver.resolve_lexical_text_classifier(text_list)
        output_2 = self.resolver.resolve_lexical_text_classifier(token_list)

        self.assertEqual(output_1, 0)
        self.assertEqual(output_2, 0)
        self.assertTrue(isinstance(output_1, float))
        self.assertTrue(isinstance(output_2, float))

    def test_resolve_offensive_words_from_string(self):
        """
        Verifica que o resolver de word_offense classifica corretamente palavras
        ofensivas contidas em uma string.
        """
        text = 'otário babaca estúpido'
        output = self.resolver.resolve_word_offense(text)

        self.assertEqual(output[0]['token'], 'otário')
        self.assertEqual(output[0]['is_offensive'], True)
        self.assertEqual(output[1]['token'], 'babaca')
        self.assertEqual(output[1]['is_offensive'], True)
        self.assertEqual(output[2]['token'], 'estúpido')
        self.assertEqual(output[2]['is_offensive'], True)

    def test_resolve_offensive_words_from_list(self):
        """
        Verifica que o resolver de word_offense classifica corretamente como
        ofensivas, palavras contidas em uma lista de palávras ou lista de
        sentenças.
        """
        token_list = ['corno', 'ridículo', 'escroto']
        text_list = ['feio porra cacete', 'ladrão vagabundo']

        token_output = self.resolver.resolve_word_offense(token_list)
        text_output = self.resolver.resolve_word_offense(text_list)

        # confere a saída do processamento de lista de tokens
        self.assertEqual(token_output[0]['token'], 'corno')
        self.assertEqual(token_output[0]['is_offensive'], True)
        self.assertEqual(token_output[1]['token'], 'ridículo')
        self.assertEqual(token_output[1]['is_offensive'], True)
        self.assertEqual(token_output[2]['token'], 'escroto')
        self.assertEqual(token_output[2]['is_offensive'], True)

        # confere a saída do processamento de lista de sentenças
        self.assertEqual(text_output[0]['token'], 'feio')
        self.assertEqual(text_output[0]['is_offensive'], True)
        self.assertEqual(text_output[1]['token'], 'porra')
        self.assertEqual(text_output[1]['is_offensive'], True)
        self.assertEqual(text_output[2]['token'], 'cacete')
        self.assertEqual(text_output[2]['is_offensive'], True)
        self.assertEqual(text_output[3]['token'], 'ladrão')
        self.assertEqual(text_output[3]['is_offensive'], True)
        self.assertEqual(text_output[4]['token'], 'vagabundo')
        self.assertEqual(text_output[4]['is_offensive'], True)

    def test_not_resolve_offensive_words_from_string(self):
        """
        Verifica que o resolver de word_offense classifica corretamente palavras
        não ofensivas contidas em uma string.
        """
        text = 'bonito borboleta macarrão'
        output = self.resolver.resolve_word_offense(text)

        self.assertEqual(output[0]['token'], 'bonito')
        self.assertEqual(output[0]['is_offensive'], False)
        self.assertEqual(output[1]['token'], 'borboleta')
        self.assertEqual(output[1]['is_offensive'], False)
        self.assertEqual(output[2]['token'], 'macarrão')
        self.assertEqual(output[2]['is_offensive'], False)

    def test_resolve_not_offensive_words_from_list(self):
        """
        Verifica que o resolver de word_offense classifica corretamente como
        não ofensivas, palavras contidas em uma lista de palávras ou lista de
        sentenças.
        """
        token_list = ['fofo', 'pastel', 'futebol']
        text_list = ['feira fruta doce', 'dama formosa']

        token_output = self.resolver.resolve_word_offense(token_list)
        text_output = self.resolver.resolve_word_offense(text_list)

        # confere a saída do processamento de lista de tokens
        self.assertEqual(token_output[0]['token'], 'fofo')
        self.assertEqual(token_output[0]['is_offensive'], False)
        self.assertEqual(token_output[1]['token'], 'pastel')
        self.assertEqual(token_output[1]['is_offensive'], False)
        self.assertEqual(token_output[2]['token'], 'futebol')
        self.assertEqual(token_output[2]['is_offensive'], False)

        # confere a saída do processamento de lista de sentenças
        self.assertEqual(text_output[0]['token'], 'feira')
        self.assertEqual(text_output[0]['is_offensive'], False)
        self.assertEqual(text_output[1]['token'], 'fruta')
        self.assertEqual(text_output[1]['is_offensive'], False)
        self.assertEqual(text_output[2]['token'], 'doce')
        self.assertEqual(text_output[2]['is_offensive'], False)
        self.assertEqual(text_output[3]['token'], 'dama')
        self.assertEqual(text_output[3]['is_offensive'], False)
        self.assertEqual(text_output[4]['token'], 'formosa')
        self.assertEqual(text_output[4]['is_offensive'], False)
