from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    # A secretary visit the login page
    @task
    def home(self):
        self.client.get("/")

    # A secretary logs in
    @task
    def loginself(self):
        self.client.post(
            "/showSummary",
            data={'email': 'john@simplylift.co'}
        )

    # A secretary get the board page
    @task
    def board(self):
        self.client.get("/board")

    # A secretary purchase places
    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': 4
            },
            )
