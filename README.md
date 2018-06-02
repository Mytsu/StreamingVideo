# Projeto de Streaming de Vídeo

Implementação de um aplicativo que transfere arquivos através de um protocolo modificado baseado em UDP, para streaming de vídeos.
# Protocolos Utilizados para transferencia
    • 0 – Transferencia de texto (usado para transferencia da lista de arquivos no diretorio de streamer)
    • 1 – Inicio da transferencia de arquivos (usado para se criar o arquivo do outro lado da rede)
    • 2 – Transferencia do arquivo em andamento
    • 3 – encerramento da transferencia (nos dados vem encerramento lista)
    • 4 -  ACK e indice 
