def main(convencao=False, cmsp=False, senado=False, camara=False):
    if convencao is not False:
        from importadores import convencao as importador_convencao

        importador_convencao.main()

    if cmsp is not False:
        from importadores import cmsp as importador_cmsp

        importador_cmsp.main()

    if senado is not False:
        from importadores import senado as importador_senado

        importador_senado.main()

    if camara is not False:
        from importadores import camara as importador_camara

        importador_camara.main()
