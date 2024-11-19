"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import bcrypt
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User

salt = bcrypt.gensalt(12)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, password: str):
        """Add new user to DB
        """
        if email and password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            user = User()
            user.hashed_password = hashed_password
            user.email = email
            self._session.add(user)
            self._session.commit()
            return user

    def find_user_by(self, **kwargs):
        """Find a user by id"""
        for key, value in kwargs.items():
            if not hasattr(User, key) or key == 'password':
                raise InvalidRequestError

        query = self._session.query(User).filter_by(**kwargs)
        user = query.first()

        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: str, **kwargs):
        """Update a user"""
        user = self.find_user_by(id=user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError

            self._session.commit()
            return None
