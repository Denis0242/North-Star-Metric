import streamlit as st


def metric_card(label: str, value, is_percent: bool = False, is_currency: bool = False):
    if is_percent:
        formatted = f'{value:.2%}'
    elif is_currency:
        formatted = f'${value:,.2f}'
    else:
        formatted = f'{value:,.2f}'
    st.metric(label, formatted)


def decision_panel():
    st.subheader('Insight → Action → Recommendation → Decision')
    st.markdown('''
    **Insight:** Variant B leads conversion but must be checked against D30 retention.  
    **Action:** Continue deeper testing while monitoring retention impact.  
    **Recommendation:** Scale Variant B only if D30 retention does not decline further.  
    **Decision:** Continue experiment monitoring before full rollout.
    ''')
