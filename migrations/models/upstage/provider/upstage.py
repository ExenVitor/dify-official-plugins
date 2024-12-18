import logging
from dify_plugin.entities.model import ModelType
from dify_plugin.errors.model import CredentialsValidateFailedError
from dify_plugin import ModelProvider

logger = logging.getLogger(__name__)


class UpstageProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        Validate provider credentials
        if validate failed, raise exception

        :param credentials: provider credentials, credentials from defined in `provider_credential_schema`.
        """
        try:
            model_instance = self.get_model_instance(ModelType.LLM)
            model_instance.validate_credentials(model="solar-1-mini-chat", credentials=credentials)
        except CredentialsValidateFailedError as e:
            logger.exception(f"{self.get_provider_schema().provider} credentials validate failed")
            raise e
        except Exception as e:
            logger.exception(f"{self.get_provider_schema().provider} credentials validate failed")
            raise e
