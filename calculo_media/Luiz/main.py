st.title("Consulta de Preços FIPE")

marca = st.text_input("Marca do veículo")
modelo = st.text_input("Modelo do veículo")

if st.button("Consultar Preços"):
    if marca and modelo:
        precos = register_repo.get_prices_by_model(marca, modelo)
        media = avg_price_repo.get_avg_price_by_model(marca, modelo)

        if precos:
            st.subheader("Preços Coletados")
            for preco in precos:
                st.write(f" R$ {preco['price']} -  {preco['date']}")

            if media:
                st.success(f" Média de Preço: **R$ {media}**")
        else:
            st.warning("Nenhum preço encontrado para este modelo.")
    else:
        st.error("Por favor, preencha a marca e o modelo.")

#TabelaFIPE-Teste1/main.py
#tela principal para exibir preços e a média