from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    def on_start(self):
        self.client.post("/registrar", json={
            "name": "Roberto Campos",
            "email": "robertocampos@email.com",
            "password": "1234",
            "cellphoneNumber": "12999998888"
        })
        
    @task
    def about(self):
        self.client.get("/usuarios")