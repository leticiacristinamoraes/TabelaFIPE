#TabelaFIPE-Teste1/pages/Manager.py
#dentro da aba de "Preços Cadastrados"

tab1, tab2 = st.tabs(["Preços Coletados", "Média de Preços"])

with tab1:
    st.header("Preços Coletados")
    marca = st.text_input("Marca do veículo")
    modelo = st.text_input("Modelo do veículo")

    if st.button("Consultar Preços"):
        if marca and modelo:
            precos = register_repo.get_prices_by_model(marca, modelo)
            if precos:
                for preco in precos:
                    st.write(f" R$ {preco['price']} - {preco['date']}")
            else:
                st.warning("Nenhum preço encontrado.")

with tab2:
    st.header("Média de Preços")
    marca = st.text_input("Marca do veículo (Média)")
    modelo = st.text_input("Modelo do veículo (Média)")

    if st.button("Consultar Média"):
        media = avg_price_repo.get_avg_price_by_model(marca, modelo)
        if media:
            st.success(f" Média de Preço: **R$ {media}**")
        else:
            st.warning("Nenhuma média disponível.")
