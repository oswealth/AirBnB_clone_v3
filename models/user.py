#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            kwargs['password'] = self._hash_password(kwargs['password'])
        super().__init__(*args, **kwargs)

    def _hash_password(self, password):
        """Hashes the user password"""
        return hashlib.md5(password.encode()).hexdigest()

    def set_password(self, password):
        """Sets the user's password, hashing it in the process"""
        self.password = self._hash_password(password)

    def to_dict(self, save_to_disk=False):
        """Converts the object to a dictionary"""
        user_dict = super().to_dict(save_to_disk=save_to_disk)
        return user_dict
