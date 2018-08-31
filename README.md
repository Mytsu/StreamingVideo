# Projeto de Streaming de Vídeo

[![CircleCI](https://circleci.com/gh/Mytsu/StreamingVideo/tree/master.svg?style=svg)](https://circleci.com/gh/Mytsu/StreamingVideo/tree/master) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg?style=flat-square)


Implementação de um aplicativo que transfere arquivos através de um protocolo modificado baseado em UDP, para streaming de vídeos.

## Protocolos Utilizados para transferencia

- 0 - GET -> `00000000`
- 1 - PAUSE -> `00000001`
- 2 - SEEK -> `00000010`
- 3 - BACK -> `00000011`
- 4 - TRANS -> `00000100`
- 5 - ACK -> `00000101`
- 6 - PLAY -> `00000110`

Package:

- ID = 3 bytes
- Type = 1 byte
- Dados = PACKAGE_SIZE

Numeração de 0-99 dos pacotes, sendo 0-49 da janela1 e 50-99 da janela2, a cada janela recebida completa escrita no buffer de saída e um ACK enviado pro servidor.

Função do servidor:

- Ler arquivo;
- Enviar video;
- Retransmitir caso _timeout_;
- Controle de fluxo (Janela deslizante);
- Pause;
- Seek e Back;
- Canal TCP para comandos de transferência e UDP para transmissão de vídeo;

Função do cliente:

- Pedir arquivo;
- Executar mpv;
- Enviar ACKs dos pacotes recebidos;
- Pause;
- Seek e Back por comando do teclado;
- Controle de janela;
