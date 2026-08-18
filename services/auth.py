import hashlib
import os

import streamlit as st

# Credentials are no longer stored as plaintext. Environment variables can override
# the demo defaults for deployment. The default values preserve the finalized demo login.
LOGIN_EMAIL = os.getenv("CUSTOMERIQ_ADMIN_EMAIL", "admin123@gmail.com")
LOGIN_PASSWORD_HASH = os.getenv(
    "CUSTOMERIQ_ADMIN_PASSWORD_HASH",
    "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
)


def _password_matches(password: str) -> bool:
    candidate = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return candidate == LOGIN_PASSWORD_HASH


def _login_styles():
    st.markdown(
        """
        <style>
        .login-page {
            min-height: 78vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
        }
        .login-card {
            width: min(430px, 100%);
            background: #FFFFFF;
            border: 1px solid #DDE3EA;
            border-radius: 16px;
            padding: 34px 36px 30px;
            box-shadow: 0 8px 28px rgba(15, 23, 42, .07);
        }
        .login-brand {
            text-align: center;
            color: #172033;
            font-size: 1.65rem;
            font-weight: 800;
            margin-bottom: 5px;
        }
        .login-tagline {
            text-align: center;
            color: #64748B;
            font-size: .9rem;
            margin-bottom: 26px;
        }
        .login-welcome {
            text-align: center;
            color: #172033;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .login-footer {
            text-align: center;
            color: #94A3B8;
            font-size: .76rem;
            margin-top: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def require_login():
    if st.session_state.get("authenticated", False):
        return True

    _login_styles()
    left, center, right = st.columns([1.05, 1.5, 1.05])
    with center:
        st.markdown(
            '<div style="text-align:center; padding-top:7vh;">'
            '<div class="login-brand">Customer Segmentation</div>'
            '<div class="login-tagline">AI-Powered Customer Intelligence</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False, border=True):
            st.markdown('<div class="login-welcome">Welcome Back</div>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if email.strip().lower() == LOGIN_EMAIL.lower() and _password_matches(password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please check your credentials.")

        st.markdown('<div class="login-footer">Secure access to customer intelligence and segmentation.</div>', unsafe_allow_html=True)

    return False
