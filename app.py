import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import os
import re
import hashlib
import sqlite3
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Re-Connect | L'Algorithme de l'Amour", 
    page_icon="🌙", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECTION CSS ULTRA-PREMIUM (ESTHÉTIQUE ZEN ET CHALEUREUSE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    
    /* Variables globales et fond */
    html, body, [class*="css"], .stApp {
        font-family: 'Quicksand', sans-serif;
        background-color: #FAF6F0; /* Crème doux */
        color: #4A3E4D;
    }
    
    /* Enlever les marges par défaut de Streamlit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Titres magnifiés */
    h1, h2, h3, h4 {
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 700 !important;
        color: #4E3D53 !important;
    }
    
    /* Bannière d'en-tête interactive */
    .hero-banner {
        background: linear-gradient(135deg, #8E7C93 0%, #B59DAF 100%);
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(142, 124, 147, 0.15);
        margin-bottom: 30px;
        color: #FFFFFF !important;
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 3rem !important;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .hero-banner p {
        color: #F3ECEF !important;
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto;
    }

    /* Cartes Interactives (Glassmorphism Doux) */
    .custom-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 24px rgba(109, 89, 122, 0.05);
        border: 1px solid rgba(142, 124, 147, 0.08);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(109, 89, 122, 0.1);
    }
    
    /* Badge de Conseil et Alertes douces */
    .badge-tip {
        display: inline-block;
        background-color: #EAE2EC;
        color: #6D597A;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 12px;
    }
    
    /* Bouton Panique et Boutons Premium */
    .stButton>button {
        background: linear-gradient(135deg, #B56576 0%, #C97A8E 100%);
        color: white !important;
        border-radius: 30px;
        border: none;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(181, 101, 118, 0.2);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 10px 25px rgba(181, 101, 118, 0.3);
        background: linear-gradient(135deg, #934B5B 0%, #B56576 100%);
        color: white !important;
    }
    
    /* Bouton d'urgence latéral distinct */
    .panic-btn>button {
        background: linear-gradient(135deg, #E56B6F 0%, #EA8C90 100%) !important;
        box-shadow: 0 6px 20px rgba(229, 107, 111, 0.3) !important;
    }
    
    /* Cartes de Conseils Personnalisés */
    .conseil-card {
        background-color: #FAF5F5;
        border-left: 5px solid #B56576;
        padding: 20px;
        border-radius: 0 15px 15px 0;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .conseil-card h5 {
        margin-top: 0;
        color: #B56576 !important;
        font-weight: 600;
    }

    /* Style des Onglets (Tabs) en haut */
    div[data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #EAE2EC;
        padding: 10px;
        border-radius: 25px;
        justify-content: center;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 20px !important;
        padding: 12px 24px !important;
        border: none !important;
    }
    button[data-baseweb="tab"] p {
        color: #4E3D53 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #8E7C93 0%, #A28FA7 100%) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: white !important;
    }
    
    /* Sidebar restylée */
    [data-testid="stSidebar"] {
        background-color: #F0EAE1 !important;
    }
    
    /* Custom radio boxes */
    div[data-testid="stRadio"] > div {
        background-color: #F8F5F0;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid rgba(142, 124, 147, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES DE SESSION ---
if 'profiles' not in st.session_state:
    st.session_state.profiles = {}
if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'temoignages' not in st.session_state:
    st.session_state.temoignages = [
        {"nom": "Alexandre", "texte": "J'avais un score estimé à 23% au tout début. Grâce au suivi des 30 jours, j'ai tenu bon et j'ai arrêté d'étouffer mon ex. Elle m'a recontacté d'elle-même au bout du 28ème jour.", "date": "Il y a 3 jours"},
        {"nom": "Mélissa", "texte": "Le dictionnaire de messages m'a évité de passer pour une personne acquise quand il m'a envoyé un simple 'Ça va ?'. L'approche pragmatique de Camil change tout.", "date": "Il y a 1 semaine"},
        {"nom": "Lucas", "texte": "Style d'attachement anxieux détecté... Ce diagnostic m'a ouvert les yeux sur mes propres comportements. Une boussole incroyable.", "date": "Il y a 2 semaines"}
    ]
if 'tracker_days' not in st.session_state:
    st.session_state.tracker_days = 0
if 'last_checkin' not in st.session_state:
    st.session_state.last_checkin = None
if 'panic_mode' not in st.session_state:
    st.session_state.panic_mode = False
if 'attachment_style' not in st.session_state:
    st.session_state.attachment_style = None

# --- FONCTION DE GÉNÉRATION D'IMAGE ---
def generate_share_image(score, profil):
    img = Image.new('RGB', (1080, 1920), color='#6D597A') # Violet élégant
    d = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
        font_score = ImageFont.truetype("arial.ttf", 250)
        font_text = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font_title = font_score = font_text = ImageFont.load_default()

    d.text((100, 300), "Re-Connect", fill="#FDFBF7", font=font_title)
    d.text((100, 450), "Mes chances de retour :", fill="#FDFBF7", font=font_text)
    d.text((100, 700), f"{score:.1f}%", fill="#E56B6F", font=font_score)
    message = "Espoir mathématique..." if score > 50 else "Reconstruction en cours..."
    d.text((100, 1100), message, fill="#FDFBF7", font=font_title)
    d.text((100, 1600), "Calcule tes chances sur :", fill="#FDFBF7", font=font_text)
    d.text((100, 1700), "@maths_demo", fill="#FDFBF7", font=font_title)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- CONSEILS STRUCTURÉS ---
def get_conseils_personnalises(raison, style, entourage, autre_personne):
    conseils = []
    
    conseils_raison = {
        "Perte de sentiments": "🔥 **Analyse de la perte d'attraction :** En physique comme en psychologie, l'attraction ne se négocie pas par la logique. Essayer de convaincre ton ex par des arguments textuels produit l'effet inverse. Coupe les ponts immédiatement pour réinitialiser sa mémoire affective.",
        "Étouffement (Besoin d'espace)": "🍃 **La dynamique de pression :** Ton ex s'est senti(e) piégé(e). Chaque message envoyé agit comme un pas de trop dans sa zone de sécurité. Ton silence complet est le plus grand cadeau de respect que tu puisses lui faire actuellement.",
        "Distance géographique": "📍 **Le défi de la présence physique :** La distance altère le besoin de sécurité immédiat. Le retour ne pourra pas se planifier virtuellement. Utilise le silence pour créer un manque si intense qu'une opportunité physique de rencontre se dessinera naturellement.",
        "Toxicité / Conflits": "⚡ **Le pic d'adrénaline négative :** Vos derniers échanges ont laissé des cicatrices émotionnelles vives. Ton ex t'associe actuellement à de l'anxiété ou de la colère. Il faut un minimum de 21 jours de silence radio absolu pour que l'amygdale cérébrale de ton ex s'apaise."
    }
    if raison in conseils_raison:
        conseils.append(conseils_raison[raison])

    conseils_style = {
        "Anxieux": "🧠 **Ton Profil Anxieux dit :** Tu as une tendance naturelle à sur-analyser chaque signal (heures de connexion, longueur des SMS). Rappelle-toi que le silence de ton ex n'est pas une punition, c'est une pause nécessaire. Canalise cette énergie dans le sport ou l'écriture créative.",
        "Évitant": "🛡️ **Ton Profil Évitant dit :** Tu as tendance à masquer ta tristesse sous une carapace de détachement ou d'hyperactivité. Ne fuis pas tes émotions. S'autoriser à être triste est la seule façon saine de guérir.",
        "Désorganisé": "🎢 **Ton Profil Désorganisé dit :** Tu oscilles entre une envie folle de lui écrire et une colère noire. Prends 10 respirations profondes avant chaque décision impulsive.",
        "Sécure": "☀️ **Ton Profil Sécure dit :** Tu gères la situation avec recul. Continue à respecter tes propres limites tout en maintenant cette distance saine."
    }
    if style and style in conseils_style:
        conseils.append(conseils_style[style])

    if entourage == "Hostile":
        conseils.append("👥 **Facteur Social Hostile :** Les amis ou la famille de ton ex alimentent sa décision. Ne cherche jamais à te justifier auprès d'eux. Ton élégance silencieuse sera ta meilleure défense.")
    if autre_personne == "Oui (Relation pansement)":
        conseils.append("💔 **La Relation Pansement :** Ton ex essaie désespérément de fuir la douleur de la rupture avec quelqu'un d'autre. Ces relations durent rarement plus de 3 mois car elles reposent sur une fuite émotionnelle et non sur un choix construit.")

    return conseils

# --- SYSTÈME DE COMPTES & MATCHMAKING (BASE DE DONNÉES LOCALE) ---
DB_PATH = "reconnect_users.db"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL,
            telephone TEXT,
            attachment_style TEXT,
            score REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def hash_password(password, salt_hex=None):
    if salt_hex is None:
        salt_hex = os.urandom(16).hex()
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), 100_000).hex()
    return pw_hash, salt_hex

def create_user(email, password, prenom, nom, telephone):
    pw_hash, salt_hex = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (email, password_hash, salt, prenom, nom, telephone, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (email.lower().strip(), pw_hash, salt_hex, prenom.strip(), nom.strip(), telephone.strip() if telephone else None, datetime.datetime.now().isoformat())
        )
        conn.commit()
        ok = True
    except sqlite3.IntegrityError:
        ok = False
    conn.close()
    return ok

def verify_login(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, salt, prenom, nom FROM users WHERE email = ?", (email.lower().strip(),))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    stored_hash, salt_hex, prenom, nom = row
    test_hash, _ = hash_password(password, salt_hex)
    if test_hash == stored_hash:
        return {"email": email.lower().strip(), "prenom": prenom, "nom": nom}
    return None

def update_user_resultats(email, attachment_style=None, score=None):
    if not email:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if attachment_style is not None:
        c.execute("UPDATE users SET attachment_style = ? WHERE email = ?", (attachment_style, email))
    if score is not None:
        c.execute("UPDATE users SET score = ? WHERE email = ?", (float(score), email))
    conn.commit()
    conn.close()

def get_my_score(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT score FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None

def get_matchs(email, attachment_style, score, limit=12):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT prenom, attachment_style, score FROM users WHERE email != ? AND score IS NOT NULL", (email,))
    rows = c.fetchall()
    conn.close()
    matchs = []
    for prenom, r_style, r_score in rows:
        style_ecart = 0 if (attachment_style and r_style == attachment_style) else 20
        score_ecart = abs((score or 0) - r_score)
        matchs.append({"prenom": prenom, "style": r_style, "score": r_score, "proximite": style_ecart + score_ecart})
    matchs.sort(key=lambda x: x["proximite"])
    return matchs[:limit]

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #4E3D53;'>👤 Espace Personnel</h3>", unsafe_allow_html=True)
    new_profile_name = st.text_input("Créer un dossier de suivi", placeholder="Ex: Camil & Sarah")
    
    if st.button("📁 Ouvrir le dossier", use_container_width=True):
        if new_profile_name and new_profile_name not in st.session_state.profiles:
            st.session_state.profiles[new_profile_name] = {}
            st.session_state.current_profile = new_profile_name
            st.success("Dossier créé et activé !")
            st.rerun()
            
    if st.session_state.profiles:
        st.session_state.current_profile = st.selectbox(
            "Dossier sélectionné :", 
            list(st.session_state.profiles.keys()), 
            index=list(st.session_state.profiles.keys()).index(st.session_state.current_profile) if st.session_state.current_profile else 0
        )
    else:
        st.info("Crée un dossier ci-dessus pour enregistrer tes données.")
        
    st.divider()
    
    # BOUTON D'URGENCE INTERACTIF
    st.markdown("<div class='panic-btn'>", unsafe_allow_html=True)
    if st.button("🆘 J'AI ENVIE DE LUI ÉCRIRE", use_container_width=True):
        st.session_state.panic_mode = not st.session_state.panic_mode
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("<p style='text-align:center; font-size:0.85rem;'>Clique ici si ton cœur s'emballe et que tu es sur le point de craquer.</p>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 💌 La Lettre du Dimanche")
    st.markdown("<p style='font-size:0.9rem;'>Un mail de recul psychologique et de soutien émotionnel envoyé chaque dimanche soir par <b>Camil</b>.</p>", unsafe_allow_html=True)
    email_input = st.text_input("Rejoins notre communauté anonyme", placeholder="ton.adresse@email.com")
    if st.button("S'inscrire", use_container_width=True):
        if "@" in email_input:
            st.success("Inscription enregistrée. À dimanche prochain.")
        else:
            st.error("Format d'adresse invalide.")

# --- BARRE DE COMPTE (HAUT DROITE, COMME SUR INSTAGRAM) ---
col_espace, col_compte = st.columns([7, 1])
with col_compte:
    if st.session_state.logged_in_user:
        initiale = st.session_state.logged_in_user["prenom"][0].upper()
        with st.popover(f"👤 {initiale}", use_container_width=True):
            st.markdown(f"**{st.session_state.logged_in_user['prenom']} {st.session_state.logged_in_user['nom']}**")
            st.caption(st.session_state.logged_in_user["email"])
            if st.button("Se déconnecter", use_container_width=True, key="btn_logout"):
                st.session_state.logged_in_user = None
                st.rerun()
    else:
        with st.popover("👤 Compte", use_container_width=True):
            mode = st.radio("", ["Se connecter", "Créer un compte"], horizontal=True, key="auth_mode_radio", label_visibility="collapsed")

            if mode == "Se connecter":
                login_email = st.text_input("Adresse e-mail", key="login_email")
                login_pwd = st.text_input("Mot de passe", type="password", key="login_pwd")
                if st.button("Se connecter", use_container_width=True, key="btn_login"):
                    utilisateur = verify_login(login_email, login_pwd)
                    if utilisateur:
                        st.session_state.logged_in_user = utilisateur
                        st.rerun()
                    else:
                        st.error("E-mail ou mot de passe incorrect.")
            else:
                st.caption("Le numéro de téléphone est facultatif.")
                s_prenom = st.text_input("Prénom", key="s_prenom")
                s_nom = st.text_input("Nom", key="s_nom")
                s_email = st.text_input("Adresse e-mail", key="s_email")
                s_tel = st.text_input("Téléphone (facultatif)", key="s_tel")
                s_pwd = st.text_input("Mot de passe", type="password", key="s_pwd")
                if st.button("Créer mon compte", use_container_width=True, key="btn_signup"):
                    if not (s_prenom and s_nom and s_email and s_pwd):
                        st.error("Merci de remplir les champs obligatoires (prénom, nom, e-mail, mot de passe).")
                    elif not EMAIL_REGEX.match(s_email):
                        st.error("Adresse e-mail invalide.")
                    elif len(s_pwd) < 6:
                        st.error("Le mot de passe doit contenir au moins 6 caractères.")
                    else:
                        cree = create_user(s_email, s_pwd, s_prenom, s_nom, s_tel)
                        if cree:
                            st.session_state.logged_in_user = {"email": s_email.lower().strip(), "prenom": s_prenom.strip(), "nom": s_nom.strip()}
                            st.rerun()
                        else:
                            st.error("Un compte existe déjà avec cet e-mail.")

# --- BANNIÈRE PRINCIPALE ---
st.markdown("""
    <div class='hero-banner'>
        <h1>🌙 RE-CONNECT</h1>
        <p>L'alliance unique de la modélisation mathématique et de la psychologie humaine pour t'accompagner pas à pas dans ta reconstruction.</p>
    </div>
    """, unsafe_allow_html=True)

# --- CONFIGURATION DU MODE PANIQUE ---
if st.session_state.panic_mode:
    st.markdown("""
    <div class='custom-card' style='border: 2px solid #E56B6F; background-color: #FFF5F5;'>
        <h3 style='color: #E56B6F !important; margin-top:0;'>🛑 RESPIRATION DE CRISE. POSE CE TÉLÉPHONE.</h3>
        <p>Ton rythme cardiaque est élevé, l'anxiété s'est emparée de ton système nerveux. C'est ce qu'on appelle une <b>tempête affective</b>.</p>
        <p>Le message que tu veux envoyer ne va pas résoudre ton problème. Il va simplement t'apporter un soulagement temporaire de 5 minutes, suivi de plusieurs jours de regrets et d'attente douloureuse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        **🧘 Exercice de Cohérence Cardiaque (5 secondes) :**
        1. Respire par le nez en gonflant le ventre pendant 5 secondes.
        2. Bloque ton souffle pendant 2 secondes.
        3. Expire lentement par la bouche pendant 5 secondes.
        *Répète cette boucle 3 fois avant de prendre la moindre décision.*
        """)
    with col_p2:
        st.markdown("""
        **⚠️ Vérité mathématique :**
        * En envoyant ce message maintenant, tu diminues tes chances de retour de **15%**.
        * Tu montres à ton ex que tu es toujours disponible à sa guise, annulant l'effet du manque.
        * S'il/elle répond de manière glaciale ou ne répond pas, ta douleur sera démultipliée par 10 ce soir.
        """)
        
    if st.button("C'est bon, j'ai respiré, la vague est passée. Je tiens bon.", use_container_width=True):
        st.session_state.panic_mode = False
        st.rerun()
    st.divider()

# --- STRUCTURE DES ONGLETS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌙 L'Algorithme (Calcul)", 
    "🧩 Test d'Attachement XXL", 
    "📅 Le Tracker 30 Jours", 
    "🧭 L'Encyclopédie des Cas",
    "💬 Le Dictionnaire SMS",
    "🌟 La Communauté",
    "💞 Matchmaking"
])

# ==========================================
# ONGLET 1 : L'ALGORITHME DE CALCUL
# ==========================================
with tab1:
    st.markdown("""
    <div class='custom-card'>
        <h4>📊 Analyse Prédictive de ta Situation</h4>
        <p>Renseigne les paramètres de votre ancienne relation pour générer ta courbe d'évolution émotionnelle.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.profiles:
        st.info("👈 Pour commencer à calculer tes chances, crée d'abord un dossier dans le menu latéral à gauche.")
    else:
        if st.session_state.attachment_style is None:
            st.warning("🧩 **Astuce :** Prends 2 minutes pour faire le **Test d'Attachement** (onglet suivant). Ton profil s'intégrera directement au calcul pour affiner les prédictions !")
        
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            st.markdown("##### 👩‍❤️‍👨 Paramètres Relationnels")
            t_R_months = st.slider("Durée globale de la relation (mois)", 1, 120, 18)
            F = 1 if st.radio("S'agissait-il de votre premier amour ?", ("Oui", "Non"), index=1) == "Oui" else 0
            amour_fin = st.slider("Intensité résiduelle estimée (1-10)", 1, 10, 7)
            etude_vous = st.selectbox("Ton univers professionnel/études", ["Sciences & Tech", "Arts & Lettres", "Commerce & Management", "Santé & Social", "Artisanat & Métiers", "Autre"])
            etude_ex = st.selectbox("L'univers de ton ex", ["Sciences & Tech", "Arts & Lettres", "Commerce & Management", "Santé & Social", "Artisanat & Métiers", "Autre"])

        with c_col2:
            st.markdown("##### 💔 Le Déclencheur de Rupture")
            raison = st.selectbox("Raison principale de la séparation", ["Perte de sentiments", "Étouffement (Besoin d'espace)", "Distance géographique", "Toxicité / Conflits"])
            recurrence = st.radio("Fréquence des ruptures", ("Première rupture", "Cycles On/Off répétés"))
            t_actuel = st.number_input("Nombre de jours de silence radio effectifs", min_value=0, max_value=365, value=14)

        with c_col3:
            st.markdown("##### 🌐 L'Environnement Externe")
            entourage = st.select_slider("Influence de son entourage", options=["Hostile", "Neutre", "Bienveillant"], value="Neutre")
            autre_personne = st.radio("Est-il/elle en contact avec une tierce personne ?", ("Non", "Je suspecte quelqu'un", "Oui (Relation pansement de transition)"))

        st.divider()

        # --- MOTEUR DE CALCUL MATHÉMATIQUE ---
        t_R = t_R_months / 12.0
        base_proba = 72.0 

        # Ajustement des variables
        if raison == "Perte de sentiments": base_proba -= 15; jour_pic = 60 
        elif raison == "Étouffement (Besoin d'espace)": base_proba += 8; jour_pic = 40 
        elif raison == "Distance géographique": base_proba -= 8; jour_pic = 30
        elif raison == "Toxicité / Conflits": base_proba -= 20; jour_pic = 25 

        if recurrence == "Cycles On/Off répétés": base_proba -= 12 
        if entourage == "Bienveillant": base_proba += 8
        elif entourage == "Hostile": base_proba -= 15
        if autre_personne == "Oui (Relation pansement de transition)": base_proba -= 18
        elif autre_personne == "Non": base_proba += 5
        if F == 1: base_proba += 8
        base_proba += (amour_fin - 5) * 2 
        if etude_vous == etude_ex: base_proba += 4
        
        # Prise en compte du style d'attachement calculé dans le Tab 2
        if st.session_state.attachment_style == "Anxieux": base_proba -= 6 
        elif st.session_state.attachment_style == "Évitant": base_proba -= 3
        elif st.session_state.attachment_style == "Désorganisé": base_proba -= 8
        elif st.session_state.attachment_style == "Sécure": base_proba += 12

        # Courbe de modélisation
        t_jours = np.linspace(0, 120, 200)
        courbe_proba = base_proba * (t_jours / jour_pic) * np.exp(1 - (t_jours / jour_pic))
        courbe_proba[t_jours <= 7] = courbe_proba[t_jours <= 7] * 0.25 
        courbe_proba = np.clip(courbe_proba, 0, 98.0) 
        proba_actuelle = np.interp(t_actuel, t_jours, courbe_proba)

        if st.session_state.logged_in_user:
            update_user_resultats(st.session_state.logged_in_user["email"], score=float(proba_actuelle))

        # Affichage du score
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #8E7C93 0%, #B56576 100%); padding: 35px; border-radius: 20px; text-align: center; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(181, 101, 118, 0.15);'>
            <h2 style='color: white !important; margin:0; font-size: 1.5rem;'>Probabilité Théorique de Re-Connexion Actuelle</h2>
            <h1 style='color: white !important; font-size: 3.8rem; margin: 10px 0;'>{proba_actuelle:.1f}%</h1>
            <p style='color: #FDFBF7 !important; margin:0; font-size:1.1rem;'>Calcul basé sur l'évolution émotionnelle à {t_actuel} jours.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Téléchargement Story
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            image_bytes = generate_share_image(proba_actuelle, st.session_state.current_profile)
            st.download_button(
                label="📸 Obtenir ma fiche personnalisée (Story Instagram / TikTok)",
                data=image_bytes,
                file_name=f"re_connect_score_{st.session_state.current_profile}.png",
                mime="image/png",
                use_container_width=True
            )

        # Graphique
        st.markdown("##### 📈 Courbe Dynamique d'Acceptation de l'Ex")
        fig, ax = plt.subplots(figsize=(10, 3.8))
        ax.plot(t_jours, courbe_proba, color='#B56576', linewidth=3.5, label="Niveau d'ouverture émotionnelle de ton ex")
        ax.axvline(x=t_actuel, color='#8E7C93', linestyle='--', linewidth=2, label=f'Aujourd\'hui (Jour {t_actuel})')
        ax.fill_between(t_jours, courbe_proba, alpha=0.1, color='#B56576')
        ax.set_facecolor('#FAF6F0')
        fig.patch.set_facecolor('#FAF6F0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#8E7C93')
        ax.spines['bottom'].set_color('#8E7C93')
        ax.set_xlabel("Jours de silence respectés", color='#4E3D53', fontweight='bold', fontsize=10)
        ax.set_ylabel("Probabilité de réceptivité (%)", color='#4E3D53', fontweight='bold', fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_xlim(0, 120)
        ax.legend(frameon=False, labelcolor='#4E3D53')
        ax.grid(True, linestyle=':', alpha=0.4)
        st.pyplot(fig)

        # Conseils personnalisés intégrés
        st.markdown("#### 💡 Ta Feuille de Route Personnalisée")
        conseils = get_conseils_personnalises(raison, st.session_state.attachment_style, entourage, autre_personne)
        for c in conseils:
            st.markdown(f"<div class='conseil-card'>{c}</div>", unsafe_allow_html=True)

# ==========================================
# ONGLET 2 : LE QUIZ D'ATTACHEMENT XXL
# ==========================================
with tab2:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>TEST PSYCHOLOGIQUE</span>
        <h3>🧩 Découvre ton profil d'attachement amoureux</h3>
        <p>Notre style d'attachement dicte notre façon de réagir face à la séparation et au manque. Réponds honnêtement à ces questions conçues par Camil pour débloquer ton analyse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("attachment_form"):
        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53;'>1. Quand ton/ta partenaire met du temps à répondre à tes messages :</p>", unsafe_allow_html=True)
        q1 = st.radio("", [
            "Je commence à m'inquiéter, je vérifie s'il/elle est actif(ve) en ligne et je renvoie parfois un message.",
            "Je m'en fiche un peu, j'apprécie d'avoir du temps pour moi.",
            "Je me sens contrarié(e) et je me promets d'ignorer sa prochaine réponse pour me venger.",
            "Je passe à autre chose, je sais qu'il/elle répondra quand il/elle aura le temps."
        ], key="q1")
        
        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53; margin-top:20px;'>2. L'idée d'être célibataire ou d'être abandonné(e) :</p>", unsafe_allow_html=True)
        q2 = st.radio("", [
            "C'est une angoisse sourde qui m'accompagne souvent en arrière-plan.",
            "Ça ne m'effraie pas, je me sens très bien seul(e).",
            "Je veux être en couple, mais dès que les choses deviennent sérieuses, j'ai envie de fuir.",
            "C'est inconfortable mais je sais que je m'en sortirais très bien."
        ], key="q2")
        
        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53; margin-top:20px;'>3. Lors d'une dispute animée avec ton ex :</p>", unsafe_allow_html=True)
        q3 = st.radio("", [
            "Je voulais tout régler immédiatement, je ne supportais pas de m'endormir fâché(e).",
            "J'avais besoin de m'isoler, de fuir la pièce ou d'éteindre mon téléphone.",
            "Je passais des pleurs aux cris, sans trop savoir comment exprimer ma détresse.",
            "Je demandais une pause pour me calmer, puis j'exposais mon point de vue posément."
        ], key="q3")

        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53; margin-top:20px;'>4. Comment perçois-tu l'intimité émotionnelle profonde ?</p>", unsafe_allow_html=True)
        q4 = st.radio("", [
            "J'en ai énormément besoin, mais j'ai peur que l'autre ne m'aime pas autant que je l'aime.",
            "Je me sens vite étouffé(e) quand on me demande de trop m'ouvrir.",
            "Je la désire profondément mais j'ai peur d'être blessé(e) si je baisse ma garde.",
            "C'est naturel, je me confie facilement et j'aime écouter l'autre."
        ], key="q4")

        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53; margin-top:20px;'>5. Quand ton ex te faisait une critique :</p>", unsafe_allow_html=True)
        q5 = st.radio("", [
            "Je la prenais comme une remise en cause totale de son amour pour moi.",
            "Je me fermais totalement ou je tournais la critique en dérision pour me protéger.",
            "Je devenais agressif(ve) puis je culpabilisais immédiatement après.",
            "J'écoutais, j'essayais de comprendre son point de vue et d'en discuter rationnellement."
        ], key="q5")

        st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#4E3D53; margin-top:20px;'>6. Ton comportement général dans l'intimité :</p>", unsafe_allow_html=True)
        q6 = st.radio("", [
            "J'ai besoin d'être rassuré(e) constamment sur l'amour de mon partenaire.",
            "Je préfère garder mon indépendance financière et mes secrets pour moi.",
            "Je pousse l'autre à bout pour tester ses limites, puis je regrette.",
            "Je fais confiance facilement tant qu'on ne me donne pas de raison de douter."
        ], key="q6")

        st.write("")
        submit_quiz = st.form_submit_button("🧪 Analyser mon style d'attachement")

    if submit_quiz:
        answers = [q1, q2, q3, q4, q5, q6]
        
        # Attribution des profils
        anxieux_score = sum(1 for a in answers if "inquiéter" in a or "angoisse sourde" in a or "régler immédiatement" in a or "énormément besoin" in a or "remise en cause" in a or "rassuré(e)" in a)
        evitant_score = sum(1 for a in answers if "m'en fiche" in a or "très bien seul(e)" in a or "m'isoler" in a or "vite étouffé(e)" in a or "me fermais" in a or "indépendance" in a)
        disorg_score = sum(1 for a in answers if "venger" in a or "envie de fuir" in a or "pleurs aux cris" in a or "peur d'être blessé(e)" in a or "agressif(ve)" in a or "tester ses limites" in a)
        secure_score = sum(1 for a in answers if "autre chose" in a or "m'en sortirais" in a or "demandais une pause" in a or "naturel" in a or "j'écoutais" in a or "confiance" in a)
        
        max_score = max(anxieux_score, evitant_score, disorg_score, secure_score)
        
        if max_score == anxieux_score:
            style = "Anxieux"
            description = "Tu as une peur intense de l'abandon. Face à la rupture, ton système d'attachement est hyper-activé. Tu as constamment envie d'agir, d'appeler ou de réclamer des explications. **La clé pour toi : apprendre à tolérer l'incertitude sans forcer les réponses.**"
        elif max_score == evitant_score:
            style = "Évitant"
            description = "Tu as tendance à minimiser ton attachement émotionnel. Tu fuis le conflit et l'intimité lorsqu'ils deviennent trop intenses. La rupture peut te donner l'impression de 'ne rien ressentir' au début, avant que le manque ne te frappe bien plus tard. **La clé : t'autoriser à ressentir la tristesse sans la masquer.**"
        elif max_score == disorg_score:
            style = "Désorganisé"
            description = "Tu es pris(e) dans un conflit interne : tu désires l'intimité mais tu as une peur panique d'être blessé(e). Tu peux passer de phases d'amour fou à des phases de rejet total. **La clé : amener de la stabilité émotionnelle par des exercices de méditation et de rationalisation.**"
        else:
            style = "Sécure"
            description = "Tu disposes de bases saines pour communiquer et accepter la réalité. Tu souffres de la rupture, mais tu as conscience de ta propre valeur indépendamment de ton ex. **La clé : utiliser ce calme intérieur pour te reconstruire de façon mature.**"
            
        st.session_state.attachment_style = style

        if st.session_state.logged_in_user:
            update_user_resultats(st.session_state.logged_in_user["email"], attachment_style=style)
        
        st.markdown(f"""
        <div style='background-color: #F4EBE8; border-left: 6px solid #B56576; padding: 25px; border-radius: 12px; margin-top:20px;'>
            <h4 style='color: #B56576 !important; margin:0 0 10px 0;'>🏆 Profil Révélé : {style}</h4>
            <p style='font-size: 1.1rem; line-height: 1.6;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Génial !** Ton profil a été mis en mémoire. Les prédictions et conseils de l'onglet **L'Algorithme** s'y sont automatiquement adaptés.")

# ==========================================
# ONGLET 3 : LE TRACKER DE SILENCE RADIO
# ==========================================
with tab3:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>DISCIPLINE & POUVOIR VOODOO</span>
        <h3>📅 Ton journal intime de 30 jours de Silence</h3>
        <p>Le Silence Radio n'est pas un jeu psychologique, c'est une détox hormonale (dopamine/ocytocine). Chaque jour validé te réapprend à vivre pour toi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.progress(min(st.session_state.tracker_days / 30.0, 1.0))
        st.markdown(f"### Jour {st.session_state.tracker_days} sur 30 validé(s)")
        
        aujourd_hui = datetime.date.today()
        
        if st.session_state.last_checkin == aujourd_hui:
            st.success("✨ Félicitations ! Ta journée est validée. Tu as fait preuve d'une force incroyable aujourd'hui.")
        else:
            if st.button("💪 J'AI TENU BON AUJOURD'HUI (0 contact)", use_container_width=True):
                st.session_state.tracker_days += 1
                st.session_state.last_checkin = aujourd_hui
                st.rerun()
                
        if st.button("⚠️ J'ai envoyé un message (Réinitialiser le compteur)", type="secondary", use_container_width=True):
            st.session_state.tracker_days = 0
            st.session_state.last_checkin = None
            st.rerun()
            
    with col_t2:
        st.markdown("##### 🏆 Les Niveaux du Silence")
        if st.session_state.tracker_days < 7:
            st.warning("🌱 **Niveau 1 : Le Sevrage** (Jours 1 à 7)\nLe cerveau réclame sa dose. C'est la phase la plus dure physiquement. Tiens bon.")
        elif st.session_state.tracker_days < 15:
            st.info("🌿 **Niveau 2 : Le Calme Plat** (Jours 8 à 15)\nLa colère de ton ex s'estompe. La nostalgie commence doucement à s'installer chez lui/elle.")
        elif st.session_state.tracker_days < 25:
            st.success("🌳 **Niveau 3 : La Reprise de Pouvoir** (Jours 16 à 25)\nTu penses moins à lui/elle. Ton magnétisme personnel remonte en flèche.")
        else:
            st.success("👑 **Niveau 4 : L'Indépendance** (Jours 26 à 30)\nTu es maître de ton destin. Si tu le recontactes, ce sera par choix logique, pas par manque.")

# ==========================================
# ONGLET 4 : L'ENCYCLOPÉDIE DE TOUS LES CAS (CONSEILS AUGMENTÉS)
# ==========================================
with tab4:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>GUIDE DE SURVIE COMPLET</span>
        <h3>🧭 La Boussole de Reconstruction</h3>
        <p>Sélectionne la situation spécifique qui te tourmente actuellement pour obtenir un plan d'action immédiat et précis rédigé par Camil.</p>
    </div>
    """, unsafe_allow_html=True)

    cas = st.selectbox("Choisis la situation qui correspond à ta rupture :", [
        "Mon ex a quelqu'un d'autre (Relation pansement)",
        "Nous travaillons ou étudions au même endroit",
        "Nous avons des enfants ou un bail immobilier en commun",
        "Mon ex fait du ghosting absolu (Zéro réponse)",
        "Mon ex m'envoie des messages 'miettes' (breadcrumbs) sans proposer de se voir",
        "La rupture s'est faite sur une trahison ou une infidélité",
        "Nous nous sommes quittés en bons termes mais l'attraction s'est éteinte"
    ])

    st.divider()

    if cas == "Mon ex a quelqu'un d'autre (Relation pansement)":
        st.markdown("""
        <div class='conseil-card'>
            <h5>🎯 Pourquoi cela se produit et comment réagir ?</h5>
            <p><b>Le mécanisme psychologique :</b> Ton ex souffre du vide laissé par la rupture mais est incapable de l'affronter de face. Il/elle utilise une tierce personne comme 'anesthésiant émotionnel'. Ces relations manquent de fondation solide et sont basées sur la fuite.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Ne montre aucune jalousie :</b> Si tu t'énerves ou poses des questions, tu valides son choix en passant pour quelqu'un d'aigri.</li>
                <li><b>Applique le Silence Radio le plus strict :</b> Ton ex va comparer la nouveauté superficielle de cette nouvelle relation avec l'histoire profonde qu'il/elle avait avec toi.</li>
                <li><b>Sois intouchable :</b> Si on te pose des questions, réponds simplement : <i>'Je lui souhaite d'être heureux/se.'</i> Le mystère que tu dégages le/la rendra fou/folle de curiosité.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif cas == "Nous travaillons ou étudions au même endroit":
        st.markdown("""
        <div class='conseil-card'>
            <h5>💼 Gérer le quotidien forcé</h5>
            <p><b>Le défi :</b> Le silence radio complet est impossible car la proximité physique est imposée par l'emploi du temps ou le travail.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Le Silence Radio 'Professionnel' :</b> Coupe tout contact personnel. Ne parle de rien d'autre que du travail ou des études.</li>
                <li><b>Zéro émotion visible :</b> Sois aimable, poli(e), mais d'un calme olympien. Pas de froideur excessive (qui montrerait que tu es affecté(e)) et pas de familiarité.</li>
                <li><b>Sois rayonnant(e) socialement :</b> Rigole avec tes collègues/amis de promo. Laisse ton ex constater de loin que ta joie de vivre ne dépend pas de sa présence.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif cas == "Nous avons des enfants ou un bail immobilier en commun":
        st.markdown("""
        <div class='conseil-card'>
            <h5>🏡 Séparations logistiques complexes</h5>
            <p><b>La stratégie :</b> Séparer l'émotionnel du logistique de manière hermétique.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Le protocole de la 'Boîte Postale' :</b> Tes seuls messages doivent être factuels, clairs et sans sous-entendu. Utilise des e-mails plutôt que des SMS instantanés pour les sujets administratifs pour mettre de la distance.</li>
                <li><b>N'utilise pas les enfants ou le bail pour créer du contact :</b> C'est un piège inconscient très fréquent. Si tu n'as rien de logistique à dire, garde le silence.</li>
                <li><b>Fais-toi aider par des tiers :</b> Si la communication est trop complexe, passe par un avocat, un médiateur ou un ami commun pour gérer les détails matériels sans interagir directement.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif cas == "Mon ex fait du ghosting absolu (Zéro réponse)":
        st.markdown("""
        <div class='conseil-card'>
            <h5>👻 Faire face au mur du silence</h5>
            <p><b>Le décryptage :</b> Le ghosting montre une incapacité criante à gérer le conflit ou la culpabilité de la part de ton ex. Ce n'est pas un reflet de ta valeur, mais de ses limites psychologiques.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Arrête d'écrire immédiatement :</b> Chaque relance de ta part creuse le fossé et valide sa décision d'ignorer tes messages.</li>
                <li><b>Efface les conversations de ton écran :</b> Ne passe pas tes soirées à relire les anciens messages en espérant y trouver une clé.</li>
                <li><b>Applique la règle de l'indifférence :</b> Le ghosteur réagit souvent lorsque le fantôme qu'il a créé disparaît pour de bon. S'il revient un jour, ne réponds pas immédiatement.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif cas == "Mon ex m'envoie des messages 'miettes' (breadcrumbs) sans proposer de se voir":
        st.markdown("""
        <div class='conseil-card'>
            <h5>🍞 Le piège de la validation facile</h5>
            <p><b>La vérité :</b> Ton ex t'envoie des messages flous ('Ça va ?', un même drôle, 'J'ai pensé à toi en écoutant cette chanson') simplement pour vérifier que tu es toujours disponible pour flatter son ego à moindres frais.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Mets un terme au ping-pong virtuel :</b> Ne réponds pas aux messages insignifiants de manière développée.</li>
                <li><b>Utilise la fermeture polie :</b> Réponds avec politesse mais mets fin à l'échange rapidement (Ex : <i>'Sympa ! J'espère que tout va bien de ton côté. Je dois y aller, passe une bonne journée.'</i>).</li>
                <li><b>S'il/elle insiste sans proposer de rendez-vous :</b> Arrête de répondre. Ton temps a de la valeur, tu n'es pas une distraction du dimanche soir.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif cas == "La rupture s'est faite sur une trahison ou une infidélité":
        st.markdown("""
        <div class='conseil-card'>
            <h5>💔 Reconstruire l'estime de soi après le choc</h5>
            <p><b>L'état d'esprit :</b> La trahison brise l'estime personnelle. Ta priorité absolue n'est pas de récupérer l'autre, mais de te soigner et de reprendre ton pouvoir.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Coupe radicalement les ponts :</b> Tu as besoin d'espace pour évacuer la colère saine. Ne cherche pas d'explications sans fin : le geste parle de lui-même.</li>
                <li><b>Re-centre toi sur ton intégrité :</b> Pratique des activités valorisantes pour reprendre confiance en tes capacités et ton charme.</li>
                <li><b>Ne pardonne pas trop vite par peur du vide :</b> Si ton ex tente de revenir, impose des conditions de changement extrêmement strictes et mesurables dans le temps.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class='conseil-card'>
            <h5>🥀 Quand l'étincelle s'est éteinte doucement</h5>
            <p><b>Le diagnostic :</b> Pas de disputes, pas de drames, juste la routine qui a tué l'attraction mutuelle. La nostalgie mettra plus de temps à s'installer mais sera plus profonde.</p>
            <p><b>Le protocole d'action :</b>
            <ol>
                <li><b>Ne sois pas l'ami(e) de consolation :</b> Refuse catégoriquement de devenir la transition amicale. C'est tout ou rien.</li>
                <li><b>Crée de la nouveauté visible :</b> Change de style, de coiffure, lance-toi dans des projets ambitieux. Ton ex doit voir une nouvelle version de toi qu'il/elle ne connaît pas encore.</li>
                <li><b>Laisse le temps faire son œuvre :</b> Ce type de rupture nécessite souvent 45 à 60 jours pour que le vide affectif pèse réellement sur ton ex.</li>
            </ol>
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# ONGLET 5 : LE DICTIONNAIRE SMS (SCRIPTS PRÊTS À L'EMPLOI)
# ==========================================
with tab5:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>SCRIPTS DE COMMUNICATION</span>
        <h3>💬 Que lui écrire si la communication reprend ?</h3>
        <p>Garde le contrôle de tes mots. Voici des modèles de messages validés scientifiquement pour ne jamais passer pour quelqu'un d'acquis.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📱 Cas 1 : Ton ex t'écrit un simple 'Tu fais quoi ?' un vendredi soir tard")
    st.info("""
    *   **Pourquoi il/elle fait ça :** Nostalgie passagère, alcool ou solitude de fin de semaine.
    *   **Ce qu'il faut faire :** Ne réponds surtout pas le soir même. Attends le lendemain matin vers 11h.
    *   **Le message idéal :** *"Hey ! J'étais de sortie hier soir donc je n'ai pas vu ton message. Tout va bien de mon côté, et toi ?"*
    *   **L'effet :** Tu montres que tu as une vie sociale active et indépendante.
    """)

    st.markdown("##### 📱 Cas 2 : Ton ex te propose un rendez-vous amical ('Prendre un café en amis')")
    st.info("""
    *   **Pourquoi il/elle fait ça :** Il/elle veut tester ta réceptivité sans s'engager, ou atténuer sa propre culpabilité de t'avoir quitté(e).
    *   **Ce qu'il faut faire :** Refuser poliment la friendzone tout en restant ouvert(e) à une vraie rencontre.
    *   **Le message idéal :** *"C'est sympa de proposer ! Mais pour être honnête, je n'ai pas trop envie d'une relation amicale amicale pour le moment. Par contre, si tu as envie qu'on se voie pour passer un bon moment et discuter de nous, on peut se caler ça la semaine prochaine."*
    *   **L'effet :** Tu affirmes tes intentions avec maturité et courage. Tu refuses ses miettes.
    """)

    st.markdown("##### 📱 Cas 3 : C'est l'anniversaire de ton ex pendant ton Silence Radio")
    st.info("""
    *   **La règle d'or :** Si tu es en plein Silence Radio de moins de 21 jours, **tu ne lui souhaites pas**.
    *   **Pourquoi :** Tout le monde va lui souhaiter. Ton absence de message sera le plus grand événement de sa journée de anniversaire.
    *   **Si tu décides de lui écrire malgré tout (plus de 21 jours de silence) :** Reste extrêmement sobre.
    *   **Le message idéal :** *"Bon anniversaire ! J'espère que tu passes une super journée."* (Pas de cœur, pas de questions ouvertes).
    """)

# ==========================================
# ONGLET 6 : LE MUR SOCIAL / COMMUNAUTÉ
# ==========================================
with tab6:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>ESPACE BIENVEILLANCE</span>
        <h3>🌟 Partage ton chemin avec d'autres</h3>
        <p>Parce que la solitude est le pire ennemi de la reconstruction. Dépose tes doutes ou lis les histoires inspirantes de la communauté.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("new_temoignage_form"):
        nom = st.text_input("Ton prénom ou pseudo d'anonymat", placeholder="Ex: Lucas_75")
        texte = st.text_area("Raconte ton histoire, tes doutes ou ta victoire...", placeholder="Hier soir, j'ai failli craquer mais j'ai ouvert le tracker...")
        submit = st.form_submit_button("📢 Partager mon message")
        if submit and texte:
            st.session_state.temoignages.insert(0, {"nom": nom if nom else "Anonyme", "texte": texte, "date": "À l'instant"})
            st.success("Ton témoignage a bien été publié sur le mur d'entraide !")
            st.rerun()
    
    st.divider()
    for t in st.session_state.temoignages:
        st.markdown(f"""
        <div style='background-color: white; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 4px solid #8E7C93; box-shadow: 0 4px 12px rgba(0,0,0,0.02);'>
            <span style='font-weight: 700; color: #4E3D53;'>{t['nom']}</span> - <span style='font-size:0.85rem; color:#8E7C93;'>{t['date']}</span>
            <p style='margin-top: 10px; font-style: italic; color: #5A5A5A;'>« {t['texte']} »</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# ONGLET 7 : MATCHMAKING
# ==========================================
with tab7:
    st.markdown("""
    <div class='custom-card'>
        <span class='badge-tip'>NOUVELLE RENCONTRE</span>
        <h3>💞 Rencontre des profils qui te ressemblent</h3>
        <p>Une fois ton score de probabilité calculé et ton Test d'Attachement réalisé, crée un compte gratuit pour être mis(e) en relation avec d'autres membres vivant une situation similaire à la tienne.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in_user:
        st.info("👤 Crée un compte gratuit (bouton en haut à droite) pour débloquer le matchmaking. Il te faut juste un e-mail et un mot de passe — le téléphone est facultatif.")
    elif not st.session_state.attachment_style:
        st.warning("🧩 Fais d'abord le **Test d'Attachement** dans l'onglet dédié pour être matché(e).")
    else:
        mon_score = get_my_score(st.session_state.logged_in_user["email"])
        matchs = get_matchs(st.session_state.logged_in_user["email"], st.session_state.attachment_style, mon_score or 0)

        if not matchs:
            st.info("Aucun autre membre pour le moment. Reviens un peu plus tard, la communauté grandit chaque jour !")
        else:
            st.markdown(f"##### {len(matchs)} profil(s) proche(s) du tien")
            cols = st.columns(3)
            for i, m in enumerate(matchs):
                with cols[i % 3]:
                    score_txt = f"{m['score']:.0f}%" if m['score'] is not None else "—"
                    st.markdown(f"""
                    <div class='custom-card' style='text-align:center;'>
                        <div style='width:60px; height:60px; border-radius:50%; background:linear-gradient(135deg, #8E7C93 0%, #B56576 100%); margin:0 auto 10px auto; display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:1.4rem;'>{m['prenom'][0].upper()}</div>
                        <b>{m['prenom']}</b><br>
                        <span style='font-size:0.85rem; color:#8E7C93;'>Style : {m['style'] or '—'}</span><br>
                        <span style='font-size:0.85rem; color:#8E7C93;'>Score : {score_txt}</span>
                    </div>
                    """, unsafe_allow_html=True)

# --- PIED DE PAGE ---
st.divider()
st.caption("<p style='text-align:center; color:#8E7C93; font-size:0.9rem;'>Re-Connect par Camil (@maths_demo). Tous droits réservés 2026. Code conçu avec amour et rigueur mathématique.</p>", unsafe_allow_html=True)
