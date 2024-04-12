import math
import numpy as np
import pandas as pd
from scipy.integrate import quad, dblquad
from scipy.optimize import minimize
import streamlit as st
import sys
from streamlit import cli as stcli
from PIL import Image

# Funções e definições anteriores

def main():
    col1, col2, col3 = st.columns(3)
    foto = Image.open('foto.png')
    col2.image(foto, use_column_width=True)

    st.title('Otimização de Manutenção')
    
    # Entrada de parâmetros pelo usuário
    beta = st.number_input('Parâmetro de forma (beta)', value=2.0, step=0.1, format='%.1f')
    eta = st.number_input('Parâmetro de escala (eta)', value=100.0, step=10.0, format='%.1f')
    Cv = st.number_input('Custo da manutenção preventiva (Cv)', value=2.0, step=0.1, format='%.1f')
    Cf = st.number_input('Custo da manutenção corretiva (Cf)', value=15.0, step=1.0, format='%.1f')
    Tp = st.number_input('Tempo de inatividade para manutenção preventiva:', value=0.0, step=0.1, format='%.1f')
    Tf = st.number_input('Tempo de inatividade resultante de falha:', value=0.0, step=0.1, format='%.1f')
    DT_max = st.number_input('Downtime máximo aceitável:', value=0.0, step=0.1, format='%.1f')
    
def otm():
    def f_W(x):
        f = (beta / eta) * ((x / eta)**(beta - 1)) * np.exp(-(x / eta)**beta)
        return f

    def R_W(x):
        R = np.exp(-(x / eta)**beta)
        return R

    def F_aW(x):
        return 1 - R_W(x)

    # Custo esperado de um ciclo de renovação
    def EC(T):
        return Cv * R_W(T) + Cf * F_aW(T)

    def aa(x):
        return (f_W(x) * (x + Tf))

    def EL(T):
        fst = (T + Tp) * R_W(T)
        sec = quad(aa, 0, T)[0]
        return fst + sec

    def ED(T):
        return Tp * R_W(T) + Tf * F_aW(T)

    def RC(T):
        return EC(T) / EL(T)

    def RD(T):
        return ED(T) / EL(T)

    def restricao(T):
        return DT_max - RD(T)
    
    T0 = [0.1]  # Palpite inicial
    cons = [{'type': 'ineq', 'fun': restricao}]  # Restrições
    
    otimo = minimize(RC, T0, method='SLSQP', constraints=cons)
    T_otimo = otimo.x[0]
    taxa_custo = otimo.fun
    integral, _ = quad(lambda x: x * f_W(x), 0, T_otimo)
    MTBOF = (integral + T_otimo * R_W(T_otimo)) / F_aW(T_otimo)
    
    return T_otimo, taxa_custo, MTBOF
    
    if st.button('Calcular ótimos'):
    tempo_otimo, taxa_custo, mtbof = otm(beta, eta, Cv, Cf, Tp, Tf, DT_max)
    st.write('O tempo ótimo é:', tempo_otimo)
    st.write('A taxa de custo é:', taxa_custo)
    st.write('O MTBOF é:', mtbof)


    if choice == menu[1]:
        st.header(menu[1])
        st.write('''Fazer o texto para colocar aqui''')

    if choice == menu[2]:
        st.header(menu[2])
        st.write('''The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 
        in order to bring together different researchers who work in the following areas: risk, maintenance and 
        operation modelling. Learn more about it through our website.''')
        st.markdown('[Click here to be redirected to our website](http://random.org.br/en/)', False)

if __name__ == "__main__":
    main()
