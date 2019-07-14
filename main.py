from aqt.utils import showInfo
from anki.hooks import addHook
from anki.utils import json
import os

addon_path  = os.path.dirname(os.path.realpath(__file__))

TOOLTIP = ["Format", "Deformat"]
ICONS = ["format.png", "deformat.png"]

def formatCode(editor):
    style_path = addon_path + "/style.css"
    format = open(style_path).read().replace('\n', '')
    selected_text=editor.web.selectedText()
    # anki evaluates html in its text fields, so take care of it
    # in case you want to learn html
    selected_text = selected_text.replace("<", "&lt;")
    selected_text = selected_text.replace(">", "&gt;")
    selected_text = "<code style=\"" + format + "\">" + selected_text + "</code>"
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(selected_text))


def formatCodeButton(buttons, editor):
    icon_path = addon_path + "/icons/" + ICONS[0]
    if not os.path.exists(icon_path):
        icon_path = ""
    editor._links['formatCode'] = formatCode
    return buttons + [editor._addButton(
        icon_path,
        "formatCode", # link name
        TOOLTIP[0])]

def removeFormatting(editor):
    # don't ask me why the next line is necessary
    # i don't understand either
    # without it it doesn't want remove <code> tag
    editor.web.eval("setFormat('bold');")
    selected_text=editor.web.selectedText()
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(selected_text))

def removeFormattingButton(buttons, editor):
    # without 'global' keywords it complains that the local variable referenced
    # before assignment. figure it out later
    global addon_path
    icon_path = addon_path + "/icons/" + ICONS[1]
    if not os.path.exists(icon_path):
        icon_path = ""
    addon_path = os.path.dirname(__file__)
    editor._links['removeFormatting'] = removeFormatting
    return buttons + [editor._addButton(
        icon_path,
        "removeFormatting", # link name
        TOOLTIP[1])]

addHook("setupEditorButtons", formatCodeButton)
addHook("setupEditorButtons", removeFormattingButton)
