import datetime
import smtplib
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv('.env')


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

    def generate_picos(self, data, tag):
        picos = ''
        for x in data:
            picos = picos + \
                f"<p> {tag} - {x['time_series']} - {x['value']} </p>"
        return picos

    def generate_report(self, data, image_paths, date_now, time_range):

        data_final_atual = datetime.datetime.strptime(
            date_now, '%d-%m-%Y-%H-%M')
        data_inicial_atual = data_final_atual - \
            datetime.timedelta(hours=int(time_range))

        html_body = """\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Relatório Periódico</h1>
                <p>Período analisado: {}-{}</p>
                <p>Visualize em tempo real: <a href="https://www.google.com.br">Pycemaker Dashboard</a></p>

                <h2>Consumo de CPU</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminuição: {}</p>
                <p>Média de Uso: {}</p>
                <p>Picos de Uso:</p>
                {}
                {}

                <h2>Consumo de RAM</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminuição: {}</p>
                <p>Média de Uso: {}</p>
                <p>Picos de Uso:</p>
                {}
                {}

                <h2>Consumo de Disco</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminuição: {}</p>
                <p>Média de Uso: {}</p>
                <p>Picos de Uso:</p>
                {}
                {}

                <h2>Tempo de Resposta</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminuição: {}</p>
                <p>Média de Uso: {}</p>
                <p>Picos de Uso:</p>
                {}
                {}

                <h2>Total de Falhas HTTP</h2>
                <img src={}><br>
                <img src={}><br>
                <p>Crescimento ou Diminuição: {}</p>
                <p>Média de Uso: {}</p>
                <p>Picos de Uso:</p>
                {}
                {}
            </body>
        </html>
        """.format(data_inicial_atual, data_final_atual,
                   image_paths[0], image_paths[1], data[0]['growth'], data[0]['mean'],
                   self.generate_picos(data[0]['higher'], "Máximo"),
                   self.generate_picos(data[0]['lower'], "Mínimo"),
                   image_paths[2], image_paths[3], data[1]['growth'], data[1]['mean'],
                   self.generate_picos(data[1]['higher'], "Máximo"),
                   self.generate_picos(data[1]['lower'], "Mínimo"),
                   image_paths[4], image_paths[5], data[2]['growth'], data[2]['mean'],
                   self.generate_picos(data[2]['higher'], "Máximo"),
                   self.generate_picos(data[2]['lower'], "Mínimo"),
                   image_paths[6], image_paths[7], data[3]['growth'], data[3]['mean'],
                   self.generate_picos(data[3]['higher'], "Máximo"),
                   self.generate_picos(data[3]['lower'], "Mínimo"),
                   image_paths[8], image_paths[9], data[4]['growth'], data[4]['mean'],
                   self.generate_picos(data[4]['higher'], "Máximo"),
                   self.generate_picos(data[4]['lower'], "Mínimo"))

        return html_body
