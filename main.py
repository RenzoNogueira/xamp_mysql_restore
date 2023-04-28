"""
    Este código tem como objetivo realizar a recuperação de backup dos bancos de dados.
    Desenvolvido por Lux Andrew, em 28/04/2023.
    Licença: MIT
    Versão: 1.0.0
"""

import sys
import os
import tkinter as tk
import shutil
import zipfile

# Nome do arquivo que contém o caminho da pasta xampp
nameFilePath = "_xampp_path_config.txt"
# Pasta atual do arquivo
thisFolder = os.path.dirname(os.path.abspath(__file__))

tasksRotina = 0
tasksConfig = 0
deleteFile = False

# Mostrar alerta
def showalert(title, message):
    root = tk.Tk()
    root.title(title)
    root.geometry('300x100')
    root.resizable(False, False)
    label = tk.Label(root, text=message)
    label.pack()
    root.mainloop()

"""
A função set_xampp_path verifica se o arquivo _xampp_path_config.txt existe na pasta atual e, caso não exista, solicita ao usuário que informe o caminho da pasta xampp.
Se o arquivo não estiver dentro da pasta xampp, o usuário é questionado se deseja mover o arquivo para a pasta correta.
Caso contrário, a função retorna o caminho padrão do xampp. A função retorna o caminho da pasta xampp.
"""
def set_xampp_path():
    global tasksConfig
    global deleteFile

    xampp_path = 'C:\\xampp\\'  # Caminho padrão do xampp
    # Veridica se o arquivo nameFilePath existe
    if not os.path.exists(nameFilePath):
        # Verifica se o arquivo está dentro da pasta xampp
        if not os.path.abspath(__file__).lower().startswith(xampp_path.lower()):
            print('Pasta xampp não encontrada.')
            tasksConfig += 1
            while True:
                response = input('(config) ' + str(tasksConfig) + ': Digite o caminho da pasta xampp: ')
                if os.path.exists(response):
                    print('Caminho válido: ' + response)
                    tasksConfig += 1
                    move_file = input('(config) ' + str(tasksConfig) + ': Deseja mover o arquivo para a pasta correta? (S/N): ')
                    break
                else:
                    print('Caminho inválido.')
            if move_file.upper() == 'S':
                # Copia o arquivo para a pasta correta
                while True:
                    try:
                        shutil.copy(os.path.abspath(__file__), xampp_path)
                        if os.path.exists(xampp_path + '\\' + os.path.basename(__file__)):
                            tasksConfig += 1
                            print('(config) ' + str(tasksConfig) + ': Arquivo movido para a pasta ' + xampp_path)
                            deleteFile = True
                        break
                    except:
                        move_file = input(
                            'Não foi possível mover o arquivo para a pasta correta. Deseja mover o arquivo manualmente? (S/N): ')
                        if move_file.upper() == 'S':
                            break

                return response
            else:
                # Cria um arquivo txt com o caminho da pasta xampp
                with open(nameFilePath, 'w') as file:
                    file.write(response)
                if os.path.exists(nameFilePath):
                    print('Arquivo xampp_path.txt criado.')
                    return response
        else:
            print('ok: pasta xampp encontrada.')
            return xampp_path
    else:
        # Retorna o caminho da pasta xampp
        with open(nameFilePath, 'r') as file:
            xampp_path = file.read()
        if os.path.exists(xampp_path):
            print('Caminho válido: ' + xampp_path)
            return xampp_path


def main():
    global tasksRotina
    global tasksConfig

    # Verifica se o arquivo está na pasta correta e salva se o arquivo deve ser movido para a pasta correta
    xampp_path = set_xampp_path()

    # Verifica se a pasta data existe
    if xampp_path != False:
        if os.path.exists(xampp_path + '\\mysql\\data'):
            print('ok: pasta data existe')
            # Verifica se a pasta backup existe
            if os.path.exists(xampp_path + '\\mysql\\backup'):
                print('INICIANDO A ROTINA DE RESTAURAÇÃO')
                # Renomeia a pasta data para daya_old
                os.rename(xampp_path + '\\mysql\\data',
                          xampp_path + '\\mysql\\data_old')
                tasksRotina += 1
                print(str(tasksRotina) + ': Pasta data renomeada para data_old')

                # Cria arquivo zip da pasta data_old
                zip = zipfile.ZipFile(
                    xampp_path + '\\mysql\\data_old.zip', 'w')
                for pasta, subpastas, arquivos in os.walk(xampp_path + '\\mysql\\data_old'):
                    for arquivo in arquivos:
                        zip.write(os.path.join(pasta, arquivo),
                                  os.path.relpath(os.path.join(
                                      pasta, arquivo), xampp_path + '\\mysql\\data_old'),
                                  compress_type=zipfile.ZIP_DEFLATED)
                zip.close()
                tasksRotina += 1
                print(str(tasksRotina) + ': Arquivo zip da pasta data_old criado')

                # Cria nova pasta data
                tasksRotina += 1
                os.mkdir(xampp_path + '\\mysql\\data')
                print(str(tasksRotina) + ': Pasta data criada')
                # Copia as pastas do backup para a pasta data
                pastas = ['mysql', 'performance_schema', 'phpmyadmin', 'test']
                for pasta in pastas:
                    shutil.copytree(xampp_path + '\\mysql\\backup\\' +
                                    pasta, xampp_path + '\\mysql\\data\\' + pasta)
                tasksRotina += 1
                print(str(tasksRotina) + ': Pastas copiadas para a nova pasta data')

                # Copia os bancos de dados da pasta data_old para a pasta data
                # Verificar se a pasta nao é padrão
                for pasta in os.listdir(xampp_path + '\\mysql\\data_old'):
                    if pasta not in pastas:
                        # Verificar se é uma pasta
                        if os.path.isdir(xampp_path + '\\mysql\\data_old\\' + pasta):
                            shutil.copytree(
                                xampp_path + '\\mysql\\data_old\\' + pasta, xampp_path + '\\mysql\\data\\' + pasta)
                tasksRotina += 1
                print(str(tasksRotina) +
                      ': Bancos copiados da pasta data_old para a pasta data')

                # Copia o arquivo ibdata1 e todos os arquivos de log
                shutil.copy(xampp_path + '\\mysql\\data_old\\ibdata1',
                            xampp_path + '\\mysql\\data\\ibdata1')
                tasksRotina += 1
                print(str(
                    tasksRotina) + ': Arquivo ibdata1 copiado da pasta data_old para a pasta data')

                # Exclui a pasta data_old
                shutil.rmtree(xampp_path + '\\mysql\\data_old')
                tasksRotina += 1
                print(str(tasksRotina) + ': Pasta data_old excluida')
            else:
                print('Pasta backup não existe')
                showalert('Erro', 'Pasta backup não existe')
        else:
            print('error: pasta data não existe')
            showalert('Erro', 'Pasta data não existe')
    else:
        print('error: pasta xampp não existe')
        showalert('Erro', 'Pasta xampp não existe')

    # Apaga o arquivo se ele foi movido para a pasta correta
    if deleteFile:
        tasksConfig += 1
        os.remove(os.path.abspath(__file__))
        print('(config) ' + str(tasksConfig) + ': O arquivo foi excluido. Busque pelo arquivo na pasta ' + xampp_path)


if __name__ == '__main__':
    # Limpa o console
    os.system('cls')
    print('Desenvolvido por: Lux Andrew')
    print('github.com/RenzoNogueira')
    main()
