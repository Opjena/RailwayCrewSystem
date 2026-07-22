"""
BaseRepository — Generic CRUD for all models.

All repositories must inherit from this to avoid duplicating
create / get_by_id / get_all / update / soft_delete / exists logic.
"""

from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing standard database operations.

    Usage:
        class MyRepository(BaseRepository[MyModel]):
            def __init__(self, db: Session):
                super().__init__(db, MyModel)
    """

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    def create(self, **kwargs) -> ModelType:
        """Create and return a new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Return a single record by primary key, or None."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
        sort: str = "id",
        order: str = "asc",
        search: Optional[str] = None,
        search_fields: Optional[list[str]] = None,
    ) -> Sequence[ModelType]:
        """
        Return a list of records with optional filtering, sorting, and
        keyword search.

        Parameters
        ----------
        skip : int           Number of records to skip (pagination).
        limit : int          Maximum records to return.
        filters : dict       Column=value pairs for exact-match filtering.
        sort : str           Column name to sort by.
        order : str          "asc" or "desc".
        search : str | None  Keyword to search across *search_fields*.
        search_fields : list Columns to search when *search* is provided.
        """
        query = self.db.query(self.model)

        # --- exact-match filters -------------------------------------------
        if filters:
            for col, val in filters.items():
                if hasattr(self.model, col) and val is not None:
                    query = query.filter(getattr(self.model, col) == val)

        # --- keyword search ------------------------------------------------
        if search and search_fields:
            from sqlalchemy import or_

            conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    conditions.append(
                        getattr(self.model, field).ilike(f"%{search}%")
                    )
            if conditions:
                query = query.filter(or_(*conditions))

        # --- sorting --------------------------------------------------------
        sort_col = getattr(self.model, sort, self.model.id)
        order_fn = asc if order.lower() == "asc" else desc
        query = query.order_by(order_fn(sort_col))

        # --- pagination ----------------------------------------------------
        return query.offset(skip).limit(limit).all()

    def count(
        self,
        *,
        filters: Optional[dict[str, Any]] = None,
        search: Optional[str] = None,
        search_fields: Optional[list[str]] = None,
    ) -> int:
        """Return the total count of records matching the given criteria."""
        query = self.db.query(self.model)

        if filters:
            for col, val in filters.items():
                if hasattr(self.model, col) and val is not None:
                    query = query.filter(getattr(self.model, col) == val)

        if search and search_fields:
            from sqlalchemy import or_

            conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    conditions.append(
                        getattr(self.model, field).ilike(f"%{search}%")
                    )
            if conditions:
                query = query.filter(or_(*conditions))

        return query.count()

    def exists(self, **filters) -> bool:
        """Return True if at least one record matches the given filters."""
        query = self.db.query(self.model)
        for col, val in filters.items():
            if hasattr(self.model, col):
                query = query.filter(getattr(self.model, col) == val)
        return query.first() is not None

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Apply attribute changes and commit."""
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    # ------------------------------------------------------------------
    # Soft Delete  (sets is_active = False)
    # ------------------------------------------------------------------
    def soft_delete(self, instance: ModelType) -> ModelType:
        """Mark a record as inactive instead of deleting it."""
        if hasattr(instance, "is_active"):
            setattr(instance, "is_active", False)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    # ------------------------------------------------------------------
    # Hard Delete
    # ------------------------------------------------------------------
    def hard_delete(self, instance: ModelType) -> None:
        """Remove a record permanently."""
        self.db.delete(instance)
        self.db.commit()


