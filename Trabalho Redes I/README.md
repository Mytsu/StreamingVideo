
# Video Streaming App

    Instituto Federal de Minas Gerais - Campus Formiga
    06/05/2018
    José Luiz
    Jonathan Arantes
    Vinícius Araújo

Este aplicativo de streaming de vídeo provê um controle de transmissão de dados de modo a não desperdiçar a rede (banda larga, wifi, 4g, etc) do usuário ao transmitir um arquivo de vídeo, enquanto mantém a bufferização do arquivo ao player de vídeo.

Até este ponto do projeto, os usos dos datagramas _UDP_ são para transferência de mensagens entre Cliente e Servidor para comunicar a lista de arquivos de vídeo que podem ser transmitidos e o _stream_ de dados partindo do servidor para o cliente.

Segue abaixo a descrição das funções implementadas, separadas por arquivo:

## Servidor

- Inicialização `__init__`:

    Inicialização do objeto Servidor;

  - `self.diretorio`: Diretório da pasta _streamer_, onde ficam localizados os arquivos de vídeo a serem transmitidos;

  - `self.poolThreads`: _Pool_ de _threads_ para processamento simultâneo das funções;

  - `self.udp`: _Socket UDP_ utilizado na trasmissão de dados;

  - `HOST` e `PORT`: Endereço IP e porto de acesso do servidor;

  - `self.arquivolog`: Arquivo para registro de _log_;

  - `self.conteudo`: Conteudo anterior do arquivo de _log_;

  - `orig`: Endereço de origem do servidor (IP:Porto);

  - `self.diretorio_arquivos`: Diretorio dos arquivos para transmissão;

- `build_thread_control(self)`: Função para travamento (_lock_) da _thread_ e execução desta;

- `build_threads(self)`: Cria a _pool_ de _threads_ do servidor;

- `wait(self)`: Espera a requisição de um cliente, um loop infinito que continua a receber pacotes do _socket_ e aceita a requisição (se houver) do cliente;

- `accept(self, msg, cliente)`: Envia a requisição para uma das _threads_ em espera na _pool_, em seguida retorna para a função `wait(self)`;

- `checkmsg(self, msg)`: Trata a mensagem recebida pelo _socket_ para o padrão de `cabecario` (_header_) e `dados` (_data_);

# Cliente

- Inicialização `__init__`:

    Inicialização do objeto Cliente;

  - `self.udp`: _Socket UDP_ do cliente para recebimento dos dados;

  - `self.meuip`: IP do cliente;

  - `orig`: IP:Porto da aplicação do cliente (porto é definido como 0 para ser decidido pela função `self.udp.bind`);

  - `self.udp.bind`: Aloca um porto à aplicação cliente para recebimento de dados;

  - `self.meuporto`: Porto de acesso da aplicação para a rede;

  - `self.servidor`: IP:Porto do servidor que irá transmitir os dados;

  - `self.controle`: Objeto `ControleEnvio()`;

  - `self.udp.settimeout(10)`: Configura o tempo de _timeout_ da transmissão _UDP_;

  - `self.buffer`: Vetor de _buffer_ do cliente;

  - `self.arquivo`: Arquivo que será gravado em disco;

  - `self.pacotes_recebidos`: Vetor de buffer do _socket_;

  - `self.num_pacotes`: Número de pacotes recebidos;

  - `self.video`: Objeto `Video()`;

- `requisita_servidor(self)`: Envia requisição para o servidor iniciar a comunicação, inicia o objeto `Video()` e entra em loop para receber as mensagens do servidor;

- `recebermsg(self)`: Recebe o pacote do _socket_ e passa esta para o padrão `mensagem` e `srvenvio`;

- `desmonta_pacote(self, msg)`: Passa o pacote para o padrão _header_:_data_;

- `checkmsg(self, msg, srvenvio)`: Executa `desmonta_pacote(self, msg)` e converte os bytes para leitura;

- `tratamento(self, msg, srv)`:

- `worker()`: Chama a execução do tocador de vídeo MPV;

# ControleEnvio

- Inicialização `__init__`:

    Inicialização do objeto ControleEnvio;

  - `self.buffersize`: Tamanho do buffer (8mb);

  - `self.windowsize`: Tamanho da janela (ainda não definida, testes são necessários);

  - `self.unidadecontrole`: Objeto `UnidadeControle()` recebida via parâmetro;

- `sendmsg(self, msg, cliente, udp, tipomsg, usounidadecontrole=False, seq_inicial = 0)`: Realiza a formatação da mensagem para ser enviada;

- `fragmenta(self, msg)`: Fragmenta a mensagem se esta for maior que o tamanho máximo para empacotamento (1016kb) e retorna uma lista com os fragmentos ordenados da mensagem;

- `adiciona_cabecalho(self, msg, numero_sequencia, tipomsg)`: Empacota a mensagem para envio, indexando o _header_ do pacote no início da mensagem;

# Pacote

- Inicialização `__init__`:

    Inicialização do objeto Pacote;

  - `self.dados`: Dados armazenados;

  - `self.time`: _Timeout_ do pacote;

  - `self.numseq`: Número de sequência (para controle em caso de fragmentação);

# Transferencia

- Inicialização `__init__`:

    Inicialização do objeto Transferencia;

  - `Thread.__init__(self)`: Inicia uma thread para executar este objeto;

  - `self.dest`: Endereço de destino dos dados;

  - `self.arquivo`: Arquivo de vídeo a ser lido;

  - `self.unidadecontrole`: Objeto `UnidadeControle()` recebido por parâmetro;

  - `self.controle`: Objeto `ControleEnvio()` que recebe o objeto `UnidadeControle()`;

  - `self.caixadeaviso`: 

  - `self.lock`: Trava de _threads_;

- `run(self)`: Função de execução da _thread_;

- `leitura_arquivo(self)`: Realiza a leitura de _bytes_ no arquivo, lendo a quantidade de _bytes_ do tamanho do _buffer_;

- `fechar_arquivo(self)`: Fecha o arquivo;

- `checkavisos(self)`: Checa as mensagens da unidade de controle;

# UnidadeControle

- Inicialização `__init__`:

    Enumeração com a ordem:

        1: PACOTE,
        2: ACK,
        3: TIME;

    Inicialização do objeto UnidadeControle;

  - `self.listaClientes`: Lista de clientes conectados ao servidor;

  - `self.threadsusadas`: Lista de _threads_ em uso;

  - `self.lock`: Trava das _threads_;

  - `self.listaPortos`: Lista de portos utilizados para comunicação com os clientes;

  - `self.udp`: _Socket_ de comunicação da unidade de controle;

  - `self.udp.settimeout(1)`: Configura o tempo de _timeout_ para 1ms;

- `run(self)`:

- `add_buffer(self, cliente, threferente)`: Buffer do controle de envio;

- `add_pacote(self, cliente, pacote, numseq, valor`: Adiciona um pacote ao buffer de envio;

- `add_porto(self, udp)`: Adiciona o porto à lista para recebimento dos _ACKs_ da transferência;

- `remover_cliente(self, cliente, udp)`: Termina a comunicação com o cliente, removendo-o da lista de clientes, das _threads_ utilizadas e da lista de portos;

- `avisar_thread(self, th, aviso)`: Manda um aviso para a _thread_ de se ela pode terminar a execução, se ela deve reenviar algum arquivo, ou se ela pode continuar executando;

- `tratamsg(self, msg, cliente)`: Desmonta o pacote e verifica o _ACK_ recebido;

- `desmonta_pacote(self, msg)`: Desmonta o pacote para o padrão _header_:_data_;

- `verifica_timeout_pacote(self)`: Verifica se o pacote chegou ao seu _timeout_, se o _timeout_ do pacote chegou a 0, reenvia o pacote e reseta o _timeout_;

- `verifica_liberacao_thread(self, cliente)`: Envia um aviso à thread para parar a execução;