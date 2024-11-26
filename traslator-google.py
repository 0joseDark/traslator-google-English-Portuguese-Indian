import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Combobox
from googletrans import Translator

# Dicionário de idiomas suportados
IDIOMAS = {
    "Inglês": "en",
    "Português Europeu": "pt",
    "Indiano": "hi"
}

# Função principal para traduzir os arquivos de texto
def traduzir_arquivos():
    pasta_entrada = pasta_entrada_var.get()
    pasta_saida = pasta_saida_var.get()
    idioma_origem = IDIOMAS[primeira_lingua_var.get()]
    idioma_destino = IDIOMAS[segunda_lingua_var.get()]

    if not pasta_entrada or not pasta_saida:
        messagebox.showerror("Erro", "Selecione as pastas de entrada e saída!")
        return
    if idioma_origem == idioma_destino:
        messagebox.showerror("Erro", "Escolha línguas diferentes para tradução!")
        return

    arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith(".txt")]
    if not arquivos:
        messagebox.showinfo("Informação", "Nenhum arquivo .txt encontrado na pasta de entrada.")
        return

    total_arquivos = len(arquivos)
    progresso["value"] = 0
    janela.update_idletasks()

    tradutor = Translator()

    for i, arquivo in enumerate(arquivos, start=1):
        caminho_entrada = os.path.join(pasta_entrada, arquivo)
        try:
            with open(caminho_entrada, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Traduzindo o conteúdo
            traducao = tradutor.translate(conteudo, src=idioma_origem, dest=idioma_destino).text

            # Salvando o arquivo traduzido na pasta de saída
            novo_nome = os.path.splitext(arquivo)[0] + "_traduzido.txt"
            caminho_saida = os.path.join(pasta_saida, novo_nome)
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(traducao)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao traduzir {arquivo}: {e}")

        # Atualizando a barra de progresso
        progresso["value"] = (i / total_arquivos) * 100
        janela.update_idletasks()

    messagebox.showinfo("Concluído", "Tradução concluída!")

# Função para escolher a pasta de entrada
def escolher_pasta_entrada():
    pasta = filedialog.askdirectory(title="Escolha a pasta de entrada")
    if pasta:
        pasta_entrada_var.set(pasta)

# Função para escolher a pasta de saída
def escolher_pasta_saida():
    pasta = filedialog.askdirectory(title="Escolha a pasta de saída")
    if pasta:
        pasta_saida_var.set(pasta)

# Criando a janela principal
janela = tk.Tk()
janela.title("Tradutor de Textos")
janela.geometry("500x400")
janela.resizable(False, False)

# Variáveis para armazenar os caminhos das pastas e as línguas
pasta_entrada_var = tk.StringVar()
pasta_saida_var = tk.StringVar()
primeira_lingua_var = tk.StringVar(value="Português Europeu")
segunda_lingua_var = tk.StringVar(value="Inglês")

# Interface da aplicação
tk.Label(janela, text="Tradutor de Textos", font=("Arial", 16)).pack(pady=10)
tk.Label(janela, text="Escolha as pastas de entrada e saída:").pack(pady=5)

# Entrada e botão para escolher a pasta de entrada
frame_entrada = tk.Frame(janela)
frame_entrada.pack(pady=5)
entrada_entrada = tk.Entry(frame_entrada, textvariable=pasta_entrada_var, width=40, state="readonly")
entrada_entrada.pack(side="left", padx=5)
botao_entrada = tk.Button(frame_entrada, text="Pasta de Entrada", command=escolher_pasta_entrada)
botao_entrada.pack(side="left", padx=5)

# Entrada e botão para escolher a pasta de saída
frame_saida = tk.Frame(janela)
frame_saida.pack(pady=5)
entrada_saida = tk.Entry(frame_saida, textvariable=pasta_saida_var, width=40, state="readonly")
entrada_saida.pack(side="left", padx=5)
botao_saida = tk.Button(frame_saida, text="Pasta de Saída", command=escolher_pasta_saida)
botao_saida.pack(side="left", padx=5)

# Seleção de línguas
tk.Label(janela, text="Selecione a Primeira Língua (Origem):").pack(pady=5)
combo_primeira_lingua = Combobox(janela, values=list(IDIOMAS.keys()), textvariable=primeira_lingua_var, state="readonly")
combo_primeira_lingua.pack(pady=5)

tk.Label(janela, text="Selecione a Segunda Língua (Destino):").pack(pady=5)
combo_segunda_lingua = Combobox(janela, values=list(IDIOMAS.keys()), textvariable=segunda_lingua_var, state="readonly")
combo_segunda_lingua.pack(pady=5)

# Barra de progresso
progresso = Progressbar(janela, orient="horizontal", length=400, mode="determinate")
progresso.pack(pady=20)

# Botão para iniciar a tradução
botao_traduzir = tk.Button(janela, text="Traduzir", command=traduzir_arquivos)
botao_traduzir.pack(pady=10)

# Botão para sair
botao_sair = tk.Button(janela, text="Sair", command=janela.destroy)
botao_sair.pack(pady=5)

# Rodar a aplicação
janela.mainloop()