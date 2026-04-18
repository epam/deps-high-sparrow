from uuid import uuid4

import factory

from deps_high_sparrow.domain import DocumentType

__all__ = ["DocumentTypeFactory"]


class DocumentTypeFactory(factory.Factory):
    class Meta:
        model = DocumentType

    id_ = factory.LazyFunction(lambda: uuid4().hex)
    tenant_id = factory.LazyFunction(lambda: uuid4().hex)
