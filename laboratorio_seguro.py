"""Demonstração local de criptografia e captura de texto consentida.

Todos os arquivos criptografados são gerados em ./laboratorio/dados_demo.
O registro de teclas observa somente o campo de texto desta janela.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cryptography.fernet import Fernet, InvalidToken

ROOT = Path(__file__).resolve().parent
LAB = ROOT / "laboratorio"
DATA = LAB / "dados_demo"
LOGS = LAB / "logs"
KEY = LAB / "chave_demo.key"
ALLOWED = {"anotacoes.txt", "clientes_ficticios.csv", "relatorio.txt"}


def preparar() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    exemplos = {
        "anotacoes.txt": "Anotação fictícia para demonstração.\n",
        "clientes_ficticios.csv": "nome,email\nExemplo,exemplo@invalid.test\n",
        "relatorio.txt": "Relatório de teste sem dados reais.\n",
    }
    for nome, conteudo in exemplos.items():
        caminho = DATA / nome
        if not caminho.exists() and not (DATA / (nome + ".enc")).exists():
            caminho.write_text(conteudo, encoding="utf-8")
    (LAB / "AVISO_SIMULACAO.txt").write_text(
        "SIMULAÇÃO EDUCACIONAL: arquivos fictícios protegidos pelo laboratório.\n"
        "Use o botão Restaurar para recuperar os exemplos.\n", encoding="utf-8")


def hash_arquivo(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def criptografar() -> str:
    if not KEY.exists():
        KEY.write_bytes(Fernet.generate_key())
    cipher = Fernet(KEY.read_bytes())
    total = 0
    for nome in sorted(ALLOWED):
        source = DATA / nome
        if source.exists():
            (DATA / (nome + ".enc")).write_bytes(cipher.encrypt(source.read_bytes()))
            source.unlink()
            total += 1
    return f"{total} arquivo(s) fictício(s) criptografado(s) na pasta do laboratório."


def restaurar() -> str:
    if not KEY.exists():
        return "Chave de demonstração não encontrada. Execute a simulação primeiro."
    cipher = Fernet(KEY.read_bytes())
    total = 0
    for nome in sorted(ALLOWED):
        encrypted = DATA / (nome + ".enc")
        if encrypted.exists():
            try:
                content = cipher.decrypt(encrypted.read_bytes())
            except InvalidToken:
                return "A chave não corresponde; os arquivos foram preservados."
            (DATA / nome).write_bytes(content)
            encrypted.unlink()
            total += 1
    return f"{total} arquivo(s) fictício(s) restaurado(s)."


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Laboratório educativo: ransomware + keylogger simulado")
        root.geometry("720x560")
        tk.Label(root, text="Demonstração segura", font=("Segoe UI", 16, "bold")).pack(pady=(14, 4))
        tk.Label(root, text="Criptografia limitada aos exemplos; captura somente neste campo visível.",
                 wraplength=660).pack(pady=(0, 10))
        buttons = tk.Frame(root)
        buttons.pack(pady=6)
        tk.Button(buttons, text="Preparar exemplos", command=self.preparar).pack(side="left", padx=5)
        tk.Button(buttons, text="Simular criptografia", command=self.criptografar).pack(side="left", padx=5)
        tk.Button(buttons, text="Restaurar arquivos", command=self.restaurar).pack(side="left", padx=5)
        tk.Label(root, text="Digite texto fictício aqui para observar o registro consentido:").pack(anchor="w", padx=24, pady=(12, 3))
        self.input = scrolledtext.ScrolledText(root, height=8, wrap="word")
        self.input.pack(fill="x", padx=24)
        self.input.bind("<KeyPress>", self.on_key)
        self.active = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Registrar teclas deste campo", variable=self.active).pack(anchor="w", padx=24, pady=6)
        tk.Label(root, text="Eventos registrados nesta sessão:").pack(anchor="w", padx=24)
        self.logview = scrolledtext.ScrolledText(root, height=9, state="disabled", wrap="word")
        self.logview.pack(fill="both", expand=True, padx=24, pady=(3, 12))
        preparar()

    def preparar(self) -> None:
        preparar()
        messagebox.showinfo("Laboratório", f"Exemplos prontos em:\n{DATA}")

    def criptografar(self) -> None:
        messagebox.showinfo("Simulação", criptografar())

    def restaurar(self) -> None:
        messagebox.showinfo("Restauração", restaurar())

    def on_key(self, event: tk.Event) -> None:
        if not self.active.get():
            return
        key = event.keysym if event.char in ("", "\r", "\n", "\t") else event.char
        entry = {"hora": datetime.now().isoformat(timespec="seconds"), "tecla": key}
        with (LOGS / "eventos_digitacao.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self.logview.configure(state="normal")
        self.logview.insert("end", f"{entry['hora']}  {key!r}\n")
        self.logview.see("end")
        self.logview.configure(state="disabled")


if __name__ == "__main__":
    preparar()
    App(tk.Tk()).root.mainloop()
