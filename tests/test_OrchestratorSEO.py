import azure.durable_functions as df
from OrchestratorSEO import orchestrator_function


def test_orchestrator_function():
    input_dict = {"test": "test"}
    context = df.DurableOrchestrationContext(df.DurableOrchestrationContext.create_default())
    context.set_input(input_dict)
    result = orchestrator_function(context)
    assert result == "ok!"