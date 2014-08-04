#Entenda as Métricas

###LOC - Lines Of Code

Nos diz o tamanho, em linhas de código, do software. É a medida mais comum utilizada para medir o tamanho de um software. São contadas apenas as linhas que são executadas, comentários e linhas em branco não entram na contagem.

* Medida correspondente à parte **Lines of code** no *dashboard* do Sonar.

###AMLOC - Average Method LOC

É a média de linhas de código por método, uma métrica derivada da anterior. Essa medida verifica se o código é bem dividido entre os métodos. Quanto maior o tamanho do método, mais coisa ele faz, o que significa que será mais difícil de ler e entender.

<p><center><table>
    <tbody>
        <tr>
            <td width="70"><b>Bom:</b></td>
            <td width="200">Até 10 linhas/método</td>
        </tr>
        <tr>
            <td width="70"><b>Regular:</b></td>
            <td width="200">De 11 à 13 linhas/método</td>
        </tr>
        <tr>
            <td width="70"><b>Ruim:</b></td>
            <td width="200">Mais de 13 linhas/método</td>
        </tr>
    </tbody>
</table></center></p>

* Medida correspondente à parte **Lines of code** no *dashboard* do Sonar.

###PODC - Percentage Of Duplicated Code

Mede a quantidade de código duplicado no projeto. Um código que possui muitas duplicações pode consumir mais tempo de leitura e entendimento, já que é mais código a ser lido, porém, sem necessidade.

* Medida correspondente à parte **Duplications** no *dashboard* do Sonar.

###ACCM - Average Cyclomatic Complexity per Method

Mede a complexidade do software. É a quantidade média de caminhos que podem ser percorridos na execução do código (if, else, for, while, etc). Não tem uma tabela de valores sugeridos, mas quanto menos melhor, pois o método terá menos informações para entender.

* Medida correspondente à parte **Complexity** no *dashboard* do Sonar.

###AWP - Accordance With PEP8

Avalia o padrão do código de acordo com a PEP8 (*Style Guide For Python Code*). Um código padronizado torna a manutenção muito mais simples, facilitando a leitura e compreensão do código.

* Medida correspondente à parte **Issues** no *dashboard* do Sonar.

###TC - Test Coverage

Define a cobertura de ódigo oferecida pela suíte de teste do projeto. Quanto maior for a cobertura, menor é a chance de uma alteração causar algum tipo de efeito colateral no código.

* Medida correspondente à parte **Unit Tests Coverage** no *dashboard* do Sonar.

###DOCL - Density of Commented Lines

Mede a quantidade de linhas comentadas. A quantidade de linhas comentadas pode auxiliar no entendimento do código, mas isso depende da qualidade do comentário, já que, muitas vezes, um comentário muito grande pode ser desnecessário.

* Medida correspondente à parte **Comments** no *dashboard* do Sonar.