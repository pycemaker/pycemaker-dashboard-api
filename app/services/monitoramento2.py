import numpy as np


class Monitoramento2:
    def __init__(self, dados, nome_do_dado) -> None:

        self.dados = dados
        self.nome_do_dado = nome_do_dado

    def get_mean(self):
        mean = np.mean([x[self.nome_do_dado] for x in self.dados])
        return mean

    def get_higher(self):
        higher = max(self.dados, key=lambda x: x[self.nome_do_dado])
        all_higher = [x for x in self.dados if x[self.nome_do_dado]
                      == higher[self.nome_do_dado]]
        return all_higher

    def get_lower(self):
        lower = min(self.dados, key=lambda x: x[self.nome_do_dado])
        all_lower = [x for x in self.dados if x[self.nome_do_dado]
                     == lower[self.nome_do_dado]]
        return all_lower

    def get_growth(self, mean, mean_anterior):
        growth = (mean - mean_anterior) / mean_anterior
        return growth * 100
