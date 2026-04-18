from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from deps_high_sparrow.extras.datasource import metadata

__all__ = ["validation_result_table"]


validation_result_table = Table(
    "validation_result",
    metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, nullable=False),
    Column("issues", JSONB, nullable=True),
    Column("cross_field_issues", JSONB, nullable=True),
    UniqueConstraint("id", "tenant_id", name="result_id_tenant_id__ukey"),
)
