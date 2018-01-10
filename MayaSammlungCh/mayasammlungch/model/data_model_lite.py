""" katalog data model """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import Column, ForeignKey, Integer, String, Binary

Model = declarative_base()


class Department(Model):
    """ Department data object """
    __tablename__ = 'departments'

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}".format(self.name)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    villages = relationship("Village", back_populates="department")


class LangGroup(Model):
    """ LangGroup data object """
    __tablename__ = 'lang_groups'

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}".format(self.name)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    villages = relationship("Village", back_populates="lang_group")


class Village(Model):
    """ Village data object """
    __tablename__ = 'villages'

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.department, self.lang_group)

    def __repr__(self):
        return "{}".format(self.name)

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", uselist=False, back_populates="villages")

    lang_group_Id = Column(Integer, ForeignKey('lang_groups.id'))
    lang_group = relationship("LangGroup", uselist=False, back_populates="villages")

    objects = relationship("Object", back_populates="village")

    @hybrid_property
    def categories(self):
        return list(set(map(lambda o: o.categroy.name, self.objects)))


class Category(Model):
    """ Category data object """
    __tablename__ = 'categories'

    @hybrid_method
    def __str__(self):
        return "{} <- {}".format(self.parent_category, self.name)\
            if self.name != "Root" else "{}".format(self.name)

    @hybrid_method
    def __repr__(self):
        return "{}".format(self.name)

    @hybrid_method
    def __eq__(self, other):
        direct = str(other) in str(self)
        recursive = self.parent_category == other if self.name != "Root" else False
        return direct or recursive

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    parent_category_id = Column(Integer, ForeignKey('categories.id'))
    parent_category = relationship("Category",
                                   back_populates="child_categories",
                                   remote_side='Category.id')

    child_categories = relationship("Category", back_populates="parent_category")

    objects = relationship("Object", back_populates="category")

    @hybrid_property
    def sub_categories(self):
        """ subcategories getter """
        uks = []
        for uk_ in self.child_categories:
            if uk_.Name != "Root":
                uks.append(uk_)
            for suk in uk_.sub_categories:
                uks.append(suk)

        return uks

    @hybrid_property
    def villages(self):
        return list(set(map(lambda o: o.village, self.objects)))

class Object(Model):
    """ Object data object """
    __tablename__ = 'objects'

    def __str__(self):
        return self.object_number

    def __repr__(self):
        return self.object_number

    id = Column(Integer, primary_key=True)

    object_number = Column(String(200), nullable=False)
    object_name = Column(String(200), nullable=False)

    description_craft = Column(String(2000), nullable=False)
    description_material = Column(String(2000), nullable=False)

    date = Column(String(500), nullable=False)
    measure = Column(String(500), nullable=False)
    condition = Column(String(500), nullable=False)
    origin = Column(String(500), nullable=False)

    more = Column(String(200), nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", uselist=False, back_populates="objects")

    village_id = Column(Integer, ForeignKey('villages.id'))
    village = relationship("Village", uselist=False, back_populates="objects")

    pictures = relationship("Picture", back_populates="object")

    @hybrid_property
    def pic_paths(self):
        return [p.original_path for p in self.pictures]
    
    @hybrid_property
    def thumbnail(self):
        """ thumbnail getter """
        return self.pictures[0]


class Picture(Model):
    """ Picture data object """
    __tablename__ = 'pictures'

    def __str__(self):
        return self.original_path

    def __repr__(self):
        return self.original_path

    id = Column(Integer, primary_key=True)

    original_path = Column(String(100), nullable=False)

    object_id = Column(Integer, ForeignKey('objects.id'))
    object = relationship("Object", back_populates="pictures")

    data = deferred(Column(Binary))

    @hybrid_property
    def b64_data(self):
        """ image data getter """
        if self.data is not None:
            b64 = self.data.encode("base64")
        else:
            b64 = None
        return 'data:image/png;base64,{}'.format(b64) if b64 is not None else ''

    @hybrid_property
    def image_tag(self):
        """ image tag getter """
        b64 = self.data.encode("base64")
        return '<img alt="Embedded Image" src="data:image/png;base64,{}" />'.format(b64)

