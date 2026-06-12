from app.model import get_session


def test_model_loads_successfully():
    session = get_session()

    assert session is not None
    assert len(session.get_inputs()) >= 1
    assert len(session.get_outputs()) >= 1
