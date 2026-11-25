from pathlib import Path

html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>QR-payload</title>
<style>body{font-family:sans-serif;margin:40px;}</style></head>
<body>
<h1>Описание формата QR-payload</h1>
<p>Строка вида: <code>id=&lt;int&gt;;ts=&lt;int&gt;sig=&lt;hex&gt;</code></p>
<p>Где <code>id</code> — номер участника, <code>ts</code> — метка времени, <code>sig</code> — учебная подпись (sha256).</p>
</body>
</html>"""

Path("public").mkdir(exist_ok=True)
Path("public/index.html").write_text(html, encoding="utf-8")
print("Docs generated in public/index.html")