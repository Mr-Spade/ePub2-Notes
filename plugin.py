import sys
import re


def run(bk):
    footnote_dict = dict()
    for [id, href] in bk.text_iter():
        current_list = [0]
        html = bk.readfile(id)
        found1 = re.search(r"fnref(\d+)", html)
        if found1 is not None:
            for m in re.finditer(r"fnref(\d+)", html):
                current_list.append(int(m.group(1)))
        footnote_dict[id] = max(current_list)
    insertnotes(footnote_dict, bk)
    return 0


def insertnotes(footnote_dict: dict[any, int], bk):
    for [id, href] in bk.text_iter():
        html = bk.readfile(id)
        html_original = html
        found = re.search(r"\^\[.*?\]", html)
        if found is not None:
            current_footnote_id = footnote_dict[id]
            while found is not None:
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
    print("Finished …")
    return 0


if __name__ == "__main__":
    sys.exit(-1)
