/***********************************************************************
 *          ##################################################
 *                              DOCUMENTAÇÃO
 *          ##################################################
 *
 *  "dadosCompletos"    é o dicionário com os dados de todos os anos a
 *                          serem considerados
 *
 *  "dictAno"           é o dicionário com os dados de um único ano
 *
 *  "listaAnos"         é a lista com os anos considerados na análise
 *                          formato: [ano1, ano2, ano3, etc]
 *
 *  "offset"            é uma lista de dois valores com as coordenadas
 *                          x e y do offset a ser aplicado
 *                              offset = [x,y]
 **********************************************************************/

/***********************************************************************
 *          ##################################################
 *                      ÁREA DE DADOS E VARIÁVEIS
 *          ##################################################
 **********************************************************************/

window.GlobalAltura = 960
window.GlobalLargura = 1280
window.GlobalRaioMaximo = 16
window.GlobalTempoAnimacao = 5000 //em milisegundos
//window.GlobalCoord={2010:{"PT":{"numPartido":99,"x":-100,"y":-100},"PSDB":{"numPartido":99,"x":100,"y":-100},"PV":{"numPartido":99,"x":-100,"y":100},"PSOL":{"numPartido":99,"x":100,"y":100},},1990:{"PT":{"numPartido":99,"x":0,"y":0},"PSDB":{"numPartido":99,"x":0,"y":0},"PV":{"numPartido":99,"x":0,"y":0},"PSOL":{"numPartido":99,"x":0,"y":0},},2005:{"PT":{"numPartido":99,"x":100,"y":-100},"PSDB":{"numPartido":99,"x":-100,"y":100},"PV":{"numPartido":99,"x":100,"y":100},"PSOL":{"numPartido":99,"x":-100,"y":-100},},2000:{"PT":{"numPartido":99,"x":-100,"y":100},"PSDB":{"numPartido":99,"x":100,"y":100},"PV":{"numPartido":99,"x":-100,"y":-100},"PSOL":{"numPartido":99,"x":100,"y":-100},},1995:{"PT":{"numPartido":99,"x":100,"y":100},"PSDB":{"numPartido":99,"x":-100,"y":-100},"PV":{"numPartido":99,"x":100,"y":-100},"PSOL":{"numPartido":99,"x":-100,"y":100},}}
window.GlobalCoord={1990:{"PT":{"numPartido":99,"x":-4.10,"y":-0.69},"PSDB":{"numPartido":99,"x":8.83,"y":2.62},"PV":{"numPartido":99,"x":0.82,"y":-0.01},"PSOL":{"numPartido":99,"x":10.28,"y":-5.84},"PCdoB":{"numPartido":99,"x":-4.03,"y":0.02},"PP":{"numPartido":99,"x":-3.16,"y":0.35},"DEM":{"numPartido":99,"x":7.33,"y":2.80},"PMDB":{"numPartido":99,"x":-3.38,"y":0.45}},2010:{"PT":{"numPartido":99,"x":4.10,"y":-0.69},"PSDB":{"numPartido":99,"x":4.83,"y":-2.62},"PV":{"numPartido":99,"x":4.82,"y":3.01},"PSOL":{"numPartido":99,"x":-4.28,"y":-5.84},"PCdoB":{"numPartido":99,"x":-4.03,"y":5.02},"PP":{"numPartido":99,"x":-1.16,"y":-0.35},"DEM":{"numPartido":99,"x":0.33,"y":2.80},"PMDB":{"numPartido":99,"x":-3.38,"y":-0.45}},2000:{"PT":{"numPartido":99,"x":-2.10,"y":-1.69},"PSDB":{"numPartido":99,"x":3.83,"y":4.62},"PV":{"numPartido":99,"x":0,"y":0},"PSOL":{"numPartido":99,"x":-2.28,"y":10.84},"PCdoB":{"numPartido":99,"x":4.03,"y":0.02},"PP":{"numPartido":99,"x":3.16,"y":-0.35},"DEM":{"numPartido":99,"x":7.33,"y":-2.80},"PMDB":{"numPartido":99,"x":3.38,"y":-2.45}},1995:{"PT":{"numPartido":99,"x":-3.38,"y":-0.45},"PSDB":{"numPartido":99,"x":0.33,"y":2.80},"PV":{"numPartido":99,"x":-1.16,"y":-0.35},"PSOL":{"numPartido":99,"x":-4.03,"y":5.02},"PCdoB":{"numPartido":99,"x":-4.28,"y":-5.84},"PP":{"numPartido":99,"x":4.82,"y":3.01},"DEM":{"numPartido":99,"x":4.83,"y":-2.62},"PMDB":{"numPartido":99,"x":4.10,"y":-0.69}}}
//window.GlobalCoord = {1990:{"PT":{"numPartido":99,"x":-4.10,"y":-0.69}, "PSDB":{"numPartido":99,"x":8.83,"y":2.62}, "PV":{"numPartido":99,"x":0.82,"y":-0.01}, "PSOL":{"numPartido":99,"x":10.28,"y":-5.84}, "PCdoB":{"numPartido":99,"x":-4.03,"y":0.02}, "PP":{"numPartido":99,"x":-3.16,"y":0.35}, "PR":{"numPartido":99,"x":-2.59,"y":-0.16}, "DEM":{"numPartido":99,"x":7.33,"y":2.80}, "PMDB":{"numPartido":99,"x":-3.38,"y":0.45}, "PSC":{"numPartido":99,"x":-2.36,"y":0.63}, "PTB":{"numPartido":99,"x":-3.03,"y":-0.14}, "PDT":{"numPartido":99,"x":-1.95,"y":-0.42}, "PSB":{"numPartido":99,"x":-3.44,"y":-0.49}, "PPS":{"numPartido":99,"x":7.46,"y":1.60}, "PRB":{"numPartido":99,"x":-3.22,"y":-0.20}}, 2000:{"PT":{"numPartido":99,"x":-2.10,"y":-1.69}, "PSDB":{"numPartido":99,"x":3.83,"y":4.62}, "PV":{"numPartido":99,"x":0,"y":0}, "PSOL":{"numPartido":99,"x":-2.28,"y":10.84}, "PCdoB":{"numPartido":99,"x":4.03,"y":0.02}, "PP":{"numPartido":99,"x":3.16,"y":-0.35}, "PR":{"numPartido":99,"x":-0.59,"y":-2.16}, "DEM":{"numPartido":99,"x":7.33,"y":-2.80}, "PMDB":{"numPartido":99,"x":3.38,"y":-2.45}, "PSC":{"numPartido":99,"x":-2.36,"y":-3.63}, "PTB":{"numPartido":99,"x":-3.03,"y":-0.14}, "PDT":{"numPartido":99,"x":-1.95,"y":-0.42}, "PSB":{"numPartido":99,"x":-3.44,"y":-0.49}, "PPS":{"numPartido":99,"x":7.46,"y":1.60}, "PRB":{"numPartido":99,"x":-3.22,"y":-0.20}}}

/***********************************************************************
 *          ##################################################
 *                             ÁREA DE FUNÇÕES
 *          ##################################################
 **********************************************************************/

/***********************************************************************
 * Função que carrega os anos existentes no combo
 **********************************************************************/
//*
function carregaComboAnos(listaAnos){
    $.each(listaAnos,function(index,ano){
            var elOptNew = document.createElement('option');
            elOptNew.text = ano
            elOptNew.value = ano
            var elSel = document.getElementById('anos')
            try {
                elSel.add(elOptNew, null) // standards compliant; doesn't work in IE
            }catch(ex){
                elSel.add(elOptNew) // IE only
            }
        });
}//*/

/***********************************************************************
 * Função que calcula o offset a ser aplicado nos valores de um
 *      determinado ano para não plotar valores negativos
 *      retorna o offset [x,y]
 **********************************************************************/
//*
function calculaOffset(dictAno){
    var offsetX = 0
    var offsetY = 0

    $.each(dictAno, function(partido, coordenadas){
        if (coordenadas['x'] < offsetX)
            offsetX = coordenadas['x']
        if (coordenadas['y'] < offsetY)
            offsetY = coordenadas['y']
    })

    offsetX = Math.abs(offsetX)
    offsetY = Math.abs(offsetY)
    return [offsetX,offsetY]
}//*/

/***********************************************************************
 * Recebe os dados e os retorna com o offset aplicado
 **********************************************************************/
//*
function aplicaOffset(dictAno,offset){
    var retorno = {}

    $.each(dictAno, function(partido, coordenadas){
        retorno[partido] = dictAno[partido]
        retorno[partido]['x'] = retorno[partido]['x']+offset[0]
        retorno[partido]['y'] = retorno[partido]['y']+offset[1]
    })

    return retorno
}//*/

/***********************************************************************
 * Retorna um vetor com os maiores valores de x e y.
 * RESTRIÇÃO: apenas para valores positivos.
 **********************************************************************/
//*
function calculaExtermos(dictAno){
    var maiorValor = [0,0] //[MaiorX,MaiorY]

    $.each(dictAno, function(partido, coordenada){
        if (maiorValor[0] < coordenada['x'])
            maiorValor[0] = coordenada['x']
        if (maiorValor[1] < coordenada['y'])
            maiorValor[1] = coordenada['y']
    })

    return maiorValor
}//*/

/***********************************************************************
 * Função que normaliza as coordenadas
 *      - Transformar os dados todos em valores positivos
 *      - retorna dicionário de dados do ano normalizado
 *              entre tamanhoX e tamanhoY
 *      Dá uma margem de GlobalRaioMaximo em cada um dos 4 lados
 *          para garantir os círculos dentro do canvas
 **********************************************************************/
//*
function normaliza(dadosCompletos, tamanhoX, tamanhoY){

    var retorno = dadosCompletos
    var temporario = [0,0]

    // variável que vai armazenaro offset a ser aplicado (maior X e maior Y)
    var offset = [0,0]

    // calculando os offsets
    $.each(dadosCompletos, function(ano,dados){
        temporario = calculaOffset(dadosCompletos[ano])
        if (temporario[0] > offset[0])
            offset[0] = temporario[0]
        if (temporario[1] > offset[1])
            offset[1] = temporario[1]
    })

    // aplicando o offset em cada ano
    $.each(dadosCompletos, function(ano,dados){
        retorno[ano] = aplicaOffset(dadosCompletos[ano],offset)
    })

    // ************************************************
    // normalizando os dados entre tamanhoX e tamanhoY
    // ************************************************
        // Calculando os maiores valores de X e Y de todos os anos
        var maximoXY = [0,0]
        $.each(retorno, function(ano,dados){
            temporario = calculaExtermos(dados)
            if (temporario[0] > maximoXY[0])
                maximoXY[0] = temporario[0]
            if (temporario[1] > maximoXY[1])
                maximoXY[1] = temporario[1]
        })

        //Faz a conta para um canvas de "tamanhoX - 2*GlobalRaioMaximo
            // para poder dar margem de GlobalRaioMaximo para cada lado
        var percentualX = (tamanhoX - 2*GlobalRaioMaximo)/maximoXY[0]
        var percentualY = (tamanhoY - 2*GlobalRaioMaximo)/maximoXY[1]

        //normalizando efetivamente
        $.each(retorno, function(ano,dados){
            $.each(retorno[ano], function(partido,coordenadas){
                retorno[ano][partido]['x'] = percentualX * retorno[ano][partido]['x'] + GlobalRaioMaximo
                retorno[ano][partido]['y'] = percentualY * retorno[ano][partido]['y'] + GlobalRaioMaximo
            })
        })

    return retorno
}//*/

/***********************************************************************
 * Função que faz o plot de um determinado ano, sem animação
 *      papel é o 'canvas' aonde devem ser plotados os dados
 *      conjunto é um elemento do tipo paper.set() que serve
 *      de agrupamento para os dados plotados e
 *      partidos é a lista de partidos
 **********************************************************************/
//*
function plotaDadosEstaticos(papel,dictAno,partidos,conjunto){
    $.each(partidos, function(index,partido){
        var partidoSet = papel.set()
        partidoSet.push(
            papel.circle(
                dictAno[partido]['x'],dictAno[partido]['y'],GlobalRaioMaximo).attr(
                    {
                        gradient: '90-#526c7a-#64a0c1',
                        stroke: '#3b4449',
                        'stroke-width': 1,
                        'stroke-linejoin': 'round',
                        rotation: -90,
                        title: partido + " - " + dictAno[partido]['numPartido'],
                        text: dictAno[partido]['numPartido']
                    }),
            papel.text(
                dictAno[partido]['x'],dictAno[partido]['y'],dictAno[partido]['numPartido']).attr(
                    {
                        'font-size': 11,
                        title: partido + " - " + dictAno[partido]['numPartido'],
                        cursor: 'default'
                    })
        )
        conjunto.push(partidoSet)
    })
    return conjunto
}//*/

/***********************************************************************
 * Função que faz a animação entre dois determinados anos
 *      papel é o 'canvas' dictAno são os dados do fim da animação,
 *      conjunto é um elemento do tipo paper.set() que serve
 *      de agrupamento para os dados plotados e
 *      partidos é a lista de partidos
 **********************************************************************/
//*
function animaDados(dictAno, partidos, conjunto){
    animObject=Raphael.animation({}, GlobalTempoAnimacao, 'linear');

    var elemento_de_referencia = partidos.length - 1
    $.each(partidos, function(index,partido){
        if (index < elemento_de_referencia){
            conjunto[index].stop().animateWith(
                    conjunto[elemento_de_referencia],
                    animObject,
                    {
                        cx:dictAno[partido]['x'],
                        cy:dictAno[partido]['y']
                    },
                    GlobalTempoAnimacao,
                    'linear'
            )
            conjunto[index][1].stop().animateWith(
                    conjunto[elemento_de_referencia],
                    animObject,
                    {
                        x:dictAno[partido]['x'],
                        y:dictAno[partido]['y']
                    },
                    GlobalTempoAnimacao,
                    'linear'
            )
        }
    })

    //Atualizando a animação do último partido
        // assim que essa animação é disparada, todas as outras também são
    conjunto[elemento_de_referencia][0].stop().animate(
            {
                cx:dictAno[partidos[elemento_de_referencia]]['x'],
                cy:dictAno[partidos[elemento_de_referencia]]['y']
            },
            GlobalTempoAnimacao,
            'linear'
    )
    conjunto[elemento_de_referencia][1].stop().animate(
            {
                x:dictAno[partidos[elemento_de_referencia]]['x'],
                y:dictAno[partidos[elemento_de_referencia]]['y']
            },
            GlobalTempoAnimacao,
            'linear'
    )

    return conjunto
}//*/

/***********************************************************************
 * Função que faz o plot inicial dos dados
 **********************************************************************/
//*
Raphael(function () {
    /*******************************************************************
     *                     INICIALIZANDO O GRÁFICO                     *
     ******************************************************************/

        var dadosCompletos = GlobalCoord
        var anosExistentes = []
        var lista_partidos = [] // Essa lista será usada só para garantir a ordem dos partidos
        var menorAno = 0
        var anoOrigem = 0 // variável usada no loop de animação

        // Recuperando a lista de anos recebida no dicionário
             // e o menor ano da lista
        $.each(dadosCompletos, function(ano, dados){
            if (menorAno == 0 || menorAno > ano)
                menorAno = ano
            anosExistentes.push(ano)
            anosExistentes.sort()
        })
        anoOrigem = menorAno //inicializando variável anoOrigem

        // Recuperando a lista de partidos recebida no dicionário
            // Aqui se considera que os partidos em todos os anos são
            // os mesmos, ou seja, se aparece em um ano TEM que aparecer
            // nos outros!
        $.each(dadosCompletos[menorAno], function(partido, infos){
            lista_partidos.push(partido)
        })
        lista_partidos.sort() // Apenas para colocar em ordem alfabética!

        var papel = Raphael(document.getElementById("animacao"),10,10)

        //Carregando o Combo com os anos disponíveis
        carregaComboAnos(anosExistentes)

        //Normalizando os dados
        dadosCompletos = normaliza(dadosCompletos,GlobalLargura,GlobalAltura)
        var tamanhoCanvas = calculaExtermos(dadosCompletos[menorAno])

        // Altera o canvas para tamanho máximo necessário +10%
        var papel = Raphael(document.getElementById("animacao"),10,10)
        papel.setSize(1.1*tamanhoCanvas[0],1.1*tamanhoCanvas[1])

        // Pseudo elemento do tipo 'conjunto' ou 'grupo' (set) para
            // agrupar os dados plotados. Nesse grupo teremos
            // aninhados outros grupos, um para cada partido,
            // contendo um elemento do tipo circle e um do tipo text
            // CONJUNTO = [PARTIDO*]
            //      PARTIDO = [CIRCLE,TEXT]
        var conjunto = papel.set()

        //Parseando os dados iniciais para plotagem
                // e plotando (agrupado em 'conjunto')
        conjunto = plotaDadosEstaticos(papel,dadosCompletos[menorAno],lista_partidos, conjunto)

    /*******************************************************************
      *                GERENCIANDO ANIMAÇÕES
      *****************************************************************/
        var selecionaAno = document.getElementById("anos")
        var animar = document.getElementById("animar")

        animar.onclick = function () {

            var anoDestino = selecionaAno.value

            // inicioLoop e fimLoop não são valores dos anos, mas sim os
                // respectivos índices no vetor anosExistentes
            var inicioLoop = $.inArray(anoOrigem,anosExistentes),
                fimLoop = $.inArray(anoDestino,anosExistentes)

            if (fimLoop != -1 && inicioLoop != fimLoop) { // apenas verificando se os anos de origem e destino existem na lista
                if (inicioLoop >= fimLoop){ // nesse caso ele volta no tempo
                    inicioLoop--
                    for (inicioLoop ; inicioLoop <= fimLoop ; inicioLoop--)
                        animaDados(dadosCompletos[anosExistentes[inicioLoop]], lista_partidos, conjunto)
                }else{
                    inicioLoop++
                    for (inicioLoop ; inicioLoop <= fimLoop ; inicioLoop++)
                        var retorno = animaDados(dadosCompletos[anosExistentes[inicioLoop]], lista_partidos, conjunto)
                }
                anoOrigem = anoDestino
            }
        }//fim da animação

    return papel
})//*/
