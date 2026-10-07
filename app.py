import streamlit as st
import random

st.set_page_config(page_title="Cesta na Olympiádu", page_icon="🏅", layout="centered")

# Pomocná funkce pro udržení hodnot mezi 0 a 100 (Streamlit progress bar by jinak spadl)
def clamp(n):
    return max(0, min(100, n))

# Inicializace herních statistik
if 'week' not in st.session_state:
    st.session_state.week = 1
    st.session_state.max_weeks = 8
    st.session_state.forma = 40       # Výkonnost hráče
    st.session_state.energie = 80     # Odpočatost
    st.session_state.riziko = 0       # Zda má v těle zakázanou látku
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.zprava = "Začínáš 8týdenní přípravu na Olympiádu. Dávej si pozor na to, co jíš a piješ!"
    st.session_state.wada_zprava = ""

# Herní situace (databáze)
situace = [
    {
        "text": "Máš zánět šlach z přetrénování. Trenér ti nabízí mastičku, kterou koupil na trhu v Asii. 'Zabírá to okamžitě,' tvrdí.",
        "moznosti": {
            "Odmítnout a dát si pár dní pauzu": {"forma": -10, "energie": +20, "riziko": 0, "msg": "Bolest ustoupila pomaleji, ztratil jsi tréninkový čas, ale jsi čistý."},
            "Namázat si to, ať můžu trénovat": {"forma": +15, "energie": 0, "riziko": 40, "msg": "Mastička funguje skvěle, ale bůhví, jestli neobsahovala kortikosteroidy!"}
        }
    },
    {
        "text": "Cítíš na sobě chřipku, ale zítra je klíčový trénink. Spolubydlící ti podává běžný 'Modafen' proti nachlazení z lékárny.",
        "moznosti": {
            "Vzít si prášek, je to přece běžný lék": {"forma": +10, "energie": +10, "riziko": 60, "msg": "Cítíš se lépe, ale léky jako Modafen obsahují pseudoefedrin, který je v soutěži zakázaný!"},
            "Vyležet to s čajem a citronem": {"forma": -15, "energie": +30, "riziko": 0, "msg": "Klasická léčba trvá déle. Přišel jsi o trénink, ale neriskuješ doping."}
        }
    },
    {
        "text": "Po těžkém závodě jsi úplně dehydratovaný. Klubový doktor navrhuje rychlou IV infuzi (kapačku) s vitamíny pro rychlou regeneraci (více než 100 ml).",
        "moznosti": {
            "Dát si kapačku, ať jsem zítra fresh": {"forma": +20, "energie": +30, "riziko": 100, "msg": "Cítíš se jako znovuzrozený. ALE! Nitrožilní infuze nad 100ml za 12 hodin jsou WADA přísně zakázané, i když jde jen o vitamíny!"},
            "Pít hodně vody a minerálek": {"forma": 0, "energie": +10, "riziko": 0, "msg": "Regenerace potrvá celou noc, ale pravidla jsi neporušil."}
        }
    },
    {
        "text": "Koupil sis nový předtréninkový 'nakopávač' z neznámého e-shopu. Má super recenze, ale chybí certifikace o čistotě.",
        "moznosti": {
            "Dát si odměrku, potřebuju energii": {"forma": +15, "energie": +20, "riziko": 30, "msg": "Máš neskutečnou energii na tréninku. Snad ten prášek nebyl kontaminovaný stimulanty."},
            "Vyhodit to a dát si espresso": {"forma": +5, "energie": +5, "riziko": 0, "msg": "Kofein je povolený. Není to sice takový 'kopanec', ale máš jistotu."}
        }
    }
]

def vyhodnot_kolo(volba, data_volby):
    # Aktualizace statistik
    st.session_state.forma = clamp(st.session_state.forma + data_volby["forma"])
    st.session_state.energie = clamp(st.session_state.energie + data_volby["energie"])
    st.session_state.riziko = clamp(st.session_state.riziko + data_volby["riziko"])
    st.session_state.zprava = data_volby["msg"]
    
    st.session_state.wada_zprava = ""
    
    # 25% šance na dopingovou kontrolu
    if random.random() < 0.25:
        if st.session_state.riziko > 0:
            st.session_state.game_over = True
            st.session_state.win = False
            st.session_state.wada_zprava = "🚨 DOPINGOVÁ KONTROLA! Komisaři ti našli v těle zakázané látky. Tvá kariéra končí ostudou s 4letým trestem."
        else:
            st.session_state.wada_zprava = "👮 Namátková dopingová kontrola. Vzorek je čistý! Pokračuješ v přípravě."

    # Posun času
    st.session_state.week += 1
    
    # Konec hry - vítězství
    if st.session_state.week > st.session_state.max_weeks and not st.session_state.game_over:
        st.session_state.game_over = True
        if st.session_state.forma >= 70:
            st.session_state.win = True
        else:
            st.session_state.win = False
            st.session_state.zprava = "Dostal ses na Olympiádu čistý, ale tvá výkonnost byla moc nízká na medaili. Zkus lépe balancovat trénink a regeneraci!"

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# --- UI Hry ---
st.title("🏅 Cesta na Olympiádu")

# Zobrazení statistik ve sloupcích s progress bary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Týden", f"{st.session_state.week} / {st.session_state.max_weeks}")
with col2:
    st.metric("💪 Forma", f"{st.session_state.forma} %")
    st.progress(st.session_state.forma / 100)
with col3:
    st.metric("🔋 Energie", f"{st.session_state.energie} %")
    st.progress(st.session_state.energie / 100)

st.divider()

# Hlášení z předchozího kola
if st.session_state.wada_zprava:
    if "🚨" in st.session_state.wada_zprava:
        st.error(st.session_state.wada_zprava)
    else:
        st.success(st.session_state.wada_zprava)
        
st.info(f"**Deník sportovce:** {st.session_state.zprava}")

# Herní smyčka
if not st.session_state.game_over:
    # Vybereme náhodnou situaci pro tento týden
    random.seed(st.session_state.week) # aby se situace nemenila pri překreslení
    aktualni_situace = random.choice(situace)
    
    st.subheader("Udělej rozhodnutí:")
    st.write(aktualni_situace["text"])
    
    # Vykreslení tlačítek pro volby
    for nazev_volby, data_volby in aktualni_situace["moznosti"].items():
        if st.button(nazev_volby):
            vyhodnot_kolo(nazev_volby, data_volby)
            st.rerun()

else:
    # Závěrečná obrazovka
    st.divider()
    if st.session_state.win:
        st.balloons()
        st.header("🏆 ZLATÁ MEDAILE!")
        st.success(f"Gratulujeme! Zvládl jsi tvrdý trénink, vyhnul ses dopingu a tvá forma ({st.session_state.forma}%) ti zajistila olympijské zlato!")
    elif st.session_state.wada_zprava and "🚨" in st.session_state.wada_zprava:
        st.header("❌ GAME OVER")
        st.error("Byl jsi pozitivně testován. Pamatuj na pravidlo 'Striktní odpovědnosti' – sportovec je zodpovědný za vše, co se najde v jeho těle. Neznalost neomlouvá.")
    else:
        st.header("📉 Nedostatečná forma")
        st.warning(st.session_state.zprava)
        
    st.button("🔄 Hrát znovu a lépe", on_click=reset_game)