/***********************************************************************
 *          ##################################################
 *                              DOCUMENTAÇÃO
 *          ##################################################
 *
 *  "dados_completos"    é o dicionário com os dados de todos os periodos a
 *                          serem considerados
 *
 *  "dict_periodo"           é o dicionário com os dados de um único periodo
 *
 *  "lista_periodos"         é a lista com os periodos considerados na análise
 *                          formato: [periodo1, periodo2, periodo3, etc]
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

window.GlobalAltura = 960*0.5
window.GlobalLargura = 1280*0.5
window.GlobalRaioMaximo = 16
window.GlobalTempoAnimacao = 5000 //em milisegundos
window.GlobalCoord={
    1990:{"PT":{"numPartido":13,"x":10,"y":10}, "PSDB":{"numPartido":45,"x":0,"y":0}, "PSOL":{"numPartido":50,"x":5,"y":0}, "DEM":{"numPartido":25,"x":0,"y":5}},
    1995:{"PT":{"numPartido":13,"x":10,"y":5}, "PSDB":{"numPartido":45,"x":10,"y":0}, "PSOL":{"numPartido":50,"x":0,"y":10}, "DEM":{"numPartido":25,"x":5,"y":0}},
    2000:{"PT":{"numPartido":13,"x":10,"y":0}, "PSDB":{"numPartido":45,"x":5,"y":0}, "PSOL":{"numPartido":50,"x":5,"y":5}, "DEM":{"numPartido":25,"x":0,"y":0}}
}
//window.GlobalCoord={2010:{"PT":{"numPartido":99,"x":-100,"y":-100},"PSDB":{"numPartido":99,"x":100,"y":-100},"PV":{"numPartido":99,"x":-100,"y":100},"PSOL":{"numPartido":99,"x":100,"y":100},},1990:{"PT":{"numPartido":99,"x":0,"y":0},"PSDB":{"numPartido":99,"x":0,"y":0},"PV":{"numPartido":99,"x":0,"y":0},"PSOL":{"numPartido":99,"x":0,"y":0},},2005:{"PT":{"numPartido":99,"x":100,"y":-100},"PSDB":{"numPartido":99,"x":-100,"y":100},"PV":{"numPartido":99,"x":100,"y":100},"PSOL":{"numPartido":99,"x":-100,"y":-100},},2000:{"PT":{"numPartido":99,"x":-100,"y":100},"PSDB":{"numPartido":99,"x":100,"y":100},"PV":{"numPartido":99,"x":-100,"y":-100},"PSOL":{"numPartido":99,"x":100,"y":-100},},1995:{"PT":{"numPartido":99,"x":100,"y":100},"PSDB":{"numPartido":99,"x":-100,"y":-100},"PV":{"numPartido":99,"x":100,"y":-100},"PSOL":{"numPartido":99,"x":-100,"y":100},}}
//window.GlobalCoord={1990:{"PT":{"numPartido":99,"x":-4.10,"y":-0.69},"PSDB":{"numPartido":99,"x":8.83,"y":2.62},"PV":{"numPartido":99,"x":0.82,"y":-0.01},"PSOL":{"numPartido":99,"x":10.28,"y":-5.84},"PCdoB":{"numPartido":99,"x":-4.03,"y":0.02},"PP":{"numPartido":99,"x":-3.16,"y":0.35},"DEM":{"numPartido":99,"x":7.33,"y":2.80},"PMDB":{"numPartido":99,"x":-3.38,"y":0.45}},2010:{"PT":{"numPartido":99,"x":4.10,"y":-0.69},"PSDB":{"numPartido":99,"x":4.83,"y":-2.62},"PV":{"numPartido":99,"x":4.82,"y":3.01},"PSOL":{"numPartido":99,"x":-4.28,"y":-5.84},"PCdoB":{"numPartido":99,"x":-4.03,"y":5.02},"PP":{"numPartido":99,"x":-1.16,"y":-0.35},"DEM":{"numPartido":99,"x":0.33,"y":2.80},"PMDB":{"numPartido":99,"x":-3.38,"y":-0.45}},2000:{"PT":{"numPartido":99,"x":-2.10,"y":-1.69},"PSDB":{"numPartido":99,"x":3.83,"y":4.62},"PV":{"numPartido":99,"x":0,"y":0},"PSOL":{"numPartido":99,"x":-2.28,"y":10.84},"PCdoB":{"numPartido":99,"x":4.03,"y":0.02},"PP":{"numPartido":99,"x":3.16,"y":-0.35},"DEM":{"numPartido":99,"x":7.33,"y":-2.80},"PMDB":{"numPartido":99,"x":3.38,"y":-2.45}},1995:{"PT":{"numPartido":99,"x":-3.38,"y":-0.45},"PSDB":{"numPartido":99,"x":0.33,"y":2.80},"PV":{"numPartido":99,"x":-1.16,"y":-0.35},"PSOL":{"numPartido":99,"x":-4.03,"y":5.02},"PCdoB":{"numPartido":99,"x":-4.28,"y":-5.84},"PP":{"numPartido":99,"x":4.82,"y":3.01},"DEM":{"numPartido":99,"x":4.83,"y":-2.62},"PMDB":{"numPartido":99,"x":4.10,"y":-0.69}}}
//window.GlobalCoord = {1990:{"PT":{"numPartido":99,"x":-4.10,"y":-0.69}, "PSDB":{"numPartido":99,"x":8.83,"y":2.62}, "PV":{"numPartido":99,"x":0.82,"y":-0.01}, "PSOL":{"numPartido":99,"x":10.28,"y":-5.84}, "PCdoB":{"numPartido":99,"x":-4.03,"y":0.02}, "PP":{"numPartido":99,"x":-3.16,"y":0.35}, "PR":{"numPartido":99,"x":-2.59,"y":-0.16}, "DEM":{"numPartido":99,"x":7.33,"y":2.80}, "PMDB":{"numPartido":99,"x":-3.38,"y":0.45}, "PSC":{"numPartido":99,"x":-2.36,"y":0.63}, "PTB":{"numPartido":99,"x":-3.03,"y":-0.14}, "PDT":{"numPartido":99,"x":-1.95,"y":-0.42}, "PSB":{"numPartido":99,"x":-3.44,"y":-0.49}, "PPS":{"numPartido":99,"x":7.46,"y":1.60}, "PRB":{"numPartido":99,"x":-3.22,"y":-0.20}}, 2000:{"PT":{"numPartido":99,"x":-2.10,"y":-1.69}, "PSDB":{"numPartido":99,"x":3.83,"y":4.62}, "PV":{"numPartido":99,"x":0,"y":0}, "PSOL":{"numPartido":99,"x":-2.28,"y":10.84}, "PCdoB":{"numPartido":99,"x":4.03,"y":0.02}, "PP":{"numPartido":99,"x":3.16,"y":-0.35}, "PR":{"numPartido":99,"x":-0.59,"y":-2.16}, "DEM":{"numPartido":99,"x":7.33,"y":-2.80}, "PMDB":{"numPartido":99,"x":3.38,"y":-2.45}, "PSC":{"numPartido":99,"x":-2.36,"y":-3.63}, "PTB":{"numPartido":99,"x":-3.03,"y":-0.14}, "PDT":{"numPartido":99,"x":-1.95,"y":-0.42}, "PSB":{"numPartido":99,"x":-3.44,"y":-0.49}, "PPS":{"numPartido":99,"x":7.46,"y":1.60}, "PRB":{"numPartido":99,"x":-3.22,"y":-0.20}}}

/***********************************************************************
 *          ##################################################
 *                             ÁREA DE FUNÇÕES
 *          ##################################################
 **********************************************************************/

/***********************************************************************
 * Função que carrega os periodos existentes no combo
 **********************************************************************/
//*
function carregaComboPeriodos(lista_periodos){
    $.each(lista_periodos,function(index,periodo){
            var elOptNew = document.createElement('option');
            elOptNew.text = periodo
            elOptNew.value = periodo
            var elSel = document.getElementById('periodos')
            try {
                elSel.add(elOptNew, null) // standards compliant; doesn't work in IE
            }catch(ex){
                elSel.add(elOptNew) // IE only
            }
        });
}//*/

/***********************************************************************
 * Função que calcula o offset a ser aplicado nos valores de um
 *      determinado periodo para não plotar valores negativos
 *      retorna o offset [x,y]
 **********************************************************************/
//*
function calculaOffset(dict_periodo){
    var offsetX = 0
    var offsetY = 0

    $.each(dict_periodo, function(partido, coordenadas){
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
function aplicaOffset(dict_periodo,offset){
    var retorno = {}

    $.each(dict_periodo, function(partido, coordenadas){
        retorno[partido] = dict_periodo[partido]
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
function calculaExtermos(dict_periodo){
    var maiorValor = [0,0] //[MaiorX,MaiorY]

    $.each(dict_periodo, function(partido, coordenada){
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
 *      - retorna dicionário de dados do periodo normalizado
 *              entre tamanhoX e tamanhoY
 *      Dá uma margem de GlobalRaioMaximo em cada um dos 4 lados
 *          para garantir os círculos dentro do canvas
 **********************************************************************/
//*
function normaliza(dados_completos, tamanhoX, tamanhoY){

    var retorno = dados_completos
    var temporario = [0,0]

    // variável que vai armazenaro offset a ser aplicado (maior X e maior Y)
    var offset = [0,0]

    // calculando os offsets
    $.each(dados_completos, function(periodo,dados){
        temporario = calculaOffset(dados_completos[periodo])
        if (temporario[0] > offset[0])
            offset[0] = temporario[0]
        if (temporario[1] > offset[1])
            offset[1] = temporario[1]
    })

    // aplicando o offset em cada periodo
    $.each(dados_completos, function(periodo,dados){
        retorno[periodo] = aplicaOffset(dados_completos[periodo],offset)
    })

    // ************************************************
    // normalizando os dados entre tamanhoX e tamanhoY
    // ************************************************
        // Calculando os maiores valores de X e Y de todos os periodos
        var maximoXY = [0,0]
        $.each(retorno, function(periodo,dados){
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
        $.each(retorno, function(periodo,dados){
            $.each(retorno[periodo], function(partido,coordenadas){
                retorno[periodo][partido]['x'] = percentualX * retorno[periodo][partido]['x'] + GlobalRaioMaximo
                retorno[periodo][partido]['y'] = percentualY * retorno[periodo][partido]['y'] + GlobalRaioMaximo
            })
        })

    return retorno
}//*/

/***********************************************************************
 * Função que faz o plot de um determinado periodo, sem animação
 *      papel é o 'canvas' aonde devem ser plotados os dados
 *      conjunto é um elemento do tipo paper.set() que serve
 *      de agrupamento para os dados plotados e
 *      partidos é a lista de partidos
 **********************************************************************/
//*
function plotaDadosEstaticos(papel,dict_periodo,partidos,conjunto){
    $.each(partidos, function(index,partido){
        var partido_set = papel.set()
        partido_set.push(
            papel.circle(
                dict_periodo[partido]['x'],dict_periodo[partido]['y'],GlobalRaioMaximo).attr(
                    {
                        gradient: '90-#526c7a-#64a0c1',
                        stroke: '#3b4449',
                        'stroke-width': 1,
                        'stroke-linejoin': 'round',
                        rotation: -90,
                        title: partido + " - " + dict_periodo[partido]['numPartido'],
                        text: dict_periodo[partido]['numPartido']
                    }),
            papel.text(
                dict_periodo[partido]['x'],dict_periodo[partido]['y'],dict_periodo[partido]['numPartido']).attr(
                    {
                        'font-size': 11,
                        title: partido + " - " + dict_periodo[partido]['numPartido'],
                        cursor: 'default'
                    })
        )
        conjunto.push(partido_set)
    })
    return conjunto
}//*/

/***********************************************************************
 * Função que faz a animação entre dois determinados periodos
 *      papel é o 'canvas' dict_periodo são os dados do fim da animação,
 *      conjunto é um elemento do tipo paper.set() que serve
 *      de agrupamento para os dados plotados e
 *      partidos é a lista de partidos
 **********************************************************************/
//*
function animaTransicao(graficos, dados_full, partidos, periodos, indice_origem, indice_destino, direcao){

    var idx_ult_partido = partidos.length - 1 // índice do último partido na lista de partidos

    //gerando uma lista de parâmetros com dois dicionários:
        //[0]: parâmetros do circulo
        //[1]: parâmetros do texto
    var parametros_gerais = geraParametrosAnimacao(dados_full, partidos[idx_ult_partido], periodos, indice_origem, indice_destino, direcao)

    //anim é um objeto do tipo 'animation' e que contém a animação que será aplicada
        //no círculo do último partido do vetor partidos.
    var animObj = Raphael.animation(parametros_gerais[0], GlobalTempoAnimacao, "linear")

    //animando o último partido da lista
        //Círculo
    var el_anima = graficos[idx_ult_partido][0].animate(animObj)
        //Texto
    graficos[idx_ult_partido][1].animateWith(
                                el_anima, animObj,
                                parametros_gerais[1],
                                GlobalTempoAnimacao,
                                "linear"
                            )

    //loop para todos os partidos exceto o último
    $.each(partidos, function(key_part, partido){
        //excluindo o último partido das iterações
        if (key_part < idx_ult_partido){

            //gerando uma lista de parâmetros com dois dicionários:
                //[0]: parâmetros do circulo
                //[1]: parâmetros do texto
            parametros_gerais = geraParametrosAnimacao(dados_full, partido, periodos, indice_origem, indice_destino, direcao)

            //Gerando objetos de objetos de animação para o círculo e para o texto
            var anima_partido_circulo = Raphael.animation(parametros_gerais[0], GlobalTempoAnimacao, "linear")
            var anima_partido_texto = Raphael.animation(parametros_gerais[1], GlobalTempoAnimacao, "linear")
            //configurando animação do círculo
            var temp = graficos[key_part][0].animateWith(
                                            el_anima,
                                            animObj,
                                            anima_partido_circulo,
                                            GlobalTempoAnimacao,
                                            "linear"
                                        )
            //configurando animação do texto
            temp = graficos[key_part][1].animateWith(
                                            el_anima,
                                            animObj,
                                            anima_partido_texto,
                                            GlobalTempoAnimacao,
                                            "linear"
                                        )
        }
    })//fim do loop para os partidos
}

// retorna um dicionário com as coordenadas 'x' e 'y' e o método de interpolação
    //tipo == círculo -> (cx,cy)
    //tipo == texto -> (x,y)
function geraParametrosAnimacao(dados_full, partido, periodos, indice_origem, indice_destino, direcao){
    var parametros_circulo = {}
    var parametros_texto = {}
    var tagRef = [],
        x = 0,
        y = 0,
        periodo_lendo = 0,
        total_intervalos = Math.abs(indice_origem - indice_destino) + 1, //variável usada como auxiliar para indexar as animações
        passo = 100/total_intervalos,
        contador = passo

    //gerando os parâmetros
        //considera o caminhamento crescente e decrescente no tempo
    if (direcao==1){
        for (var i=indice_origem; i<=indice_destino; i++){
            periodo_lendo = periodos[i]
            x = dados_full[periodo_lendo][partido]['x']
            y = dados_full[periodo_lendo][partido]['y']

            parametros_circulo[contador+"%"] = {
                                'cx': x,
                                'cy': y
                            }
            parametros_texto[contador+"%"] = {
                                'x': x,
                                'y': y
                            }
            contador += passo
        }

    }else{
        for (var i=indice_origem; i>=indice_destino; i--){
            periodo_lendo = periodos[i]
            x = dados_full[periodo_lendo][partido]['x']
            y = dados_full[periodo_lendo][partido]['y']

            parametros_circulo[contador+"%"] = {
                                'cx': x,
                                'cy': y
                            }
            parametros_texto[contador+"%"] = {
                                'x': x,
                                'y': y
                            }
            contador += passo
        }

    }



    return [parametros_circulo, parametros_texto]
}

/***********************************************************************
 * Função que faz o plot inicial dos dados
 **********************************************************************/
//*
Raphael(function () {
    /*******************************************************************
     *                     INICIALIZANDO O GRÁFICO                     *
     ******************************************************************/

        var dados_completos = GlobalCoord
        var lista_periodos = []
        var lista_partidos = [] // Essa lista será usada só para garantir a ordem dos partidos
        var menor_periodo = 0
        var periodo_origem = 0 // variável usada no loop de animação

        // Recuperando a lista de periodos recebida no dicionário
             // e o menor periodo da lista
        $.each(dados_completos, function(periodo, dados){
            if (menor_periodo == 0 || menor_periodo > periodo)
                menor_periodo = periodo
            lista_periodos.push(periodo)
            lista_periodos.sort()
        })
        periodo_origem = menor_periodo //inicializando variável periodo_origem

        // Recuperando a lista de partidos recebida no dicionário
            // Aqui se considera que os partidos em todos os periodos são
            // os mesmos, ou seja, se aparece em um periodo TEM que aparecer
            // nos outros!
        $.each(dados_completos[menor_periodo], function(partido, infos){
            lista_partidos.push(partido)
        })
        lista_partidos.sort() // Apenas para colocar em ordem alfabética!

        //Carregando o Combo com os periodos disponíveis
        carregaComboPeriodos(lista_periodos)

        //Normalizando os dados
        dados_completos = normaliza(dados_completos,GlobalLargura,GlobalAltura)
        //var tamanho_canvas = calculaExtermos(dados_completos[menor_periodo])

        // Altera o canvas para tamanho máximo necessário +10%
        var papel = Raphael(document.getElementById("animacao"),GlobalLargura,GlobalAltura)
        //papel.setSize(1.1*tamanho_canvas[0],1.1*tamanho_canvas[1])

        // Pseudo elemento do tipo 'conjunto' ou 'grupo' (set) para
            // agrupar os dados plotados. Nesse grupo teremos
            // aninhados outros grupos, um para cada partido,
            // contendo um elemento do tipo circle e um do tipo text
            // CONJUNTO = [PARTIDO*]
            //      PARTIDO = [CIRCLE,TEXT]
        var conjunto = papel.set()

        //Parseando os dados iniciais para plotagem
                // e plotando (agrupado em 'conjunto')
        conjunto = plotaDadosEstaticos(papel,dados_completos[menor_periodo],lista_partidos, conjunto)

    /*******************************************************************
      *                GERENCIANDO ANIMAÇÕES
      *****************************************************************/
        var seleciona_periodo = document.getElementById("periodos")
        var animar = document.getElementById("animar")
        var direcao_temporal = 1 // 1 é para direita e -1 é para esquerda

        animar.onclick = function () {

            var periodo_destino = seleciona_periodo.value
            if (periodo_destino != periodo_origem){
                //calculando variável que indica direção temporal do movimento
                if (periodo_destino > periodo_origem)
                    direcao_temporal = 1
                else
                    direcao_temporal = -1

                var indice_periodo_origem = $.inArray(periodo_origem, lista_periodos)
                var indice_periodo_destino = $.inArray(periodo_destino, lista_periodos)

                animaTransicao(conjunto, dados_completos, lista_partidos, lista_periodos, indice_periodo_origem, indice_periodo_destino, direcao_temporal)

                periodo_origem = periodo_destino
            }
        }//fim da animação

    return papel
})//*/
