from flask import flash


class MessageLevel():
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'


class Message:
    @staticmethod
    def get_err_message(errors):
        return list(errors)[0][0]

    @staticmethod
    def flash_message(message, message_lvl):
        flash(message, message_lvl)
