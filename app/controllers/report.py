from flask import Response, jsonify
from flask_restful import Resource
import datetime


from app.entities.cpu_usage import CpuUsage
from app.services.image_uploader import ImageUploader
from app.services.mailer import Mailer
from app.services.monitoramento import Monitoramento
from app.services.monitoramento2 import Monitoramento2
from app.services.plot_generator import plot_barh_chart, plot_line_chart


class Report(Resource):

    def get(self, date_now, time_range, email_to) -> Response:

        # try:
            uploader = ImageUploader()

            metricas = [CpuUsage, CpuUsage, CpuUsage, CpuUsage, CpuUsage]
            data = []
            image_paths = []

            for x in metricas:

                monitorar = Monitoramento(x, date_now, time_range)
                dados = monitorar.get_data()
                data.append(dados)

                buf = plot_line_chart(dados['data'])

                imagem = uploader.uploadBytesImage(buf)
                buf.close()

                image_paths.append(imagem)

                buf = plot_barh_chart(dados['data'])

                imagem = uploader.uploadBytesImage(buf)
                buf.close()

                image_paths.append(imagem)

            assunto = 'Pycemaker - Relatório Periódico'
            mailer = Mailer(email_to, assunto)
            html_body = mailer.generate_report(data, image_paths, date_now, time_range)
            mailer = mailer.dispatch_email(html_body)

            uploader.close()

            return jsonify({'msg': "E-mail enviado com sucesso!"})
        # except:
        #     return jsonify({'msg': "Não foi possível finalizar a operação"})
