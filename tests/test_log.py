from clixon.log import get_log_factory
import logging


def test_log():
    logger = get_log_factory()

    assert logger.name == "pyserver"
    assert logger.level == logging.INFO
    assert logger.hasHandlers() is True


def test_log_stdout():
    logger = get_log_factory(output="stdout")

    assert logger.name == "pyserver"
    assert logger.level == logging.INFO
    assert logger.hasHandlers() is True

    assert logger.info("test") is None
    assert logger.debug("test") is None


def test_log_debug():
    logger = get_log_factory(debug=True)

    assert logger.name == "pyserver"
    assert logger.level == logging.DEBUG
    assert logger.hasHandlers() is True

    assert logger.info("test") is None
    assert logger.debug("test") is None
