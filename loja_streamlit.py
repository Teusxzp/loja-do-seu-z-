import streamlit as st

# ============================================
# DICIONÁRIO DA LOJA (preço e estoque de cada produto)
# ============================================
# Usamos "session_state" pra guardar o estoque de forma que ele
# não reinicie sempre que a página atualizar (o Streamlit recarrega
# o script inteiro a cada interação do usuário, então sem isso o
# estoque voltaria ao valor original a cada clique).
if "mercado" not in st.session_state:
    st.session_state.mercado = {
        "arroz": {"preco": 15.70, "estoque": 72},
        "feijao": {"preco": 8.99, "estoque": 38},
        "farinha": {"preco": 4.25, "estoque": 17},
    }

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []  # lista que vai guardar cada item comprado

if "total_da_compra" not in st.session_state:
    st.session_state.total_da_compra = 0

mercado = st.session_state.mercado

# ============================================
# TÍTULO E CATÁLOGO
# ============================================
st.title("Catálogo 🛒")

for produto, dados in mercado.items():
    st.write(f"**{produto}** - R$ {dados['preco']:.2f} - Estoque: {dados['estoque']}")

st.divider()

# ============================================
# FORMULÁRIO DE COMPRA
# ============================================
st.subheader("Fazer um pedido")

escolha = st.selectbox("Qual produto você deseja?", list(mercado.keys()))
quantidade = st.number_input("Quantas unidades?", min_value=1, step=1)

if st.button("Adicionar ao carrinho"):
    if quantidade <= mercado[escolha]["estoque"]:
        valor_item = quantidade * mercado[escolha]["preco"]
        mercado[escolha]["estoque"] -= quantidade
        st.session_state.total_da_compra += valor_item
        st.session_state.carrinho.append(
            f"{escolha} x{quantidade} = R$ {valor_item:.2f}"
        )
        st.success(f"Adicionado: {escolha} x{quantidade} = R$ {valor_item:.2f}")
    else:
        st.error("Estoque insuficiente!")

# ============================================
# CARRINHO E TOTAL
# ============================================
st.divider()
st.subheader("Carrinho")

if st.session_state.carrinho:
    for item in st.session_state.carrinho:
        st.write(item)
else:
    st.write("Nenhum item adicionado ainda.")

st.subheader(f"Total da compra: R$ {st.session_state.total_da_compra:.2f}")

if st.button("Finalizar e limpar carrinho"):
    st.session_state.carrinho = []
    st.session_state.total_da_compra = 0
    st.rerun()
