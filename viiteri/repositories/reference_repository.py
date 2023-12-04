""" viiteri/repositories/reference_repository.py """
from sqlalchemy.sql import text

from viiteri.entities.references import Reference
from viiteri.utils.reference_factory import ReferenceFactory
from viiteri.utils.db import db


class ReferenceRepository:
    """Handles the reference database."""

    def __init__(self, connection):
        self._connection = connection

    def add_reference(self, reference: Reference):
        """Adds a new reference to the database."""
        cursor = self._connection.session()
        cursor.execute(text(
            'insert into reference_table (content) values (:content);'),
            {"content": str(reference)}
        )
        cursor.commit()
        return reference

    def get_all_references(self) -> list[(int, Reference)]:
        """Gets all references from the database"""
        cursor = self._connection.session()
        result = cursor.execute(text(
            'select id, content from reference_table;'
        ))
        references = [(content[0], ReferenceFactory.from_str(
            content[1])) for content in result.fetchall()]
        return references

    def delete_all(self):
        """Empties whole database"""
        cursor = self._connection.session()
        cursor.execute(text('delete from reference_table'))
        cursor.commit()


reference_repository = ReferenceRepository(db)
