import logging

from dify_plugin.interfaces.model import ModelProvider

logger = logging.getLogger(__name__)


class HuggingfaceHubProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        pass
