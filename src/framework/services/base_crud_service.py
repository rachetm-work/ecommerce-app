class BaseCrudService:

    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session

    def get_all(self):
        return self.db_session.query(self.model).all()

    def create(self, resource):
        db_item = self.model(**resource.model_dump())
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)
        return db_item
