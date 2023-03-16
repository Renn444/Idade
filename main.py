# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 00:29:31 2022

@author: yanri
"""

import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import dblquad
from scipy.integrate import quad
from scipy.integrate import tplquad
from PIL import Image

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
        
        b1=st.number_input("Insert the weibull shape parameter for weak subpopulation - {}1" .format(chr(946)), min_value = 1.0, max_value = 6.0, value = 2.5) #forma fraca
        a1=st.number_input("Insert the characteristic life parameter for weak subpopulation - {}1" .format(chr(945)), min_value = 0.0, value = 0.8) #escala fraca
        b2=st.number_input("Insert the weibull shape parameter for strong subpopulation - {}2" .format(chr(946)), min_value = 1.0, max_value = 6.0, value = 5.0) #forma forte
        a2=st.number_input("Insert the characteristic life parameter for strong subpopulation - {}2" .format(chr(945)), min_value = 0.0, value = 3.6) #escala forte
        p=st.number_input("Insert the mixing parameter - q", min_value = 0.0, max_value = 1.0, value = 0.1) #parâmetro de mistura
        u=st.number_input("Insert the rate of arrival of opportunities parameter - {}" .format(chr(956)), min_value = 0.0, max_value = 5.0, value = 2.0) #taxa de chegada de oportunidades
        l=st.number_input("Insert the reciprocal of the mean of the delay time distribution parameter - {}" .format(chr(955)), min_value = 0.1, value = 1.0) #inverso da média da distribuição do delay time
        ci=st.number_input("Insert the cost of inspection parameter - Ci", min_value = 0.0, value = 0.03) #custo de inspeção
        co=st.number_input("Insert the cost of opportunistic replacement parameter - Co", min_value = 0.0, value = 0.5) #custo da preventiva na oportunidade
        cf=st.number_input("Insert the cost of corrective replacement parameter - Cf", min_value = 0.0, value = 5.0) #custo de falha
        cr=st.number_input("Insert the cost of preventive replacement parameter - Cp", min_value = 0.0, value = 1.0) #custo da preventiva
        
        st.subheader("Insert the decision variable values below:")
        
        delta=st.number_input("Insert the inspection interval - {}" .format(chr(948)), min_value = 0., max_value = 2., step = 0.01)
        S=st.number_input("Insert the initial threshold of opportunities variable - S", min_value = 0., max_value = 10., step = 0.01) #Limite inferior da janela de oportunidades
        T=st.number_input("Insert the age for preventive replacement - T", min_value = 0., max_value = 10., step = 0.01) #Limite inferior da janela de oportunidades
        k=int(st.number_input("Insert the total number of inspection variable - K", min_value = 0, max_value = 10, step = 1)) #Número total de visitas
        
        st.subheader("Click on botton below to run this application:")
        
        botao = st.button("Get cost-rate")

        if botao:
        
            def otm():

                def f01(x):#weibull densidade (componente fraco)
                    return (b1/a1)*((x/a1)**(b1-1))*np.exp(-(x/a1)**b1)
                def f02(x):#weibull densidade (componente forte)
                    return (b2/a2)*((x/a2)**(b2-1))*np.exp(-(x/a2)**b2)
                def fx(x):
                    return p*f01(x)+(1-p)*f02(x)
                def fh(h):#exponencial densidade
                    return l*np.exp(-l*h)
                def Fh(h):#exponencial acumulada
                    return 1-np.exp(-l*h)
                
                #Funções utilizadas no cálculo do Custo Esperado
                def f1(x):
                    return ((1-Fh(i*delta-x))*fx(x))
                def f2(x):
                    return ((Fh(i*delta-x)*fx(x)))
                def f3(x):
                    return ((Fh(S-x))*fx(x))
                def f4(h,x):
                    return (np.exp(-u*(x+h-S))*fh(h)*fx(x))
                def f5(h,x):
                    return ((1-np.exp(-u*(x+h-S)))*fh(h)*fx(x))
                def f6(x):
                    return ((1-np.exp(-u*(T-S)))*(1-Fh(T-x))*fx(x))
                def f7(x):
                    return ((1-Fh(T-x))*fx(x))
                
                #Funções utilizadas no cálculo do Tamanho Esperado
                def f8(h,x):
                    return ((x+h)*fh(h)*fx(x))
                def f9(h,x):
                    return ((x+h)*np.exp(-u*(x+h-S))*fh(h)*fx(x))
                def f10(z,h,x):
                    return ((z+S)*u*np.exp(-u*z)*fh(h)*fx(x))
                def f11(z,x):
                    return ((1-Fh(T-x))*(z+S)*u*np.exp(-u*z)*fx(x))
                def f12(z,x):
                    return ((1-Fh(T-x))*(z+S)*u*np.exp(-u*z)*fx(x))
                def f13(z):
                    return ((z+S)*u*np.exp(-u*z))

                sc = sv = 0                

                ##CÁLCULO DO CUSTO ESPERADO DO CICLO

                #PARTE 1 - EC
                #Custo quando um defeito é encontrado na iésima inspeção (multiplicado por sua respectiva probabilidade de ocorrência)
                for i in range (1, k+1):
                    r,_= quad(f1, (i-1)*delta, i*delta)
                    sc = sc + ((cr+i*ci)*r)
                
                #PARTE 2 - EC
                #Custo quando ocorre uma falha entre duas inspeções (multiplicado por sua respectiva probabilidade de ocorrência)
                for i in range (1, k+1):
                    r,_= quad(f2, (i-1)*delta, i*delta)
                    sc = sc + ((cf+(i-1)*ci)*r)
                
                #PARTE 3 - EC
                #Custo quando ocorre uma falha após todas as inspeções (multiplicado por sua respectiva probabilidade de ocorrência)
                r1,_= quad(f3, k*delta, S)
                r2,_= dblquad(f4, k*delta, S, lambda x: S-x, lambda x: T-x)
                r3,_= dblquad(f4, S, T, lambda x: 0, lambda x: T-x)
                sc = sc + ((cf+(k*ci))*(r1+r2+r3))
                
                #PARTE 4 - EC
                #Custo quando o componente é substituido na wear-out phase através de uma oportunidade (multiplicado por sua respectiva probabilidade de ocorrência)
                r1,_= dblquad(f5, k*delta, S, lambda x: S-x, lambda x: T-x)
                r2,_= quad(f6, k*delta, S)
                r3,_= dblquad(f5, S, T, lambda x: 0, lambda x: T-x)
                r4,_= quad(f6, S, T)
                r5,_= quad(fx, T, np.inf)
                sc = sc + ((co+(k*ci))*(r1+r2+r3+r4+((1-np.exp(-u*(T-S)))*r5)))
                
                #PARTE 5 - EC
                #Custo quando o componente é somente substituido de forma preventiva no final do ciclo (multiplicado por sua respectiva probabilidade de ocorrência)
                r1,_= quad(f7, k*delta, T)
                r2,_= quad(fx, T, np.inf)
                Pr=(np.exp(-u*(T-S))*(r1+r2))
                sc = sc + ((cr+(k*ci))*(np.exp(-u*(T-S))*(r1+r2)))
                
                ##CÁLCULO DO TAMANHO ESPERADO DO CICLO
                
                #PARTE 1 - EV
                for i in range(1, k+1):
                    v,_= quad(f1, (i-1)*delta, i*delta)
                    v1,_= dblquad(f8, (i-1)*delta, i*delta, lambda x: 0, lambda x: i*delta-x)
                    sv = sv + (i*delta*v) + v1
                
                #PARTE 2 - EV
                v,_= dblquad(f8, k*delta, S, lambda x: 0, lambda x: S-x)
                sv = sv + v
                
                #PARTE 3 - EV
                v,_= dblquad(f9, k*delta, S, lambda x: S-x, lambda x: T-x)
                sv = sv + v
                
                #PARTE 4 - EV
                v,_= dblquad(f9, S, T, lambda x: 0, lambda x: T-x)
                sv = sv + v
                
                #PARTE 5 - EV
                v,_= tplquad(f10, k*delta, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: x+h-S)
                sv = sv + v
                
                #PARTE 6 - EV
                v,_ = dblquad(f11, k*delta, S, lambda x: 0, lambda x: T-S)
                sv = sv + v
                
                #PARTE 7 - EV
                v,_= tplquad(f10, S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x+h-S)
                sv = sv + v
                
                #PARTE 8 - EV
                v,_= dblquad(f12, S, T, lambda x: 0, lambda x: T-S)
                sv = sv + v
                
                #PARTE 9 - EV
                v,_ = quad(f13, 0, T-S)
                v3,_ = quad(fx, T, np.inf)
                v2,_= quad(f7, k*delta, T)
                sv = sv + v3*v + T*Pr

                #Expected cost-rate
                c = sc/sv
                
                return c
            
            taxadecusto = otm()
            st.write("Cost-rate result: {:.3f}" .format(taxadecusto))

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
