from datetime import datetime
import sys
import traceback
from flask import jsonify
from app.entities.cpu import CpuUsage
from app.entities.ram import JvmMemoryUsage
from app.entities.request_count import RequestCount
from app.entities.response_time import ResponseTime
from app.services.image_uploader import ImageUploader
from app.services.mailer import Mailer
from app.services.monitoramento import Monitoramento
from app.services.plot_generator import plot_barh_chart, plot_line_chart


class Reporter:

    def __init__(self, time_range, email_to):
        self.time_range = time_range
        self.email_to = email_to
        self.data = []
        self.image_paths = []
        self.metricas = [CpuUsage, JvmMemoryUsage,
                         RequestCount, ResponseTime]
        self.isPercentage = [False, False, True, True]

    def get_report(self):

        uploader = ImageUploader()

        try:

            for k, v in enumerate(self.metricas):

                date_now = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

                monitorar = Monitoramento(v, date_now, self.time_range)
                dados = monitorar.get_interval_data()
                self.data.append(dados)

                buf = plot_line_chart(dados['data'], self.isPercentage[k])
                imagem = uploader.uploadBytesImage(buf)
                buf.close()
                self.image_paths.append(imagem)

                buf = plot_barh_chart(dados['data'])
                imagem = uploader.uploadBytesImage(buf)
                buf.close()
                self.image_paths.append(imagem)

            assunto = 'Pycemaker - Relatório Periódico'
            mailer = Mailer(self.email_to, assunto)
            html_body = mailer.generate_report(
                self.data, self.image_paths, date_now, self.time_range)
            mailer = mailer.dispatch_email(html_body)
            uploader.close()

            return "Relatório enviado com sucesso!"

        finally:
            uploader.close()
