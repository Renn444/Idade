# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import quad
from PIL import Image
from scipy.optimize import minimize


def main():
    #criando 3 colunas
    col1, col2, col3 = st.columns(3)
    foto = Image.open('foto.png')
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    
    st.title('Política de Manutenção por Idade')

    menu = ["Aplicação", "Informação", "Website"]
    
    choice = st.sidebar.selectbox("Select here", menu)
    
    if choice == menu[0]:
        
        st.header(menu[0])

        st.subheader("Insira os valores dos parâmetros abaixo:")
        
        beta = st.number_input('Parâmetro de forma (beta)', value=2.0, step=0.1, format='%.1f')
        eta = st.number_input('Parâmetro de escala (eta)', value=100.0, step=10.0, format='%.1f')
        Cp = st.number_input('Custo da manutenção preventiva (Cp)', value=100.0, step=10.0, format='%.1f')
        Cf = st.number_input('Custo da manutenção corretiva:', min_value=0.01, step=0.01)
        Tp = st.number_input('Tempo de inatividade para manutenção preventiva:', min_value=0.01, step=0.01)
        Tf = st.number_input('Tempo de inatividade resultante de falha:', min_value=0.01, step=0.01)
        DT_max = st.number_input('Downtime máximo aceito:', min_value=0.01, step=0.01)
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
                
                #PALPITE INICIAL
                T0=[0.1]
                
                #RESTRIÇÕES
                cons = [{'type':'ineq','fun':restricao}]
                
                otimo = minimize(RC,T0,method='SLSQP',constraints=cons)
                
                T_otimo = otimo.x[0]
                taxa_custo = otimo.fun[0]
                downtime = RD(otimo.x[0])
                

                
                return T_otimo, taxa_custo, downtime
            
            st.write('O tempo ótimo é:', otm()[0])
            st.write('A taxa de custo é:', otm()[1])
            st.write('O downtime é:', otm()[2])


    if choice == menu[1]:
        
        st.header(menu[1])
        
        st.write('''Fazer o texto para colocar aqui
''' .format(chr(948), chr(948), chr(948), chr(948), chr(948)))
        
        
    if choice == menu[2]:
        
        st.header(menu[2])
        
        st.write('''The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 
                 in order to bring together different researchers who work in the following areas: risk, maintenance a
                 nd operation modelling. Learn more about it through our website.''')
        st.markdown('[Click here to be redirected to our website](http://random.org.br/en/)',False)
        
if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
