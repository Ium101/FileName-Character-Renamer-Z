# Filename Character Renamer Z

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

---

<div align="center">
<img width="1152" height="735" alt="image" src="https://github.com/user-attachments/assets/25188300-73b5-40c3-84b5-f7ac8c01df50" />

---

## 📖 Language | Idioma

- [English](#english)
- [Português (Brasil)](#português-brasil)

---

<a name="english"></a>
## 🇺🇸 English

### What it does

A simple GUI tool to clean up filenames in bulk — remove characters, fix Dolphin/KDE copy artefacts, or add missing extensions. It **only renames files**, never touches their contents.

### Features

- Remove any substring from filenames (letters, numbers, symbols, anything)
- Fix Dolphin/KDE duplicate artefacts — `photo (1).png (1)` → `photo (1).png`
- Add an extension to files that don't have one (example: add `.png` to all extensionless files)
- Case-sensitive or case-insensitive matching
- Warns you before anything that would change an existing file extension
- Never overwrites — if the target name already exists, it auto-increments: `file (2).png`, `file (3).png`, etc.
- Bilingual UI — switch between English and Brazilian Portuguese with one click
- Made by Ium101

### Requirements

- Python 3.6+
- tkinter (bundled with Python on Windows; on Linux: `sudo apt-get install python3-tk`)

### Running from source

**Windows:**
```bash
python filename-character-renamer-z.py
```

**Linux / macOS:**
```bash
python3 filename-character-renamer-z.py
```

### Building a standalone executable

**Windows:**
```bash
build.bat
```

**Linux / macOS:**
```bash
chmod +x build.sh
./build.sh
```

Output:
- Windows → `dist\Filename Character Renamer Z.exe`
- Linux → `dist/Filename Character Renamer Z`
- macOS → `dist/Filename Character Renamer Z.app`

### How to use

The three main modes are mutually exclusive — pick one at a time:

**Mode 1 — Remove a substring**
1. Leave both top checkboxes unchecked
2. Type the substring to remove in the text field (example: `[]`)
3. Select a folder or a single file
4. Review the preview list, then hit **RENAME FILES**

**Mode 2 — Fix Dolphin artefacts**
1. Check **"Fix Dolphin/KDE duplicate artefacts"**
2. Select a folder — it will find all files with trailing ` (N)` after their extension
3. Review and rename

**Mode 3 — Add extension to extensionless files**
1. Check **"Add extension to files that have no extension"**
2. Type the extension (example: `.png`)
3. Select a folder — only files with no extension will be listed
4. Review and rename

### Safety

- The tool only uses `os.rename()` — file contents are never read or modified
- If a rename would result in a duplicate, it adds `(2)`, `(3)`, etc. instead of overwriting
- If removing a substring would change an existing extension, you get a warning before anything happens
- You always get a final confirmation dialog before any renames run

### FAQ

**Can I undo?**
No automatic undo. Make a backup first, or keep copies somewhere.

**Does it scan subfolders?**
No, it only processes files directly inside the selected folder.

**What if two files would get the same name?**
It automatically picks the next available name — `file (2).png`, `file (3).png`, etc.

**Will it corrupt my files?**
No. `os.rename()` only changes the filesystem entry. Contents are never touched.

---

<a name="português-brasil"></a>
## 🇧🇷 Português (Brasil)

### O que faz

Uma ferramenta GUI simples para limpar nomes de arquivos em massa — remove caracteres, corrige artefatos de cópia do Dolphin/KDE, ou adiciona extensões que faltam. Ela **apenas renomeia arquivos**, nunca toca no conteúdo deles.

### Recursos

- Remove qualquer substring dos nomes de arquivo (letras, números, símbolos, qualquer coisa)
- Corrige artefatos duplicados do Dolphin/KDE — `foto (1).png (1)` → `foto (1).png`
- Adiciona extensão a arquivos que não têm nenhuma (exemplo: adicionar `.png` a todos os arquivos sem extensão)
- Correspondência com ou sem diferenciação de maiúsculas
- Avisa antes de qualquer operação que alteraria uma extensão de arquivo existente
- Nunca sobrescreve — se o nome alvo já existe, incrementa automaticamente: `arquivo (2).png`, `arquivo (3).png`, etc.
- Interface bilíngue — alterne entre Inglês e Português Brasileiro com um clique
- Feito por Ium101

### Requisitos

- Python 3.6+
- tkinter (incluso com Python no Windows; no Linux: `sudo apt-get install python3-tk`)

### Executando pelo código-fonte

**Windows:**
```bash
python filename-character-renamer-z.py
```

**Linux / macOS:**
```bash
python3 filename-character-renamer-z.py
```

### Construindo um executável independente

**Windows:**
```bash
build.bat
```

**Linux / macOS:**
```bash
chmod +x build.sh
./build.sh
```

Saída:
- Windows → `dist\Filename Character Renamer Z.exe`
- Linux → `dist/Filename Character Renamer Z`
- macOS → `dist/Filename Character Renamer Z.app`

### Como usar

Os três modos principais são mutuamente exclusivos — escolha um por vez:

**Modo 1 — Remover substring**
1. Deixe ambos os checkboxes do topo desmarcados
2. Digite a substring a remover no campo de texto (exemplo: `[]`)
3. Selecione uma pasta ou um único arquivo
4. Revise a lista de pré-visualização e clique em **RENOMEAR ARQUIVOS**

**Modo 2 — Corrigir artefatos do Dolphin**
1. Marque **"Corrigir artefatos duplicados do Dolphin/KDE"**
2. Selecione uma pasta — vai encontrar todos os arquivos com ` (N)` após a extensão
3. Revise e renomeie

**Modo 3 — Adicionar extensão a arquivos sem extensão**
1. Marque **"Adicionar extensão a arquivos sem extensão"**
2. Digite a extensão (exemplo: `.png`)
3. Selecione uma pasta — apenas arquivos sem extensão serão listados
4. Revise e renomeie

### Segurança

- A ferramenta usa apenas `os.rename()` — o conteúdo dos arquivos nunca é lido ou modificado
- Se uma renomeação resultaria em duplicata, adiciona `(2)`, `(3)`, etc. em vez de sobrescrever
- Se remover uma substring alteraria uma extensão existente, você recebe um aviso antes de qualquer coisa acontecer
- Sempre há um diálogo de confirmação final antes de qualquer renomeação ser executada

### Perguntas Frequentes

**Posso desfazer?**
Sem desfazer automático. Faça backup primeiro, ou mantenha cópias em algum lugar.

**Varre subpastas?**
Não, processa apenas arquivos diretamente dentro da pasta selecionada.

**E se dois arquivos tiverem o mesmo nome resultante?**
Escolhe automaticamente o próximo nome disponível — `arquivo (2).png`, `arquivo (3).png`, etc.

**Vai corromper meus arquivos?**
Não. `os.rename()` apenas altera a entrada no sistema de arquivos. O conteúdo nunca é tocado.
