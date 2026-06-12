import numpy as np

from app.model import get_session


def test_model_prediction_shape():
    session = get_session()

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    dummy_input = np.random.rand(1, 3, 224, 224).astype(np.float32)
    prediction = session.run([output_name], {input_name: dummy_input})

    assert prediction[0].shape[0] == 1
