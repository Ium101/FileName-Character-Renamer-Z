# User Manual | Manual do Usuário

## 📖 Language | Idioma

- [English](#english)
- [Português (Brasil)](#português-brasil)

---

<a name="english"></a>
## 🇺🇸 English

### Installation

**Run from source (all platforms):**

Windows:
```bash
python filename-character-renamer-z.py
```

Linux / macOS:
```bash
python3 filename-character-renamer-z.py
```

**Pre-built executable:**
- **Windows** — double-click `Filename Character Renamer Z.exe`
- **Linux** — run `./Filename\ Character\ Renamer\ Z` in terminal, or double-click if your file manager supports it
- **macOS** — double-click `Filename Character Renamer Z.app` in Finder

**Build it yourself:**

Windows:
```bash
build.bat
```

Linux / macOS:
```bash
chmod +x build.sh
./build.sh
```

---

### The three modes

The top two checkboxes and the substring field are **mutually exclusive** — only one mode can be active at a time. Enabling a top checkbox automatically disables the substring field.

---

#### Mode 1 — Remove a substring

Use this to strip a specific string from every filename in a folder.

1. Make sure both top checkboxes are **unchecked**
2. Type the substring to remove in the **"Substring to remove"** field (example: `[]`)
3. Toggle **Case-sensitive matching** on or off depending on your needs
4. Click **Select Folder** or **Select File**
5. The list updates immediately with a preview: `old name  ->  new name`
6. Click **RENAME FILES**, confirm the dialog

**Examples:**

| Substring | Before | After |
|-----------|--------|-------|
| `[]` | `photo[1].jpg` | `photo1.jpg` |
| `_draft` | `report_draft.pdf` | `report.pdf` |
| `(copy)` | `file(copy).txt` | `file.txt` |

---

#### Mode 2 — Fix Dolphin/KDE duplicate artefacts

Dolphin (the KDE file manager) sometimes appends ` (1)` after the file extension when copying — so you end up with `photo (1).png (1)` instead of `photo (1).png`. Windows can't even display these as images. This mode fixes that.

1. Check **"Fix Dolphin/KDE duplicate artefacts"**
2. Click **Select Folder**
3. It will list all affected files with the corrected names
4. Click **RENAME FILES**

**What it fixes:**

| Before | After |
|--------|-------|
| `photo (1).png (1)` | `photo (1).png` |
| `document (2).pdf (3)` | `document (2).pdf` |
| `screenshot (1).jpeg (1)` | `screenshot (1).jpeg` |

Files without this artefact are left alone.

---

#### Mode 3 — Add extension to extensionless files

Useful when files are missing their extension entirely — for example, images downloaded without a `.jpg` or `.png`.

1. Check **"Add extension to files that have no extension"**
2. Type the extension in the field that appears (example: `.png` — the dot is optional, `png` works too)
3. Click **Select Folder**
4. Only files with no extension will be listed
5. Click **RENAME FILES**

Files that already have an extension are ignored by this mode.

---

### Duplicate handling

If a rename would produce a name that already exists on disk, the tool automatically picks the next free name instead of overwriting:

- `photo.png` already exists → result becomes `photo (2).png`
- `photo (2).png` also exists → result becomes `photo (3).png`
- and so on

You will never lose a file due to an accidental overwrite.

---

### Extension change warning

If removing a substring would accidentally change or remove a file's existing extension (example: removing `.jp` from `photo.jpg` would produce `photo.g`), the tool shows a warning dialog listing all affected files before continuing. You can cancel at that point.

---

### Language toggle

The small button in the top-right corner of the yellow banner switches the interface between **English** and **Brazilian Portuguese**. All labels, buttons, dialogs, and the credits line switch instantly.

---

### Troubleshooting

**No files appear in the list**
- Check that you typed the right substring
- Make sure you selected the right folder
- If using Dolphin fix, the folder may have no artefacts — that's fine

**"New filename would be empty"**
- The substring you're removing makes up the entire filename (without extension)
- Try a more specific substring

**"Permission denied"**
- Close any programs that have those files open
- On Linux/macOS, check file permissions: `ls -la`
- On Windows, try running as administrator

**The window won't resize**
- That's intentional — the window size is fixed so it stays consistent

---

<a name="português-brasil"></a>
## 🇧🇷 Português (Brasil)

### Instalação

**Executar pelo código-fonte (todas as plataformas):**

Windows:
```bash
python filename-character-renamer-z.py
```

Linux / macOS:
```bash
python3 filename-character-renamer-z.py
```

**Executável pré-compilado:**
- **Windows** — clique duas vezes em `Filename Character Renamer Z.exe`
- **Linux** — execute `./Filename\ Character\ Renamer\ Z` no terminal, ou clique duas vezes se seu gerenciador de arquivos suportar
- **macOS** — clique duas vezes em `Filename Character Renamer Z.app` no Finder

**Compilar você mesmo:**

Windows:
```bash
build.bat
```

Linux / macOS:
```bash
chmod +x build.sh
./build.sh
```

---

### Os três modos

Os dois checkboxes do topo e o campo de substring são **mutuamente exclusivos** — apenas um modo pode estar ativo por vez. Ativar um checkbox do topo desativa automaticamente o campo de substring.

---

#### Modo 1 — Remover uma substring

Use para remover uma string específica de todos os nomes de arquivo em uma pasta.

1. Certifique-se de que ambos os checkboxes do topo estão **desmarcados**
2. Digite a substring a remover no campo **"Substring a remover"** (exemplo: `[]`)
3. Ative ou desative **Correspondência com diferenciação de maiúsculas** conforme necessário
4. Clique em **Selecionar Pasta** ou **Selecionar Arquivo**
5. A lista atualiza imediatamente com uma pré-visualização: `nome antigo  ->  nome novo`
6. Clique em **RENOMEAR ARQUIVOS** e confirme o diálogo

**Exemplos:**

| Substring | Antes | Depois |
|-----------|-------|--------|
| `[]` | `foto[1].jpg` | `foto1.jpg` |
| `_rascunho` | `relatorio_rascunho.pdf` | `relatorio.pdf` |
| `(copia)` | `arquivo(copia).txt` | `arquivo.txt` |

---

#### Modo 2 — Corrigir artefatos duplicados do Dolphin/KDE

O Dolphin (gerenciador de arquivos do KDE) às vezes adiciona ` (1)` após a extensão do arquivo ao copiar — resultando em `foto (1).png (1)` em vez de `foto (1).png`. O Windows nem consegue exibir esses arquivos como imagens. Este modo corrige isso.

1. Marque **"Corrigir artefatos duplicados do Dolphin/KDE"**
2. Clique em **Selecionar Pasta**
3. Listará todos os arquivos afetados com os nomes corrigidos
4. Clique em **RENOMEAR ARQUIVOS**

**O que corrige:**

| Antes | Depois |
|-------|--------|
| `foto (1).png (1)` | `foto (1).png` |
| `documento (2).pdf (3)` | `documento (2).pdf` |
| `captura (1).jpeg (1)` | `captura (1).jpeg` |

Arquivos sem esse artefato são ignorados.

---

#### Modo 3 — Adicionar extensão a arquivos sem extensão

Útil quando arquivos estão sem extensão — por exemplo, imagens baixadas sem `.jpg` ou `.png`.

1. Marque **"Adicionar extensão a arquivos sem extensão"**
2. Digite a extensão no campo que aparece (exemplo: `.png` — o ponto é opcional, `png` também funciona)
3. Clique em **Selecionar Pasta**
4. Apenas arquivos sem extensão serão listados
5. Clique em **RENOMEAR ARQUIVOS**

Arquivos que já têm uma extensão são ignorados por este modo.

---

### Tratamento de duplicatas

Se uma renomeação produziria um nome que já existe no disco, a ferramenta escolhe automaticamente o próximo nome disponível em vez de sobrescrever:

- `foto.png` já existe → resultado vira `foto (2).png`
- `foto (2).png` também existe → resultado vira `foto (3).png`
- e assim por diante

Você nunca perderá um arquivo por sobrescrita acidental.

---

### Aviso de alteração de extensão

Se remover uma substring alteraria ou removeria acidentalmente a extensão existente de um arquivo (exemplo: remover `.jp` de `foto.jpg` produziria `foto.g`), a ferramenta mostra um diálogo de aviso listando todos os arquivos afetados antes de continuar. Você pode cancelar nesse ponto.

---

### Alternância de idioma

O pequeno botão no canto superior direito do banner amarelo alterna a interface entre **Inglês** e **Português Brasileiro**. Todos os rótulos, botões, diálogos e o texto de créditos mudam instantaneamente.

---

### Solução de Problemas

**Nenhum arquivo aparece na lista**
- Verifique se digitou a substring correta
- Certifique-se de ter selecionado a pasta correta
- Se usar a correção do Dolphin, a pasta pode não ter artefatos — tudo certo

**"Novo nome ficaria vazio"**
- A substring que está removendo compõe o nome completo do arquivo (sem extensão)
- Tente uma substring mais específica

**"Permissão negada"**
- Feche programas que tenham esses arquivos abertos
- No Linux/macOS, verifique as permissões: `ls -la`
- No Windows, tente executar como administrador

**A janela não redimensiona**
- Isso é intencional — o tamanho da janela é fixo para manter consistência

---

<div align="center">

**Important | Importante:** This tool ONLY renames files. It does NOT modify file contents.

Esta ferramenta APENAS renomeia arquivos. NÃO modifica o conteúdo dos arquivos.

*Made by Ium101 | Feito por Ium101*

</div>
