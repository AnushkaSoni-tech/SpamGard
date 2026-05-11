import streamlit as st
import pandas as pd
from pydantic import ValidationError
from pipeline.wrapper import classify_message, classify_batch
from config import OUTDIR

st.set_page_config(page_title='Spam Detector', page_icon='📧', layout='wide')

st.markdown('''
<style>
.main {background:#f8fafc;}
.block-container {padding-top:2rem; max-width:1100px;}
h1,h2,h3 {color:#0f172a;}
p,label,span {color:#334155;}
textarea, .stTextArea textarea {border-radius:14px !important; border:1px solid #cbd5e1 !important;}
.stButton>button {
 background:#0f172a; color:white; border:none; border-radius:12px;
 height:3rem; width:100%; font-weight:700;
}
.stButton>button:hover {background:#1e293b; color:white;}
.metric-card {padding:18px; border-radius:16px; background:white; border:1px solid #e2e8f0;}
.badge-spam {background:#fee2e2; color:#b91c1c; padding:6px 12px; border-radius:999px; font-weight:700;}
.badge-safe {background:#dcfce7; color:#166534; padding:6px 12px; border-radius:999px; font-weight:700;}
.badge-uncertain {background:#fef3c7; color:#92400e; padding:6px 12px; border-radius:999px; font-weight:700;}
</style>
''', unsafe_allow_html=True)

st.markdown('# 📧 Spam Detector')
st.caption('Detect spam, phishing, fraud, and suspicious messages instantly using AI.')

# top tabs
single_tab, batch_tab = st.tabs(['Single Scan', 'Batch Upload'])

with single_tab:
    st.subheader('Scan a Message')
    user_input = st.text_area('Paste email or message', height=220, placeholder='Example: Congratulations! You won $5000. Click the link now...')

    if st.button('🔍 Scan Message'):
        if not user_input.strip():
            st.warning('Please enter a message.')
        else:
            with st.spinner('Analyzing...'):
                try:
                    result = classify_message(user_input)
                    st.markdown('---')
                    st.subheader('Result')

                    label = str(result.label).upper()
                    if 'SPAM' in label:
                        badge = "<span class='badge-spam'>SPAM</span>"
                    elif 'NOT' in label or 'SAFE' in label:
                        badge = "<span class='badge-safe'>SAFE</span>"
                    else:
                        badge = "<span class='badge-uncertain'>UNCERTAIN</span>"

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"<div class='metric-card'><h4>Classification</h4>{badge}</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<div class='metric-card'><h4>Risk Score</h4><h2>{result.risk_score}</h2></div>", unsafe_allow_html=True)

                    st.markdown('### Why it was flagged')
                    st.info(result.reasons)

                    st.markdown('### Red Flags')
                    st.warning(result.red_flags)

                    st.markdown('### Recommended Action')
                    st.success(result.suggested_action)

                    with st.expander('Raw JSON'):
                        st.json(result.model_dump())
                except ValidationError as e:
                    st.error(f'Validation failed: {e}')

with batch_tab:
    st.subheader('Batch CSV Analysis')
    st.caption('Upload a CSV file. First column should contain messages.')

    uploaded = st.file_uploader('Choose CSV file', type='csv')

    if uploaded:
        df = pd.read_csv(uploaded)
        df.to_csv(r"Data\test.csv", index=False)
        st.dataframe(df.head(10), use_container_width=True)

        if st.button('🚀 Run Batch Scan'):
            with st.spinner('Processing records...'):
                results_df = classify_batch(df.iloc[:,0].tolist())
                results_df.to_csv(f"{OUTDIR}\res.csv")
                st.success('Analysis complete.')
                st.dataframe(results_df, use_container_width=True)
                st.download_button('⬇ Download Results', data=results_df.to_csv(index=False).encode('utf-8'), file_name='spam_results.csv', mime='text/csv')
