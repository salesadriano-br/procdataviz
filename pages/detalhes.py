import streamlit as st
import json
import os
from streamlit.components.v1 import html as components_html

st.set_page_config(page_title="Detalhes do Processo", layout="wide")

# CSS para esconder elementos do Streamlit e garantir fundo branco
st.markdown("""
<style>*,body,html{font-family:sans-serif !important;}
[data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebarContent"] { background-color: #CAD0F6 !important; }
body { background-color: #ffffff !important; }
.main { background-color: #ffffff !important; }
[data-testid="stMainBlockContainer"] { padding: 0 !important; background-color: #ffffff !important; }
.block-container { padding: 0 !important; max-width: 100% !important; background-color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")

def load_process(filename):
    filepath = os.path.join(DB_PATH, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

proc_file = st.query_params.get("proc", "proposta_comercial_xyz.json")
proc = load_process(proc_file)

if not proc:
    st.error("Processo nao encontrado.")
    st.stop()

proc_nome = proc.get("nome", "Processo")
proc_data = proc.get("data", "")
proc_versao = proc.get("versao", "")
proc_elaborado = proc.get("elaborado_por", "")
num_etapas = proc.get("total_etapas", 0)
areas = proc.get("areas_envolvidas", [])
num_areas = len(areas)
etapas = proc.get("etapas", [])

# Construir nodes para o diagrama
nodes_js = ""
for i, etapa in enumerate(etapas):
    num = etapa.get("numero", i+1)
    titulo = etapa.get("titulo", "").replace('"', "'").replace("<", "&lt;").replace(">", "&gt;")
    nodes_js += f'{{ id: {num}, label: "{num}. {titulo}" }},'

# Construir cards das etapas
etapas_cards = ""
for etapa in etapas:
    num = etapa.get("numero", "")
    titulo = etapa.get("titulo", "")
    area = etapa.get("area", "")
    resp = etapa.get("responsavel", "")
    cargo = etapa.get("cargo", "")
    desc = etapa.get("descricao", "")
    etapas_cards += f"""
    <div style="background:#fff;border:1.5px solid #e0e6f8;border-radius:12px;padding:18px 20px;margin-bottom:14px;box-shadow:0 1px 4px rgba(0,74,215,0.06);">
        <div style="font-size:11px;font-weight:700;color:#004ad7;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Etapa {num}</div>
        <div style="font-size:16px;font-weight:700;color:#1a1a2e;margin-bottom:10px;">{titulo}</div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:#555;margin-bottom:8px;">
            <span>&#127970; <strong>Area:</strong>&nbsp;{area}</span>
            <span>&#128100; <strong>Responsavel:</strong>&nbsp;{resp}</span>
            <span>&#128188; <strong>Cargo:</strong>&nbsp;{cargo}</span>
        </div>
        <div style="font-size:14px;color:#444;line-height:1.6;margin-top:8px;padding-top:8px;border-top:1px solid #f0f0f0;">{desc}</div>
    </div>
    """

# HTML completo e unificado com header
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>*,body,html{font-family:sans-serif !important;}
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', 'Segoe UI', sans-serif; }}
body {{ background: #fff; padding: 0; margin: 0; }}
.header {{
    height: 100px;
    width: 100%;
    background-color: #CAD0F6;
    display: flex;
    align-items: center;
    padding: 0 32px;
}}
.header h1 {{
    font-size: 24px;
    font-weight: 700;
    color: #004ad7;
}}
.page-wrapper {{
    max-width: 1408px;
    margin: 0 auto;
    padding: 28px 32px;
    background: #fff;
    min-height: calc(100vh - 100px);
}}
.back-btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 18px;
    border: 1.5px solid #004ad7;
    border-radius: 8px;
    color: #004ad7;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    background: #fff;
    cursor: pointer;
    margin-bottom: 22px;
}}
.back-btn:hover {{ background: #f0f4ff; }}
.proc-nome {{ font-size: 24px; font-weight: 800; color: #004ad7; margin: 0 0 10px 0; }}
.proc-meta {{ display: flex; gap: 20px; font-size: 14px; color: #444; margin-bottom: 22px; flex-wrap: wrap; }}
.proc-meta span {{ display: flex; align-items: center; gap: 4px; }}
.boxes-row {{ display: flex; gap: 14px; margin-bottom: 28px; flex-wrap: wrap; }}
.info-box {{ background: #f5f7ff; border: 1.5px solid #CAD0F6; border-radius: 12px; padding: 16px 24px; display: flex; align-items: center; gap: 12px; min-width: 200px; }}
.ib-num {{ font-size: 34px; font-weight: 800; color: #004ad7; }}
.ib-label {{ font-size: 14px; color: #004ad7; font-weight: 700; }}
.ib-sub {{ font-size: 12px; color: #888; }}
.section-title {{ font-size: 17px; font-weight: 700; color: #004ad7; margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px; }}
hr.divider {{ border: none; border-top: 1px solid #e0e6f8; margin-bottom: 16px; }}
.zoom-bar {{ display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }}
.zoom-btn {{ width: 30px; height: 30px; border-radius: 6px; border: none; background: #004ad7; color: #fff; font-size: 18px; cursor: pointer; font-weight: bold; }}
.zoom-reset {{ padding: 4px 12px; border-radius: 6px; border: 1.5px solid #004ad7; background: #fff; color: #004ad7; font-size: 12px; cursor: pointer; font-weight: 600; }}
.zoom-level {{ font-size: 13px; color: #444; font-weight: 700; min-width: 40px; }}
.diagram-outer {{ overflow: auto; border: 1.5px solid #e0e6f8; border-radius: 12px; background: #f9faff; padding: 20px; width: 100%; min-height: 200px; max-height: 500px; }}
#diagramInner {{ transform-origin: top left; transition: transform 0.2s; display: flex; flex-wrap: wrap; gap: 0; align-items: center; padding: 20px; }}
.node {{ background: #fff; border: 2px solid #004ad7; border-radius: 10px; padding: 12px 18px; font-size: 13px; font-weight: 600; color: #004ad7; white-space: nowrap; text-align: center; box-shadow: 0 2px 6px rgba(0,74,215,0.12); min-width: 180px; }}
.arrow {{ color: #004ad7; font-size: 22px; padding: 0 8px; font-weight: bold; }}
</style>
</head>
<body>
<div class="header">
    <h1>Painel de Processos</h1>
</div>
<div class="page-wrapper">
    <a class="back-btn" href="/" onclick="window.top.location.href='/'; return false;">&#8592; Voltar ao Painel</a>
    <h2 class="proc-nome">{proc_nome}</h2>
    <div class="proc-meta">
        <span>&#128197; <strong>Data:</strong>&nbsp;{proc_data}</span>
        <span>&#128196; <strong>Versao:</strong>&nbsp;{proc_versao}</span>
        <span>&#9999;&#65039; <strong>Elaborado por:</strong>&nbsp;{proc_elaborado}</span>
    </div>
    <div class="boxes-row">
        <div class="info-box"><span class="ib-num">{num_etapas}</span><span><div class="ib-label">Etapas do Processo</div><div class="ib-sub">mapeadas neste fluxo</div></span></div>
        <div class="info-box"><span class="ib-num">{num_areas}</span><span><div class="ib-label">Areas Envolvidas</div><div class="ib-sub">neste processo</div></span></div>
    </div>
    <div class="section-title">&#128200; Diagrama do Processo</div>
    <hr class="divider">
    <div class="zoom-bar">
        <button class="zoom-btn" onclick="changeZoom(20)">+</button>
        <button class="zoom-btn" onclick="changeZoom(-20)">-</button>
        <button class="zoom-reset" onclick="resetZoom()">Resetar</button>
        <span class="zoom-level" id="zoomLabel">100%</span>
    </div>
    <div class="diagram-outer" id="diagramOuter">
        <div id="diagramInner"></div>
    </div>
    <div style="margin-top:32px;">
        <div class="section-title">&#128203; Descricao do Processo</div>
        {etapas_cards}
    </div>
</div>
<script>
var nodes = [{nodes_js}];
var inner = document.getElementById('diagramInner');
nodes.forEach(function(n, i) {{
    var box = document.createElement('div');
    box.className = 'node';
    box.textContent = n.label;
    inner.appendChild(box);
    if (i < nodes.length - 1) {{
        var arr = document.createElement('span');
        arr.className = 'arrow';
        arr.textContent = '\u2192';
        inner.appendChild(arr);
    }}
}});
var zoom = 100;
function changeZoom(d) {{
    zoom = Math.min(200, Math.max(40, zoom + d));
    inner.style.transform = 'scale(' + zoom/100 + ')';
    document.getElementById('zoomLabel').textContent = zoom + '%';
}}
function resetZoom() {{
    zoom = 100;
    inner.style.transform = 'scale(1)';
    document.getElementById('zoomLabel').textContent = '100%';
}}
</script>
</body>
</html>
"""

components_html(full_html, height=4500, scrolling=True)