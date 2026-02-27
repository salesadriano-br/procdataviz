import json
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Painel de Processos", layout="wide")

st.markdown("""
<style>*,body,html{font-family:sans-serif !important;}
[data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
[data-testid="stHeader"] { background-color: #CAD0F6 !important; height: 100px !important; padding-bottom: 20px !important; margin-bottom: 16px !important; }
[data-testid="stSidebarContent"] { background-color: #CAD0F6 !important; }
body { background-color: #ffffff !important; }
.main { background-color: #ffffff !important; }
[data-testid="stMainBlockContainer"] { padding-top: 1rem !important; padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; background-color: #ffffff !important; }
.block-container { padding-top: 1rem !important; padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; overflow-x: hidden !important; background-color: #ffffff !important; }
.proc-item-wrap{display:flex;flex-direction:column;gap:8px;background:#fff;padding:8px 0;}.proc-header{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;background:#f8f9ff;border-radius:10px;}.proc-info{display:flex;flex-direction:column;gap:4px;flex:1;}.p-name{font-size:15px;font-weight:600;color:#1a1a2e;}.p-area{font-size:13px;color:#555;}.proc-btn{background:#004ad7;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:600;cursor:pointer;text-decoration:none !important;display:inline-block;}.proc-btn:hover{background:#0035a0;}.ultimos-title{font-size:16px;font-weight:700;color:#1a1a2e;margin:24px 0 12px 0;}</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(__file__), "database")

def load_all_processes():
    processos = []
    if not os.path.exists(DB_PATH):
        return processos
    for fname in sorted(os.listdir(DB_PATH)):
        if fname.endswith(".json"):
            fpath = os.path.join(DB_PATH, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["_filename"] = fname
                    processos.append(data)
            except Exception:
                pass
    return processos

all_procs = load_all_processes()
total = len(all_procs)

proc_items_html = ""
for p in all_procs:
    nome = p.get("nome", "Processo")
    areas = p.get("areas_envolvidas", [])
    area_label = areas[0] if areas else "Geral"
    fname = p.get("_filename", "proposta_comercial_xyz.json")
    proc_items_html += "<div class='proc-item-wrap'>"
    proc_items_html += "<div class='proc-header'>"
    proc_items_html += "<span class='proc-name'>" + nome + "</span>"
    proc_items_html += "<a class='proc-btn' href='#' onclick='window.parent.location.href=window.parent.location.origin+''/detalhes?proc=" + fname + "'''>+ Detalhes</a>"
    proc_items_html += "</div>"
    proc_items_html += "<span class='proc-area'>&#127970; " + area_label + "</span>"
    proc_items_html += "</div>"

areas_set = set()
for p in all_procs:
    for a in p.get("areas_envolvidas", []):
        areas_set.add(a)
areas_list = sorted(areas_set)

area_icons = {
    "Planejamento Comercial": "&#128202;",
    "Desenvolvimento de Negocios": "&#129309;",
    "Vendas": "&#128181;",
    "Engenharia de Solucoes": "&#9881;",
    "Gerenciamento de Projetos": "&#128203;",
    "Financeiro": "&#128176;",
    "Marketing e Comunicacao": "&#128226;",
    "Juridico": "&#9878;",
    "Comite de Aprovacao": "&#9989;",
    "Customer Success e Operacoes": "&#127775;",
}

quick_cards_html = ""
for area in areas_list:
    icon = area_icons.get(area, "&#128196;")
    quick_cards_html += "<div class='quick-card'><span class='qc-icon'>" + icon + "</span><span class='qc-label'>" + area + "</span></div>"

options_html = "<option value=''>Filtrar por área</option>"
for area in areas_list:
    options_html += "<option value='" + area + "'>" + area + "</option>"

html_parts = []
html_parts.append("<div class='outer-wrap'>")
html_parts.append("<div class='sidebar'>")
html_parts.append("<div class='sidebar-title'>Lista de Processos</div>")
html_parts.append("<div class='search-wrap'><input class='search-input' type='text' placeholder='Buscar processo...' /><button class='search-btn' onclick=\"document.querySelector('.filter-btn').click()\">&#128269;</button></div>")
html_parts.append("<select class='area-select'>" + options_html + "</select>")
html_parts.append("<button class='filter-btn'>Filtrar</button>")
html_parts.append("</div>")
html_parts.append("<div class='content'>")
html_parts.append("<div class='welcome-title'>Bem-vindo ao Painel de Processos</div>")
html_parts.append("<p class='welcome-sub'>Use o menu lateral para buscar e filtrar processos por area.</p>")
html_parts.append("<div class='stats-row'><div class='stat-box'>")
html_parts.append("<span class='stat-num'>" + str(total) + "</span>")
html_parts.append("<span class='stat-label'><b>Total de Processos</b><br/>cadastrados no painel</span>")
html_parts.append("</div></div>")
html_parts.append("<div class='section-title'>Busca Rapida</div>")
html_parts.append("<div class='carousel-wrap'>")
html_parts.append("<button class='car-btn car-left' onclick='scrollCar(-1)'>&#8249;</button>")
html_parts.append("<div class='carousel-clip'><div class='carousel' id='qCarousel'>" + quick_cards_html + "</div></div>")
html_parts.append("<button class='car-btn car-right' onclick='scrollCar(1)'>&#8250;</button>")
html_parts.append("</div>")
html_parts.append("<div class='section-title' style='margin-top:28px;'>Últimos Processos</div>")
html_parts.append("""
<style>*,body,html{font-family:sans-serif !important;}
body,html{margin:0;padding:0;box-sizing:border-box;width:100%;overflow-x:hidden}
.outer-wrap{display:flex;width:100%;max-width:1408px;margin:0 auto;background:#fff;min-height:80vh;padding-top:66px}
.sidebar{width:260px;min-width:260px;background:#CAD0F6;padding:32px 20px 20px;border-radius:12px;margin-top:16px}
.sidebar-title{font-size:16px;font-weight:700;color:#1a1a2e;margin-bottom:18px}
.search-wrap{display:flex;gap:6px;margin-bottom:10px;align-items:center;}.search-btn{background:#004ad7;color:#fff;border:none;border-radius:8px;padding:8px 12px;font-size:16px;cursor:pointer;flex-shrink:0;}.search-input{flex:1;padding:8px 12px;border-radius:8px;border:1px solid #004ad7;font-size:14px;background:#ffffff;box-sizing:border-box}
.area-select{width:100%;padding:8px 12px;border-radius:8px;border:1px solid #004ad7;font-size:14px;margin-bottom:10px;background:#fff;color:#1a1a2e;}
.filter-btn{width:100%;padding:8px 0;background:#004ad7;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}
.content{flex:1;min-width:0;overflow:hidden;padding:32px 40px}
.welcome-title{color:#0b5fff !important;font-size:26px;font-weight:700;margin-bottom:6px}
.welcome-sub{color:#555;font-size:14px;margin-bottom:24px}
.stats-row{display:flex;gap:16px;margin-bottom:28px}
.stat-box{background:#f0f4ff;border-radius:10px;padding:16px 24px;display:flex;align-items:center;gap:16px}
.stat-num{font-size:32px;font-weight:700;color:#004ad7}
.stat-label{font-size:13px;color:#444}
.section-title{font-size:16px;font-weight:700;color:#1a1a2e;margin-bottom:14px}
.carousel-wrap{display:flex;align-items:center;margin-bottom:28px;width:100%;max-width:100%;box-sizing:border-box;gap:8px;overflow:hidden}.carousel-clip{flex:1;min-width:0;overflow:hidden}
.carousel{display:flex;gap:14px;overflow:hidden;scroll-behavior:smooth}
.quick-card{min-width:160px;max-width:160px;min-height:140px;background:#fff;border:1px solid #004ad7;border-radius:12px;padding:20px 14px;text-align:center;cursor:pointer;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.qc-icon{font-size:28px;display:block;margin-bottom:8px}
.qc-label{font-size:11px;color:#004ad7;font-weight:600;display:block;line-height:1.3}
.car-btn{flex-shrink:0;background:#004ad7;color:#fff;border:none;border-radius:50%;width:36px;height:36px;font-size:22px;cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:2;line-height:1;padding:0}.car-btn:hover{background:#0035a0}
.proc-list{display:flex;flex-direction:column;gap:12px}
.process-item{display:flex;flex-direction:column
;background:#f8f9ff;border-radius:10px;padding:14px 18px}
.process-header{display:flex;align-items:center;justify-content:space-between;gap:12px}
.process-info{display:flex;flex-direction:column;gap:4px}
.p-name{font-size:15px;font-weight:600;color:#1a1a2e}
.p-area{font-size:13px;color:#555}
.details-btn{background:#004ad7;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:600;cursor:pointer;text-decoration:none !important;display:inline-block}
</style>
<script>
function scrollCar(d){var c=document.getElementById('qCarousel');if(c)c.scrollLeft+=d*260;}
document.addEventListener('click',function(e){var b=e.target.closest('.details-btn');if(b){var p=b.getAttribute('data-proc');if(p)window.parent.location.href=window.parent.location.origin+'/detalhes?proc='+p;}});
</script>
""")
html = "".join(html_parts)
components.html(html, height=900 + len(all_procs)*120, scrolling=True)
