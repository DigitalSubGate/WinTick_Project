import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import pygame
import winsound
import os
import json
import threading
import time
import pystray
from PIL import Image, ImageDraw
from math import sin, cos, radians, pi
import pyautogui
import ctypes
from ctypes import wintypes
import sys
import subprocess

# Путь к файлу иконки
ICON_PATH = "icon.ico"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

try:
    pygame.mixer.init()
except:
    pass

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040

def prevent_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

def allow_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def check_single_instance():
    mutex_name = "WinTick_SingleInstance_Mutex"
    try:
        kernel32 = ctypes.windll.kernel32
        mutex = kernel32.CreateMutexW(None, False, mutex_name)
        if mutex and kernel32.GetLastError() == 183:
            messagebox.showwarning("WinTick", "Application is already running!")
            sys.exit(0)
    except Exception:
        pass

check_single_instance()

# ====================== МНОГОЯЗЫЧНОСТЬ ======================
class I18n:
    def __init__(self, lang='ru'):
        self.lang = lang
        self.strings = {
            'ru': {
                'alarm': 'Будильник',
                'timer': 'Таймер',
                'about': 'О программе',
                'new_alarm': 'Новый будильник',
                'new_timer': 'Новый таймер',
                'edit_alarm': 'Редактирование будильника',
                'edit_timer': 'Редактирование таймера',
                'set_time': 'Установите время',
                'name': 'Название:',
                'sound': 'Мелодия:',
                'system_sound': 'Системная мелодия:',
                'use_custom': 'Использовать свой файл',
                'browse': 'Обзор...',
                'snooze': 'Отложить на (мин):',
                'repeat': 'Повторение',
                'on_finish': 'Действие по окончании',
                'on_trigger': 'Действие по срабатыванию',
                'launch_app': 'Запустить программу',
                'program': 'Программа:',
                'arguments': 'Аргументы:',
                'start': 'Запустить',
                'save': 'Сохранить',
                'cancel': 'Отмена',
                'window_size': 'Размер окна:',
                'font': 'Шрифт:',
                'prevent_sleep': 'Не давать экрану заснуть',
                'mode': 'Режим:',
                'no_movement': 'Без движения',
                'line': 'Линия',
                'circle': 'Круг',
                'zigzag': 'Зигзаг',
                'small': 'Маленький',
                'medium': 'Средний',
                'large': 'Большой',
                'on': 'ВКЛ',
                'off': 'ВЫКЛ',
                'once': 'однократно',
                'days': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                'error': 'Ошибка',
                'warning': 'Предупреждение',
                'invalid_time': 'Введите корректное время',
                'minutes_seconds': 'Минуты и секунды от 0 до 59',
                'time_positive': 'Введите время больше 0',
                'select_sound': 'Выберите мелодию',
                'file_not_found': 'Файл не найден',
                'play_error': 'Не удалось воспроизвести',
                'launch_error': 'Не удалось запустить',
                'app_running': 'Приложение уже запущено!',
                'volume': 'Громкость',
                'show': 'Показать',
                'exit': 'Выход',
                'pause': 'ПАУЗА',
                'reset': 'СБРОС',
                'stop': 'СТОП',
                'settings': 'Настройки',
                'global_prevent': 'Постоянно не давать экрану заснуть',
            },
            'en': {
                'alarm': 'Alarm',
                'timer': 'Timer',
                'about': 'About',
                'new_alarm': 'New alarm',
                'new_timer': 'New timer',
                'edit_alarm': 'Edit alarm',
                'edit_timer': 'Edit timer',
                'set_time': 'Set time',
                'name': 'Name:',
                'sound': 'Sound:',
                'system_sound': 'System sound:',
                'use_custom': 'Use custom file',
                'browse': 'Browse...',
                'snooze': 'Snooze (min):',
                'repeat': 'Repeat',
                'on_finish': 'On finish',
                'on_trigger': 'On trigger',
                'launch_app': 'Launch program',
                'program': 'Program:',
                'arguments': 'Arguments:',
                'start': 'Start',
                'save': 'Save',
                'cancel': 'Cancel',
                'window_size': 'Window size:',
                'font': 'Font:',
                'prevent_sleep': 'Prevent sleep',
                'mode': 'Mode:',
                'no_movement': 'No movement',
                'line': 'Line',
                'circle': 'Circle',
                'zigzag': 'Zigzag',
                'small': 'Small',
                'medium': 'Medium',
                'large': 'Large',
                'on': 'ON',
                'off': 'OFF',
                'once': 'once',
                'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'error': 'Error',
                'warning': 'Warning',
                'invalid_time': 'Enter valid time',
                'minutes_seconds': 'Minutes and seconds must be 0-59',
                'time_positive': 'Enter time greater than 0',
                'select_sound': 'Select a sound',
                'file_not_found': 'File not found',
                'play_error': 'Could not play',
                'launch_error': 'Could not launch',
                'app_running': 'Application is already running!',
                'volume': 'Volume',
                'show': 'Show',
                'exit': 'Exit',
                'pause': 'PAUSE',
                'reset': 'RESET',
                'stop': 'STOP',
                'settings': 'Settings',
                'global_prevent': 'Always prevent sleep',
            },
            'de': {
                'alarm': 'Wecker',
                'timer': 'Timer',
                'about': 'Über',
                'new_alarm': 'Neuer Wecker',
                'new_timer': 'Neuer Timer',
                'edit_alarm': 'Wecker bearbeiten',
                'edit_timer': 'Timer bearbeiten',
                'set_time': 'Zeit einstellen',
                'name': 'Name:',
                'sound': 'Klang:',
                'system_sound': 'Systemklang:',
                'use_custom': 'Eigene Datei verwenden',
                'browse': 'Durchsuchen...',
                'snooze': 'Schlummern (Min):',
                'repeat': 'Wiederholung',
                'on_finish': 'Bei Ende',
                'on_trigger': 'Bei Auslösung',
                'launch_app': 'Programm starten',
                'program': 'Programm:',
                'arguments': 'Argumente:',
                'start': 'Starten',
                'save': 'Speichern',
                'cancel': 'Abbrechen',
                'window_size': 'Fenstergröße:',
                'font': 'Schriftart:',
                'prevent_sleep': 'Bildschirm wach halten',
                'mode': 'Modus:',
                'no_movement': 'Keine Bewegung',
                'line': 'Linie',
                'circle': 'Kreis',
                'zigzag': 'Zickzack',
                'small': 'Klein',
                'medium': 'Mittel',
                'large': 'Groß',
                'on': 'EIN',
                'off': 'AUS',
                'once': 'einmal',
                'days': ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'],
                'error': 'Fehler',
                'warning': 'Warnung',
                'invalid_time': 'Gültige Zeit eingeben',
                'minutes_seconds': 'Minuten und Sekunden 0-59',
                'time_positive': 'Zeit > 0 eingeben',
                'select_sound': 'Klang auswählen',
                'file_not_found': 'Datei nicht gefunden',
                'play_error': 'Wiedergabe fehlgeschlagen',
                'launch_error': 'Start fehlgeschlagen',
                'app_running': 'Anwendung läuft bereits!',
                'volume': 'Lautstärke',
                'show': 'Anzeigen',
                'exit': 'Beenden',
                'pause': 'PAUSE',
                'reset': 'ZURÜCKSETZEN',
                'stop': 'STOPP',
                'settings': 'Einstellungen',
                'global_prevent': 'Bildschirm immer wach halten',
            },
            'fr': {
                'alarm': 'Alarme',
                'timer': 'Minuteur',
                'about': 'À propos',
                'new_alarm': 'Nouvelle alarme',
                'new_timer': 'Nouveau minuteur',
                'edit_alarm': 'Modifier l\'alarme',
                'edit_timer': 'Modifier le minuteur',
                'set_time': 'Définir l\'heure',
                'name': 'Nom:',
                'sound': 'Son:',
                'system_sound': 'Son système:',
                'use_custom': 'Utiliser un fichier personnel',
                'browse': 'Parcourir...',
                'snooze': 'Répéter (min):',
                'repeat': 'Répétition',
                'on_finish': 'À la fin',
                'on_trigger': 'Au déclenchement',
                'launch_app': 'Lancer un programme',
                'program': 'Programme:',
                'arguments': 'Arguments:',
                'start': 'Démarrer',
                'save': 'Enregistrer',
                'cancel': 'Annuler',
                'window_size': 'Taille de la fenêtre:',
                'font': 'Police:',
                'prevent_sleep': 'Empêcher le sommeil',
                'mode': 'Mode:',
                'no_movement': 'Aucun mouvement',
                'line': 'Ligne',
                'circle': 'Cercle',
                'zigzag': 'Zigzag',
                'small': 'Petit',
                'medium': 'Moyen',
                'large': 'Grand',
                'on': 'ACT',
                'off': 'DES',
                'once': 'une fois',
                'days': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
                'error': 'Erreur',
                'warning': 'Avertissement',
                'invalid_time': 'Entrez une heure valide',
                'minutes_seconds': 'Minutes et secondes 0-59',
                'time_positive': 'Entrez un temps > 0',
                'select_sound': 'Choisissez un son',
                'file_not_found': 'Fichier introuvable',
                'play_error': 'Impossible de lire',
                'launch_error': 'Impossible de lancer',
                'app_running': 'L\'application est déjà en cours d\'exécution!',
                'volume': 'Volume',
                'show': 'Afficher',
                'exit': 'Quitter',
                'pause': 'PAUSE',
                'reset': 'RÉINITIALISER',
                'stop': 'ARRÊT',
                'settings': 'Paramètres',
                'global_prevent': 'Toujours empêcher le sommeil',
            },
            'es': {
                'alarm': 'Alarma',
                'timer': 'Temporizador',
                'about': 'Acerca de',
                'new_alarm': 'Nueva alarma',
                'new_timer': 'Nuevo temporizador',
                'edit_alarm': 'Editar alarma',
                'edit_timer': 'Editar temporizador',
                'set_time': 'Establecer hora',
                'name': 'Nombre:',
                'sound': 'Sonido:',
                'system_sound': 'Sonido del sistema:',
                'use_custom': 'Usar archivo propio',
                'browse': 'Examinar...',
                'snooze': 'Posponer (min):',
                'repeat': 'Repetición',
                'on_finish': 'Al finalizar',
                'on_trigger': 'Al activarse',
                'launch_app': 'Iniciar programa',
                'program': 'Programa:',
                'arguments': 'Argumentos:',
                'start': 'Iniciar',
                'save': 'Guardar',
                'cancel': 'Cancelar',
                'window_size': 'Tamaño de ventana:',
                'font': 'Fuente:',
                'prevent_sleep': 'Evitar suspensión',
                'mode': 'Modo:',
                'no_movement': 'Sin movimiento',
                'line': 'Línea',
                'circle': 'Círculo',
                'zigzag': 'Zigzag',
                'small': 'Pequeño',
                'medium': 'Mediano',
                'large': 'Grande',
                'on': 'ENC',
                'off': 'APG',
                'once': 'una vez',
                'days': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                'error': 'Error',
                'warning': 'Advertencia',
                'invalid_time': 'Ingrese hora válida',
                'minutes_seconds': 'Minutos y segundos 0-59',
                'time_positive': 'Ingrese tiempo > 0',
                'select_sound': 'Seleccione un sonido',
                'file_not_found': 'Archivo no encontrado',
                'play_error': 'No se pudo reproducir',
                'launch_error': 'No se pudo iniciar',
                'app_running': '¡La aplicación ya está en ejecución!',
                'volume': 'Volumen',
                'show': 'Mostrar',
                'exit': 'Salir',
                'pause': 'PAUSA',
                'reset': 'REINICIAR',
                'stop': 'PARAR',
                'settings': 'Configuración',
                'global_prevent': 'Evitar suspensión siempre',
            },
            'zh': {
                'alarm': '闹钟',
                'timer': '计时器',
                'about': '关于',
                'new_alarm': '新建闹钟',
                'new_timer': '新建计时器',
                'edit_alarm': '编辑闹钟',
                'edit_timer': '编辑计时器',
                'set_time': '设置时间',
                'name': '名称：',
                'sound': '铃声：',
                'system_sound': '系统铃声：',
                'use_custom': '使用自定义文件',
                'browse': '浏览...',
                'snooze': '贪睡（分钟）：',
                'repeat': '重复',
                'on_finish': '结束时',
                'on_trigger': '触发时',
                'launch_app': '启动程序',
                'program': '程序：',
                'arguments': '参数：',
                'start': '启动',
                'save': '保存',
                'cancel': '取消',
                'window_size': '窗口大小：',
                'font': '字体：',
                'prevent_sleep': '阻止屏幕休眠',
                'mode': '模式：',
                'no_movement': '无移动',
                'line': '直线',
                'circle': '圆形',
                'zigzag': '锯齿',
                'small': '小',
                'medium': '中',
                'large': '大',
                'on': '开',
                'off': '关',
                'once': '单次',
                'days': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                'error': '错误',
                'warning': '警告',
                'invalid_time': '请输入有效时间',
                'minutes_seconds': '分钟和秒必须在0-59之间',
                'time_positive': '请输入大于0的时间',
                'select_sound': '请选择铃声',
                'file_not_found': '文件未找到',
                'play_error': '无法播放',
                'launch_error': '无法启动',
                'app_running': '应用程序已在运行！',
                'volume': '音量',
                'show': '显示',
                'exit': '退出',
                'pause': '暂停',
                'reset': '重置',
                'stop': '停止',
                'settings': '设置',
                'global_prevent': '始终阻止休眠',
            },
            'ar': {
                'alarm': 'منبه',
                'timer': 'مؤقت',
                'about': 'حول',
                'new_alarm': 'منبه جديد',
                'new_timer': 'مؤقت جديد',
                'edit_alarm': 'تعديل المنبه',
                'edit_timer': 'تعديل المؤقت',
                'set_time': 'ضبط الوقت',
                'name': 'الاسم:',
                'sound': 'الصوت:',
                'system_sound': 'صوت النظام:',
                'use_custom': 'استخدام ملف مخصص',
                'browse': 'تصفح...',
                'snooze': 'تأجيل (دقائق):',
                'repeat': 'تكرار',
                'on_finish': 'عند الانتهاء',
                'on_trigger': 'عند التشغيل',
                'launch_app': 'تشغيل برنامج',
                'program': 'البرنامج:',
                'arguments': 'الوسائط:',
                'start': 'بدء',
                'save': 'حفظ',
                'cancel': 'إلغاء',
                'window_size': 'حجم النافذة:',
                'font': 'الخط:',
                'prevent_sleep': 'منع السكون',
                'mode': 'الوضع:',
                'no_movement': 'بدون حركة',
                'line': 'خط',
                'circle': 'دائرة',
                'zigzag': 'متعرج',
                'small': 'صغير',
                'medium': 'متوسط',
                'large': 'كبير',
                'on': 'تشغيل',
                'off': 'إيقاف',
                'once': 'مرة واحدة',
                'days': ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'],
                'error': 'خطأ',
                'warning': 'تحذير',
                'invalid_time': 'أدخل وقتًا صحيحًا',
                'minutes_seconds': 'الدقائق والثواني يجب أن تكون بين 0-59',
                'time_positive': 'أدخل وقتًا أكبر من 0',
                'select_sound': 'اختر صوتًا',
                'file_not_found': 'الملف غير موجود',
                'play_error': 'تعذر التشغيل',
                'launch_error': 'تعذر التشغيل',
                'app_running': 'التطبيق قيد التشغيل بالفعل!',
                'volume': 'مستوى الصوت',
                'show': 'عرض',
                'exit': 'خروج',
                'pause': 'إيقاف مؤقت',
                'reset': 'إعادة تعيين',
                'stop': 'إيقاف',
                'settings': 'الإعدادات',
                'global_prevent': 'منع السكون دائمًا',
            }
        }
    def tr(self, key):
        return self.strings.get(self.lang, self.strings['ru']).get(key, f'?{key}?')

    def set_language(self, lang):
        self.lang = lang

i18n = I18n('ru')

# ====================== КНОПКА ВЫБОРА ЯЗЫКА ======================
class LanguageMenu(tk.Label):
    def __init__(self, master, colors, app, **kwargs):
        super().__init__(master, text='🌐', font=('Segoe UI', 16), bg=colors['card'], fg=colors['text'], cursor='hand2')
        self.app = app
        self.colors = colors
        self.bind('<Button-1>', self.show_menu)
        self.menu = tk.Menu(self, tearoff=0, bg=colors['card'], fg=colors['text'])
        self.build_menu()

    def build_menu(self):
        languages = [
            ('ru', '🇷🇺 Русский'),
            ('en', '🇬🇧 English'),
            ('de', '🇩🇪 Deutsch'),
            ('fr', '🇫🇷 Français'),
            ('es', '🇪🇸 Español'),
            ('zh', '🇨🇳 中文'),
            ('ar', '🇸🇦 العربية'),
        ]
        for code, name in languages:
            self.menu.add_command(label=name, command=lambda c=code: self.change_language(c))

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def change_language(self, lang_code):
        i18n.set_language(lang_code)
        self.app.settings['language'] = lang_code
        self.app.rebuild_ui()
        self.app.save_data()

# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======================
def create_styled_button(master, text='', command=None, bg='#1a73e8', fg='white',
                         font=('Roboto', 10, 'bold'), width=10, height=1, **kwargs):
    return tk.Button(master, text=text, command=command, bg=bg, fg=fg,
                     font=font, width=width, height=height,
                     relief='raised', bd=3, activebackground=bg,
                     activeforeground=fg, **kwargs)

class VolumeControl(tk.Toplevel):
    def __init__(self, parent, current_volume, callback):
        super().__init__(parent)
        self.title(i18n.tr('volume'))
        self.geometry("300x100")
        self.configure(bg=parent.colors['card'])
        self.transient(parent)
        self.grab_set()
        self.callback = callback
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() - 320
        y = parent.winfo_rooty() + 50
        self.geometry(f"+{x}+{y}")
        tk.Label(self, text=i18n.tr('volume'), bg=self['bg'], fg=parent.colors['text'],
                 font=('Roboto', 12)).pack(pady=5)
        self.volume_var = tk.IntVar(value=current_volume)
        scale = tk.Scale(self, from_=0, to=100, orient='horizontal',
                         variable=self.volume_var, bg=self['bg'], fg=parent.colors['text'],
                         length=250, command=self.on_scale)
        scale.pack(pady=5)

    def on_scale(self, val):
        self.callback(int(val))

class BigTimer(tk.Toplevel):
    def __init__(self, parent, timer_data, colors, settings):
        super().__init__(parent)
        self.timer = timer_data
        self.colors = colors
        self.settings = settings
        self.title(self.timer['name'])
        size_map = {i18n.tr('small'): 400, i18n.tr('medium'): 500, i18n.tr('large'): 600}
        self.size = size_map.get(timer_data.get('size', i18n.tr('medium')), 500)
        self.geometry(f"{self.size}x{self.size+100}")
        self.configure(bg=colors['bg'])
        self.attributes("-topmost", self.settings.get('always_on_top', True))
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.size) // 2
        y = (self.winfo_screenheight() - (self.size+100)) // 2
        self.geometry(f"+{x}+{y}")
        font_map = {i18n.tr('small'): 45, i18n.tr('medium'): 65, i18n.tr('large'): 85}
        self.font_size = font_map.get(timer_data.get('font', i18n.tr('medium')), 65)
        canvas_size = self.size - 100
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size,
                               bg=colors['bg'], highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.create_oval(20, 20, canvas_size-20, canvas_size-20,
                                outline='#444', width=12)
        self.arc = self.canvas.create_arc(20, 20, canvas_size-20, canvas_size-20,
                                         start=90, extent=359,
                                         outline=colors['accent'], width=12, style='arc')
        self.txt = self.canvas.create_text(canvas_size//2, canvas_size//2,
                                          text='', fill=colors['text'],
                                          font=('Roboto', self.font_size, 'bold'))
        btns = tk.Frame(self, bg=colors['bg'])
        btns.pack(pady=10)
        self.btn_p = create_styled_button(btns, text=i18n.tr('pause'), command=self.toggle,
                                          bg=colors['accent'], fg='black',
                                          width=12, height=1, font=('Roboto', 12, 'bold'))
        self.btn_p.pack(side='left', padx=10)
        self.reset_btn = create_styled_button(btns, text=i18n.tr('reset'), command=self.reset,
                                              bg=colors['btn'], fg=colors['text'],
                                              width=10, height=1, font=('Roboto', 12))
        self.reset_btn.pack(side='left', padx=10)
        self.update_big_ui()

    def toggle(self):
        self.timer['run'] = not self.timer['run']
        text = i18n.tr('start') if not self.timer['run'] else i18n.tr('pause')
        self.btn_p.config(text=text.upper(), bg='#5f6368' if not self.timer['run'] else self.colors['accent'])

    def reset(self):
        self.timer['rem'] = self.timer['total']

    def update_big_ui(self):
        if not self.winfo_exists(): return
        m, s = divmod(self.timer['rem'], 60)
        h = m // 60
        m %= 60
        if h > 0:
            self.canvas.itemconfig(self.txt, text=f"{h:01d}:{m:02d}:{s:02d}")
        else:
            self.canvas.itemconfig(self.txt, text=f"{m:02d}:{s:02d}")
        ext = (self.timer['rem'] / self.timer['total'] * 359.9) if self.timer['total'] else 0
        self.canvas.itemconfig(self.arc, extent=ext)
        self.after(500, self.update_big_ui)

# ====================== ДИАЛОГ ДОБАВЛЕНИЯ ТАЙМЕРА ======================
class AddTimerDialog(tk.Toplevel):
    # (Полный код из частей 2-3)
    def __init__(self, parent, colors, sounds, callback, edit_data=None, edit_index=None):
        super().__init__(parent)
        self.parent = parent
        self.colors = colors
        self.sounds = sounds
        self.callback = callback
        self.edit_data = edit_data
        self.edit_index = edit_index
        self.title(i18n.tr('edit_timer') if edit_data else i18n.tr('new_timer'))
        self.geometry("450x650")
        self.configure(bg=colors['card'])
        self.transient(parent)
        self.grab_set()
        self.parent.active_dialog = self

        self.update_idletasks()
        x = (self.winfo_screenwidth() - 450) // 2
        y = (self.winfo_screenheight() - 650) // 2
        self.geometry(f"+{x}+{y}")

        tk.Label(self, text=i18n.tr('edit_timer') if edit_data else i18n.tr('new_timer'),
                 bg=colors['card'], fg=colors['accent'],
                 font=('Roboto', 16, 'bold')).pack(pady=10)

        # Название
        name_frame = tk.Frame(self, bg=colors['card'])
        name_frame.pack(pady=5, fill='x', padx=20)
        tk.Label(name_frame, text=i18n.tr('name'), bg=colors['card'], fg=colors['text']).pack(anchor='w')
        self.name_entry = tk.Entry(name_frame, width=30, bg=colors['bg'], fg=colors['text'],
                                   font=('Roboto', 12))
        self.name_entry.pack(fill='x', pady=5)
        if edit_data:
            self.name_entry.insert(0, edit_data.get('name', i18n.tr('timer')))
        else:
            self.name_entry.insert(0, i18n.tr('timer'))

        # Время
        time_frame = tk.Frame(self, bg=colors['card'])
        time_frame.pack(pady=10)

        vcmd = (self.register(self._validate), '%S')

        if edit_data:
            total = edit_data.get('total', 0)
            hh = total // 3600
            mm = (total % 3600) // 60
            ss = total % 60
        else:
            hh = mm = ss = 0

        self.hours = tk.Entry(time_frame, width=3, font=('Roboto', 24, 'bold'),
                              bg=colors['bg'], fg=colors['text'], bd=0, justify='center',
                              validate='key', validatecommand=vcmd)
        self.hours.insert(0, str(hh))
        self.hours.pack(side='left')
        tk.Label(time_frame, text='ч', bg=colors['card'], fg='gray').pack(side='left')

        self.minutes = tk.Entry(time_frame, width=3, font=('Roboto', 24, 'bold'),
                                bg=colors['bg'], fg=colors['text'], bd=0, justify='center',
                                validate='key', validatecommand=vcmd)
        self.minutes.insert(0, str(mm))
        self.minutes.pack(side='left')
        tk.Label(time_frame, text='м', bg=colors['card'], fg='gray').pack(side='left')

        self.seconds = tk.Entry(time_frame, width=3, font=('Roboto', 24, 'bold'),
                                bg=colors['bg'], fg=colors['text'], bd=0, justify='center',
                                validate='key', validatecommand=vcmd)
        self.seconds.insert(0, str(ss))
        self.seconds.pack(side='left')
        tk.Label(time_frame, text='с', bg=colors['card'], fg='gray').pack(side='left')

        # Мелодия
        sound_main_frame = tk.LabelFrame(self, text=i18n.tr('sound'), bg=colors['card'],
                                          fg=colors['text'], font=('Roboto', 10))
        sound_main_frame.pack(pady=10, padx=20, fill='x')

        self.use_custom_sound = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(sound_main_frame, text=i18n.tr('use_custom'),
                            variable=self.use_custom_sound,
                            bg=colors['card'], fg=colors['text'], selectcolor=colors['bg'],
                            command=self.toggle_sound_source)
        cb.pack(anchor='w', pady=2)

        self.system_frame = tk.Frame(sound_main_frame, bg=colors['card'])
        self.system_frame.pack(fill='x', pady=5)
        tk.Label(self.system_frame, text=i18n.tr('system_sound'), bg=colors['card'], fg=colors['text']).pack(side='left')
        self.sound_var = tk.StringVar(value='Alarm01.wav')
        self.sound_combo = ttk.Combobox(self.system_frame, textvariable=self.sound_var, values=self.sounds,
                                         state='readonly', width=18)
        self.sound_combo.pack(side='left', padx=5)
        self.sound_combo.bind('<<ComboboxSelected>>', self.on_sound_selected)

        self.custom_frame = tk.Frame(sound_main_frame, bg=colors['card'])
        self.custom_path = tk.StringVar()
        self.custom_label = tk.Label(self.custom_frame, text=i18n.tr('file_not_found'), bg=colors['card'],
                                      fg=colors['text'], wraplength=300)
        self.custom_label.pack(side='left', padx=5)
        self.browse_btn = create_styled_button(self.custom_frame, text=i18n.tr('browse'),
                                                command=self.browse_custom_sound,
                                                bg=colors['btn'], fg=colors['text'],
                                                width=8, height=1, font=('Roboto', 9))
        self.browse_btn.pack(side='right', padx=5)

        self.preview_btn = tk.Button(sound_main_frame, text='▶', command=self.toggle_preview, width=2)
        self.preview_btn.pack(pady=5)

        # Настройки таймера
        settings_frame = tk.LabelFrame(self, text=i18n.tr('settings'), bg=colors['card'],
                                        fg=colors['text'], font=('Roboto', 10))
        settings_frame.pack(pady=10, padx=20, fill='x')

        size_frame = tk.Frame(settings_frame, bg=colors['card'])
        size_frame.pack(fill='x', pady=2)
        tk.Label(size_frame, text=i18n.tr('window_size'), bg=colors['card'], fg=colors['text']).pack(side='left')
        self.size_var = tk.StringVar(value=edit_data.get('size', i18n.tr('medium')) if edit_data else i18n.tr('medium'))
        ttk.Combobox(size_frame, textvariable=self.size_var, values=[i18n.tr('small'), i18n.tr('medium'), i18n.tr('large')],
                     state='readonly', width=10).pack(side='right')

        font_frame = tk.Frame(settings_frame, bg=colors['card'])
        font_frame.pack(fill='x', pady=2)
        tk.Label(font_frame, text=i18n.tr('font'), bg=colors['card'], fg=colors['text']).pack(side='left')
        self.font_var = tk.StringVar(value=edit_data.get('font', i18n.tr('medium')) if edit_data else i18n.tr('medium'))
        ttk.Combobox(font_frame, textvariable=self.font_var, values=[i18n.tr('small'), i18n.tr('medium'), i18n.tr('large')],
                     state='readonly', width=10).pack(side='right')

        self.prevent_sleep_var = tk.BooleanVar(value=edit_data.get('prevent_sleep', False) if edit_data else False)
        prevent_frame = tk.Frame(settings_frame, bg=colors['card'])
        prevent_frame.pack(fill='x', pady=5)
        tk.Checkbutton(prevent_frame, text=i18n.tr('prevent_sleep'),
                       variable=self.prevent_sleep_var,
                       bg=colors['card'], fg=colors['text'], selectcolor=colors['bg']).pack(anchor='w')

        self.move_mode_var = tk.StringVar(value=edit_data.get('move_mode', 'line') if edit_data else 'line')
        mode_frame = tk.Frame(settings_frame, bg=colors['card'])
        mode_frame.pack(fill='x', pady=5)
        tk.Label(mode_frame, text=i18n.tr('mode'), bg=colors['card'], fg=colors['text']).pack(side='left')
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.move_mode_var,
                                   values=[i18n.tr('no_movement'), i18n.tr('line'), i18n.tr('circle'), i18n.tr('zigzag')],
                                   state='readonly', width=12)
        mode_combo.pack(side='right')

        # Запуск приложения
        app_frame = tk.LabelFrame(self, text=i18n.tr('on_finish'), bg=colors['card'],
                                   fg=colors['text'], font=('Roboto', 10))
        app_frame.pack(pady=10, padx=20, fill='x')

        self.launch_app_var = tk.BooleanVar(value=edit_data.get('launch_app', False) if edit_data else False)
        launch_cb = tk.Checkbutton(app_frame, text=i18n.tr('launch_app'),
                                    variable=self.launch_app_var,
                                    bg=colors['card'], fg=colors['text'], selectcolor=colors['bg'],
                                    command=self.toggle_app_options)
        launch_cb.pack(anchor='w', pady=2)

        self.app_frame = tk.Frame(app_frame, bg=colors['card'])
        self.app_frame.pack(fill='x', pady=5, padx=10)

        tk.Label(self.app_frame, text=i18n.tr('program'), bg=colors['card'], fg=colors['text']).grid(row=0, column=0, sticky='w')
        self.app_path_var = tk.StringVar(value=edit_data.get('app_path', '') if edit_data else '')
        self.app_entry = tk.Entry(self.app_frame, textvariable=self.app_path_var,
                                   bg=colors['bg'], fg=colors['text'], width=30)
        self.app_entry.grid(row=0, column=1, padx=5)
        self.app_browse_btn = create_styled_button(self.app_frame, text=i18n.tr('browse'),
                                                   command=self.browse_app,
                                                   bg=colors['btn'], fg=colors['text'],
                                                   width=8, height=1, font=('Roboto', 9))
        self.app_browse_btn.grid(row=0, column=2)

        tk.Label(self.app_frame, text=i18n.tr('arguments'), bg=colors['card'], fg=colors['text']).grid(row=1, column=0, sticky='w', pady=5)
        self.app_args_var = tk.StringVar(value=edit_data.get('app_args', '') if edit_data else '')
        self.app_args_entry = tk.Entry(self.app_frame, textvariable=self.app_args_var,
                                        bg=colors['bg'], fg=colors['text'], width=40)
        self.app_args_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        self.toggle_app_options()

        btn_frame = tk.Frame(self, bg=colors['card'])
        btn_frame.pack(pady=20)

        create_styled_button(btn_frame, text=i18n.tr('save'), command=self.on_ok,
                             bg=colors['accent'], fg='black', width=10).pack(side='left', padx=5)
        create_styled_button(btn_frame, text=i18n.tr('cancel'), command=self.on_close,
                             bg=colors['btn'], fg=colors['text'], width=8).pack(side='left', padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.toggle_sound_source()

        if edit_data:
            sound = edit_data.get('sound', 'Alarm01.wav')
            if os.path.exists(sound):
                self.use_custom_sound.set(True)
                self.custom_path.set(sound)
                self.custom_label.config(text=os.path.basename(sound))
            else:
                self.use_custom_sound.set(False)
                self.sound_var.set(sound)
            self.toggle_sound_source()

    def _validate(self, char):
        return char.isdigit()

    def toggle_sound_source(self):
        if self.use_custom_sound.get():
            for child in self.system_frame.winfo_children():
                child.configure(state='disabled')
            self.sound_combo.configure(state='disabled')
            self.custom_frame.pack(fill='x', pady=5, before=self.preview_btn)
        else:
            for child in self.system_frame.winfo_children():
                child.configure(state='normal')
            self.sound_combo.configure(state='readonly')
            self.custom_frame.pack_forget()

    def browse_custom_sound(self):
        filename = filedialog.askopenfilename(
            title=i18n.tr('browse'),
            filetypes=[("Звуковые файлы", "*.wav *.mp3"), ("Все файлы", "*.*")]
        )
        if filename:
            self.custom_path.set(filename)
            short_name = os.path.basename(filename)
            self.custom_label.config(text=short_name)

    def on_sound_selected(self, event):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.preview_btn.config(text='▶')

    def toggle_preview(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.preview_btn.config(text='▶')
        else:
            sound_file = self._get_current_sound()
            if not sound_file:
                messagebox.showerror(i18n.tr('error'), i18n.tr('select_sound'))
                return
            try:
                if os.path.exists(sound_file):
                    pygame.mixer.music.load(sound_file)
                else:
                    full_path = f"C:/Windows/Media/{sound_file}"
                    if not os.path.exists(full_path):
                        messagebox.showerror(i18n.tr('error'), f"{i18n.tr('file_not_found')}: {sound_file}")
                        return
                    pygame.mixer.music.load(full_path)
                pygame.mixer.music.play(0)
                self.preview_btn.config(text='⏸')
            except Exception as e:
                messagebox.showerror(i18n.tr('error'), f"{i18n.tr('play_error')}: {e}")

    def _get_current_sound(self):
        if self.use_custom_sound.get():
            return self.custom_path.get()
        else:
            return self.sound_var.get()

    def toggle_app_options(self):
        if self.launch_app_var.get():
            for child in self.app_frame.winfo_children():
                child.grid()
        else:
            for child in self.app_frame.winfo_children():
                child.grid_remove()

    def browse_app(self):
        filename = filedialog.askopenfilename(
            title=i18n.tr('browse'),
            filetypes=[("Исполняемые файлы", "*.exe"), ("Все файлы", "*.*")]
        )
        if filename:
            self.app_path_var.set(filename)

    def on_ok(self):
        try:
            h = int(self.hours.get() or 0)
            m = int(self.minutes.get() or 0)
            s = int(self.seconds.get() or 0)
            if not (0 <= m <= 59 and 0 <= s <= 59):
                messagebox.showerror(i18n.tr('error'), i18n.tr('minutes_seconds'))
                return
            total = h*3600 + m*60 + s
            if total <= 0:
                messagebox.showerror(i18n.tr('error'), i18n.tr('time_positive'))
                return
            name = self.name_entry.get().strip()
            if not name:
                name = f"{i18n.tr('timer')} {h:02d}:{m:02d}:{s:02d}" if h else f"{i18n.tr('timer')} {m:02d}:{s:02d}"
            sound = self._get_current_sound()
            if not sound:
                messagebox.showerror(i18n.tr('error'), i18n.tr('select_sound'))
                return
            prevent_sleep = self.prevent_sleep_var.get()
            move_mode = self.move_mode_var.get() if prevent_sleep else i18n.tr('no_movement')
            launch_app = self.launch_app_var.get()
            app_path = self.app_path_var.get() if launch_app else ""
            app_args = self.app_args_var.get() if launch_app else ""
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.callback(h, m, s, total, name, sound, prevent_sleep, move_mode,
                          self.size_var.get(), self.font_var.get(),
                          launch_app, app_path, app_args, self.edit_index)
            self.on_close()
        except:
            messagebox.showerror(i18n.tr('error'), i18n.tr('invalid_time'))

    def on_close(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.parent.active_dialog = None
        self.destroy()

# ====================== ДИАЛОГ ДОБАВЛЕНИЯ БУДИЛЬНИКА ======================
class AddAlarmDialog(tk.Toplevel):
    # (Полный код из частей 4-6)
    def __init__(self, parent, colors, sounds, default_snooze, callback, edit_data=None, edit_index=None):
        super().__init__(parent)
        self.parent = parent
        self.colors = colors
        self.sounds = sounds
        self.default_snooze = default_snooze
        self.callback = callback
        self.edit_data = edit_data
        self.edit_index = edit_index
        self.title(i18n.tr('edit_alarm') if edit_data else i18n.tr('new_alarm'))
        self.geometry("450x650")
        self.configure(bg=colors['card'])
        self.transient(parent)
        self.grab_set()
        self.parent.active_dialog = self

        self.update_idletasks()
        x = (self.winfo_screenwidth() - 450) // 2
        y = (self.winfo_screenheight() - 650) // 2
        self.geometry(f"+{x}+{y}")

        tk.Label(self, text=i18n.tr('edit_alarm') if edit_data else i18n.tr('new_alarm'),
                 bg=colors['card'], fg=colors['accent'],
                 font=('Roboto', 16, 'bold')).pack(pady=10)

        # Время
        time_frame = tk.Frame(self, bg=colors['card'])
        time_frame.pack(pady=5)

        vcmd = (self.register(self._validate), '%S')
        if edit_data:
            t = edit_data['time'].split(':')
            cur_h = t[0]
            cur_m = t[1]
        else:
            cur_h = datetime.now().strftime("%H")
            cur_m = (datetime.now()+timedelta(minutes=1)).strftime("%M")

        self.hour = tk.Entry(time_frame, width=2, font=('Roboto', 28, 'bold'),
                             bg=colors['bg'], fg=colors['text'], bd=0, justify='center',
                             validate='key', validatecommand=vcmd)
        self.hour.insert(0, cur_h)
        self.hour.pack(side='left')
        tk.Label(time_frame, text=':', font=('Roboto', 28), bg=colors['card'], fg=colors['text']).pack(side='left')
        self.minute = tk.Entry(time_frame, width=2, font=('Roboto', 28, 'bold'),
                               bg=colors['bg'], fg=colors['text'], bd=0, justify='center',
                               validate='key', validatecommand=vcmd)
        self.minute.insert(0, cur_m)
        self.minute.pack(side='left')

        # Название
        name_frame = tk.Frame(self, bg=colors['card'])
        name_frame.pack(pady=5, fill='x', padx=20)
        tk.Label(name_frame, text=i18n.tr('name'), bg=colors['card'], fg=colors['text']).pack(anchor='w')
        self.name_entry = tk.Entry(name_frame, width=30, bg=colors['bg'], fg=colors['text'],
                                    font=('Roboto', 12))
        self.name_entry.pack(fill='x', pady=5)
        if edit_data:
            self.name_entry.insert(0, edit_data.get('name', i18n.tr('alarm')))
        else:
            self.name_entry.insert(0, i18n.tr('alarm'))

        # Мелодия
        sound_main_frame = tk.LabelFrame(self, text=i18n.tr('sound'), bg=colors['card'],
                                          fg=colors['text'], font=('Roboto', 10))
        sound_main_frame.pack(pady=10, padx=20, fill='x')

        self.use_custom_sound = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(sound_main_frame, text=i18n.tr('use_custom'),
                            variable=self.use_custom_sound,
                            bg=colors['card'], fg=colors['text'], selectcolor=colors['bg'],
                            command=self.toggle_sound_source)
        cb.pack(anchor='w', pady=2)

        self.system_frame = tk.Frame(sound_main_frame, bg=colors['card'])
        self.system_frame.pack(fill='x', pady=5)
        tk.Label(self.system_frame, text=i18n.tr('system_sound'), bg=colors['card'], fg=colors['text']).pack(side='left')
        self.sound_var = tk.StringVar(value='Alarm01.wav')
        self.sound_combo = ttk.Combobox(self.system_frame, textvariable=self.sound_var, values=self.sounds,
                                         state='readonly', width=18)
        self.sound_combo.pack(side='left', padx=5)
        self.sound_combo.bind('<<ComboboxSelected>>', self.on_sound_selected)

        self.custom_frame = tk.Frame(sound_main_frame, bg=colors['card'])
        self.custom_path = tk.StringVar()
        self.custom_label = tk.Label(self.custom_frame, text=i18n.tr('file_not_found'), bg=colors['card'],
                                      fg=colors['text'], wraplength=300)
        self.custom_label.pack(side='left', padx=5)
        self.browse_btn = create_styled_button(self.custom_frame, text=i18n.tr('browse'),
                                                command=self.browse_custom_sound,
                                                bg=colors['btn'], fg=colors['text'],
                                                width=8, height=1, font=('Roboto', 9))
        self.browse_btn.pack(side='right', padx=5)

        self.preview_btn = tk.Button(sound_main_frame, text='▶', command=self.toggle_preview, width=2)
        self.preview_btn.pack(pady=5)

        # Интервал откладывания
        snooze_frame = tk.LabelFrame(self, text=i18n.tr('snooze'), bg=colors['card'],
                                      fg=colors['text'], font=('Roboto', 10))
        snooze_frame.pack(pady=10, padx=20, fill='x')
        self.snooze_var = tk.IntVar(value=edit_data.get('snooze', self.default_snooze) if edit_data else self.default_snooze)
        snooze_options = [1, 3, 5, 10, 15, 30]
        opt_frame = tk.Frame(snooze_frame, bg=colors['card'])
        opt_frame.pack()
        for v in snooze_options:
            rb = tk.Radiobutton(opt_frame, text=str(v), variable=self.snooze_var, value=v,
                                bg=colors['card'], fg=colors['text'], selectcolor=colors['bg'])
            rb.pack(side='left', padx=5)

        # Дни недели
        days_frame = tk.LabelFrame(self, text=i18n.tr('repeat'), bg=colors['card'],
                                    fg=colors['text'], font=('Roboto', 10))
        days_frame.pack(pady=10, padx=20, fill='x')
        days_inner = tk.Frame(days_frame, bg=colors['card'])
        days_inner.pack(pady=5)
        self.day_btns = {}
        days = i18n.tr('days')
        self.active_days = {}
        if edit_data:
            for d in days:
                self.active_days[d] = d in edit_data.get('days', [])
        else:
            for d in days:
                self.active_days[d] = False

        for d in days:
            btn = tk.Button(days_inner, text=d, width=3, bg=colors['bg'], fg=colors['text'],
                            bd=0, command=lambda x=d: self.toggle_day(x))
            btn.pack(side='left', padx=2)
            self.day_btns[d] = btn
            if self.active_days[d]:
                btn.config(bg=self.colors['accent'])

        # Запуск приложения
        app_frame = tk.LabelFrame(self, text=i18n.tr('on_trigger'), bg=colors['card'],
                                   fg=colors['text'], font=('Roboto', 10))
        app_frame.pack(pady=10, padx=20, fill='x')

        self.launch_app_var = tk.BooleanVar(value=edit_data.get('launch_app', False) if edit_data else False)
        launch_cb = tk.Checkbutton(app_frame, text=i18n.tr('launch_app'),
                                    variable=self.launch_app_var,
                                    bg=colors['card'], fg=colors['text'], selectcolor=colors['bg'],
                                    command=self.toggle_app_options)
        launch_cb.pack(anchor='w', pady=2)

        self.app_frame = tk.Frame(app_frame, bg=colors['card'])
        self.app_frame.pack(fill='x', pady=5, padx=10)

        tk.Label(self.app_frame, text=i18n.tr('program'), bg=colors['card'], fg=colors['text']).grid(row=0, column=0, sticky='w')
        self.app_path_var = tk.StringVar(value=edit_data.get('app_path', '') if edit_data else '')
        self.app_entry = tk.Entry(self.app_frame, textvariable=self.app_path_var,
                                   bg=colors['bg'], fg=colors['text'], width=30)
        self.app_entry.grid(row=0, column=1, padx=5)
        self.app_browse_btn = create_styled_button(self.app_frame, text=i18n.tr('browse'),
                                                   command=self.browse_app,
                                                   bg=colors['btn'], fg=colors['text'],
                                                   width=8, height=1, font=('Roboto', 9))
        self.app_browse_btn.grid(row=0, column=2)

        tk.Label(self.app_frame, text=i18n.tr('arguments'), bg=colors['card'], fg=colors['text']).grid(row=1, column=0, sticky='w', pady=5)
        self.app_args_var = tk.StringVar(value=edit_data.get('app_args', '') if edit_data else '')
        self.app_args_entry = tk.Entry(self.app_frame, textvariable=self.app_args_var,
                                        bg=colors['bg'], fg=colors['text'], width=40)
        self.app_args_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        self.toggle_app_options()

        btn_frame = tk.Frame(self, bg=colors['card'])
        btn_frame.pack(pady=20)

        create_styled_button(btn_frame, text=i18n.tr('save'), command=self.on_ok,
                             bg=colors['accent'], fg='black', width=10).pack(side='left', padx=5)
        create_styled_button(btn_frame, text=i18n.tr('cancel'), command=self.on_close,
                             bg=colors['btn'], fg=colors['text'], width=8).pack(side='left', padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.toggle_sound_source()

        if edit_data:
            sound = edit_data.get('sound', 'Alarm01.wav')
            if os.path.exists(sound):
                self.use_custom_sound.set(True)
                self.custom_path.set(sound)
                self.custom_label.config(text=os.path.basename(sound))
            else:
                self.use_custom_sound.set(False)
                self.sound_var.set(sound)
            self.toggle_sound_source()

    def _validate(self, char):
        return char.isdigit()

    def toggle_day(self, d):
        self.active_days[d] = not self.active_days[d]
        self.day_btns[d].config(bg=self.colors['accent'] if self.active_days[d] else self.colors['bg'])

    def toggle_sound_source(self):
        if self.use_custom_sound.get():
            for child in self.system_frame.winfo_children():
                child.configure(state='disabled')
            self.sound_combo.configure(state='disabled')
            self.custom_frame.pack(fill='x', pady=5, before=self.preview_btn)
        else:
            for child in self.system_frame.winfo_children():
                child.configure(state='normal')
            self.sound_combo.configure(state='readonly')
            self.custom_frame.pack_forget()

    def browse_custom_sound(self):
        filename = filedialog.askopenfilename(
            title=i18n.tr('browse'),
            filetypes=[("Звуковые файлы", "*.wav *.mp3"), ("Все файлы", "*.*")]
        )
        if filename:
            self.custom_path.set(filename)
            short_name = os.path.basename(filename)
            self.custom_label.config(text=short_name)

    def on_sound_selected(self, event):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.preview_btn.config(text='▶')

    def toggle_preview(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.preview_btn.config(text='▶')
        else:
            sound_file = self._get_current_sound()
            if not sound_file:
                messagebox.showerror(i18n.tr('error'), i18n.tr('select_sound'))
                return
            try:
                if os.path.exists(sound_file):
                    pygame.mixer.music.load(sound_file)
                else:
                    full_path = f"C:/Windows/Media/{sound_file}"
                    if not os.path.exists(full_path):
                        messagebox.showerror(i18n.tr('error'), f"{i18n.tr('file_not_found')}: {sound_file}")
                        return
                    pygame.mixer.music.load(full_path)
                pygame.mixer.music.play(0)
                self.preview_btn.config(text='⏸')
            except Exception as e:
                messagebox.showerror(i18n.tr('error'), f"{i18n.tr('play_error')}: {e}")

    def _get_current_sound(self):
        if self.use_custom_sound.get():
            return self.custom_path.get()
        else:
            return self.sound_var.get()

    def toggle_app_options(self):
        if self.launch_app_var.get():
            for child in self.app_frame.winfo_children():
                child.grid()
        else:
            for child in self.app_frame.winfo_children():
                child.grid_remove()

    def browse_app(self):
        filename = filedialog.askopenfilename(
            title=i18n.tr('browse'),
            filetypes=[("Исполняемые файлы", "*.exe"), ("Все файлы", "*.*")]
        )
        if filename:
            self.app_path_var.set(filename)

    def on_ok(self):
        try:
            h = int(self.hour.get() or 0)
            m = int(self.minute.get() or 0)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                messagebox.showerror(i18n.tr('error'), i18n.tr('invalid_time'))
                return
            name = self.name_entry.get().strip()
            if not name:
                name = f"{i18n.tr('alarm')} {h:02d}:{m:02d}"
            sound = self._get_current_sound()
            if not sound:
                messagebox.showerror(i18n.tr('error'), i18n.tr('select_sound'))
                return
            days = [d for d, active in self.active_days.items() if active]
            snooze = self.snooze_var.get()
            launch_app = self.launch_app_var.get()
            app_path = self.app_path_var.get() if launch_app else ""
            app_args = self.app_args_var.get() if launch_app else ""
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.callback(h, m, name, sound, days, snooze, launch_app, app_path, app_args, self.edit_index)
            self.on_close()
        except:
            messagebox.showerror(i18n.tr('error'), i18n.tr('invalid_time'))

    def on_close(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.parent.active_dialog = None
        self.destroy()

# ====================== ОСНОВНОЕ ПРИЛОЖЕНИЕ ======================
class WinTickApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WinTick")
        self.geometry("450x700")
        self.minsize(400, 600)

        icon_path = resource_path(ICON_PATH)
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(default=icon_path)
            except:
                pass

        self.settings = {
            'theme': 'dark',
            'selected_sound': 'Alarm01.wav',
            'snooze_min': 5,
            'volume': 70,
            'time_format': '24h',
            'auto_off_alarm': 5,
            'gradual_volume': False,
            'big_timer_size': i18n.tr('medium'),
            'big_timer_font': i18n.tr('medium'),
            'always_on_top': True,
            'timer_action': 'sound_notify',
            'timer_auto_repeat': False,
            'timer_repeat_count': 1,
            'warn_before': False,
            'warn_minutes': 1,
            'language': 'ru',
            'global_prevent': False,
        }

        self.colors = {}
        self.volume_window = None
        self.alert_windows = []
        self.alert_count = 0
        self.active_dialog = None
        self.timers = []
        self.timer_widgets = []
        self.alarms = []
        self.snooze_count = {}
        self.sounds = ['Alarm01.wav', 'Alarm05.wav', 'Alarm10.wav', 'Ring06.wav']

        self.mouse_threads = {}          # для таймеров
        self.global_prevent_thread = None
        self.global_prevent_stop = threading.Event()

        self.tray_icon = None

        self.load_data()
        i18n.set_language(self.settings.get('language', 'ru'))

        self.top_bar = tk.Frame(self, height=50)
        self.top_bar.pack(side='top', fill='x')
        self.top_bar.pack_propagate(False)

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill='both')

        self.nav = tk.Frame(self, height=70)
        self.nav.pack(side='bottom', fill='x')
        self.nav.pack_propagate(False)

        self.current_tab = 'alarm'

        self.draw_theme()
        self.show_alarm_tab()

        self.apply_settings()
        self.sync_loop()

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        if self.settings.get('global_prevent', False):
            self.start_global_prevent()

    def rebuild_ui(self):
        if self.active_dialog and self.active_dialog.winfo_exists():
            self.active_dialog.destroy()
            self.active_dialog = None
        for w in self.alert_windows[:]:
            if w.winfo_exists():
                w.destroy()
        self.alert_windows.clear()
        self.alert_count = 0

        self.draw_theme()
        if self.current_tab == 'alarm':
            self.show_alarm_tab()
        else:
            self.show_timer_tab()

        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None

    def draw_theme(self):
        if self.settings.get('theme') == 'dark':
            self.colors = {
                'bg': '#1e1e1e',
                'card': '#2d2f31',
                'text': '#ffffff',
                'accent': '#8ab4f8',
                'btn': '#3c4043',
                'danger': '#f28b82'
            }
        else:
            self.colors = {
                'bg': '#ffffff',
                'card': '#f1f3f4',
                'text': '#202124',
                'accent': '#1a73e8',
                'btn': '#e8eaed',
                'danger': '#d93025'
            }

        self.configure(bg=self.colors['bg'])
        self.container.configure(bg=self.colors['bg'])
        self.top_bar.configure(bg=self.colors['card'])
        self.nav.configure(bg=self.colors['card'])

        self.create_top_icons()
        self.create_navigation()

    def create_top_icons(self):
        for w in self.top_bar.winfo_children():
            w.destroy()

        icons_frame = tk.Frame(self.top_bar, bg=self.colors['card'])
        icons_frame.pack(side='right', padx=10)

        self.lang_icon = LanguageMenu(icons_frame, self.colors, self)
        self.lang_icon.pack(side='left', padx=10)

        self.theme_icon = tk.Label(icons_frame, text='🌙' if self.settings['theme']=='dark' else '☀️',
                                    font=('Segoe UI', 20), bg=self.colors['card'], fg=self.colors['text'])
        self.theme_icon.pack(side='left', padx=10)
        self.theme_icon.bind('<Button-1>', lambda e: self.toggle_theme())
        self.theme_icon.bind('<Enter>', lambda e: self.theme_icon.configure(fg=self.colors['accent']))
        self.theme_icon.bind('<Leave>', lambda e: self.theme_icon.configure(fg=self.colors['text']))

        self.volume_icon = tk.Label(icons_frame, text='🔊', font=('Segoe UI', 20),
                                     bg=self.colors['card'], fg=self.colors['text'])
        self.volume_icon.pack(side='left', padx=10)
        self.volume_icon.bind('<Button-1>', lambda e: self.show_volume_control())
        self.volume_icon.bind('<Enter>', lambda e: self.volume_icon.configure(fg=self.colors['accent']))
        self.volume_icon.bind('<Leave>', lambda e: self.volume_icon.configure(fg=self.colors['text']))

        self.about_icon = tk.Label(icons_frame, text='ℹ️', font=('Segoe UI', 20),
                                    bg=self.colors['card'], fg=self.colors['text'])
        self.about_icon.pack(side='left', padx=10)
        self.about_icon.bind('<Button-1>', lambda e: self.show_about())
        self.about_icon.bind('<Enter>', lambda e: self.about_icon.configure(fg=self.colors['accent']))
        self.about_icon.bind('<Leave>', lambda e: self.about_icon.configure(fg=self.colors['text']))

        self.add_btn = create_styled_button(self.top_bar, text='+', command=self.on_add_click,
                                            bg=self.colors['accent'], fg='black',
                                            width=2, height=1, font=('Roboto', 16, 'bold'))
        self.add_btn.pack(side='right', padx=5, pady=5)

    def toggle_theme(self):
        self.settings['theme'] = 'light' if self.settings['theme'] == 'dark' else 'dark'
        self.draw_theme()
        if self.current_tab == 'alarm':
            self.show_alarm_tab()
        else:
            self.show_timer_tab()

    def show_volume_control(self):
        if self.volume_window and self.volume_window.winfo_exists():
            self.volume_window.lift()
            return
        self.volume_window = VolumeControl(self, self.settings['volume'], self.set_volume)

    def set_volume(self, val):
        self.settings['volume'] = val
        try:
            pygame.mixer.music.set_volume(val / 100)
        except:
            pass

    def on_add_click(self):
        if self.current_tab == 'alarm':
            self.show_add_alarm()
        else:
            self.show_add_timer()

    def show_about(self):
        about = tk.Toplevel(self)
        about.title(i18n.tr('about'))
        about.geometry("350x300")
        about.configure(bg=self.colors['card'])
        about.transient(self)
        about.grab_set()
        about.resizable(False, False)
        about.update_idletasks()
        x = (about.winfo_screenwidth() - 350) // 2
        y = (about.winfo_screenheight() - 300) // 2
        about.geometry(f"+{x}+{y}")

        tk.Label(about, text="WinTick", font=('Roboto', 18, 'bold'),
                 bg=self.colors['card'], fg=self.colors['accent']).pack(pady=10)
        tk.Label(about, text="Version 1.7", bg=self.colors['card'],
                 fg=self.colors['text']).pack()
        tk.Label(about, text="Developer: Alex Potoshov", bg=self.colors['card'],
                 fg=self.colors['text']).pack(pady=5)
        tk.Label(about, text="© 2026 Potoshov Dev. All rights reserved.", bg=self.colors['card'],
                 fg=self.colors['text']).pack()
        tk.Label(about, text="Powered by AI Assistant", bg=self.colors['card'],
                 fg=self.colors['text']).pack(pady=(10,0))
        tk.Label(about, text="(GitHub Copilot / ChatGPT)", bg=self.colors['card'],
                 fg=self.colors['text'], font=('Roboto', 8)).pack()
        tk.Label(about, text="Alarm + Timer with app launch and\nprevent sleep function",
                 bg=self.colors['card'], fg=self.colors['text'], justify='center').pack(pady=10)
        tk.Button(about, text="OK", command=about.destroy,
                  bg=self.colors['btn'], fg=self.colors['text'],
                  width=10, relief='raised', bd=2).pack(pady=10)

    def start_global_prevent(self):
        if self.global_prevent_thread and self.global_prevent_thread.is_alive():
            return
        self.global_prevent_stop.clear()
        self.global_prevent_thread = threading.Thread(target=self._global_prevent_worker, daemon=True)
        self.global_prevent_thread.start()

    def stop_global_prevent(self):
        self.global_prevent_stop.set()
        if self.global_prevent_thread:
            self.global_prevent_thread.join(timeout=2)
            self.global_prevent_thread = None

    def _global_prevent_worker(self):
        while not self.global_prevent_stop.is_set():
            prevent_sleep()
            self.global_prevent_stop.wait(30)

    def toggle_global_prevent(self):
        if self.settings.get('global_prevent', False):
            self.stop_global_prevent()
            self.settings['global_prevent'] = False
        else:
            self.start_global_prevent()
            self.settings['global_prevent'] = True
        # меню трея обновится при следующем показе

    def create_navigation(self):
        for w in self.nav.winfo_children():
            w.destroy()

        nav_frame = tk.Frame(self.nav, bg=self.colors['card'])
        nav_frame.pack(expand=True, fill='both', padx=20, pady=5)

        self.alarm_nav_btn = tk.Frame(nav_frame, bg=self.colors['card'])
        self.alarm_nav_btn.pack(side='left', expand=True, fill='both')
        self.alarm_nav_btn.bind('<Button-1>', lambda e: self.show_alarm_tab())

        alarm_icon = tk.Label(self.alarm_nav_btn, text='⏰', font=('Segoe UI', 20),
                              bg=self.colors['card'], fg=self.colors['accent'] if self.current_tab=='alarm' else self.colors['text'])
        alarm_icon.pack()
        alarm_icon.bind('<Button-1>', lambda e: self.show_alarm_tab())

        alarm_text = tk.Label(self.alarm_nav_btn, text=i18n.tr('alarm'), font=('Roboto', 10),
                              bg=self.colors['card'], fg=self.colors['accent'] if self.current_tab=='alarm' else self.colors['text'])
        alarm_text.pack()
        alarm_text.bind('<Button-1>', lambda e: self.show_alarm_tab())

        self.timer_nav_btn = tk.Frame(nav_frame, bg=self.colors['card'])
        self.timer_nav_btn.pack(side='left', expand=True, fill='both')
        self.timer_nav_btn.bind('<Button-1>', lambda e: self.show_timer_tab())

        timer_icon = tk.Label(self.timer_nav_btn, text='⏲', font=('Segoe UI', 20),
                              bg=self.colors['card'], fg=self.colors['accent'] if self.current_tab=='timer' else self.colors['text'])
        timer_icon.pack()
        timer_icon.bind('<Button-1>', lambda e: self.show_timer_tab())

        timer_text = tk.Label(self.timer_nav_btn, text=i18n.tr('timer'), font=('Roboto', 10),
                              bg=self.colors['card'], fg=self.colors['accent'] if self.current_tab=='timer' else self.colors['text'])
        timer_text.pack()
        timer_text.bind('<Button-1>', lambda e: self.show_timer_tab())

    def update_nav_colors(self):
        for child in self.alarm_nav_btn.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(fg=self.colors['accent'] if self.current_tab=='alarm' else self.colors['text'])
        for child in self.timer_nav_btn.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(fg=self.colors['accent'] if self.current_tab=='timer' else self.colors['text'])

    # ------------------------------------------------------------------
    # Вкладка Будильник
    # ------------------------------------------------------------------
    def show_alarm_tab(self):
        self.current_tab = 'alarm'
        self.update_nav_colors()
        self.clear_container()

        header = tk.Frame(self.container, bg=self.colors['bg'])
        header.pack(fill='x', padx=15, pady=10)
        tk.Label(header, text=i18n.tr('alarm'), font=('Roboto', 20, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['accent']).pack(side='left')

        self.alarm_list_frame = tk.Frame(self.container, bg=self.colors['bg'])
        self.alarm_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_alarm_list()

    def show_add_alarm(self):
        AddAlarmDialog(self, self.colors, self.sounds, self.settings['snooze_min'], self.add_alarm_callback)

    def add_alarm_callback(self, h, m, name, sound, days, snooze, launch_app, app_path, app_args, edit_index=None):
        if edit_index is not None:
            self.alarms[edit_index] = {
                'time': f"{h:02d}:{m:02d}",
                'name': name,
                'days': days,
                'active': self.alarms[edit_index].get('active', True),
                'sound': sound,
                'snooze': snooze,
                'launch_app': launch_app,
                'app_path': app_path,
                'app_args': app_args
            }
        else:
            self.alarms.append({
                'time': f"{h:02d}:{m:02d}",
                'name': name,
                'days': days,
                'active': True,
                'sound': sound,
                'snooze': snooze,
                'launch_app': launch_app,
                'app_path': app_path,
                'app_args': app_args
            })
        self.refresh_alarm_list()

    def refresh_alarm_list(self):
        for w in self.alarm_list_frame.winfo_children():
            w.destroy()
        for i, a in enumerate(self.alarms):
            card = tk.Frame(self.alarm_list_frame, bg=self.colors['card'], padx=15, pady=10)
            card.pack(fill='x', pady=5)

            card.bind('<Button-1>', lambda e, idx=i: self.open_edit_alarm(idx))
            for child in card.winfo_children():
                child.bind('<Button-1>', lambda e, idx=i: self.open_edit_alarm(idx), add=True)

            if self.settings['time_format'] == '12h':
                try:
                    t = datetime.strptime(a['time'], "%H:%M")
                    time_str = t.strftime("%I:%M %p").lstrip('0')
                except:
                    time_str = a['time']
            else:
                time_str = a['time']
            time_label = tk.Label(card, text=time_str, font=('Roboto', 20, 'bold'),
                                  bg=self.colors['card'], fg=self.colors['text'])
            time_label.pack(side='left')
            time_label.bind('<Button-1>', lambda e, idx=i: self.open_edit_alarm(idx))

            days_str = f" ({', '.join(a['days'])})" if a['days'] else f" ({i18n.tr('once')})"
            name_text = a['name']
            if a.get('launch_app', False) and a.get('app_path'):
                name_text += " [📁]"
            name_label = tk.Label(card, text=f"{name_text}{days_str}", bg=self.colors['card'],
                                  fg=self.colors['accent'], font=('Roboto', 10))
            name_label.pack(side='left', padx=10)
            name_label.bind('<Button-1>', lambda e, idx=i: self.open_edit_alarm(idx))

            btn_frame = tk.Frame(card, bg=self.colors['card'])
            btn_frame.pack(side='right')

            state_text = i18n.tr('on') if a['active'] else i18n.tr('off')
            state_color = self.colors['accent'] if a['active'] else 'gray'
            toggle_btn = create_styled_button(btn_frame, text=state_text, command=lambda idx=i: self.toggle_alarm(idx),
                                              bg=state_color, fg='black', width=5, height=1, font=('Roboto', 9, 'bold'))
            toggle_btn.pack(side='left', padx=2)

            del_btn = tk.Button(btn_frame, text='✕', command=lambda idx=i: self.delete_alarm(idx),
                                bg=self.colors['card'], fg=self.colors['danger'], bd=0, font=('Roboto', 14))
            del_btn.pack(side='left', padx=2)

    def toggle_alarm(self, idx):
        self.alarms[idx]['active'] = not self.alarms[idx]['active']
        self.refresh_alarm_list()

    def delete_alarm(self, idx):
        self.alarms.pop(idx)
        self.refresh_alarm_list()

    def open_edit_alarm(self, idx):
        alarm = self.alarms[idx]
        AddAlarmDialog(self, self.colors, self.sounds, self.settings['snooze_min'],
                       self.add_alarm_callback, edit_data=alarm, edit_index=idx)

    # ------------------------------------------------------------------
    # Вкладка Таймер
    # ------------------------------------------------------------------
    def show_timer_tab(self):
        self.current_tab = 'timer'
        self.update_nav_colors()
        self.clear_container()

        header = tk.Frame(self.container, bg=self.colors['bg'])
        header.pack(fill='x', padx=15, pady=10)
        tk.Label(header, text=i18n.tr('timer'), font=('Roboto', 20, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['accent']).pack(side='left')

        self.timer_list_frame = tk.Frame(self.container, bg=self.colors['bg'])
        self.timer_list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.rebuild_timer_list()

    def rebuild_timer_list(self):
        for w in self.timer_list_frame.winfo_children():
            w.destroy()
        self.timer_widgets = []
        for i, t in enumerate(self.timers):
            self._add_timer_widget(i, t)

    def _add_timer_widget(self, idx, timer):
        card = tk.Frame(self.timer_list_frame, bg=self.colors['card'], padx=15, pady=10)
        card.pack(fill='x', pady=5)

        card.bind('<Button-1>', lambda e, i=idx: self.open_edit_timer(i))
        for child in card.winfo_children():
            child.bind('<Button-1>', lambda e, i=idx: self.open_edit_timer(i), add=True)

        time_label = tk.Label(card, font=('Roboto', 20, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        time_label.pack(side='left')
        time_label.bind('<Button-1>', lambda e, i=idx: self.open_edit_timer(i))

        name_text = timer['name']
        if timer.get('launch_app', False) and timer.get('app_path'):
            name_text += " [📁]"
        name_label = tk.Label(card, text=name_text, bg=self.colors['card'],
                              fg=self.colors['accent'], font=('Roboto', 10))
        name_label.pack(side='left', padx=10)
        name_label.bind('<Button-1>', lambda e, i=idx: self.open_edit_timer(i))

        if timer.get('prevent_sleep', False):
            sleep_icon = tk.Label(card, text='💤', bg=self.colors['card'], fg=self.colors['accent'])
            sleep_icon.pack(side='left', padx=2)
            sleep_icon.bind('<Button-1>', lambda e, i=idx: self.open_edit_timer(i))

        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(side='right')

        play_btn = create_styled_button(btn_frame, text='⏸' if timer['run'] else '▶',
                                        command=lambda x=timer: self.toggle_timer_run(x),
                                        bg=self.colors['card'], fg=self.colors['accent'],
                                        width=2, height=1, font=('Roboto', 14))
        play_btn.pack(side='left', padx=2)

        reset_btn = create_styled_button(btn_frame, text='↺',
                                         command=lambda x=timer: self.reset_timer(x),
                                         bg=self.colors['card'], fg=self.colors['text'],
                                         width=2, height=1, font=('Roboto', 14))
        reset_btn.pack(side='left', padx=2)

        big_btn = create_styled_button(btn_frame, text='↗',
                                       command=lambda x=timer: self.open_big_timer(x),
                                       bg=self.colors['card'], fg=self.colors['text'],
                                       width=2, height=1, font=('Roboto', 14))
        big_btn.pack(side='left', padx=2)

        del_btn = tk.Button(btn_frame, text='✕', command=lambda idx=idx: self.delete_timer(idx),
                            bg=self.colors['card'], fg=self.colors['danger'], bd=0, font=('Roboto', 14))
        del_btn.pack(side='left', padx=2)

        self.timer_widgets.append({
            'frame': card,
            'time_label': time_label,
            'play_btn': play_btn,
            'timer': timer
        })

    def show_add_timer(self):
        AddTimerDialog(self, self.colors, self.sounds, self.add_timer_callback)

    def add_timer_callback(self, h, m, s, total, name, sound, prevent_sleep, move_mode, size, font,
                           launch_app, app_path, app_args, edit_index=None):
        if edit_index is not None:
            old = self.timers[edit_index]
            self.timers[edit_index] = {
                'total': total,
                'rem': total,
                'run': old.get('run', True),
                'name': name,
                'sound': sound,
                'prevent_sleep': prevent_sleep,
                'move_mode': move_mode,
                'size': size,
                'font': font,
                'repeat_left': self.settings['timer_repeat_count'] if self.settings['timer_auto_repeat'] else 0,
                'launch_app': launch_app,
                'app_path': app_path,
                'app_args': app_args
            }
            if prevent_sleep and self.timers[edit_index]['run']:
                self.start_mouse_jiggle(edit_index, move_mode)
            elif not prevent_sleep:
                self.stop_mouse_jiggle(edit_index)
        else:
            timer_index = len(self.timers)
            self.timers.append({
                'total': total,
                'rem': total,
                'run': True,
                'name': name,
                'sound': sound,
                'prevent_sleep': prevent_sleep,
                'move_mode': move_mode,
                'size': size,
                'font': font,
                'repeat_left': self.settings['timer_repeat_count'] if self.settings['timer_auto_repeat'] else 0,
                'launch_app': launch_app,
                'app_path': app_path,
                'app_args': app_args
            })
            if prevent_sleep:
                self.start_mouse_jiggle(timer_index, move_mode)
        self.rebuild_timer_list()

    def delete_timer(self, idx):
        self.stop_mouse_jiggle(idx)
        self.timers.pop(idx)
        self.rebuild_timer_list()

    def toggle_timer_run(self, timer):
        timer['run'] = not timer['run']
        idx = self.timers.index(timer)
        if timer.get('prevent_sleep', False):
            if timer['run']:
                self.start_mouse_jiggle(idx, timer.get('move_mode', i18n.tr('no_movement')))
            else:
                self.stop_mouse_jiggle(idx)
        self.update_timer_widgets()

    def reset_timer(self, timer):
        timer['rem'] = timer['total']
        self.update_timer_widgets()

    def open_big_timer(self, timer):
        BigTimer(self, timer, self.colors, self.settings)

    def open_edit_timer(self, idx):
        timer = self.timers[idx]
        AddTimerDialog(self, self.colors, self.sounds, self.add_timer_callback,
                       edit_data=timer, edit_index=idx)

    def update_timer_widgets(self):
        for w in self.timer_widgets:
            t = w['timer']
            m, s = divmod(t['rem'], 60)
            h = m // 60
            m %= 60
            time_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            w['time_label'].config(text=time_str)
            play_text = '⏸' if t['run'] else '▶'
            w['play_btn'].config(text=play_text)

    # ------------------------------------------------------------------
    # Функции движения мыши
    # ------------------------------------------------------------------
    def start_mouse_jiggle(self, timer_idx, mode='Без движения'):
        if timer_idx in self.mouse_threads:
            self.stop_mouse_jiggle(timer_idx)
        stop_event = threading.Event()
        thread = threading.Thread(target=self._mouse_jiggle_worker, args=(timer_idx, stop_event, mode), daemon=True)
        self.mouse_threads[timer_idx] = (thread, stop_event, mode)
        thread.start()

    def stop_mouse_jiggle(self, timer_idx):
        if timer_idx in self.mouse_threads:
            thread, stop_event, _ = self.mouse_threads[timer_idx]
            stop_event.set()
            thread.join(timeout=2)
            del self.mouse_threads[timer_idx]

    def _mouse_jiggle_worker(self, timer_idx, stop_event, mode):
        amplitude = 30
        delay = 60
        last_winapi = time.time()
        while not stop_event.is_set():
            now = time.time()
            if now - last_winapi > 30:
                prevent_sleep()
                last_winapi = now

            if timer_idx >= len(self.timers):
                break
            timer = self.timers[timer_idx]

            if not timer['run']:
                if stop_event.wait(1):
                    break
                continue

            if mode == i18n.tr('no_movement') or mode == 'Без движения':
                if stop_event.wait(delay):
                    break
                continue

            if stop_event.wait(delay):
                break
            if timer['run']:
                try:
                    current_x, current_y = pyautogui.position()
                    if mode == i18n.tr('line') or mode == 'Линия':
                        pyautogui.moveTo(current_x + amplitude, current_y, duration=0.2)
                        pyautogui.moveTo(current_x, current_y, duration=0.2)
                    elif mode == i18n.tr('circle') or mode == 'Круг':
                        radius = amplitude
                        for angle in range(0, 360, 30):
                            x = current_x + radius * cos(radians(angle))
                            y = current_y + radius * sin(radians(angle))
                            pyautogui.moveTo(x, y, duration=0.1)
                        pyautogui.moveTo(current_x, current_y, duration=0.2)
                    elif mode == i18n.tr('zigzag') or mode == 'Зигзаг':
                        pyautogui.moveTo(current_x + amplitude, current_y - amplitude//2, duration=0.2)
                        pyautogui.moveTo(current_x - amplitude, current_y + amplitude//2, duration=0.2)
                        pyautogui.moveTo(current_x, current_y, duration=0.2)
                except:
                    try:
                        pt = POINT()
                        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                        if mode == i18n.tr('line') or mode == 'Линия':
                            ctypes.windll.user32.SetCursorPos(pt.x + amplitude, pt.y)
                            time.sleep(0.2)
                            ctypes.windll.user32.SetCursorPos(pt.x, pt.y)
                        elif mode == i18n.tr('circle') or mode == 'Круг':
                            for angle in range(0, 360, 45):
                                dx = int(amplitude * cos(radians(angle)))
                                dy = int(amplitude * sin(radians(angle)))
                                ctypes.windll.user32.SetCursorPos(pt.x + dx, pt.y + dy)
                                time.sleep(0.05)
                            ctypes.windll.user32.SetCursorPos(pt.x, pt.y)
                        elif mode == i18n.tr('zigzag') or mode == 'Зигзаг':
                            ctypes.windll.user32.SetCursorPos(pt.x + amplitude, pt.y - amplitude//2)
                            time.sleep(0.2)
                            ctypes.windll.user32.SetCursorPos(pt.x - amplitude, pt.y + amplitude//2)
                            time.sleep(0.2)
                            ctypes.windll.user32.SetCursorPos(pt.x, pt.y)
                    except:
                        pass

    # ------------------------------------------------------------------
    # Основная логика
    # ------------------------------------------------------------------
    def apply_settings(self):
        try:
            pygame.mixer.music.set_volume(self.settings['volume'] / 100)
        except:
            pass

    def sync_loop(self):
        now = datetime.now().strftime("%H:%M")
        weekday = i18n.tr('days')[datetime.now().weekday()]

        for t in self.timers[:]:
            if t['run'] and t['rem'] > 0:
                t['rem'] -= 1
            if t['rem'] <= 0 and t['run']:
                t['run'] = False
                self.handle_timer_end(t)

        if self.current_tab == 'timer':
            self.update_timer_widgets()

        for a in self.alarms:
            if a['time'] == now and a['active']:
                if not a['days'] or weekday in a['days']:
                    a['active'] = False
                    self.show_alert(a['name'], i18n.tr('alarm'), a)

        self.after(1000, self.sync_loop)

    def handle_timer_end(self, timer):
        idx = self.timers.index(timer)
        sound = timer.get('sound', self.settings['selected_sound'])
        self.play_sound(sound, timer['name'], i18n.tr('timer'))
        self.show_alert(timer['name'], i18n.tr('timer'), timer, timer_idx=idx)
        if self.settings['timer_auto_repeat'] and timer.get('repeat_left', 0) > 0:
            timer['rem'] = timer['total']
            timer['run'] = True
            timer['repeat_left'] -= 1
            if timer.get('prevent_sleep', False) and timer['run']:
                if idx not in self.mouse_threads:
                    self.start_mouse_jiggle(idx, timer.get('move_mode', i18n.tr('no_movement')))

    def play_sound(self, sound_file, name, typ):
        def _play():
            try:
                if self.settings['gradual_volume']:
                    for i in range(1,11):
                        vol = (self.settings['volume']/100) * (i/10)
                        pygame.mixer.music.set_volume(vol)
                        time.sleep(0.5)
                else:
                    pygame.mixer.music.set_volume(self.settings['volume']/100)
                if os.path.exists(sound_file):
                    pygame.mixer.music.load(sound_file)
                else:
                    full_path = f"C:/Windows/Media/{sound_file}"
                    if os.path.exists(full_path):
                        pygame.mixer.music.load(full_path)
                    else:
                        winsound.Beep(1000, 2000)
                        return
                pygame.mixer.music.play(-1)
            except:
                winsound.Beep(1000, 2000)
        threading.Thread(target=_play, daemon=True).start()

    def show_alert(self, name, typ, obj=None, timer_idx=None):
        if self.alert_count == 0 and self.active_dialog and self.active_dialog.winfo_exists():
            self.active_dialog.grab_release()
        self.alert_count += 1

        if typ == i18n.tr('timer') and obj:
            sound = obj.get('sound', self.settings['selected_sound'])
            launch_app = obj.get('launch_app', False)
            app_path = obj.get('app_path', '')
            app_args = obj.get('app_args', '')
        elif typ == i18n.tr('alarm') and obj:
            sound = obj.get('sound', self.settings['selected_sound'])
            launch_app = obj.get('launch_app', False)
            app_path = obj.get('app_path', '')
            app_args = obj.get('app_args', '')
        else:
            sound = self.settings['selected_sound']
            launch_app = False
            app_path = ''
            app_args = ''

        self.play_sound(sound, name, typ)

        if self.settings['auto_off_alarm'] > 0 and typ == i18n.tr('alarm'):
            self.after(self.settings['auto_off_alarm']*60*1000, self.stop_all_sounds)

        win = tk.Toplevel(self)
        win.geometry("450x350")
        win.configure(bg=self.colors['bg'])
        win.attributes("-topmost", True)
        win.protocol("WM_DELETE_WINDOW", lambda: self.close_alert(win, timer_idx))

        self.alert_windows.append(win)

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 450) // 2
        y = (win.winfo_screenheight() - 350) // 2
        win.geometry(f"+{x}+{y}")

        win.lift()
        win.focus_force()

        icon = '⏰' if typ == i18n.tr('alarm') else '⏲'
        tk.Label(win, text=icon, fg=self.colors['accent'], bg=self.colors['bg'],
                 font=('Segoe UI', 64)).pack(pady=20)

        tk.Label(win, text=name, fg=self.colors['accent'], bg=self.colors['bg'],
                 font=('Roboto', 22, 'bold')).pack(pady=10)

        btn_f = tk.Frame(win, bg=self.colors['bg'])
        btn_f.pack(pady=30)

        def on_alert_close():
            self.close_alert(win, timer_idx)
            self.alert_count -= 1
            if self.alert_count == 0 and self.active_dialog and self.active_dialog.winfo_exists():
                self.active_dialog.grab_set()

        stop_btn = create_styled_button(btn_f, text=i18n.tr('stop'), command=on_alert_close,
                                        bg=self.colors['danger'], fg='white', width=10, height=1, font=('Roboto', 12, 'bold'))
        stop_btn.pack(side='left', padx=10)

        if typ == i18n.tr('alarm') and obj:
            alarm_key = f"{obj['time']}_{obj['name']}"
            snooze_minutes = obj.get('snooze', self.settings['snooze_min'])
            def snooze_action():
                on_alert_close()
                if alarm_key not in self.snooze_count:
                    self.snooze_count[alarm_key] = 0
                self.snooze_count[alarm_key] += 1
                new_time = (datetime.now() + timedelta(minutes=snooze_minutes)).strftime("%H:%M")
                self.alarms.append({
                    'time': new_time,
                    'name': f"{obj['name']} (Zzz)",
                    'days': [],
                    'active': True,
                    'sound': obj.get('sound', self.settings['selected_sound']),
                    'snooze': snooze_minutes
                })
            snooze_btn = create_styled_button(btn_f, text=i18n.tr('snooze'), command=snooze_action,
                                              bg=self.colors['accent'], fg='black', width=10, height=1, font=('Roboto', 12, 'bold'))
            snooze_btn.pack(side='left', padx=10)

        if launch_app and app_path:
            try:
                if app_args:
                    subprocess.Popen([app_path] + app_args.split(), shell=True)
                else:
                    subprocess.Popen(app_path, shell=True)
            except Exception as e:
                messagebox.showerror(i18n.tr('error'), f"{i18n.tr('launch_error')}: {app_path}\n{e}")

    def close_alert(self, win, timer_idx=None):
        try:
            pygame.mixer.music.stop()
        except:
            pass
        win.destroy()
        if win in self.alert_windows:
            self.alert_windows.remove(win)

        if timer_idx is not None:
            self.stop_mouse_jiggle(timer_idx)

    def stop_all_sounds(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ------------------------------------------------------------------
    # Системный трей
    # ------------------------------------------------------------------
    def create_tray_icon(self):
        try:
            icon_file = resource_path(ICON_PATH)
            image = Image.open(icon_file)
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
        except:
            width = 64
            height = 64
            image = Image.new('RGBA', (width, height), color=(0,0,0,0))
            dc = ImageDraw.Draw(image)
            dc.ellipse((2, 2, width-2, height-2), outline=self.colors['accent'], width=2, fill=self.colors['bg'])
            center_x = width//2
            center_y = height//2
            radius = width//2 - 8
            dc.text((center_x-4, 4), "12", fill=self.colors['text'])
            dc.text((width-20, center_y-6), "3", fill=self.colors['text'])
            dc.text((center_x-4, height-20), "6", fill=self.colors['text'])
            dc.text((4, center_y-6), "9", fill=self.colors['text'])
            hour_angle = 50
            hour_length = radius * 0.5
            hour_x = center_x + hour_length * sin(radians(hour_angle))
            hour_y = center_y - hour_length * cos(radians(hour_angle))
            dc.line((center_x, center_y, hour_x, hour_y), fill=self.colors['accent'], width=3)
            minute_angle = 20
            minute_length = radius * 0.8
            minute_x = center_x + minute_length * sin(radians(minute_angle))
            minute_y = center_y - minute_length * cos(radians(minute_angle))
            dc.line((center_x, center_y, minute_x, minute_y), fill=self.colors['accent'], width=2)
            dc.ellipse((center_x-3, center_y-3, center_x+3, center_y+3), fill=self.colors['accent'])

        global_prevent_text = i18n.tr('global_prevent')
        if self.settings.get('global_prevent', False):
            global_prevent_text = "✓ " + global_prevent_text

        menu = pystray.Menu(
            pystray.MenuItem(i18n.tr('show'), self.show_window, default=True),
            pystray.MenuItem(global_prevent_text, self.toggle_global_prevent),
            pystray.MenuItem(i18n.tr('about'), self.show_about_from_tray),
            pystray.MenuItem(i18n.tr('exit'), self.quit_app)
        )
        self.tray_icon = pystray.Icon("wintick", image, "WinTick", menu)

    def show_about_from_tray(self):
        self.after(0, self.show_about)

    def hide_window(self):
        self.withdraw()
        if not self.tray_icon:
            self.create_tray_icon()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self):
        self.after(0, self._show_window)

    def _show_window(self):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.deiconify()
        self.lift()
        self.focus_force()

    def quit_app(self):
        self.after(0, self._quit_app)

    def _quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.on_closing()

    # ------------------------------------------------------------------
    # Сохранение и загрузка
    # ------------------------------------------------------------------
    def save_data(self):
        try:
            with open('clock_data.json', 'w') as f:
                json.dump({
                    'timers': self.timers,
                    'alarms': self.alarms,
                    'settings': self.settings
                }, f, indent=2)
        except:
            pass

    def load_data(self):
        try:
            with open('clock_data.json', 'r') as f:
                data = json.load(f)
                self.timers = data.get('timers', [])
                self.alarms = data.get('alarms', [])
                saved = data.get('settings', {})
                for k, v in saved.items():
                    if k in self.settings:
                        self.settings[k] = v
        except:
            pass

    def on_closing(self):
        for idx in list(self.mouse_threads.keys()):
            self.stop_mouse_jiggle(idx)
        self.stop_global_prevent()
        if self.volume_window:
            self.volume_window.destroy()
        for w in self.alert_windows:
            try:
                w.destroy()
            except:
                pass
        self.save_data()
        try:
            pygame.mixer.music.stop()
        except:
            pass
        self.destroy()

# ----------------------------------------------------------------------
# Запуск
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = WinTickApp()
    app.mainloop()