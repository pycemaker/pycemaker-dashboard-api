from image_uploader import ImageUploader
from mailer import Mailer
# from pycemaker import Pycemaker
from plot_generator import plot_line_chart, plot_barh_chart

# spring_app = Pycemaker(prom_url='http://localhost:9090/api/v1/query',
#     db_host='localhost',
#     db_port='27017',
#     db='pycemaker',
#     collection='appdata')

#spring_app.save_data(doc_count=10, time_to_save=30)
# spring_app.export_data_csv()
# spring_app.export_data_json(Path.cwd())

# email_to = email_destinario_aqui
# image_paths = []
# uploader = ImageUploader()
# for x in range(1, 6):
#     imagem = uploader.uploadImage("D:/chatillon/Área de Trabalho/a{}.png".format(x))
#     image_paths.append(imagem)

# mailer = Mailer(email_to, image_paths)
# mailer = mailer.dispatch_email()


# data = [{"time_series": x, "value": x} for x in range (0,10)]

# buf = plot_line_chart(data)

# uploader = ImageUploader()
# imagem = uploader.uploadBytesImage(buf)
# buf.close()

# print(imagem)

data = [{"time_series": x, "value": x, "criticity": "Muito Alto"}
        for x in range(0, 3)]
data = data + [{"time_series": x, "value": x, "criticity": "Baixo"}
               for x in range(0, 5)]
data = data + [{"time_series": x, "value": x, "criticity": "Médio"}
               for x in range(0, 4)]
data = data + [{"time_series": x, "value": x, "criticity": "Alto"}
               for x in range(0, 2)]

plot_barh_chart(data)

buf = plot_barh_chart(data)

uploader = ImageUploader()
imagem = uploader.uploadBytesImage(buf)
buf.close()
