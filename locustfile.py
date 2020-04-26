from locust import HttpLocust, TaskSet, task, between

class UserBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        response = self.client.get("/it/utenti/entra/")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/it/utenti/entra/", {"username":"divani", "password":"EF&3xbHuSZdY"}, headers={"X-CSRFToken": csrftoken})

    def logout(self):
        self.client.post("/it/utenti/esci/")

    @task(1)
    def profile(self):
        self.client.get("/it/utenti/parruc/")

    @task(2)
    def networking(self):
        self.client.get("/it/utenti/networking/")

    @task(3)
    def calendar(self):
        self.client.get("/it/eventi/")

    @task(4)
    def exhibitor(self):
        self.client.get("/it/espositori/divani-e-divani/")


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
