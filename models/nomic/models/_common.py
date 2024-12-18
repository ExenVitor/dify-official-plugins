from dify_plugin.errors.model import (InvokeAuthorizationError,
                                      InvokeBadRequestError,
                                      InvokeConnectionError, InvokeError,
                                      InvokeRateLimitError,
                                      InvokeServerUnavailableError)


class _CommonNomic:
    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        """
        Map model invoke error to unified error
        The key is the error type thrown to the caller
        The value is the error type thrown by the model,
        which needs to be converted into a unified error type for the caller.

        :return: Invoke error mapping
        """
        return {
            InvokeConnectionError: [InvokeConnectionError],
            InvokeServerUnavailableError: [InvokeServerUnavailableError],
            InvokeRateLimitError: [InvokeRateLimitError],
            InvokeAuthorizationError: [InvokeAuthorizationError],
            InvokeBadRequestError: [KeyError, InvokeBadRequestError],
        }
