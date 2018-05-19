# Documentação de projeto

Definições de projeto e do protocolo de streaming

## Cliente
1.	Requerimento do arquivo: 

	-	cliente - `Get <nomedoarquivo.video>`

	-	servidor - `head <resolucaodovideo> <tamanhodovideo>`

	-	cliente - `<ok/erro> <tamanhodivisao>`

	Inicio da transferencia

2.	Transferencia do arquivo:

	-	Armazenar o buffer do cliente no HD

	-	Leitura do MPV diretamento do HD
 
3.	Servidor

	-	Espera requisicao:
	
		Definir pool de threads para espera da requisicao

	-	Aceitar requisicao:

		Resposta do pedido.

		Divisao do arquivo.

		Inicio da transferencia.

	-	Transferencia:

		CheckSum da divisao

		Numero de serie da divisao e das datagramas

		Envio da divisao e esperar time para envio da próxima divisao

	-	CheckSum incorreto:

		Reenvio da divisao

	-	Datagrama não recebido(NACK)

		reenvio do datagrama
