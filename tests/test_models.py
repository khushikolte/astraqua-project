import torch
from models.scenario_model import ScenarioModel


def test_model_output_shape():
    model = ScenarioModel()
    model.eval()

    # Create a random fleet state
    x = torch.rand(1, 32)

    with torch.no_grad():
        output = model(x)

    assert output.shape == (1, 8)


def test_model_output_range():
    model = ScenarioModel()
    model.eval()

    x = torch.rand(1, 32)

    with torch.no_grad():
        output = model(x)

    # Sigmoid outputs should always be between 0 and 1
    assert torch.all(output >= 0)
    assert torch.all(output <= 1)


def test_batch_inference():
    model = ScenarioModel()
    model.eval()

    # Simulate a batch of 16 fleets
    x = torch.rand(16, 32)

    with torch.no_grad():
        output = model(x)

    assert output.shape == (16, 8)


def test_no_nan_values():
    model = ScenarioModel()
    model.eval()

    x = torch.rand(10, 32)

    with torch.no_grad():
        output = model(x)

    assert not torch.isnan(output).any()


def test_model_forward_pass_speed():
    import time

    model = ScenarioModel()
    model.eval()

    x = torch.rand(1, 32)

    start = time.perf_counter()

    with torch.no_grad():
        model(x)

    elapsed_ms = (time.perf_counter() - start) * 1000

    # Should be far under the API target
    assert elapsed_ms < 10
    