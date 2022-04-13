import sys
import traceback
from flask import Response, jsonify
from flask_restful import Resource


from app.entities.cpu import CpuUsage
from app.entities.ram import JvmMemoryUsage
from app.services.image_uploader import ImageUploader
from app.services.mailer import Mailer
from app.services.monitoramento import Monitoramento
from app.services.reporter import Reporter
from app.services.plot_generator import plot_barh_chart, plot_line_chart


class ReportTest(Resource):

    def get(self, date_now, time_range, email_to) -> Response:

        uploader = ImageUploader()
        try:

            metricas = [CpuUsage, JvmMemoryUsage, CpuUsage, CpuUsage, CpuUsage]
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
            html_body = mailer.generate_report(
                data, image_paths, date_now, time_range)
            mailer = mailer.dispatch_email(html_body)

            uploader.close()

            return jsonify({'msg': "E-mail enviado com sucesso!"})
        except Exception:
            uploader.close()
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            return jsonify({'msg': "Não foi possível finalizar a operação"})


class Report(Resource):

    def get(self, date_now, time_range, email_to) -> Response:

        try:
            report = Reporter(date_now, time_range, email_to)
            report = report.get_report()

            return jsonify({'msg': report})
        except Exception as err:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            return jsonify({'msg': err})
