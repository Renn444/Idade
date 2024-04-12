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

    st.title('Política Manutenção por Idade')

    menu = ["Aplicação", "Informação", "Website"]
    choice = st.sidebar.selectbox("Selecione aqui", menu)
    
    if choice == menu[0]:
        st.header(menu[0])
        st.subheader("Insira os valores dos parâmetros abaixo:")

        beta = st.number_input('Parâmetro de forma (beta)', value=2.0, step=0.1, format='%.1f')
        eta = st.number_input('Parâmetro de escala (eta)', value=100.0, step=10.0, format='%.1f')
        Cp = st.number_input('Custo da manutenção preventiva (Cp)', value=100.0, step=10.0, format='%.1f')
        Cf = st.number_input('Custo da manutenção corretiva:', min_value=0.01, step=0.01)
        Tp = st.number_input('Tempo de inatividade para manutenção preventiva:')
        Tf = st.number_input('Tempo de inatividade resultante de falha:')
        DT_max = st.number_input('Downtime máximo aceito:')
        st.subheader("Clique no botão abaixo para rodar esse aplicativo:")
        
        botao = st.button("Obtenha os valores")
        if botao:
            def otm():
                               def f_W(x):
                    f = (beta/eta)*((x/eta)**(beta-1))*np.exp(-(x/eta)**beta)
                    return f
                
                def R_W(x):
                    R = np.exp(-(x/eta)**beta)  
                    return R

                def F_aW(x):
                    return 1-R_W(x)

                #Custo esperado de um ciclo de renovação

                def EC(T):
                    return Cp*R_W(T) + Cf*F_aW(T)

                def aa(x):
                    return (f_W(x)*(x+Tf))

                def EL(T):
                    fst = (T+Tp)*R_W(T)
                    sec = quad(aa,0,T)[0]
                    return fst+sec

                def ED(T):
                    return Tp*R_W(T) + Tf*F_aW(T)
                
                def RC(T):
                    return EC(T)/EL(T)
                
                def RD(T):
                    return ED(T)/EL(T)
                
                def restricao(T):
                    return DT_max - RD(T)
                
                T0 = [0.1]  # Palpite inicial
                cons = [{'type': 'ineq', 'fun': restricao}]  # Restrições
                
                otimo = minimize(RC, T0, method='SLSQP', constraints=cons)
                T_otimo = otimo.x[0]
                taxa_custo = otimo.fun
                integral, _ = quad(lambda x: x * f_W(x), 0, T_otimo)
                MTBOF = (integral + T_otimo * R_W(T_otimo)) / F_aW(T_otimo)
            
                return T_otimo, otimo.fun, MTBOF

            tempo_otimo, taxa_custo, mtbof = otm()
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
