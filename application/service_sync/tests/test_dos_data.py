from datetime import date, time
from os import environ
from unittest.mock import call, MagicMock, patch

from aws_lambda_powertools.logging import Logger
from pytest import raises

from application.common.opening_times import OpenPeriod, SpecifiedOpeningTime
from application.service_sync.dos_data import (
    get_dos_service_and_history,
    run_db_health_check,
    save_demographics_into_db,
    save_specified_opening_times_into_db,
    save_standard_opening_times_into_db,
    update_dos_data,
)

FILE_PATH = "application.service_sync.dos_data"


@patch(f"{FILE_PATH}.add_metric")
@patch(f"{FILE_PATH}.put_circuit_is_open")
@patch.object(Logger, "info")
@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db_replica")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_run_db_health_check_success(
    mock_connect_to_dos_db: MagicMock,
    mock_connect_to_dos_db_replica: MagicMock,
    query_dos_db: MagicMock,
    mock_logger: MagicMock,
    mock_put_circuit_is_open: MagicMock,
    mock_add_metric: MagicMock,
):
    # Arrange
    environ["CIRCUIT"] = circuit = "dos"
    query_dos_db.return_value.fetchall.return_value = ["test"]
    # Act
    run_db_health_check()
    # Assert
    mock_logger.assert_has_calls(
        [call("Running health check"), call("DoS database is running"), call("DoS database replica is running")]
    )
    mock_connect_to_dos_db.assert_called_once()
    mock_connect_to_dos_db_replica.assert_called_once()
    mock_put_circuit_is_open.assert_called_once_with(circuit, False)
    mock_add_metric.assert_called_once_with("ServiceSyncHealthCheckSuccess")
    # Cleanup
    del environ["CIRCUIT"]


@patch(f"{FILE_PATH}.add_metric")
@patch(f"{FILE_PATH}.put_circuit_is_open")
@patch.object(Logger, "error")
@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db_replica")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_run_db_health_check_db_failure(
    mock_connect_to_dos_db: MagicMock,
    mock_connect_to_dos_db_replica: MagicMock,
    query_dos_db: MagicMock,
    mock_logger: MagicMock,
    mock_put_circuit_is_open: MagicMock,
    mock_add_metric: MagicMock,
):
    # Arrange
    query_dos_db.return_value.fetchall.return_value = []
    # Act
    run_db_health_check()
    # Assert
    mock_logger.assert_has_calls([call("Health check failed - No services found in DoS DB")])
    mock_connect_to_dos_db.assert_called_once()
    mock_connect_to_dos_db_replica.assert_not_called()
    mock_put_circuit_is_open.assert_not_called()
    mock_add_metric.assert_called_once_with("ServiceSyncHealthCheckFailure")


@patch(f"{FILE_PATH}.add_metric")
@patch(f"{FILE_PATH}.put_circuit_is_open")
@patch.object(Logger, "error")
@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db_replica")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_run_db_health_check_db_replica_failure(
    mock_connect_to_dos_db: MagicMock,
    mock_connect_to_dos_db_replica: MagicMock,
    query_dos_db: MagicMock,
    mock_logger: MagicMock,
    mock_put_circuit_is_open: MagicMock,
    mock_add_metric: MagicMock,
):
    # Arrange
    query_dos_db.return_value.fetchall.side_effect = ["test", []]
    # Act
    run_db_health_check()
    # Assert
    mock_logger.assert_has_calls([call("Health check failed - No services found in DoS DB Replica")])
    mock_connect_to_dos_db.assert_called_once()
    mock_connect_to_dos_db_replica.assert_called_once()
    mock_put_circuit_is_open.assert_not_called()
    mock_add_metric.assert_called_once_with("ServiceSyncHealthCheckFailure")


@patch(f"{FILE_PATH}.add_metric")
@patch(f"{FILE_PATH}.put_circuit_is_open")
@patch.object(Logger, "exception")
@patch(f"{FILE_PATH}.connect_to_dos_db_replica")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_run_db_health_check_exception(
    mock_connect_to_dos_db: MagicMock,
    mock_connect_to_dos_db_replica: MagicMock,
    mock_logger: MagicMock,
    mock_put_circuit_is_open: MagicMock,
    mock_add_metric: MagicMock,
):
    # Arrange
    mock_connect_to_dos_db.side_effect = Exception("test")
    # Act
    run_db_health_check()
    # Assert
    mock_logger.assert_has_calls([call("Health check failed")])
    mock_connect_to_dos_db.assert_called_once()
    mock_connect_to_dos_db_replica.assert_not_called()
    mock_put_circuit_is_open.assert_not_called()
    mock_add_metric.assert_called_once_with("ServiceSyncHealthCheckFailure")


@patch(f"{FILE_PATH}.ServiceHistories")
@patch(f"{FILE_PATH}.get_specified_opening_times_from_db")
@patch(f"{FILE_PATH}.get_standard_opening_times_from_db")
@patch(f"{FILE_PATH}.DoSService")
@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_get_dos_service_and_history(
    mock_connect_to_dos_db: MagicMock,
    mock_query_dos_db: MagicMock,
    mock_dos_service: MagicMock,
    mock_get_standard_opening_times_from_db: MagicMock,
    mock_get_specified_opening_times_from_db: MagicMock,
    mock_service_histories: MagicMock,
):
    # Arrange
    service_id = 12345
    mock_query_dos_db.return_value.fetchall.return_value = [["Test"]]
    # Act
    dos_service, service_history = get_dos_service_and_history(service_id)
    # Assert
    assert mock_dos_service() == dos_service
    mock_get_standard_opening_times_from_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(), service_id=service_id
    )
    mock_get_specified_opening_times_from_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(), service_id=service_id
    )
    assert mock_service_histories() == service_history
    mock_service_histories.return_value.get_service_history_from_db.assert_called_once_with(
        mock_connect_to_dos_db().__enter__()
    )
    mock_service_histories.return_value.create_service_histories_entry.assert_called_once_with()


@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_get_dos_service_and_history_no_match(
    mock_connect_to_dos_db: MagicMock,
    mock_query_dos_db: MagicMock,
):
    # Arrange
    service_id = 12345
    mock_query_dos_db.return_value.fetchall.return_value = []
    # Act
    with raises(ValueError, match=f"Service ID {service_id} not found"):
        get_dos_service_and_history(service_id)
    mock_connect_to_dos_db.assert_called_once()


@patch(f"{FILE_PATH}.query_dos_db")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_get_dos_service_and_history_mutiple_matches(
    mock_connect_to_dos_db: MagicMock,
    mock_query_dos_db: MagicMock,
):
    # Arrange
    service_id = 12345
    mock_query_dos_db.return_value.fetchall.return_value = [["Test"], ["Test"]]
    # Act
    with raises(ValueError, match=f"Multiple services found for Service Id: {service_id}"):
        get_dos_service_and_history(service_id)
    mock_connect_to_dos_db.assert_called_once()


@patch(f"{FILE_PATH}.save_specified_opening_times_into_db")
@patch(f"{FILE_PATH}.save_standard_opening_times_into_db")
@patch(f"{FILE_PATH}.save_demographics_into_db")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_update_dos_data(
    mock_connect_to_dos_db: MagicMock,
    mock_save_demographics_into_db: MagicMock,
    mock_save_standard_opening_times_into_db: MagicMock,
    mock_save_specified_opening_times_into_db: MagicMock,
):
    # Arrange
    change_to_dos = MagicMock()
    service_histories = MagicMock()
    service_id = 1
    # Act
    update_dos_data(change_to_dos, service_id, service_histories)
    # Assert
    mock_save_demographics_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        demographics_changes=change_to_dos.demographic_changes,
    )
    mock_save_standard_opening_times_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        standard_opening_times_changes=change_to_dos.standard_opening_times_changes,
    )
    mock_save_specified_opening_times_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        is_changes=change_to_dos.specified_opening_times_changes,
        specified_opening_times_changes=change_to_dos.new_specified_opening_times,
    )
    service_histories.save_service_histories.assert_called_once_with(connection=mock_connect_to_dos_db().__enter__())
    mock_connect_to_dos_db.return_value.__enter__.return_value.commit.assert_called_once()
    mock_connect_to_dos_db.return_value.__enter__.return_value.close.assert_called_once()


@patch(f"{FILE_PATH}.save_specified_opening_times_into_db")
@patch(f"{FILE_PATH}.save_standard_opening_times_into_db")
@patch(f"{FILE_PATH}.save_demographics_into_db")
@patch(f"{FILE_PATH}.connect_to_dos_db")
def test_update_dos_data_no_changes(
    mock_connect_to_dos_db: MagicMock,
    mock_save_demographics_into_db: MagicMock,
    mock_save_standard_opening_times_into_db: MagicMock,
    mock_save_specified_opening_times_into_db: MagicMock,
):
    # Arrange
    change_to_dos = MagicMock()
    service_histories = MagicMock()
    service_id = 1
    mock_save_demographics_into_db.return_value = False
    mock_save_standard_opening_times_into_db.return_value = False
    mock_save_specified_opening_times_into_db.return_value = False
    # Act
    update_dos_data(change_to_dos, service_id, service_histories)
    # Assert
    mock_save_demographics_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        demographics_changes=change_to_dos.demographic_changes,
    )
    mock_save_standard_opening_times_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        standard_opening_times_changes=change_to_dos.standard_opening_times_changes,
    )
    mock_save_specified_opening_times_into_db.assert_called_once_with(
        connection=mock_connect_to_dos_db().__enter__(),
        service_id=service_id,
        is_changes=change_to_dos.specified_opening_times_changes,
        specified_opening_times_changes=change_to_dos.new_specified_opening_times,
    )
    service_histories.save_service_histories.assert_not_called()
    mock_connect_to_dos_db.return_value.__enter__.return_value.close.assert_called_once()


@patch(f"{FILE_PATH}.query_dos_db")
def test_save_demographics_into_db(mock_query_dos_db: MagicMock):
    # Arrange
    mock_connection = MagicMock()
    service_id = 1
    demographics_changes = {"test": "test"}
    # Act
    response = save_demographics_into_db(mock_connection, service_id, demographics_changes)
    # Assert
    assert True is response
    mock_query_dos_db.assert_called_once_with(
        connection=mock_connection,
        query="UPDATE services SET test = 'test' WHERE id = %(SERVICE_ID)s;",
        vars={"SERVICE_ID": service_id},
    )


def test_save_demographics_into_db_no_changes():
    # Arrange
    mock_connection = MagicMock()
    service_id = 1
    demographics_changes = None
    # Act
    response = save_demographics_into_db(mock_connection, service_id, demographics_changes)
    # Assert
    assert False is response


@patch(f"{FILE_PATH}.query_dos_db")
def test_save_standard_opening_times_into_db(mock_query_dos_db: MagicMock):
    # Arrange
    mock_connection = MagicMock()
    service_id = 1
    open_period = OpenPeriod(time(1, 0, 0), time(2, 0, 0))
    standard_opening_times_changes = {
        1: [open_period],
        2: [open_period],
        3: [open_period],
        4: [open_period],
        5: [open_period],
        6: [open_period],
        7: [open_period],
    }
    # Act
    response = save_standard_opening_times_into_db(mock_connection, service_id, standard_opening_times_changes)
    # Assert
    assert True is response


@patch(f"{FILE_PATH}.query_dos_db")
def test_save_specified_opening_times_into_db(mock_query_dos_db: MagicMock):
    # Arrange
    mock_connection = MagicMock()
    service_id = 1
    open_period_list = [OpenPeriod(time(1, 0, 0), time(2, 0, 0))]
    specified_opening_time_list = [SpecifiedOpeningTime(open_period_list, date(2022, 12, 24), True)]
    # Act
    response = save_specified_opening_times_into_db(mock_connection, service_id, True, specified_opening_time_list)
    # Assert
    assert True is response


@patch(f"{FILE_PATH}.query_dos_db")
def test_save_specified_opening_times_into_db_closed(mock_query_dos_db: MagicMock):
    # Arrange
    mock_connection = MagicMock()
    service_id = 1
    open_period_list = [OpenPeriod(time(1, 0, 0), time(2, 0, 0))]
    specified_opening_time_list = [SpecifiedOpeningTime(open_period_list, date(2022, 12, 24), False)]
    # Act
    response = save_specified_opening_times_into_db(mock_connection, service_id, True, specified_opening_time_list)
    # Assert
    assert True is response
