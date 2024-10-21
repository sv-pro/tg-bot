# framework code
## the framework is responsible for abstracting the telegram bot api
## it handles all the telegram specific details: classes, methods, async handling, etc
from tg_bot.infra.app import App

#####################################################################################
if __name__ == "__main__":
    # application code
    ## the application is responsible for handling the business logic
    ## each method in the application code is a handler for a specific command
    ## it accepts a message and returns a response

    ## define an echo handler
    def start_callback(message: str) -> str:
        return "Hello, I am an echo bot. I will repeat whatever you say"

    def default_msg_callback(message: str) -> str:
        return message

    def default_cmd_callback(cmd: str) -> str:
        return cmd

    def delayed_callback(message: str, *args, **kwargs) -> str:
        import time
        time.sleep(5)
        return message

    app = App(start_callback=start_callback)
    # app.set_default_command_handler(default_cmd_callback)
    app.set_default_message_handler(default_msg_callback)
    app.add_command_handler("delay", delayed_callback)

    ## start the app
    app.run()