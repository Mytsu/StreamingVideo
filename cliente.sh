#!/bin/sh

if ! [ -e "$1" ]; then
  ajuda
  exit 1
fi

while :
do
    case "$1" in
        -i | --ipServidor)
            ipServidor = $1
            shift 2
            ;;
        -p | --portoServidor)
            portoServidor = $1
            shift 2
            ;;
        -m | --ipCliente)
            ipcliente = $1
            shift 2
            ;;
        -h | --help)
            ajuda
            exit 0
            ;;
        --)
            shift
            break
            ;;
        -*)          
            exit 1 
            ;;
        *)
            break
            ;;
    esac
done

ajuda() {
    echo "Uso: $0 -i [ip_servidor] -p [porto_servidor] -m [ip_cliente] {nome_arquivo}" >&2
    echo
    echo "   -i, --ipServidor        ->   IP do servidor"
    echo "   -p, --portoServidor     ->   Porto do servidor "
    echo "   -m, --ipCliente         ->   IP deste computador"
    echo "   -h, --help              ->   Menu de ajuda"
    echo
    exit 1
}

python3 cliente/Cliente.py -i $ipServidor -p $portoServidor -m $ipCliente $arquivo
