# Recuperação de Backup
Este código tem como objetivo realizar a recuperação de backup dos bancos de dados. Ele foi desenvolvido por Lux Andrew, em 28/04/2023 e está sob a licença MIT.

O arquivo principal é o main.py. Ao executá-lo, ele verifica se o arquivo _xampp_path_config.txt existe na pasta atual e, caso não exista, solicita ao usuário que informe o caminho da pasta xampp. Se o arquivo não estiver dentro da pasta xampp, o usuário é questionado se deseja mover o arquivo para a pasta correta. Caso contrário, a função retorna o caminho padrão do xampp.

Em seguida, o programa verifica se a pasta data existe. Se ela existir, ele verifica se a pasta backup existe. Se a pasta backup existir, ele inicia a rotina de restauração.

A rotina de restauração consiste em renomear a pasta data para data_old, criar um arquivo zip da pasta data_old, criar uma nova pasta data, copiar as pastas do backup para a pasta data, copiar os bancos de dados da pasta data_old para a pasta data, copiar o arquivo ibdata1 e todos os arquivos de log, e excluir a pasta data_old.

Se a pasta backup não existir ou a pasta data não existir, o programa exibe uma mensagem de erro e encerra.

Por fim, se o arquivo _xampp_path_config.txt foi movido para a pasta correta, o programa o exclui.

# Como usar
Para utilizar o programa, basta executar o arquivo main.py e seguir as instruções apresentadas no console.

# Requisitos
Este programa foi desenvolvido em Python 3. É necessário ter o Python 3 instalado na máquina para executar o código.
