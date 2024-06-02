from typing import List
from sqlalchemy.orm import Session
from .schemas import Library, NewLibraryParam, Folder, NewEntityParam, Entity, Plugin, NewPluginParam, UpdateEntityParam
from .models import LibraryModel, FolderModel, EntityModel, EntityModel, PluginModel, LibraryPluginModel


def get_library_by_id(library_id: int, db: Session) -> Library | None:
    return db.query(LibraryModel).filter(LibraryModel.id == library_id).first()


def create_library(library: NewLibraryParam, db: Session) -> Library:
    db_library = LibraryModel(name=library.name)
    db.add(db_library)
    db.commit()
    db.refresh(db_library)

    for folder_path in library.folders:
        db_folder = FolderModel(path=str(folder_path), library_id=db_library.id)
        db.add(db_folder)

    db.commit()
    return Library(
        id=db_library.id,
        name=db_library.name,
        folders=[Folder(id=db_folder.id, path=db_folder.path) for db_folder in db_library.folders],
        plugins=[]
    )


def get_libraries(db: Session) -> List[Library]:
    return db.query(LibraryModel).all()


def create_entity(library_id: int, entity: NewEntityParam, db: Session) -> Entity:
    db_entity = EntityModel(
        **entity.model_dump(),
        library_id=library_id
    )
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_entity_by_id(entity_id: int, db: Session) -> Entity | None:
    return db.query(EntityModel).filter(EntityModel.id == entity_id).first()


def get_entity_by_filepath(filepath: str, db: Session) -> Entity | None:
    return db.query(EntityModel).filter(EntityModel.filepath == filepath).first()


def create_plugin(newPlugin: NewPluginParam, db: Session) -> Plugin:
    db_plugin = PluginModel(**newPlugin.model_dump(mode='json'))
    db.add(db_plugin)
    db.commit()
    db.refresh(db_plugin)
    return db_plugin


def add_plugin_to_library(library_id: int, plugin_id: int, db: Session):
    library_plugin = LibraryPluginModel(library_id=library_id, plugin_id=plugin_id)
    db.add(library_plugin)
    db.commit()
    db.refresh(library_plugin)


def get_entity_by_id(entity_id: int, db: Session) -> Entity | None:
    return db.query(EntityModel).filter(EntityModel.id == entity_id).first()


def update_entity(entity_id: int, updated_entity: UpdateEntityParam, db: Session) -> Entity:
    db_entity = get_entity_by_id(entity_id, db)
    for key, value in updated_entity.model_dump().items():
        setattr(db_entity, key, value)
    db.commit()
    db.refresh(db_entity)
    return db_entity