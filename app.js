async function buscarReceita() {
    const query = document.getElementById('query').value;
    const url = `http://127.0.0.1:8000/receitas/${query}`;
    const resultadoDiv = document.getElementById('resultado');
    const loadingDiv = document.getElementById('loading');

    // Exibir o efeito de carregamento e esconder o resultado enquanto carrega
    loadingDiv.style.display = 'flex';
    resultadoDiv.style.display = 'none';

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Erro ao buscar receita");
        }

        const data = await response.json();

        // Verifica se os dados 'ingredientes' e 'instrucoes' existem no retorno
        if (data.ingredientes && data.instrucoes) {
            resultadoDiv.innerHTML = `
          <h2>Ingredientes:</h2>
          <p>${data.ingredientes.replace(/\n/g, "<br>")}</p>
          <h2>Instruções:</h2>
          <p>${data.instrucoes.replace(/\n/g, "<br>")}</p>
        `;
        } else {
            // Caso as chaves não existam no retorno
            resultadoDiv.innerHTML = "<p>Erro: Receita mal formatada ou incompleta.</p>";
        }

        // Exibir o resultado e esconder o carregamento
        resultadoDiv.style.display = 'block';
        loadingDiv.style.display = 'none';

    } catch (error) {
        // Mostrar mensagem de erro caso ocorra algum problema na requisição
        resultadoDiv.innerHTML = `<p>Erro: ${error.message}</p>`;
        resultadoDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
    }
}