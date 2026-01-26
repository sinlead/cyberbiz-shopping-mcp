"""Client for executing BigQuery operations for Cyberbiz."""

import logging
from typing import Any, Optional

from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError

logger = logging.getLogger(__name__)


class CyberbizBigQueryClient:
    """BigQuery client for Cyberbiz operations with automatic shop_id filtering."""

    def __init__(self, client: bigquery.Client, shop_id: int):
        """
        Initialize Cyberbiz BigQuery client.

        Args:
            client: Shared BigQuery client instance
            shop_id: Shop ID for filtering queries
        """
        self.client = client
        self.shop_id = shop_id

    async def query(self, sql: str, params: Optional[dict[str, Any]] = None) -> list[dict]:
        """
        Execute a SQL query and return results as list of dictionaries.

        Automatically injects shop_id from token into query parameters.
        Handles both SELECT queries (returns rows) and DML statements
        (INSERT/UPDATE/DELETE - returns empty list).

        Args:
            sql: SQL query or statement (use @param_name for parameters)
            params: Optional dictionary of query parameters for safe parameterization
                   Note: shop_id is automatically added from token

        Returns:
            List of dictionaries, where each dict represents a row.
            For DML statements, returns empty list.

        Raises:
            GoogleCloudError: If query execution fails

        Example:
            # SELECT query
            rows = await client.query(
                "SELECT * FROM table WHERE shop_id = @shop_id AND id = @id",
                {"id": 123}
            )

            # DML statement
            await client.query(
                "UPDATE table SET value = @value WHERE shop_id = @shop_id",
                {"value": "new"}
            )
        """
        try:
            logger.info(f"BigQuery executing: {sql[:200]}...")

            params = params or {}
            params["shop_id"] = self.shop_id

            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = self._build_query_parameters(params)
            query_job = self.client.query(sql, job_config=job_config)
            results = query_job.result()
            rows = [dict(row) for row in results]

            logger.info(
                f"BigQuery completed - "
                f"Rows: {len(rows)}, "
                f"DML affected: {query_job.num_dml_affected_rows or 0}, "
                f"Bytes processed: {query_job.total_bytes_processed}, "
                f"Bytes billed: {query_job.total_bytes_billed}"
            )

            return rows

        except GoogleCloudError as e:
            logger.error(f"BigQuery failed: {sql[:200]}... Error: {str(e)}")
            raise

    def _build_query_parameters(self, params: dict[str, Any]) -> list:
        """
        Convert parameter dictionary to BigQuery query parameters.

        Args:
            params: Dictionary of parameter names to values

        Returns:
            List of BigQuery query parameter objects
        """
        query_params = []
        for name, value in params.items():
            # Handle array types
            if isinstance(value, list):
                if value and isinstance(value[0], float):
                    query_params.append(bigquery.ArrayQueryParameter(name, "FLOAT64", value))
                elif value and isinstance(value[0], int):
                    query_params.append(bigquery.ArrayQueryParameter(name, "INT64", value))
                else:
                    query_params.append(bigquery.ArrayQueryParameter(name, "STRING", value))
                continue

            # Handle scalar types
            if isinstance(value, bool):
                param_type = "BOOL"
            elif isinstance(value, int):
                param_type = "INT64"
            elif isinstance(value, float):
                param_type = "FLOAT64"
            elif isinstance(value, str):
                param_type = "STRING"
            else:
                param_type = "STRING"
                value = str(value)

            query_params.append(bigquery.ScalarQueryParameter(name, param_type, value))

        return query_params
