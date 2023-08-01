class FormatError:
    @staticmethod
    def format_serializer_errors(errors):
        return {
            field: messages[0] if isinstance(messages, list) else messages
            for field, messages in errors.items()
        }
