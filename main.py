# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:40:52 2023

@author: RANDOM CENTAURUS
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 00:29:31 2022

@author: yanri
"""

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
    
    st.title('A general inspection and opportunistic replacement policy for one-component systems of variable quality')

    menu = ["Application", "Information", "Website"]
    
    choice = st.sidebar.selectbox("Select here", menu)
    
    if choice == menu[0]:
        
        st.header(menu[0])

        st.subheader("Insert the parameter values below:")
        
        beta = st.number_input('Parâmetro de forma (beta)', value=2.0, step=0.1, format='%.1f')
        eta = st.number_input('Parâmetro de escala (eta)', value=100.0, step=10.0, format='%.1f')
        Cp = st.number_input('Custo da manutenção preventiva (Cp)', value=100.0, step=10.0, format='%.1f')
        Cf = st.number_input('Custo da manutenção corretiva:', min_value=0.01, step=0.01)
        Tp = st.number_input('Tempo de inatividade para manutenção preventiva:', min_value=0.01, step=0.01)
        Tf = st.number_input('Tempo de inatividade resultante de falha:', min_value=0.01, step=0.01)
        DT_max = st.number_input('Downtime máximo aceito:', min_value=0.01, step=0.01)
        st.subheader("Click on botton below to run this application:")
        
        botao = st.button("Get cost-rate")

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
            
            st.write(otm()[0])
            st.write(otm()[1])
            st.write(otm()[2])


    if choice == menu[1]:
        
        st.header(menu[1])
        
        st.write('''This is the information section regarding the prototype created by members of the RANDOM
research group, which aims to assist in the application of a general inspection and opportunitistic replacement policy
for one-component systems of variable quality presented by Cavalcante et al. (2021). Here we bring the
policy summary and the notation of the parameters that are requested at application.

The maintenance policy on this prototype is a hybrid of periodic inspection and
opportunistic replacement. From new, the system is inspected every {} time units until K{} or a defect is found at 
inspection or a failure occurs, whichever occurs soonest. Inspections are
perfect in that the true state of the system is revealed at inspection. 
Further if the system survives beyond age K{}, then inspection ceases, 
and the system is replaced on failure or at age T or at
the first opportunity that arises after age S (S < T), whichever
occurs soonest. Replacements are instantaneous.

The innovation of this model is the consideration of the age
threshold for opportunistic replacement S, whereby replacement is
carried out at opportunities that arise during the wear-out phase
[K{}, T]. In this way, the policy takes greater care in the initial
life of an equipment and then in mid-life utilises opportunities for
more cost-effective replacement. We call this policy 1 and study
this in detail in the paper.

The decision criterion used in this modeling is the cost rate returned by dividing the
expected cost and expected length of a renewal cycle, containing the
following decision variables: K, which represents the number of total inspections that must be
performed in the component's life cycle; S, which represents bottom of the window of
opportunities, allowing the system to be replaced through opportunistic maintenance; 
T, which represents the age for preventive replacement; and {}, which represents the inspection interval.

This prototype has restrictions regarding the solution search space. If it is in the user's 
interest to use a wider range of solution combinations or if there is
any question about the study and/or this prototype can be directed to any of the following e-mail 
addresses. 

c.a.v.cavalcante@random.org.br

a.r.alberti@random.org.br

a.j.s.rodrigues@random.org.br

y.r.melo@random.org.br
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
