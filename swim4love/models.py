from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from swim4love import app, db, login_manager


class Swimmer(db.Model):
    '''Model for the swimmers table.'''

    __tablename__ = 'swimmers'

    # TODO(thomas): this should be changed to also include swim time & year group
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    laps = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Swimmer #{:03d} {!r}>'.format(self.id, self.name)


class Volunteer(db.Model, UserMixin):
    '''Model for volunteer or administrator user.'''

    __tablename__ = 'volunteers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # I think it's good to keep it unordered
    # so that the newly added swimmers are at the bottom
    swimmers = db.relationship('Swimmer', secondary='volunteer_swimmers') # , order_by='Swimmer.id')

    def __repr__(self):
        return '<Volunteer #{} {!r}>'.format(self.id, self.username)


class VolunteerSwimmers(db.Model):
    '''Association table between a volunteer and the swimmers he/she manages.'''

    __tablename__ = 'volunteer_swimmers'

    id = db.Column(db.Integer(), primary_key=True)
    volunteer_id = db.Column(db.Integer(), db.ForeignKey('volunteers.id', ondelete='CASCADE'))
    swimmer_id = db.Column(db.Integer(), db.ForeignKey('swimmers.id', ondelete='CASCADE'))


db.create_all() # Create tables using the above configuration


@login_manager.user_loader
def load_user(user_id):
    return Volunteer.query.get(int(user_id))


Volunteer.query.filter_by(username='admin').delete()
master_admin = Volunteer(username='admin',
                         password=generate_password_hash(app.secret_key, 'sha256'),
                         is_admin=True)
db.session.add(master_admin)
db.session.commit()
