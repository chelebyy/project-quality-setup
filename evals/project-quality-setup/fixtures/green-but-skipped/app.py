"""Synthetic reports query; never connect to a live database."""


def count_open_reports(connection):
    return connection.execute(
        "SELECT COUNT(*) FROM reports WHERE state = ?", ("open",)
    ).fetchone()[0]
