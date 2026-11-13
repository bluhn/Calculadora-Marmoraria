import streamlit as st

st.set_page_config(page_title="Calculadora Marmoraria", page_icon="🪨")

PERDA_PADRAO = 5  # % de perda/quebra de material

TIPOS = {
    "Pedra reta (+30%)": ("Pedra reta", 30),
    "Bancada (+70%)": ("Bancada", 70),
}


def calcular_peca(
    comprimento_m,
    largura_m,
    preco_m2,
    acrescimo_percentual,
    perda_percentual=PERDA_PADRAO,
):
  area = comprimento_m * largura_m
  area_com_perda = area * (1 + perda_percentual / 100)
  custo_pedra = area_com_perda * preco_m2
  acrescimo = custo_pedra * acrescimo_percentual / 100
  total = custo_pedra + acrescimo
  return area, area_com_perda, custo_pedra, acrescimo, total


def formatar_dinheiro(valor):
  texto = f"{valor:,.2f}"
  texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
  return f"R$ {texto}"


def main():
  st.title("🪨 Calculadora - Marmoraria")

  # Guarda as peças adicionadas na memória da tela
  if "pecas" not in st.session_state:
    st.session_state.pecas = []

  st.subheader(f"Adicionar Peça {len(st.session_state.pecas) + 1}")

  opcao_escolhida = st.radio(
      "Tipo da peça:", list(TIPOS.keys()), horizontal=True
  )
  nome_tipo, percentual = TIPOS[opcao_escolhida]

  col1, col2 = st.columns(2)
  with col1:
    comprimento = st.number_input(
        "Comprimento (metros)", min_value=0.0, step=0.10, format="%.2f"
    )
  with col2:
    largura = st.number_input(
        "Largura (metros)", min_value=0.0, step=0.10, format="%.2f"
    )

  preco = st.number_input(
      "Valor do m² da pedra (R$)", min_value=0.0, step=10.0, format="%.2f"
  )

  if st.button("➕ Adicionar Peça ao Orçamento", type="primary"):
    if comprimento > 0 and largura > 0 and preco > 0:
      area, area_perda, custo, acrescimo, total = calcular_peca(
          comprimento, largura, preco, percentual
      )
      st.session_state.pecas.append({
          "tipo": nome_tipo,
          "percentual": percentual,
          "area": area,
          "area_perda": area_perda,
          "custo": custo,
          "acrescimo": acrescimo,
          "total": total,
      })
      st.rerun()
    else:
      st.warning(
          "Por favor, preencha comprimento, largura e valor com números maiores"
          " que zero."
      )

  # Mostra o resumo se já houver peças adicionadas
  if st.session_state.pecas:
    st.divider()
    st.subheader("📋 Resumo do Serviço")

    subtotal_geral = 0
    acrescimo_geral = 0

    for i, item in enumerate(st.session_state.pecas, start=1):
      with st.expander(
          f"Peça {i} - {item['tipo']}: {formatar_dinheiro(item['total'])}",
          expanded=True,
      ):
        st.write(
            f"**Área:** {item['area']:.2f} m² *(com {PERDA_PADRAO}% de perda:"
            f" {item['area_perda']:.2f} m²)*"
        )
        st.write(f"**Custo da pedra:** {formatar_dinheiro(item['custo'])}")
        st.write(
            f"**Acréscimo ({item['percentual']}%):**"
            f" {formatar_dinheiro(item['acrescimo'])}"
        )

      subtotal_geral += item["custo"]
      acrescimo_geral += item["acrescimo"]

    total_servico = subtotal_geral + acrescimo_geral

    st.success(f"### TOTAL DO SERVIÇO: {formatar_dinheiro(total_servico)}")
    st.caption(
        f"Subtotal pedra: {formatar_dinheiro(subtotal_geral)} | Acréscimos:"
        f" {formatar_dinheiro(acrescimo_geral)}"
    )

    if st.button("🗑️ Limpar Tudo (Novo Orçamento)"):
      st.session_state.pecas = []
      st.rerun()


if __name__ == "__main__":
  main()
