#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import tkinter as tk
from tkinter import simpledialog


def run(bk):
    # cssfound = 0
    lastid = 0
    fnid = 0
    footnote_dict = dict()
    fnid1 = 0
    filename = ""
    # Uncomment next line for test purposes
    # print (str(cssfound) + ' ' + str(lastid) + ' ' + str(fnid))
    # Test for existing footnote.css - if so, set cssfound variable to 1
    # for id, href in bk.css_iter():
    #     filename = os.path.basename(href)
    #     # print(id, href+'\n'+ filename+'1')
    #     if filename == "footnote.css":
    #         cssfound = 1
    #     else:
    #         print("-----")
    # alist = [0]
    for [id, href] in bk.text_iter():
        current_list = [0]
        html = bk.readfile(id)
        found1 = re.search(r"fnref(\d+)", html)
        # fnid1 = found1
        if found1 is not None:
            for m in re.finditer(r"fnref(\d+)", html):
                # alist.append(int(m.group(1)))
                current_list.append(int(m.group(1)))
        footnote_dict[id] = max(current_list)
    # Uncomment next line for test purposes
    # print(max(alist))
    # fnid = max(alist)
    # if fnid > 0:
    #     returnres(fnid, bk)
    # else:
    #     insertnotes(0, bk)
    insertnotes(footnote_dict, bk)
    return 0


# def returnres(fnid, bk):
#     # Dialog warning user for found notes
#     # and allowing to inject new start reference number for new notes
#     title = "Existing notes found!"
#     prompt = (
#         "There seems to be notes in this book already.\nNotes IDs will continue from >> "
#         + str(fnid + 1)
#         + " << or any entered below.\n\nNew notes will be inserted below existing.\n"
#     )
#     application_window = tk.Tk()
#     application_window.withdraw()
#     result = simpledialog.askinteger(title, prompt, initialvalue=fnid + 1, minvalue=1)
#     if result is not None:
#         fnid = result - 1
#         insertnotes(fnid, bk)
#     else:
#         print("ePub2-notes cancelled by your request")
#         return 0


def insertnotes(fnid, footnote_dict: dict[any, int], bk):
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
            # cssexist = re.search(r"\.\.\/Styles\/footnote\.css", html)
            # if not cssexist:
            #     html = re.sub(
            #         r"\<\/head\>",
            #         r'<link href="../Styles/footnote.css" rel="stylesheet" type="text/css"/>\n</head>',
            #         html,
            #     )
            current_footnote_id = footnote_dict[id]
            while found is not None:
                # once for every found note. If necessary,
                # replace the words "Note" and "Back" with whatever you see fit
                # fnid = fnid + 1
                current_footnote_id += 1
                html = re.sub(
                    r"\^\[(.*?)\]",
                    r'<sup><small><a class="footnoteRef" href="#fn'
                    + str(current_footnote_id)
                    + '" id="fnref'
                    + str(current_footnote_id)
                    + '">['
                    + str(current_footnote_id)
                    + "]</a></small></sup>",
                    html,
                    1,
                )
                html = re.sub(
                    r"\<\/body\>",
                    r'\n\n<div class="footnote" id="fn'
                    + str(current_footnote_id)
                    + '"><a href="#fnref'
                    + str(current_footnote_id)
                    + '">['
                    + str(current_footnote_id)
                    + "]</a>"
                    + found.group(0).strip("[]^").replace("\\", "\\\\")
                    + "</div>\n</body>",
                    html,
                    1,
                )
                print(
                    id,
                    href,
                    "Note "
                    + str(current_footnote_id)
                    + ":"
                    + found.group(0).strip("[]^"),
                )
                found = re.search(r"\^\[.*?\]", html)
        else:
            print(id, href, "No notes found")
        if not html == html_original:
            bk.writefile(id, html)
        lastid = id
        # Uncomment next line for test purposes
        # print(str(cssfound) + ' ' + str(lastid) + ' ' + str(fnid))
        # css
    # if fnid > 0 and cssfound == 0:
    #     cssdata = ""
    #     basename = "footnote.css"
    #     uid = "footnotecss"
    #     mime = "text/css"
    #     bk.addfile(uid, basename, cssdata, mime)
    # elif cssfound == 1:
    #     print(
    #         '\n\n!!!\nExisting file "footnote.css" found. If this was NOT created by a previous run of this plugin, or you have edited it, you should check the formatting of any newly inserted footnotes.'
    #     )
    # else:
    print("Finished …")
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
