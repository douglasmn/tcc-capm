### TCC - Uma Análise Estatística da Bolsa de Valores

##### Trabalho de Conclusão de Curso de Ciência da Computação - UNICARIOCA

#### OBJETIVO PRINCIPAL

Este trabalho visa a sistematização do modelo matemátcio chamado CAPM que é utilizado para o cálculo da estimativa do retorno de um investimento em ações e uma sistematização do cálculo do Beta que representa o risco de uma determinada ação.
Para tanto foi utilizado o arquivo da série histórica da BOVESPA e utlizada a liguagem Python para a elabotração do algoritmo.

Pela pouca eficiência em trabalhar com leitura de arquivo, para o algorimto processar os dados, foi elaborado um algoritmo auxiliar **(tcc-importa-acoes-ibov.py)** para popular um banco de dados relacional em PostgreSQL que através do arquivo da série histórica do BOVESPA o algoritmo fez a inserção dos valores necessários no banco de dados. 

O algoritmo principal **(tcc-calcula-capm.py)** tem uma função chamada *calcula_capm(arg1, arg2, arg3, arg4)* com os quatro seguintes argumentos:
  - arg1 - destinado a informar o código da ação de operação na bolsa de valores a ser analisada. ex: (PETR4, ABEV3, BBAS3)
  - arg2 - destinado a informar a data inicial do período a ser analisado. A data deve estar no formato AAAA-MM-DD. ex: (2019-01-01)
  - arg3 - destinado a informar a data final do período a ser analisado. A data deve estar no formato AAAA-MM-DD. ex: (2019-01-31)
  - arg4 - destinado a informar o tipo de gráfico desejado na saída do algoritmo. Os valores aceitos são '1' e '2'. 1 para gerar o gráfico do retorno do Ibovespa x Ação analisada; 2 para gerar o gráfico do Beta da ação

Por questão do arquivo da serie histórica anual das ações listadas na BOVESPA term mais de 25Mb, o limite permitido pelo guithub, não foi possível o carregamento do mesmo. Porém o arquivo da série histórica pode ser facilmente encontrado através do link http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/ .

Já os índices históricos do IBOVESPA, no arquivo aqui disponibilizado, foi uma trabalho manual de copiar em tela os dados informados para um arquivo .TXT pois não foi encontrado no site da BOVESPA um opção de download de um arquivo contendo tais informações. O link http://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-estatisticas-historicas.htm disponibiliza a visualização em tela dos índices Ibovespa.

Para facilitar a utilização do algoritmo, está disponibilizado o arquivo de replicação do banco de dados **(bovespa-tcc.sql)** bastando sua importação num banco de dados PostgreSQL e a configuração das credenciais e endereço do banco de dados no algoritmo principal **(tcc-calcula-capm.py)** no campo destinado a esses dados conforme linha abaixo: <br><br>
*connection = psycopg2.connect(user = "usuário", password = "senha",host = "IP do banco de dados",port = "5432",database = "bovespa")*
