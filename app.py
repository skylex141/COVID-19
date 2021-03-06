import streamlit as st
from models.seir_bayes import (
    run_SEIR_BAYES_model, 
    make_lognormal_params_95_ci,
    seir_bayes_plot, 
    seir_bayes_interactive_plot,
)
import matplotlib.pyplot as plt



def _run_SEIR_BAYES_model(N, E0, I0, R0,
                          R0__params: 'repr. rate mean and std',
                          gamma_inv_params: 'removal rate mean and std',
                          alpha_inv_params: 'incubation rate mean and std',
                          t_max, runs, interactive=True, 
                          scale='log', show_uncertainty=True):
    S, E, I, R, t_space = run_SEIR_BAYES_model(
                                        N, E0, I0, R0, 
                                        R0__params,
                                        gamma_inv_params,
                                        alpha_inv_params,
                                        t_max, runs)
    
    if interactive: 
        return seir_bayes_interactive_plot(N, E0, I0, R0, 
                                           t_max, runs, S, E, I, R, t_space,
                                           scale=scale, show_uncertainty=show_uncertainty)

    return seir_bayes_plot(N, E0, I0, R0, 
                           R0__params,
                           gamma_inv_params,
                           alpha_inv_params,
                           t_max, runs, S, E, I, R, t_space)


if __name__ == '__main__':
    st.markdown(
        """
        # COVID-19
        O objetivo deste projeto é iniciar uma força tarefa conjunta da comunidade científica e tecnológica a fim de criar modelos de previsão de infectados (e talvez outras métricas) pelo COVID-19, focando no Brasil. O projeto é público e pode ser usado por todos.
        
        Acesse [este link](https://github.com/3778/COVID-19) para mais informações.

        ## Previsão de infectados
        **Obs.**: Os resultados apresentados são *preliminares* e estão em fase de validação.
        """)

    st.sidebar.title("Parâmetros da simulação")
    st.sidebar.markdown("Para simular outros cenários, altere um parâmetro e tecle **Enter**. O novo resultado será calculado e apresentado automaticamente.")

    N = st.sidebar.number_input('População total (N)',
                                min_value=0, max_value=1_000_000_000,
                                value=13_000_000)

    E0 = st.sidebar.number_input('Indivíduos expostos inicialmente (E(0))',
                                 min_value=0, max_value=1_000_000_000,
                                 value=50)

    I0 = st.sidebar.number_input('Indivíduos infecciosos inicialmente (I(0))',
                                 min_value=0, max_value=1_000_000_000,
                                 value=152)

    R0 = st.sidebar.number_input('Indivíduos removidos com imunidade inicialmente (R(0))',
                                 min_value=0, max_value=1_000_000_000,
                                 value=1)

    R0__inf = st.sidebar.number_input('Limite inferior do Número básico de reprodução médio (R0)',
                                      min_value=0.01, max_value=10.0, step = 0.01,
                                      value=1.96)

    R0__sup = st.sidebar.number_input('Limite superior do Número básico de reprodução médio (R0)',
                                      min_value=R0__inf, max_value=10.0, step = 0.01,
                                      value=2.55)

    gamma_inf = st.sidebar.number_input('Limite inferior do período infeccioso médio em dias (1/γ)',
                                        min_value=1.0, max_value=60.0, step = 0.01,
                                        value=10.0)

    gamma_sup = st.sidebar.number_input('Limite superior do período infeccioso médio em dias (1/γ)',
                                        min_value=gamma_inf, max_value=60.0, step = 0.01,
                                        value=16.0)

    alpha_inf = st.sidebar.number_input('Limite inferior do tempo de incubação médio em dias (1/α)',
                                         min_value=0.1, max_value=60.0, step = 0.01,
                                         value=4.1)

    alpha_sup = st.sidebar.number_input('Limite superior do tempo de incubação médio em dias (1/α)',
                                         min_value=alpha_inf, max_value=60.0, step = 0.01,
                                         value=7.0)

    t_max = st.sidebar.number_input('Período de simulação em dias (t_max)',
                                    min_value=1, max_value=12*30, step = 1,
                                    value=6*30)

    runs = st.sidebar.number_input('Qtde. de iterações da simulação (runs)',
                                    min_value=1, max_value=10_000, step = 1,
                                    value=1_000)

    st.sidebar.text(""); st.sidebar.text("")  # Spacing
    st.markdown(
        """
        ### Modelo SEIR-Bayes
        O gráfico abaixo mostra o resultado da simulação da evolução de pacientes infectados para os parâmetros escolhidos no menu da barra à esquerda. Mais informações sobre este modelo [aqui](https://github.com/3778/COVID-19#seir-bayes).
        
        ### Limites inferiores e superiores dos parâmetros
        Ao lado, você pode configurar os limites superior e inferiores dos parâmetros período infeccioso, tempo de incubação e Número básico de reprodução. Estes limites definem um intervalo de confiança de 95% de uma distribuição log-normal para cada parâmetro.\n\n\n
        """)

    S0 = N - (E0 + I0 + R0)
    R0__params = make_lognormal_params_95_ci(R0__inf, R0__sup)
    gamma_inv_params = make_lognormal_params_95_ci(gamma_inf, gamma_sup)
    alpha_inv_params = make_lognormal_params_95_ci(alpha_inf, alpha_sup)

    scale = st.selectbox('Escala do eixo Y', ['log', 'linear'])
    show_uncertainty = st.checkbox("Mostrar intervalo de confiança", value=True)
    chart = _run_SEIR_BAYES_model(N, E0, I0, R0,
                          R0__params,
                          gamma_inv_params,
                          alpha_inv_params,
                          t_max, runs, 
                          interactive=True, 
                          scale=scale, 
                          show_uncertainty=show_uncertainty)

    st.write(chart)
    st.button('Rodar novamente')
