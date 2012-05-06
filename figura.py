#!/usr/bin/python
# -*- coding: utf-8 -*-

# Em desenvolvimento.

from matplotlib.pyplot import figure, show, scatter,text
from matplotlib.patches import Ellipse
import matplotlib.colors
import numpy
import analise

#                     / Datas inicio e fim \       /tamanho minimo de partidos a considerar.
a = analise.Analise('2011-01-01','2011-12-31',[],4)

print a
dados = a.partidos_2d()

fig = figure(1)
fig.clf()

cores_partidos = {'PT'   :'#FF0000',
                  'PSOL' :'#FFFF00',
                  'PV'   :'#00CC00',
                  'DEM'  :'#002664',
                  'PSDB' :'#0059AB',
                  'PSD'  :'#80c341',
                  'PMDB' :'#CC0000',
                  'PR'   :'#110274',
                  'PSC'  :'#25b84a',
                  'PSB'  :'#ff8d00',
                  'PP'   :'#203487',
                  'PCdoB':'#da251c',
                  'PTB'  :'#1f1a17',
                  'PPS'  :'#fea801',
                  'PDT'  :'#6c85b1',
                  'PRB'  :'#67a91e'}

lista_cores_partidos = []
for p in a.lista_partidos:
    if p in cores_partidos:
        lista_cores_partidos.append(cores_partidos[p])
    else:
        lista_cores_partidos.append((1,1,1))

colormap_partidos = matplotlib.colors.ListedColormap(lista_cores_partidos,name='partidos')

ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(-1,5), ylim=(-5,3))
x = dados[:,0]
y = dados[:,1]
size = numpy.array(a.tamanho_partido) * 2
scatter(x, y, size, range(len(x)), marker='o', cmap=colormap_partidos) #, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

ip = -1
for p in a.lista_partidos:
    ip += 1
    text(dados[ip,0]+.005,dados[ip,1],p,fontsize=12,stretch=100,alpha=1)



if 0:
    fig = figure(1,figsize=(8,5))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-4,3))

    t = numpy.arange(0.0, 5.0, 0.01)
    s = numpy.cos(2*numpy.pi*t)
    line, = ax.plot(t, s, lw=3, color='purple')

    ax.annotate('arrowstyle', xy=(0, 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->")
                )

    ax.annotate('arc3', xy=(0.5, -1),  xycoords='data',
                xytext=(-30, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3,rad=.2")
                )

    ax.annotate('arc', xy=(1., 1),  xycoords='data',
                xytext=(-40, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc,angleA=0,armA=30,rad=10"),
                )

    ax.annotate('arc', xy=(1.5, -1),  xycoords='data',
                xytext=(-40, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc,angleA=0,armA=20,angleB=-90,armB=15,rad=7"),
                )

    ax.annotate('angle', xy=(2., 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )

    ax.annotate('angle3', xy=(2.5, -1),  xycoords='data',
                xytext=(-50, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle3,angleA=0,angleB=-90"),
                )


    ax.annotate('angle', xy=(3., 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )

    ax.annotate('angle', xy=(3.5, -1),  xycoords='data',
                xytext=(-70, -60), textcoords='offset points',
                size=20,
                bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=-90,rad=10"),
                )

    ax.annotate('angle', xy=(4., 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                shrinkA=0, shrinkB=10,
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )


    ann = ax.annotate('', xy=(4., 1.),  xycoords='data',
                xytext=(4.5, -1), textcoords='data',
                arrowprops=dict(arrowstyle="<->",
                                connectionstyle="bar",
                                ec="k",
                                shrinkA=5, shrinkB=5,
                                )
                )


if 0:
    fig = figure(1)
    fig.clf()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-5,3))

    x = [3, 1, 0]
    y = [-4, 1, 2]
    s = [100, 50, 250]

    scatter(x, y, s, ['b','r','k'], marker='o') #, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

    el = Ellipse((2, -1), 0.5, 0.5)
    ax.add_patch(el)

    ax.annotate('$->$', xy=(2., -1),  xycoords='data',
                xytext=(-150, -140), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                patchB=el,
                                connectionstyle="angle,angleA=90,angleB=0,rad=10"),
                )

    ax.annotate('fancy', xy=(2., -1),  xycoords='data',
                xytext=(-100, 60), textcoords='offset points',
                size=20,
                #bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="fancy",
                                fc="0.6", ec="none",
                                patchB=el,
                                connectionstyle="angle3,angleA=0,angleB=-90"),
                )

    ax.annotate('simple', xy=(2., -1),  xycoords='data',
                xytext=(100, 60), textcoords='offset points',
                size=20,
                #bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="simple",
                                fc="0.6", ec="none",
                                patchB=el,
                                connectionstyle="arc3,rad=0.3"),
                )

    ax.annotate('wedge', xy=(2., -1),  xycoords='data',
                xytext=(-100, -100), textcoords='offset points',
                size=20,
                #bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="wedge,tail_width=0.7",
                                fc="0.6", ec="none",
                                patchB=el,
                                connectionstyle="arc3,rad=-0.3"),
                )


    ann = ax.annotate('wedge', xy=(2., -1),  xycoords='data',
                xytext=(0, -45), textcoords='offset points',
                size=20,
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5)),
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                fc=(1.0, 0.7, 0.7), ec=(1., .5, .5),
                                patchA=None,
                                patchB=el,
                                relpos=(0.2, 0.8),
                                connectionstyle="arc3,rad=-0.1"),
                )

    ann = ax.annotate('wedge', xy=(2., -1),  xycoords='data',
                xytext=(35, 0), textcoords='offset points',
                size=20, va="center",
                bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"),
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                fc=(1.0, 0.7, 0.7), ec="none",
                                patchA=None,
                                patchB=el,
                                relpos=(0.2, 0.5),
                                )
                )


show()
