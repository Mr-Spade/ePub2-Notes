#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import tkinter as tk
from tkinter import simpledialog


def run(bk):
    cssfound = 0
    lastid = 0
    fnid = 0
    fnid1 = 0
    filename = ""
    # Uncomment next line for test purposes
    # print (str(cssfound) + ' ' + str(lastid) + ' ' + str(fnid))
    # Test for existing footnote.css - if so, set cssfound variable to 1
    for id, href in bk.css_iter():
        filename = os.path.basename(href)
        # print(id, href+'\n'+ filename+'1')
        if filename == "footnote.css":
            cssfound = 1
        else:
            print("-----")
    alist = [0]
    for [id, href] in bk.text_iter():
        html = bk.readfile(id)
        found1 = re.search(r"fnref(\d+)", html)
        # fnid1 = found1
        if found1 is not None:
            for m in re.finditer(r"fnref(\d+)", html):
                alist.append(int(m.group(1)))
    # Uncomment next line for test purposes
    # print(max(alist))
    fnid = max(alist)
    if fnid > 0:
        returnres(fnid, bk, cssfound)
    else:
        insertnotes(0, bk, cssfound)
    return 0


def returnres(fnid, bk, cssfound):
    # Dialog warning user for found notes
    # and allowing to inject new start reference number for new notes
    title = "Existing notes found!"
    prompt = (
        "There seems to be notes in this book already.\nNotes IDs will continue from >> "
        + str(fnid + 1)
        + " << or any entered below.\n\nNew notes will be inserted below existing.\n"
    )
    application_window = tk.Tk()
    application_window.withdraw()
    result = simpledialog.askinteger(title, prompt, initialvalue=fnid + 1, minvalue=1)
    if result is not None:
        fnid = result - 1
        insertnotes(fnid, bk, cssfound)
    else:
        print("ePub2-notes cancelled by your request")
        return 0


def insertnotes(fnid, bk, cssfound):
    # Making and inserting the notes:
    # Iterate through all xhtml/html-files in the epub and
    # 1) Inserts link(s) to found notes in the text and link to footnote.css
    # in files with notes
    # 2)Moves found notes to the end of the file in which it's found
    for [id, href] in bk.text_iter():
        html = bk.readfile(id)
        html_original = html
        found = re.search(r"\^\[.*?\]", html)
        if found is not None:
            # only once for each file with notes
            cssexist = re.search(r"\.\.\/Styles\/footnote\.css", html)
            if not cssexist:
                html = re.sub(
                    r"\<\/head\>",
                    r'<link href="../Styles/footnote.css" rel="stylesheet" type="text/css"/>\n</head>',
                    html,
                )
            while found is not None:
                # once for every found note. If necessary,
                # replace the words "Note" and "Back" with whatever you see fit
                fnid = fnid + 1
                html = re.sub(
                    r"\^\[(.*?)\]",
                    r'<a class="footnoteRef" href="#fn'
                    + str(fnid)
                    + '" id="fnref'
                    + str(fnid)
                    + '">Note '
                    + str(fnid)
                    + ")</a>",
                    html,
                    1,
                )
                html = re.sub(
                    r"\<\/body\>",
                    r'\n\n<div class="footnote" id="fn'
                    + str(fnid)
                    + '">\n<p class="fn"><b>Note '
                    + str(fnid)
                    + '</b></p>\n<p class="fn">'
                    + found.group(0).strip("[]^").replace("\\", "\\\\")
                    + '</p>\n<p class="fnrightalign"><a href="#fnref'
                    + str(fnid)
                    + '">Back</a></p>\n</div>\n</body>',
                    html,
                    1,
                )
                print(id, href, "Note " + str(fnid) + ":" + found.group(0).strip("[]^"))
                found = re.search(r"\^\[.*?\]", html)
        else:
            print(id, href, "No notes found")
        if not html == html_original:
            bk.writefile(id, html)
        lastid = id
        # Uncomment next line for test purposes
        # print(str(cssfound) + ' ' + str(lastid) + ' ' + str(fnid))
        # css
    if fnid > 0 and cssfound == 0:
        cssdata = ""
        basename = "footnote.css"
        uid = "footnotecss"
        mime = "text/css"
        bk.addfile(uid, basename, cssdata, mime)
    elif cssfound == 1:
        print(
            '\n\n!!!\nExisting file "footnote.css" found. If this was NOT created by a previous run of this plugin, or you have edited it, you should check the formatting of any newly inserted footnotes.'
        )
    else:
        print("Finished …")
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
