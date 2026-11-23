"""Ensambla docs/INFORME_EJECUTIVO.pdf a partir de los textos del informe.

Combina la carátula, el resumen ejecutivo (docs/31_resumen_ejecutivo.md), la Parte I
(docs/30_informe_ejecutivo_parte1.md) y la Parte II (docs/31_informe_ejecutivo_parte2.md),
y lo imprime a PDF con Google Chrome o Microsoft Edge en modo sin interfaz.

Requisitos: pip install markdown, y Chrome o Edge instalado.
Uso (desde la raíz del repositorio): python docs/31_ensamblar_informe.py
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
SALIDA = DOCS / "INFORME_EJECUTIVO.pdf"

TITULO = "Abandono de clientes en telecomunicaciones: análisis exploratorio y modelos predictivos"
INTEGRANTES = ["Matías Ferreira", "Julián Schmidt", "Emmanuel Flores"]
FECHA = "Noviembre de 2026"
REPOSITORIO = "https://github.com/julianschmidt1/tpi-analisis-de-datos"

NAVEGADORES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]

CSS = """
@page { size: A4; margin: 2.2cm 2cm 2.2cm 2cm;
  @bottom-center { content: "Introducción al Análisis de Datos · TPI · Página " counter(page);
                   font-size: 8.5pt; color: #666; } }
@page cover { margin: 2.2cm 2.4cm; @bottom-center { content: none; } }
body { font-family: "Segoe UI", Calibri, Arial, sans-serif; font-size: 10.5pt; line-height: 1.5;
       color: #1d1d1f; }
h1 { font-size: 20pt; color: #0b3d6b; border-bottom: 2px solid #0b3d6b; padding-bottom: 6px;
     margin: 0 0 14px 0; page-break-before: always; }
h1.sin-salto { page-break-before: avoid; }
h2 { font-size: 14pt; color: #0b3d6b; margin: 22px 0 8px 0; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #333; margin: 16px 0 6px 0; page-break-after: avoid; }
p { margin: 6px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 4px 0; font-size: 9.2pt;
        page-break-inside: avoid; }
th { background: #0b3d6b; color: #fff; text-align: left; padding: 5px 7px; }
td { border-bottom: 1px solid #d0d7de; padding: 4px 7px; vertical-align: top; }
tr:nth-child(even) td { background: #f5f8fb; }
img { display: block; margin: 10px auto 4px auto; max-width: 100%; max-height: 15cm;
      page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #eef1f4; padding: 1px 4px;
       border-radius: 3px; }
pre { background: #eef1f4; padding: 8px 10px; border-radius: 4px; font-size: 9pt; }
pre code { background: none; padding: 0; }
ul, ol { margin: 6px 0 6px 20px; }
li { margin: 3px 0; }
.cover { page: cover; text-align: center; padding-top: 2.2cm; }
.cover .inst { font-size: 12pt; letter-spacing: 1px; color: #0b3d6b; font-weight: 600; }
.cover .sub { font-size: 11pt; color: #555; margin-top: 4px; }
.cover .materia { font-size: 15pt; margin-top: 2.4cm; color: #222; }
.cover .tipo { font-size: 11pt; color: #555; margin-top: 6px; }
.cover h1.titulo { font-size: 25pt; border: none; page-break-before: avoid; line-height: 1.25;
                   margin: 1.6cm 0 8px 0; color: #0b3d6b; }
.cover .dataset { font-size: 12pt; color: #444; }
.cover .bloque { margin-top: 2.4cm; font-size: 11pt; line-height: 1.7; }
.cover .bloque b { color: #0b3d6b; }
.cover ul { list-style: none; margin: 4px 0; padding: 0; }
.indice { page-break-before: always; }
.indice h2 { margin-top: 0; }
.indice ul { list-style: none; margin: 0; padding: 0; }
.indice li.parte { font-weight: 700; margin-top: 12px; color: #0b3d6b; }
.indice li.sec { margin-left: 16px; }
"""


def buscar_navegador():
    for ruta in NAVEGADORES:
        if ruta.is_file():
            return ruta
    for nombre in ("chrome", "msedge", "google-chrome", "chromium"):
        encontrado = shutil.which(nombre)
        if encontrado:
            return Path(encontrado)
    sys.exit("No se encontró Chrome ni Edge. Instalá alguno para generar el PDF.")


def cuerpo_parte1():
    """Devuelve la Parte I sin su encabezado, sin la sección de fuentes y sin la nota
    de continuidad, que dejan de aplicar en el documento unificado."""
    texto = (DOCS / "30_informe_ejecutivo_parte1.md").read_text(encoding="utf-8")
    inicio = texto.index("## 1. Resumen ejecutivo")
    fin = texto.index("## 7. Fuentes internas y reproducción")
    cuerpo = texto[inicio:fin].rstrip()
    cuerpo = cuerpo.replace("## 1. Resumen ejecutivo", "## 1. Resumen de la Parte I", 1)
    parrafos = cuerpo.split("\n\n")
    parrafos = [p for p in parrafos if not p.startswith("La segunda parte incorporará")]
    return "\n\n".join(parrafos)


def preparar(markdown_texto):
    """Rutas de imágenes absolutas y enlaces internos convertidos a texto."""
    def imagen(m):
        ruta = (DOCS / m.group(2)).resolve()
        return f"![{m.group(1)}]({ruta.as_uri()})"

    texto = re.sub(r"!\[([^\]]*)\]\((\.\./[^)]+)\)", imagen, markdown_texto)
    texto = re.sub(r"(?<!!)\[([^\]]+)\]\((\.\./[^)]+)\)", r"\1", texto)
    return texto


def indice(texto):
    partes = []
    for linea in texto.splitlines():
        if linea.startswith("# Parte"):
            partes.append(f"<li class='parte'>{html.escape(linea[2:])}</li>")
        elif linea.startswith("## "):
            partes.append(f"<li class='sec'>{html.escape(linea[3:])}</li>")
    return "<div class='indice'><h2>Índice</h2><ul>" + "".join(partes) + "</ul></div>"


def caratula():
    integrantes = "".join(f"<li>{html.escape(n)}</li>" for n in INTEGRANTES)
    return f"""
<div class="cover">
  <div class="inst">UNIVERSIDAD TECNOLÓGICA NACIONAL</div>
  <div class="sub">Facultad Regional Avellaneda · Tecnicatura Universitaria en Programación</div>
  <div class="materia"><b>Introducción al Análisis de Datos</b></div>
  <div class="tipo">Trabajo Práctico Integrador (Segundo Parcial) · Informe técnico-ejecutivo</div>
  <h1 class="titulo">{html.escape(TITULO)}</h1>
  <div class="dataset">Dataset: Telco Customer Churn (Kaggle)</div>
  <div class="bloque">
    <div><b>División:</b> 343 · Segundo cuatrimestre de 2026</div>
    <div><b>Docente a cargo:</b> Enzo Martín Zotti</div>
    <div><b>Integrantes:</b></div>
    <ul>{integrantes}</ul>
    <div><b>Fecha:</b> {html.escape(FECHA)}</div>
    <div><b>Repositorio:</b> {html.escape(REPOSITORIO)}</div>
  </div>
</div>"""


def construir_html():
    resumen = (DOCS / "31_resumen_ejecutivo.md").read_text(encoding="utf-8")
    parte2 = (DOCS / "31_informe_ejecutivo_parte2.md").read_text(encoding="utf-8")
    titulo_parte1 = "# Parte I · Problema, metodología, limpieza y análisis exploratorio"

    fuente = "\n\n".join([titulo_parte1, cuerpo_parte1(), parte2])
    fuente = preparar(fuente)
    resumen = preparar(resumen)

    convertir = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    html_resumen = convertir.convert(resumen)
    convertir.reset()
    html_cuerpo = convertir.convert(fuente)
    # El resumen es una sección con salto de página propio, como los títulos de parte.
    html_resumen = html_resumen.replace("<h2>", "<h1 class='sin-salto'>", 1).replace("</h2>", "</h1>", 1)

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Informe ejecutivo · TPI</title>
<style>{CSS}</style></head><body>
{caratula()}
{indice("## Resumen ejecutivo" + chr(10) + fuente)}
<div style="page-break-before: always">{html_resumen}</div>
{html_cuerpo}
</body></html>"""


def metadatos():
    """Pone título y autores al PDF (Chrome deja su identificador como creador)."""
    try:
        import pymupdf
    except ImportError:
        return
    temporal = SALIDA.with_suffix(".tmp")
    with pymupdf.open(SALIDA) as doc:
        doc.set_metadata({
            "title": TITULO,
            "author": ", ".join(INTEGRANTES),
            "subject": "Introducción al Análisis de Datos · UTN FRA · División 343",
            "creator": "",
            "producer": "",
        })
        doc.save(temporal, garbage=3, deflate=True)
    temporal.replace(SALIDA)


def main():
    navegador = buscar_navegador()
    SALIDA.unlink(missing_ok=True)  # si Chrome falla, no se da por bueno un PDF viejo
    with tempfile.TemporaryDirectory() as tmp:
        ruta_html = Path(tmp) / "informe.html"
        ruta_html.write_text(construir_html(), encoding="utf-8")
        perfil = Path(tmp) / "perfil"
        comando = [
            str(navegador), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--allow-file-access-from-files", f"--user-data-dir={perfil}",
            f"--print-to-pdf={SALIDA}", ruta_html.as_uri(),
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=180)
    if not SALIDA.is_file() or SALIDA.stat().st_size == 0:
        sys.exit(f"No se generó el PDF.\n{resultado.stderr}")
    metadatos()
    print(f"PDF generado: {SALIDA.relative_to(RAIZ)} ({SALIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
