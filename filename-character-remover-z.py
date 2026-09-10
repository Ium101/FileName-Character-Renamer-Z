#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
import os
import re
import sys
import io
import base64
import configparser
import shutil
import subprocess
import platform

# DPI awareness fix for Windows high-DPI screens
if platform.system() == "Windows":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # SYSTEM_AWARE
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Embedded app icon (base64 PNG, 256x256, RGBA).
# Teal document glyph -- fully transparent background and interior, no
# black anywhere. This is the single source of truth for the icon: it
# sets the live Tk window/taskbar icon below, and is also exported to
# .ico (Windows) / .svg (Linux) by build.bat / build.sh via the hidden
# --generate-icon flag, so the on-disk exe icon always matches what the
# running app actually shows.
# ---------------------------------------------------------------------------

ICON_BASE64 = """
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
W4IAAAAASUVORK5CYII=
""".strip().replace("\n", "")


def _load_icon_image():
    """Return the embedded icon as a PIL Image (RGBA), or None if Pillow
    isn't available (the running app degrades gracefully without it)."""
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        raw = base64.b64decode(ICON_BASE64)
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception:
        return None


def generate_icon_files(ico_path=None, svg_path=None):
    """Export the embedded icon to .ico (multi-resolution, BMP frames) and/or
    a flat-color .svg, for use by the build scripts. Headless-safe (no Tk
    required) -- invoked via the hidden --generate-icon CLI flag."""
    from PIL import Image

    img = _load_icon_image()
    if img is None:
        print("[ERROR] Pillow not available; cannot generate icon.")
        return False

    if ico_path:
        sizes = [16, 24, 32, 48, 64, 128, 256]
        frames = [img.resize((sz, sz), Image.LANCZOS) for sz in sizes]
        # Save as BMP-format ICO frames (not PNG-compressed) for max
        # compatibility with older Windows icon caches/Explorer.
        frames[-1].save(
            ico_path, format="ICO",
            sizes=[(f.width, f.height) for f in frames],
            bitmap_format="bmp",
        )
        print("[OK] Icon (.ico) saved:", ico_path)

    if svg_path:
        # Flat teal SVG companion (used for Linux desktop/icon-theme entries).
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 106" width="256" height="256">
  <polyline points="14,6 65,6 86,27 86,97 14,97 14,6"
            fill="none" stroke="#00A8A8" stroke-width="5"
            stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="65,6 65,27 86,27"
            fill="none" stroke="#00A8A8" stroke-width="5"
            stroke-linejoin="round" stroke-linecap="round"/>
  <line x1="24" y1="52" x2="76" y2="52" stroke="#00A8A8" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="24" y1="65" x2="76" y2="65" stroke="#00A8A8" stroke-width="3.5" stroke-linecap="round"/>
  <text x="50" y="91" font-family="Arial,Helvetica,sans-serif" font-weight="bold"
        font-size="20" fill="#00A8A8" text-anchor="middle">Z</text>
</svg>
"""
        with open(svg_path, "w") as f:
            f.write(svg)
        print("[OK] Icon (.svg) saved:", svg_path)

    return True


# ---------------------------------------------------------------------------
# Config helpers  (INI file stored next to the executable / script)
# ---------------------------------------------------------------------------

def _get_config_path():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    name = ("filename_character_remover_z_windows.ini"
            if platform.system() == "Windows"
            else "filename_character_remover_z_linux.ini")
    return os.path.join(base, name)


# ---------------------------------------------------------------------------
# Theme palettes
# ---------------------------------------------------------------------------

THEMES = {
    "light": {
        "root_bg":         "#F0F0F0",
        "warn_bg":         "#E0E0E0",
        "warn1_fg":        "red",
        "warn2_fg":        "black",
        "warn3_fg":        "black",
        "title_fg":        "#111111",
        "dolphin_bg":      "#E8F4FD",
        "dolphin_fg":      "#005A8E",
        "addext_bg":       "#F0FFF0",
        "addext_fg":       "#1A6B1A",
        "addext_hint_fg":  "gray",
        "input_bg":        "#F0F0F0",
        "substr_fg":       "black",
        "substr_hint_fg":  "gray",
        "entry_bg":        "white",
        "entry_fg":        "black",
        "entry_ins":       "black",
        "entry_dis_bg":    "#D8D8D8",
        "entry_dis_fg":    "#888888",
        "case_fg":         "blue",
        "list_bg":         "white",
        "list_fg":         "black",
        "list_sel_bg":     "#BDD8F5",
        "list_sel_fg":     "black",
        "status_info":     "blue",
        "status_success":  "green",
        "credits_fg":      "#999999",
        "corner_bg":       "#E0E0E0",  # must match warn_bg
        "lang_btn_bg":     "#555555",
        "theme_btn_bg":    "#444444",
        "btn_folder_bg":   "#007ACC",
        "btn_file_bg":     "#17A2B8",
        "btn_rename_bg":   "#DC3545",
        "cb_select":       "#F0F0F0",
        "theme_icon":      "Light",  # sun symbol (switch TO light)
    },
    "dark": {
        "root_bg":         "#1E1E1E",
        "warn_bg":         "#252525",
        "warn1_fg":        "#FF6B6B",
        "warn2_fg":        "#CCCCCC",
        "warn3_fg":        "#999999",
        "title_fg":        "#E0E0E0",
        "dolphin_bg":      "#162330",
        "dolphin_fg":      "#7EC8E3",
        "addext_bg":       "#152015",
        "addext_fg":       "#6BCF6B",
        "addext_hint_fg":  "#888888",
        "input_bg":        "#1E1E1E",
        "substr_fg":       "#E0E0E0",
        "substr_hint_fg":  "#888888",
        "entry_bg":        "#2D2D2D",
        "entry_fg":        "#E0E0E0",
        "entry_ins":       "#E0E0E0",
        "entry_dis_bg":    "#3A3A3A",
        "entry_dis_fg":    "#666666",
        "case_fg":         "#8888FF",
        "list_bg":         "#2D2D2D",
        "list_fg":         "#DDDDDD",
        "list_sel_bg":     "#163A5A",
        "list_sel_fg":     "#E0E0E0",
        "status_info":     "#6AA8FF",
        "status_success":  "#5FBF5F",
        "credits_fg":      "#555555",
        "corner_bg":       "#252525",  # must match warn_bg
        "lang_btn_bg":     "#444444",
        "theme_btn_bg":    "#335533",
        "btn_folder_bg":   "#005FA3",
        "btn_file_bg":     "#0D7A8E",
        "btn_rename_bg":   "#9B1C2A",
        "cb_select":       "#2D2D2D",
        "theme_icon":      "Dark",  # moon symbol (switch TO dark)
    },
}


# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------

STRINGS = {
    "en": {
        # window
        "window_title":        "Filename Character Remover Z",
        # warning banner
        "warn1":               "WARNING: THIS TOOL ONLY RENAMES FILENAMES",
        "warn2":               "IT DOES NOT OPEN, READ, OR MODIFY FILE CONTENTS",
        "warn3":               "IT ONLY USES os.rename() - THE SAFEST RENAME METHOD",
        # title
        "app_title":           "Remove Custom Characters from Filenames",
        # dolphin row
        "dolphin_cb":          'Fix Dolphin/KDE duplicate artefacts  (example:  "photo (1).png (1)"  ->  "photo (1).png")',
        # add-ext row
        "addext_cb":           "Add extension to files that have no extension:",
        "addext_hint":         "(example: .png  .jpg  .txt - dot optional)",
        # substring row
        "substr_label":        "Character(s) to remove:",
        "substr_hint":         "<- Enter the character(s) (example: []abc123 )",
        # path bar row
        "path_label":          "Path:",
        "path_hint":           "Type or paste a folder/file path, then press Enter",
        "warn_bad_path":       "Invalid Path",
        "warn_bad_path_msg":   "That path doesn't exist. Please check it and try again.",
        # case row
        "case_cb":             "Case-sensitive matching",
        # buttons
        "btn_folder":          "Select Folder",
        "btn_file":            "Select File",
        "btn_rename":          "RENAME FILES",
        # list label
        "list_label":          "Files that will be renamed:",
        # status messages
        "status_init":         "Step 1: Configure options above, then select a folder or file",
        "status_scanning":     "Selected folder: {folder}\nScanning for files...",
        "status_found1":       "Found 1 file to rename.",
        "status_no_change":    "No changes needed for the selected file.",
        "status_none":         "No files matched the current settings.",
        "status_found":        "Found {n} files to rename.",
        "status_done":         "Done! Renamed {ok} files, Failed: {fail}",
        # warnings / dialogs
        "warn_no_folder":      "No Folder",
        "warn_no_folder_msg":  "Please select a folder first",
        "warn_no_ext":         "No Extension",
        "warn_no_ext_msg":     "Please enter the extension to add (example: .png)",
        "warn_no_files":       "No Files",
        "warn_no_files_msg":   "Please scan for files first",
        "err_scan":            "Error scanning folder: {e}",
        # extension-change dialog
        "extchg_title":        "WARNING: File Extensions Will Change",
        "extchg_body":         (
            "The following {n} file(s) will have their existing extension changed:\n\n"
            "{sample}\n\n"
            "Changing extensions can make files unreadable by their associated applications.\n\n"
            "Are you sure you want to proceed?"
        ),
        "extchg_more":         "  ... and {n} more",
        # final confirmation
        "confirm_title":       "FINAL CONFIRMATION",
        "confirm_body":        (
            "This will RENAME {n} file(s).\n\n"
            "Operations:\n{notes}\n\n"
            "WARNING: Make sure you have BACKUPS first!\n\n"
            "Duplicate targets will be resolved automatically by adding (N).\n"
            "This action ONLY renames files - file contents are never touched.\n\n"
            "Continue?"
        ),
        "note_substr":         "Removing characters: '{s}'",
        "note_dolphin":        "Fixing Dolphin/KDE duplicate artefacts",
        "note_addext":         "Adding '{ext}' to {n} extensionless file(s)",
        # result dialog
        "result_title":        "Complete",
        "result_ok":           "Successfully renamed {n} files!",
        "result_fail":         "\nFailed: {n} files",
        "result_errors":       "\n\nErrors (first 10):\n",
        "err_empty":           "{f}: New filename would be empty",
        # language button
        "lang_btn":            "PT-BR",
        # credits
        "credits":             "Made by Ium101",
    },
    "pt": {
        # window
        "window_title":        "Filename Character Remover Z",
        # warning banner
        "warn1":               "AVISO: ESTA FERRAMENTA RENOMEIA APENAS NOMES DE ARQUIVO",
        "warn2":               "ELA NAO ABRE, LE NEM MODIFICA O CONTEUDO DOS ARQUIVOS",
        "warn3":               "USA APENAS os.rename() - O METODO MAIS SEGURO DE RENOMEAR",
        # title
        "app_title":           "Remover Caracteres Personalizados de Nomes de Arquivo",
        # dolphin row
        "dolphin_cb":          'Corrigir artefatos duplicados do Dolphin/KDE  (exemplo:  "foto (1).png (1)"  ->  "foto (1).png")',
        # add-ext row
        "addext_cb":           "Adicionar extensao a arquivos sem extensao:",
        "addext_hint":         "(exemplo: .png  .jpg  .txt - ponto opcional)",
        # substring row
        "substr_label":        "Caractere(s) a remover:",
        "substr_hint":         "<- Digite caractere(s) (exemplo: []abc123 )",
        # path bar row
        "path_label":          "Caminho:",
        "path_hint":           "Digite ou cole um caminho de pasta/arquivo e pressione Enter",
        "warn_bad_path":       "Caminho Invalido",
        "warn_bad_path_msg":   "Esse caminho nao existe. Verifique e tente novamente.",
        # case row
        "case_cb":             "Correspondencia com diferenciacao de maiusculas",
        # buttons
        "btn_folder":          "Selecionar Pasta",
        "btn_file":            "Selecionar Arquivo",
        "btn_rename":          "RENOMEAR ARQUIVOS",
        # list label
        "list_label":          "Arquivos que serao renomeados:",
        # status messages
        "status_init":         "Passo 1: Configure as opcoes acima, depois selecione uma pasta ou arquivo",
        "status_scanning":     "Pasta selecionada: {folder}\nVarendo arquivos...",
        "status_found1":       "1 arquivo encontrado para renomear.",
        "status_no_change":    "Nenhuma alteracao necessaria para o arquivo selecionado.",
        "status_none":         "Nenhum arquivo correspondeu as configuracoes atuais.",
        "status_found":        "{n} arquivos encontrados para renomear.",
        "status_done":         "Concluido! Renomeados: {ok}, Falhas: {fail}",
        # warnings / dialogs
        "warn_no_folder":      "Sem Pasta",
        "warn_no_folder_msg":  "Selecione uma pasta primeiro",
        "warn_no_ext":         "Sem Extensao",
        "warn_no_ext_msg":     "Digite a extensao a adicionar (exemplo: .png)",
        "warn_no_files":       "Sem Arquivos",
        "warn_no_files_msg":   "Varredura de arquivos necessaria antes de renomear",
        "err_scan":            "Erro ao varrer a pasta: {e}",
        # extension-change dialog
        "extchg_title":        "AVISO: Extensoes de Arquivo Serao Alteradas",
        "extchg_body":         (
            "Os seguintes {n} arquivo(s) terao sua extensao existente alterada:\n\n"
            "{sample}\n\n"
            "Alterar extensoes pode tornar arquivos ilegíveis pelos aplicativos associados.\n\n"
            "Tem certeza que deseja continuar?"
        ),
        "extchg_more":         "  ... e mais {n}",
        # final confirmation
        "confirm_title":       "CONFIRMACAO FINAL",
        "confirm_body":        (
            "Isso ira RENOMEAR {n} arquivo(s).\n\n"
            "Operacoes:\n{notes}\n\n"
            "AVISO: Certifique-se de ter BACKUPS primeiro!\n\n"
            "Alvos duplicados serao resolvidos automaticamente adicionando (N).\n"
            "Esta acao APENAS renomeia arquivos - o conteudo nunca e tocado.\n\n"
            "Continuar?"
        ),
        "note_substr":         "Removendo caracteres: '{s}'",
        "note_dolphin":        "Corrigindo artefatos duplicados do Dolphin/KDE",
        "note_addext":         "Adicionando '{ext}' a {n} arquivo(s) sem extensao",
        # result dialog
        "result_title":        "Concluido",
        "result_ok":           "Renomeados com sucesso: {n} arquivos!",
        "result_fail":         "\nFalhas: {n} arquivos",
        "result_errors":       "\n\nErros (primeiros 10):\n",
        "err_empty":           "{f}: Novo nome ficaria vazio",
        # language button
        "lang_btn":            "EN",
        # credits
        "credits":             "Feito por Ium101",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fix_dolphin_duplicate(filename):
    pattern = re.compile(r'^(.*\.[^./ \\]+?)(\s+\(\d+\))+$')
    m = pattern.match(filename)
    return m.group(1) if m else filename


def safe_target_path(directory, new_name):
    target = os.path.join(directory, new_name)
    if not os.path.exists(target):
        return target, new_name
    base, ext = os.path.splitext(new_name)
    base_clean = re.sub(r'\s*\(\d+\)$', '', base)
    counter = 2
    while True:
        candidate_name = f"{base_clean} ({counter}){ext}"
        candidate_path = os.path.join(directory, candidate_name)
        if not os.path.exists(candidate_path):
            return candidate_path, candidate_name
        counter += 1


def extension_changed(old_name, new_name):
    real_old_ext = os.path.splitext(fix_dolphin_duplicate(old_name))[1].lower()
    new_ext = os.path.splitext(new_name)[1].lower()
    return real_old_ext != new_ext


def has_no_extension(filename):
    _, ext = os.path.splitext(filename)
    return ext == ""


def normalise_extension(raw):
    raw = raw.strip().lower()
    if not raw:
        return ""
    if not raw.startswith("."):
        raw = "." + raw
    return raw


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class CustomCharacterRemover:
    def __init__(self, root):
        self.root        = root
        self.lang        = "en"
        self.files       = []
        self.base_folder = None
        self.dark_mode   = False
        self.last_folder = ""

        # Defaults always set here so they exist even when INI is absent (first run)
        self._cfg_fix_dolphin     = False
        self._cfg_add_ext_enabled = False
        self._cfg_add_ext_value   = ".png"
        self._cfg_case_sensitive  = True
        self._cfg_char_value      = "[]"

        try:
            self.root.tk.call('tk', 'scaling', 1.5)
        except Exception:
            pass

        self._load_config()
        self._build_ui()
        # Restore saved checkbox/entry states from INI
        self.fix_dolphin.set(self._cfg_fix_dolphin)
        self.add_ext_enabled.set(self._cfg_add_ext_enabled)
        self.add_ext_entry.delete(0, tk.END)
        self.add_ext_entry.insert(0, self._cfg_add_ext_value)
        self.case_sensitive.set(self._cfg_case_sensitive)
        self.char_entry.delete(0, tk.END)
        self.char_entry.insert(0, self._cfg_char_value)
        if self.last_folder:
            self.path_var.set(self.last_folder)
        self._update_mode()
        self._apply_lang()
        self._apply_theme()
        root.after(0, self._lock_size)

    # -----------------------------------------------------------------------
    # Config persistence  (INI file next to the exe/script)
    # -----------------------------------------------------------------------

    def _load_config(self):
        path = _get_config_path()
        cfg  = configparser.ConfigParser()
        if not cfg.read(path, encoding="utf-8"):
            return   # file absent — defaults from __init__ stay in place
        s = "settings"
        if not cfg.has_section(s):
            return   # file empty — same
        self.dark_mode            = cfg.getboolean(s, "dark_mode",        fallback=False)
        self.lang                 = cfg.get       (s, "lang",             fallback="en")
        self.last_folder          = cfg.get       (s, "last_folder",      fallback="")
        self._cfg_fix_dolphin     = cfg.getboolean(s, "fix_dolphin",      fallback=False)
        self._cfg_add_ext_enabled = cfg.getboolean(s, "add_ext_enabled",  fallback=False)
        self._cfg_add_ext_value   = cfg.get       (s, "add_ext_value",    fallback=".png")
        self._cfg_case_sensitive  = cfg.getboolean(s, "case_sensitive",   fallback=True)
        self._cfg_char_value      = cfg.get       (s, "char_value",       fallback="[]")

    def _save_config(self):
        path = _get_config_path()
        cfg  = configparser.ConfigParser()
        cfg["settings"] = {
            "dark_mode":       str(self.dark_mode),
            "lang":            self.lang,
            "last_folder":     self.last_folder,
            "fix_dolphin":     str(self.fix_dolphin.get()),
            "add_ext_enabled": str(self.add_ext_enabled.get()),
            "add_ext_value":   self.add_ext_entry.get(),
            "case_sensitive":  str(self.case_sensitive.get()),
            "char_value":      self.char_entry.get(),
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                cfg.write(f)
        except Exception:
            pass

    def _lock_size(self):
        """
        Compute the tallest/widest reqsize across all languages so the window
        never opens clipped (e.g. credits disappearing on Linux with PT-BR),
        then use that as a MINIMUM size only. The window stays freely
        resizable and maximizable in both directions.
        Applies every language, measures, keeps the max, then restores.
        """
        max_w = 1080
        max_h = 0
        original_lang = self.lang

        for lang in STRINGS:
            self.lang = lang
            self._apply_lang()
            self.root.update_idletasks()
            w = self.root.winfo_reqwidth()
            h = self.root.winfo_reqheight()
            max_w = max(max_w, w, getattr(self, "_min_window_w", 0))
            max_h = max(max_h, h)

        self.lang = original_lang
        self._apply_lang()

        self.root.resizable(True, True)
        self.root.minsize(max_w, max_h)

    # -----------------------------------------------------------------------
    # Theme helpers
    # -----------------------------------------------------------------------

    def _palette(self):
        return THEMES["dark"] if self.dark_mode else THEMES["light"]

    def _sc(self, semantic):
        """Return status fg color for 'info' or 'success' in the current theme."""
        p = self._palette()
        return p["status_info"] if semantic == "info" else p["status_success"]

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        root = self.root
        mono_font = "Consolas" if platform.system() == "Windows" else "Monospace"

        # Warning banner
        self.warning_frame = tk.Frame(root, bg="#E0E0E0", pady=10)
        self.warning_frame.pack(fill=tk.X)

        # Warning labels packed FIRST so they occupy space before the
        # corner buttons are placed on top.  wraplength for the top (red)
        # line is wide enough to keep the PT-BR text on a single line,
        # while staying narrow enough to never flow under the buttons.
        self.lbl_warn1 = tk.Label(self.warning_frame, text="",
                 font=("Arial", 16, "bold"), bg="#E0E0E0", fg="red",
                 wraplength=820)
        self.lbl_warn1.pack()
        self.lbl_warn2 = tk.Label(self.warning_frame, text="",
                 font=("Arial", 11), bg="#E0E0E0", fg="black",
                 wraplength=700)
        self.lbl_warn2.pack()
        self.lbl_warn3 = tk.Label(self.warning_frame, text="",
                 font=("Arial", 9), bg="#E0E0E0", fg="black",
                 wraplength=700)
        self.lbl_warn3.pack()

        # Corner buttons (theme + lang) — placed top-right AFTER the labels
        # so the banner height is already known.  Both buttons share identical
        # font/width/padding so they render the same size.
        self.corner_frame = tk.Frame(self.warning_frame, bg="#E0E0E0")
        self.corner_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-6, y=14)

        BTN_FONT  = ("Arial", 9, "bold")
        BTN_W     = 5      # character-unit width — same for both
        BTN_IPADX = 4
        BTN_IPADY = 3

        self.theme_btn = tk.Button(
            self.corner_frame, text="( )",
            font=BTN_FONT, width=BTN_W,
            bg="#444444", fg="white",
            relief=tk.FLAT, cursor="hand2",
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side=tk.LEFT, padx=(0, 3),
                            ipadx=BTN_IPADX, ipady=BTN_IPADY)

        self.lang_btn = tk.Button(
            self.corner_frame, text="", width=BTN_W,
            font=BTN_FONT,
            bg="#555555", fg="white",
            relief=tk.FLAT, cursor="hand2",
            command=self._toggle_lang,
        )
        self.lang_btn.pack(side=tk.LEFT, ipadx=BTN_IPADX, ipady=BTN_IPADY)

        # App title
        self.lbl_title = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.lbl_title.pack(pady=8)

        # Dolphin fix toggle
        self.dolphin_frame = tk.Frame(root, bg="#E8F4FD", pady=6, padx=10,
                                      relief=tk.GROOVE, bd=1)
        self.dolphin_frame.pack(fill=tk.X, padx=20, pady=(0, 4))
        self.fix_dolphin = tk.BooleanVar(value=False)
        self.dolphin_cb_widget = tk.Checkbutton(
            self.dolphin_frame, text="",
            variable=self.fix_dolphin,
            font=("Arial", 10, "bold"), fg="#005A8E", bg="#E8F4FD",
            wraplength=880,
            command=self._on_dolphin_toggle,
        )
        self.dolphin_cb_widget.pack(side=tk.LEFT)

        # Add-extension toggle
        self.addext_frame = tk.Frame(root, bg="#F0FFF0", pady=6, padx=10,
                                     relief=tk.GROOVE, bd=1)
        self.addext_frame.pack(fill=tk.X, padx=20, pady=(0, 4))
        self.add_ext_enabled = tk.BooleanVar(value=False)
        self.addext_cb_widget = tk.Checkbutton(
            self.addext_frame, text="",
            variable=self.add_ext_enabled,
            font=("Arial", 10, "bold"), fg="#1A6B1A", bg="#F0FFF0",
            wraplength=880,
            command=self._on_addext_toggle,
        )
        self.addext_cb_widget.pack(side=tk.LEFT)
        self.add_ext_entry = tk.Entry(self.addext_frame, font=("Arial", 11),
                                      width=10, state=tk.DISABLED,
                                      disabledbackground="#D8D8D8")
        self.add_ext_entry.pack(side=tk.LEFT, padx=(6, 2))
        self.add_ext_entry.insert(0, ".png")
        self.add_ext_entry.bind("<FocusOut>", lambda e: (self._rescan(), self._save_config()))
        self.add_ext_entry.bind("<Return>",   lambda e: (self._rescan(), self._save_config()))
        self.lbl_addext_hint = tk.Label(self.addext_frame, text="",
                 font=("Arial", 9), fg="gray", bg="#F0FFF0")
        self.lbl_addext_hint.pack(side=tk.LEFT, padx=4)

        # Substring input
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=6)
        self.lbl_substr = tk.Label(self.input_frame, text="",
                 font=("Arial", 11, "bold"))
        self.lbl_substr.pack(side=tk.LEFT, padx=5)
        self.char_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=30)
        self.char_entry.pack(side=tk.LEFT, padx=5)
        self.char_entry.insert(0, "[]")
        self.char_entry.bind("<FocusOut>", lambda e: (self._rescan(), self._save_config()))
        self.char_entry.bind("<Return>",   lambda e: (self._rescan(), self._save_config()))
        self.lbl_substr_hint = tk.Label(self.input_frame, text="",
                 font=("Arial", 9), fg="gray")
        self.lbl_substr_hint.pack(side=tk.LEFT, padx=5)

        # Address bar + Case sensitivity (same row: path entry on the left,
        # case-sensitive checkbox on the right)
        self.case_sensitive = tk.BooleanVar(value=True)
        self.path_var = tk.StringVar()
        self.case_frame = tk.Frame(root)
        self.case_frame.pack(pady=3, padx=20, fill=tk.X)

        self.lbl_path = tk.Label(self.case_frame, text="",
                 font=("Arial", 11, "bold"))
        self.lbl_path.pack(side=tk.LEFT, padx=(0, 5))
        self.path_entry = tk.Entry(self.case_frame, textvariable=self.path_var,
                                   font=("Arial", 12))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True,
                             padx=(0, 15))
        self.path_entry.bind("<Return>", self._on_path_entry_submit)

        self.case_cb = tk.Checkbutton(self.case_frame, text="",
                       variable=self.case_sensitive,
                       font=("Arial", 11, "bold"), fg="blue",
                       command=lambda: (self._rescan(), self._save_config()))
        self.case_cb.pack(side=tk.LEFT)

        # Buttons
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=8)
        self.btn_folder = tk.Button(self.btn_frame, text="",
                  command=self.select_folder,
                  bg="#007ACC", fg="white", padx=20, pady=8,
                  font=("Arial", 10, "bold"))
        self.btn_folder.pack(side=tk.LEFT, padx=5)
        self.btn_file = tk.Button(self.btn_frame, text="",
                  command=self.select_file,
                  bg="#17A2B8", fg="white", padx=20, pady=8,
                  font=("Arial", 10, "bold"))
        self.btn_file.pack(side=tk.LEFT, padx=5)
        self.btn_rename = tk.Button(self.btn_frame, text="",
                  command=self.rename_files,
                  bg="#DC3545", fg="white", padx=20, pady=8,
                  font=("Arial", 10, "bold"))
        self.btn_rename.pack(side=tk.LEFT, padx=5)

        # File list
        self.lbl_list = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_list.pack()
        self.list_frame = tk.Frame(root)
        self.list_frame.pack(pady=6, padx=20, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self.list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox = tk.Listbox(self.list_frame,
                                       yscrollcommand=scrollbar.set,
                                       font=(mono_font, 9),
                                       selectmode=tk.SINGLE)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # Status
        self.status = tk.Label(root, text="",
                              font=("Arial", 11), fg="blue", wraplength=880)
        self.status.pack(pady=(4, 0))

        # Credits
        self.lbl_credits = tk.Label(root, text="",
                                    font=("Arial", 8), fg="#999999")
        self.lbl_credits.pack(pady=(2, 6))

    # -----------------------------------------------------------------------
    # Language
    # -----------------------------------------------------------------------

    def _t(self, key):
        return STRINGS[self.lang][key]

    def _toggle_lang(self):
        self.lang = "pt" if self.lang == "en" else "en"
        self._apply_lang()
        self._save_config()

    def _apply_lang(self):
        t = self._t
        self.root.title(t("window_title"))
        self.lang_btn.config(text=t("lang_btn"))
        self.lbl_warn1.config(text=t("warn1"))
        # Measure the actual rendered width of this line in its own font
        # and size wraplength to fit it exactly (+ small buffer), so the
        # warning always renders on a single line regardless of language,
        # OS font rendering, or display scaling.
        warn1_font = tkfont.Font(font=self.lbl_warn1.cget("font"))
        warn1_text_w = warn1_font.measure(t("warn1"))
        self.lbl_warn1.config(wraplength=warn1_text_w + 20)
        # The corner buttons (theme/lang toggle) float on top of this banner
        # at the top-right via .place(), so they don't factor into the
        # frame's natural width the way packed widgets do. Since warn1 is
        # centered, work out the total window width needed so its centered
        # text never reaches under the buttons, using the buttons' actual
        # measured width (which itself varies slightly by language).
        self.root.update_idletasks()
        corner_w = self.corner_frame.winfo_reqwidth()
        self._min_window_w = warn1_text_w + 2 * (corner_w + 40)
        self.lbl_warn2.config(text=t("warn2"))
        self.lbl_warn3.config(text=t("warn3"))
        self.lbl_title.config(text=t("app_title"))
        self.dolphin_cb_widget.config(text=t("dolphin_cb"))
        self.addext_cb_widget.config(text=t("addext_cb"))
        self.lbl_addext_hint.config(text=t("addext_hint"))
        self.lbl_substr.config(text=t("substr_label"))
        self.lbl_substr_hint.config(text=t("substr_hint"))
        self.lbl_path.config(text=t("path_label"))
        self.case_cb.config(text=t("case_cb"))
        self.btn_folder.config(text=t("btn_folder"))
        self.btn_file.config(text=t("btn_file"))
        self.btn_rename.config(text=t("btn_rename"))
        self.lbl_list.config(text=t("list_label"))
        self.lbl_credits.config(text=t("credits"))
        current = self.status.cget("text")
        if current in (STRINGS["en"]["status_init"], STRINGS["pt"]["status_init"]):
            self.status.config(text=t("status_init"))

    # -----------------------------------------------------------------------
    # Theme
    # -----------------------------------------------------------------------

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._apply_theme()
        self._save_config()

    def _apply_theme(self):
        p = self._palette()

        # Theme toggle button icon
        self.theme_btn.config(text=p["theme_icon"],
                              bg=p["theme_btn_bg"])

        # Root
        self.root.config(bg=p["root_bg"])

        # Warning frame
        self.warning_frame.config(bg=p["warn_bg"])
        self.corner_frame.config(bg=p["corner_bg"])
        self.lbl_warn1.config(bg=p["warn_bg"], fg=p["warn1_fg"])
        self.lbl_warn2.config(bg=p["warn_bg"], fg=p["warn2_fg"])
        self.lbl_warn3.config(bg=p["warn_bg"], fg=p["warn3_fg"])
        self.lang_btn.config(bg=p["lang_btn_bg"])

        # App title
        self.lbl_title.config(bg=p["root_bg"], fg=p["title_fg"])

        # Dolphin frame
        self.dolphin_frame.config(bg=p["dolphin_bg"])
        self.dolphin_cb_widget.config(
            bg=p["dolphin_bg"], fg=p["dolphin_fg"],
            activebackground=p["dolphin_bg"], activeforeground=p["dolphin_fg"],
            selectcolor=p["cb_select"],
        )

        # Add-ext frame
        self.addext_frame.config(bg=p["addext_bg"])
        self.addext_cb_widget.config(
            bg=p["addext_bg"], fg=p["addext_fg"],
            activebackground=p["addext_bg"], activeforeground=p["addext_fg"],
            selectcolor=p["cb_select"],
        )
        self.lbl_addext_hint.config(bg=p["addext_bg"], fg=p["addext_hint_fg"])
        if str(self.add_ext_entry.cget("state")) == "normal":
            self.add_ext_entry.config(bg=p["entry_bg"], fg=p["entry_fg"],
                                      insertbackground=p["entry_ins"])
        else:
            self.add_ext_entry.config(disabledbackground=p["entry_dis_bg"],
                                      disabledforeground=p["entry_dis_fg"])

        # Input frame
        self.input_frame.config(bg=p["input_bg"])
        self.lbl_substr.config(bg=p["input_bg"], fg=p["substr_fg"])
        self.lbl_substr_hint.config(bg=p["input_bg"], fg=p["substr_hint_fg"])
        if str(self.char_entry.cget("state")) == "normal":
            self.char_entry.config(bg=p["entry_bg"], fg=p["entry_fg"],
                                   insertbackground=p["entry_ins"])
        else:
            self.char_entry.config(disabledbackground=p["entry_dis_bg"],
                                   disabledforeground=p["entry_dis_fg"])

        # Case frame (path bar + case checkbox)
        self.case_frame.config(bg=p["root_bg"])
        self.lbl_path.config(bg=p["root_bg"], fg=p["substr_fg"])
        if str(self.path_entry.cget("state")) == "normal":
            self.path_entry.config(bg=p["entry_bg"], fg=p["entry_fg"],
                                   insertbackground=p["entry_ins"])
        else:
            self.path_entry.config(disabledbackground=p["entry_dis_bg"],
                                   disabledforeground=p["entry_dis_fg"])
        self.case_cb.config(
            bg=p["root_bg"], fg=p["case_fg"],
            activebackground=p["root_bg"], activeforeground=p["case_fg"],
            selectcolor=p["cb_select"],
        )

        # Button frame
        self.btn_frame.config(bg=p["root_bg"])
        self.btn_folder.config(bg=p["btn_folder_bg"])
        self.btn_file.config(bg=p["btn_file_bg"])
        self.btn_rename.config(bg=p["btn_rename_bg"])

        # List area
        self.lbl_list.config(bg=p["root_bg"], fg=p["substr_fg"])
        self.list_frame.config(bg=p["root_bg"])
        self.file_listbox.config(
            bg=p["list_bg"], fg=p["list_fg"],
            selectbackground=p["list_sel_bg"],
            selectforeground=p["list_sel_fg"],
        )

        # Status (re-apply fg if it was set to a standard color)
        self.status.config(bg=p["root_bg"])
        cur_fg = self.status.cget("fg")
        # Remap known light-mode colors to dark equivalents and vice-versa
        remap = {
            # light -> dark
            "blue":  p["status_info"],
            "green": p["status_success"],
            # dark -> light (when switching back)
            THEMES["dark"]["status_info"]:    THEMES["light"]["status_info"],
            THEMES["dark"]["status_success"]: THEMES["light"]["status_success"],
        }
        if cur_fg in remap:
            self.status.config(fg=remap[cur_fg])

        # Credits
        self.lbl_credits.config(bg=p["root_bg"], fg=p["credits_fg"])

    # -----------------------------------------------------------------------
    # Mode / mutual-exclusion logic
    # -----------------------------------------------------------------------

    def _on_dolphin_toggle(self):
        if self.fix_dolphin.get():
            self.add_ext_enabled.set(False)
        self._update_mode()
        self._save_config()

    def _on_addext_toggle(self):
        if self.add_ext_enabled.get():
            self.fix_dolphin.set(False)
        self._update_mode()
        self._save_config()

    def _update_mode(self):
        p = self._palette()
        either_on = self.fix_dolphin.get() or self.add_ext_enabled.get()
        if either_on:
            self.char_entry.config(state=tk.DISABLED,
                                   disabledbackground=p["entry_dis_bg"],
                                   disabledforeground=p["entry_dis_fg"])
            self.case_cb.config(state=tk.DISABLED)
        else:
            self.char_entry.config(state=tk.NORMAL,
                                   bg=p["entry_bg"], fg=p["entry_fg"],
                                   insertbackground=p["entry_ins"])
            self.case_cb.config(state=tk.NORMAL)
        if self.add_ext_enabled.get():
            self.add_ext_entry.config(state=tk.NORMAL,
                                      bg=p["entry_bg"], fg=p["entry_fg"],
                                      insertbackground=p["entry_ins"])
        else:
            self.add_ext_entry.config(state=tk.DISABLED,
                                      disabledbackground=p["entry_dis_bg"],
                                      disabledforeground=p["entry_dis_fg"])
        self._rescan()

    def _rescan(self):
        if self.base_folder:
            self.scan_files()

    # -----------------------------------------------------------------------
    # Folder picker (Linux: try kdialog for native KDE tree view)
    # -----------------------------------------------------------------------

    def _pick_folder(self, initial=""):
        """
        On Linux, try kdialog (native KDE/Dolphin tree dialog) first,
        then fall back to tkinter's askdirectory.
        On Windows/macOS always use tkinter.
        """
        start = initial if (initial and os.path.isdir(initial)) else \
                os.path.expanduser("~")
        if platform.system() == "Linux" and shutil.which("kdialog"):
            try:
                result = subprocess.run(
                    ["kdialog", "--getexistingdirectory", start],
                    capture_output=True, text=True, timeout=120
                )
                if result.returncode == 0:
                    folder = result.stdout.strip()
                    if folder and os.path.isdir(folder):
                        return folder
            except Exception:
                pass
        return filedialog.askdirectory(
            title=self._t("btn_folder"),
            initialdir=start,
        )

    # -----------------------------------------------------------------------
    # Core logic
    # -----------------------------------------------------------------------

    def _get_add_ext(self):
        if not self.add_ext_enabled.get():
            return ""
        return normalise_extension(self.add_ext_entry.get())

    def _build_entry(self, full_path, old_name):
        substring = self.char_entry.get()
        add_ext   = self._get_add_ext()

        after_dolphin = fix_dolphin_duplicate(old_name) if self.fix_dolphin.get() else old_name

        if substring:
            if self.case_sensitive.get():
                after_sub = after_dolphin.replace(substring, "")
            else:
                pat = re.compile(re.escape(substring), re.IGNORECASE)
                after_sub = pat.sub("", after_dolphin)
        else:
            after_sub = after_dolphin

        if add_ext and has_no_extension(after_sub):
            new_name = after_sub + add_ext
        else:
            new_name = after_sub

        if new_name == old_name:
            return None
        return (full_path, old_name, new_name)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _load_folder(self, folder):
        """Common path for loading a folder, whether chosen via the picker
        dialog or typed/pasted directly into the address bar."""
        self.base_folder  = folder
        self.last_folder  = folder
        self.path_var.set(folder)
        self._save_config()
        self.status.config(
            text=self._t("status_scanning").format(folder=folder),
            fg=self._sc("info"))
        self.scan_files()

    def _load_file(self, file_path):
        """Common path for loading a single file, whether chosen via the
        picker dialog or typed/pasted directly into the address bar."""
        # Remember the directory of the selected file
        self.last_folder = os.path.dirname(file_path)
        self.path_var.set(file_path)
        self._save_config()

        self.base_folder = None
        self.files = []
        self.file_listbox.delete(0, tk.END)

        old_name = os.path.basename(file_path)
        entry = self._build_entry(file_path, old_name)

        if entry:
            self.files.append(entry)
            _, old, new = entry
            self.file_listbox.insert(tk.END, f"{old}  ->  {new}")
            self.status.config(text=self._t("status_found1"),
                               fg=self._sc("info"))
        else:
            self.status.config(text=self._t("status_no_change"),
                               fg=self._sc("success"))

    def select_folder(self):
        folder = self._pick_folder(self.last_folder)
        if not folder:
            return
        self._load_folder(folder)

    def select_file(self):
        initial = self.last_folder if (self.last_folder and
                                        os.path.isdir(self.last_folder)) else None
        file_path = filedialog.askopenfilename(
            title=self._t("btn_file"),
            initialdir=initial,
        )
        if not file_path:
            return
        self._load_file(file_path)

    def _on_path_entry_submit(self, event=None):
        """Handle Enter in the address bar: load whatever path was typed
        or pasted in, as a folder or a single file."""
        raw = self.path_var.get().strip()
        if not raw:
            return
        path = os.path.expanduser(os.path.expandvars(raw))
        if os.path.isdir(path):
            self._load_folder(path)
        elif os.path.isfile(path):
            self._load_file(path)
        else:
            messagebox.showwarning(self._t("warn_bad_path"),
                                   self._t("warn_bad_path_msg"))

    def scan_files(self):
        if not self.base_folder:
            messagebox.showwarning(self._t("warn_no_folder"),
                                   self._t("warn_no_folder_msg"))
            return

        add_ext = self._get_add_ext()
        if self.add_ext_enabled.get() and not add_ext:
            messagebox.showwarning(self._t("warn_no_ext"),
                                   self._t("warn_no_ext_msg"))
            return

        self.files = []
        self.file_listbox.delete(0, tk.END)
        found_count = 0

        try:
            for file in sorted(os.listdir(self.base_folder)):
                full_path = os.path.join(self.base_folder, file)
                if not os.path.isfile(full_path):
                    continue
                entry = self._build_entry(full_path, file)
                if entry:
                    self.files.append(entry)
                    _, old, new = entry
                    self.file_listbox.insert(tk.END, f"{old}  ->  {new}")
                    found_count += 1
        except Exception as e:
            messagebox.showerror("Error", self._t("err_scan").format(e=e))
            return

        if found_count == 0:
            self.status.config(text=self._t("status_none"),
                               fg=self._sc("success"))
        else:
            self.status.config(
                text=self._t("status_found").format(n=found_count),
                fg=self._sc("info"))

    def rename_files(self):
        if not self.files:
            messagebox.showwarning(self._t("warn_no_files"),
                                   self._t("warn_no_files_msg"))
            return

        substring = self.char_entry.get()
        add_ext   = self._get_add_ext()

        ext_changes = [
            (old, new) for _, old, new in self.files
            if extension_changed(old, new)
            and not has_no_extension(fix_dolphin_duplicate(old))
        ]
        if ext_changes:
            sample = "\n".join(
                f"  {old}  ->  {new}" for old, new in ext_changes[:8])
            if len(ext_changes) > 8:
                sample += "\n" + self._t("extchg_more").format(
                    n=len(ext_changes) - 8)
            proceed = messagebox.askyesno(
                self._t("extchg_title"),
                self._t("extchg_body").format(
                    n=len(ext_changes), sample=sample),
                icon="warning",
            )
            if not proceed:
                return

        notes = []
        if substring:
            notes.append(self._t("note_substr").format(s=substring))
        if self.fix_dolphin.get():
            notes.append(self._t("note_dolphin"))
        if add_ext:
            ext_targets = [old for _, old, _ in self.files
                           if has_no_extension(fix_dolphin_duplicate(old))]
            notes.append(self._t("note_addext").format(
                ext=add_ext, n=len(ext_targets)))
        notes_text = "\n".join(f"  - {n}" for n in notes)

        confirm = messagebox.askyesno(
            self._t("confirm_title"),
            self._t("confirm_body").format(
                n=len(self.files), notes=notes_text),
        )
        if not confirm:
            return

        success = 0
        failed  = 0
        errors  = []

        for full_path, old_name, new_name in self.files:
            try:
                directory = os.path.dirname(full_path)
                if not new_name.strip():
                    errors.append(self._t("err_empty").format(f=old_name))
                    failed += 1
                    continue
                final_path, _ = safe_target_path(directory, new_name)
                os.rename(full_path, final_path)
                success += 1
            except Exception as e:
                errors.append(f"{old_name}: {str(e)}")
                failed += 1

        result = self._t("result_ok").format(n=success)
        if failed > 0:
            result += self._t("result_fail").format(n=failed)
            if errors:
                result += self._t("result_errors") + "\n".join(errors[:10])

        messagebox.showinfo(self._t("result_title"), result)
        self.status.config(
            text=self._t("status_done").format(ok=success, fail=failed),
            fg=self._sc("success"))

        self.files = []
        self.file_listbox.delete(0, tk.END)


if __name__ == "__main__":
    # Hidden headless flag, consumed by build.bat / build.sh to export the
    # embedded icon to .ico / .svg without ever opening a Tk window.
    if "--generate-icon" in sys.argv:
        idx = sys.argv.index("--generate-icon")
        args = sys.argv[idx + 1:]
        ico_out = next((a.split("=", 1)[1] for a in args if a.startswith("--ico=")), None)
        svg_out = next((a.split("=", 1)[1] for a in args if a.startswith("--svg=")), None)
        ok = generate_icon_files(ico_path=ico_out, svg_path=svg_out)
        sys.exit(0 if ok else 1)

    root = tk.Tk()

    # Set the live window/taskbar icon from the embedded teal PNG so the
    # running app matches the .exe file icon (no default Tk icon, no black).
    _icon_img = _load_icon_image()
    if _icon_img is not None:
        try:
            from PIL import ImageTk
            _icon_photo = ImageTk.PhotoImage(_icon_img)
            root.iconphoto(True, _icon_photo)
        except Exception:
            pass

    app = CustomCharacterRemover(root)
    root.mainloop()
