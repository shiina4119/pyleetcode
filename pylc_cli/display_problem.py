import html2text
from rich.markdown import Markdown
from rich.padding import Padding
from . import console, con

DIFF_COLOR = {"Easy": "green", "Medium": "yellow", "Hard": "red"}

def display_problem(id: int):
    def replaceSup(r: str) -> str:
        r = r.replace("<sup>", "^")
        r = r.replace("</sup>", "")
        return r

    res = con.execute(
        "SELECT md.frontend_id, md.title, md.difficulty, c.content, c.tags "
        "FROM "
        "metadata AS md "
        "JOIN "
        "content AS c "
        "ON "
        "md.frontend_id = c.frontend_id "
        "WHERE "
        f"md.frontend_id = {id}"
    )
    data = res.fetchone()
    diff = data["difficulty"]
    question_id = data["frontend_id"]
    title = data["title"]
    color = DIFF_COLOR[diff]

    console.print(
        Padding(f"[b][[{color}]{question_id}[/{color}]] [u]{title}[/u][/b]", (1, 2))
    )

    html = "\n".join(map(str, data["content"].split("\n")))
    html = replaceSup(html)
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_emphasis = True
    md = h.handle(html)
    console.print(Padding(Markdown(markup=md), (1, 2)))

    console.print(Padding(f"Topics: {data["tags"]}", (1, 2)))