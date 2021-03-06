import datetime
import smtplib
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage
# from dotenv import load_dotenv
from dateutil import parser
# import locale
# locale.setlocale(locale.LC_ALL, "pt_br")

# load_dotenv('.env')


class Mailer:

    def __init__(self, email_to, assunto):
        self.email_from = os.environ.get('EMAIL_FROM')
        self.password = os.environ.get('PASSWORD')
        self.email_to = email_to
        self.assunto = assunto

    def generate_body(self, msg: EmailMessage(), html_body):
        msg['Subject'] = self.assunto
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        # msg['To'] = (", ").join(self.email_to)

        # Plain text
        msg.set_content('This is a plain text email')

        # HTML Body
        # text_part = msg.iter_parts()
        # text_part
        msg.add_alternative(html_body, subtype='html')
        # <img src="cid:image1"><br>
        return msg

    def attach_images(self, msg: EmailMessage()) -> EmailMessage():
        counter = 1
        for file_path in self.image_paths:
            filename = os.path.basename(file_path)
            file_path = open(file_path, 'rb')
            msgImage = MIMEImage(file_path.read())
            file_path.close()
            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<image'+str(counter)+'>')
            msgImage.add_header('Content-Disposition',
                                'attachment', filename=filename)
            msg.attach(msgImage)
            counter += 1
        return msg

    def dispatch_email(self, html_body):

        msg = EmailMessage()
        msg = self.generate_body(msg, html_body)
        # msg = self.attach_images(msg)

        print("Enviando e-mail, aguarde...")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email_from, self.password)
            smtp.send_message(msg)

        print("E-mail enviado com sucesso!")

    def generate_picos(self, data, tag, str_indicator="", isPercentage=False):
        picos = ''
        for x in data:
            if isPercentage:
                picos = picos + \
                    f"<li> {tag} - {self.format_date(x['time_series'])} - {round(x['value'], 2)}{str_indicator} </li>"
                return picos
            else:
                picos = picos + \
                    f"<li> {tag} - {self.format_date(x['time_series'])} - {round(x['value'] * 100, 2)}{str_indicator} </li>"
                return picos

    # def generate_picos_2(self, data, tag, str_indicator=""):
    #     picos = ''
    #     for x in data:
    #         picos = picos + \
    #             f"<li> {tag} - {self.format_date(x['time_series'])} - {int(x['value'])}{str_indicator} </li>"
    #     return picos

    def format_date(self, date):
        # date = parser.parse(date)
        return date.strftime("%a, %d de %b, %H:%M:%S")

    def format_date_2(self, date):
        return date.strftime("%d/%m/%Y %H:%M")

    def generate_report_old(self, data, image_paths, date_now, time_range):

        data_final_atual = datetime.datetime.strptime(
            date_now, '%d-%m-%Y-%H-%M-%S')
        data_inicial_atual = data_final_atual - \
            datetime.timedelta(hours=int(time_range))

        html_body = """\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Relat??rio Peri??dico</h1>
                <p>Per??odo analisado: {} - {}</p>
                <p>Visualize em tempo real: <a href="https://www.google.com.br">Pycemaker Dashboard</a></p>

                <h2>Consumo de CPU</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>M??dia de Uso: {}%</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>

                <h2>Consumo de RAM</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>M??dia de Uso: {}%</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>

            </body>
        </html>
        """.format(self.format_date_2(data_inicial_atual), self.format_date_2(data_final_atual),
                   image_paths[0], image_paths[1], round(
                       data[0]['growth'] * 100, 2), round(data[0]['mean'] * 100, 2),
                   self.generate_picos(data[0]['higher'], "M??ximo", "%"),
                   self.generate_picos(data[0]['lower'], "M??nimo", "%"),
                   image_paths[2], image_paths[3], round(
                       data[1]['growth'] * 100, 2), round(data[1]['mean'], 2),
                   self.generate_picos(data[1]['higher'], "M??ximo", "%", True),
                   self.generate_picos(data[1]['lower'], "M??nimo", "%", True))

        return html_body

    def generate_report(self, data, image_paths, date_now, time_range):

        data_final_atual = datetime.datetime.strptime(
            date_now, '%d-%m-%Y-%H-%M-%S')
        data_final_atual = data_final_atual + \
            datetime.timedelta(hours=int(3))
        data_inicial_atual = data_final_atual - \
            datetime.timedelta(hours=int(time_range))

        html_body = """\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Relat??rio Peri??dico</h1>
                <p>Per??odo analisado: {} - {}</p>
                <p>Visualize em tempo real: <a href="https://www.google.com.br">Pycemaker Dashboard</a></p>

                <h2>Sa??de do Sistema</h2>
                <img src={}><br>
                <p>Tempo restante para a sa??de do sistema ser menor que 30%: {}</p>

                <h2>Consumo de CPU</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>M??dia de Uso: {}%</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>

                <h2>Consumo de RAM</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>M??dia de Uso: {}%</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>

                <h2>N??mero de Requisi????es</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>M??dia de Uso: {}</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>

                <h2>Tempo de Resposta</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminui????o: {}%</p>
                <p>Tempo M??dio: {}s</p>
                <p>Picos de Uso:</p>
                <ul>
                {}
                {}
                </ul>
            </body>
        </html>
        """.format(self.format_date_2(data_inicial_atual), self.format_date_2(data_final_atual),
                   image_paths[8],
                   data[4],
                   image_paths[0], image_paths[1], round(
                       data[0]['growth'] * 100, 2), round(data[0]['mean'] * 100, 2),
                   self.generate_picos(data[0]['higher'], "M??ximo", "%"),
                   self.generate_picos(data[0]['lower'], "M??nimo", "%"),
                   image_paths[2], image_paths[3], round(
                       data[1]['growth'] * 100, 2), round(data[1]['mean'] * 100, 2),
                   self.generate_picos(data[1]['higher'], "M??ximo", "%"),
                   self.generate_picos(data[1]['lower'], "M??nimo", "%"),
                   image_paths[4], image_paths[5], round(
                       data[2]['growth'] * 100, 2), round(data[2]['mean'], 2),
                   self.generate_picos(data[2]['higher'], "M??ximo", "", True),
                   self.generate_picos(data[2]['lower'], "M??nimo", "", True),
                   image_paths[6], image_paths[7], round(
                       data[3]['growth'] * 100, 2), round(data[3]['mean'], 2),
                   self.generate_picos(data[3]['higher'], "M??ximo", "s", True),
                   self.generate_picos(data[3]['lower'], "M??nimo", "s", True))

        return html_body
