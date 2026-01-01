import streamlit as st
from rag_core import answer

# Page configuration
st.set_page_config(
    page_title="TP RAG Multimodal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Title styling */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .title-text {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle-text {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Response container */
    .response-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Context cards */
    .context-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .context-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Modality badges */
    .badge-text {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .badge-image {
        background: #f093fb;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    /* Score badge */
    .score-badge {
        background: #4facfe;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input field */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🤖 RAG Multimodal</h1>
        <p class="subtitle-text">OpenAI + pgvector | Intelligence artificielle avancée</p>
    </div>
""", unsafe_allow_html=True)

# Search section
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown("### 🔍 Posez votre question")
    st.write("Interrogez le corpus indexé comprenant des textes et des images.")
    query = st.text_input("", placeholder="Entrez votre question ici...", label_visibility="collapsed")
    search_button = st.button("🚀 Rechercher & Répondre")
    st.markdown('</div>', unsafe_allow_html=True)

# Process query
if search_button and query:
    with st.spinner("🔄 Analyse en cours..."):
        try:
            resp, rows = answer(query, k=5)
            
            # Response section
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.markdown('<div class="response-container">', unsafe_allow_html=True)
                st.markdown("### 💡 Réponse")
                st.markdown(f"**{resp}**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Context section
                st.markdown("### 📚 Contexte récupéré (Top 5)")
                st.write("")
                
                for idx, (src, chunk, modality, score) in enumerate(rows, 1):
                    badge_class = "badge-image" if modality.lower() == "image" else "badge-text"
                    icon = "🖼️" if modality.lower() == "image" else "📄"
                    
                    with st.expander(f"**{icon} Résultat #{idx}** | {modality} | Score: {score:.3f}", expanded=(idx == 1)):
                        st.markdown(f"**Source:** `{src}`")
                        st.markdown("---")
                        st.write(chunk)
                        
                        # Progress bar for score visualization
                        st.progress(min(score, 1.0))
        
        except Exception as e:
            st.error(f"❌ Une erreur s'est produite: {str(e)}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📊 Modèle:** OpenAI GPT")
with col2:
    st.markdown("**🗄️ Base de données:** pgvector")
with col3:
    st.markdown("**🎯 Mode:** Multimodal")