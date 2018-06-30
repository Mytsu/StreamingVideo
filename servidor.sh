if ! [ -x "$(command -v mediainfo)" ]; then
  echo 'Erro: mediainfo nao esta instalado.' >&2
  echo 'Instale mediainfo e tente novamente. :)' >&2
  exit 1
fi

python3 servidor/Servidor.py 
