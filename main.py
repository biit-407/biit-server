from biit_server import create_app
import google.cloud.logging

app = create_app()

if __name__ == "__main__":
    # Instantiates a client
    client = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default this captures all logs
    # at INFO level and higher
    client.get_default_handler()
    client.setup_logging()
    create_app().run()
