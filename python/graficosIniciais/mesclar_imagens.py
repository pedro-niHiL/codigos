import os
from PIL import Image
import argparse

def main():
    parser = argparse.ArgumentParser(description='Mesclar imagens de duas pastas lado a lado')
    parser.add_argument('pasta1', help='Primeira pasta com imagens')
    parser.add_argument('pasta2', help='Segunda pasta com imagens')
    parser.add_argument('saida', help='Pasta de saída para imagens mescladas')
    args = parser.parse_args()

    # Criar pasta de saída se não existir
    os.makedirs(args.saida, exist_ok=True)

    # Mapear arquivos pelas bases dos nomes
    def mapear_bases(pasta):
        bases = {}
        for arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho):
                base = os.path.splitext(arquivo)[0]
                if base in bases:
                    print(f'Aviso: Nome duplicado "{base}" em {pasta}, usando último arquivo')
                bases[base] = caminho
        return bases

    bases1 = mapear_bases(args.pasta1)
    bases2 = mapear_bases(args.pasta2)

    # Encontrar bases comuns
    bases_comuns = set(bases1.keys()) & set(bases2.keys())
    print(f'Encontradas {len(bases_comuns)} imagens para mesclar')

    for base in bases_comuns:
        try:
            # Abrir imagens
            img1 = Image.open(bases1[base])
            img2 = Image.open(bases2[base])

            # Determinar modo de cor
            modo1 = img1.mode
            modo2 = img2.mode
            novo_modo = 'RGBA' if 'A' in modo1 or 'A' in modo2 else 'RGB'

            # Converter imagens
            img1 = img1.convert(novo_modo)
            img2 = img2.convert(novo_modo)

            # Calcular dimensões
            largura1, altura1 = img1.size
            largura2, altura2 = img2.size
            largura_total = largura1 + largura2
            altura_max = max(altura1, altura2)

            # Criar nova imagem
            nova_imagem = Image.new(novo_modo, (largura_total, altura_max))
            nova_imagem.paste(img1, (0, 0))
            nova_imagem.paste(img2, (largura1, 0))

            # Salvar como PNG
            caminho_saida = os.path.join(args.saida, f'{base}.png')
            nova_imagem.save(caminho_saida)
            print(f'Mesclado: {base} → {caminho_saida}')

        except Exception as e:
            print(f'Erro ao processar {base}: {str(e)}')

if __name__ == '__main__':
    main()