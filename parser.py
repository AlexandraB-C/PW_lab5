import re
import html as html_lib


# drop script/style blocks, then strip all tags
_script = re.compile(r"<(script|style)[^>]*>.*?</(script|style)>", re.IGNORECASE | re.DOTALL)
_block  = re.compile(r"<(br|p|div|h[1-6]|li|tr|td|th)[^>]*>", re.IGNORECASE)
_tag    = re.compile(r"<[^>]+>")
_spaces = re.compile(r"[ \t]+")


def strip_html(s):
    s = _script.sub("", s)
    s = _block.sub("\n", s)
    s = _tag.sub("", s)
    s = html_lib.unescape(s)
    s = _spaces.sub(" ", s)

    # collapse extra blank lines
    lines = [l.strip() for l in s.splitlines()]
    out = []
    blank = 0
    for l in lines:
        if not l:
            blank += 1
            if blank == 1:
                out.append("")
        else:
            blank = 0
            out.append(l)

    return "\n".join(out).strip()
