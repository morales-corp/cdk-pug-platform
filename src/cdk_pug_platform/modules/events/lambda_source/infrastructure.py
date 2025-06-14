from aws_cdk import (
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
)

from cdk_pug_platform.models.modules.pug_module import PugModule
from cdk_pug_platform.models.modules.runtime.runtime_function import RuntimeIFunction
from cdk_pug_platform.models.modules.runtime.runtime_event_source import (
    RuntimeIEventSource,
)


class LambdaSourceParams:
    source: lambda_.IEventSource
    lambda_function: lambda_.IFunction

    def __init__(
        self, source: lambda_.IEventSource, lambda_function: lambda_.IFunction
    ) -> None:
        self.source = source
        self.lambda_function = lambda_function


class LambdaSourcePug(PugModule[lambda_.IFunction]):
    def __init__(self, params: LambdaSourceParams) -> None:
        assert isinstance(params.source, RuntimeIEventSource)

        params.lambda_function.add_event_source(params.source)

        self._grant_permissions(params)

        assert isinstance(params.lambda_function, RuntimeIFunction)

        super().__init__(params.lambda_function)

    def _grant_permissions(self, params: LambdaSourceParams):
        if isinstance(params.source, lambda_event_sources.SqsEventSource):
            params.source.queue.grant_consume_messages(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.ApiEventSource):
            params.source.bind(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.S3EventSource):
            params.source.bucket.grant_read(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.DynamoEventSource):
            params.source.bind(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.KinesisEventSource):
            params.source.stream.grant_read(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.SnsEventSource):
            params.source.topic.grant_publish(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.ManagedKafkaEventSource):
            params.source.bind(params.lambda_function)
        elif isinstance(
            params.source, lambda_event_sources.SelfManagedKafkaEventSource
        ):
            params.source.bind(params.lambda_function)
        elif isinstance(params.source, lambda_event_sources.StreamEventSource):
            params.source.bind(params.lambda_function)
