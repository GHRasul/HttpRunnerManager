from django.db import models

'''用户类型表操作'''


class UserTypeManager(models.Manager):
    def insert_user_type(self, user_type):
        self.create(user_type=user_type)

    def insert_type_name(self, type_name):
        self.create(type_name=type_name)

    def insert_type_desc(self, type_desc):
        self.create(type_desc=type_desc)

    def get_objects(self, user_type_id):  # 根据user_type得到一条数据
        return self.get(user_type_id=user_type_id)


'''用户信息表操作'''


class UserInfoManager(models.Manager):
    def insert_user(self, username, password, email, object):
        self.create(username=username, password=password, email=email, user_type=object)

    def query_user(self, username, password):
        return self.filter(username__exact=username, password__exact=password).count()


'''项目信息表操作'''


class ProjectInfoManager(models.Manager):
    def insert_project(self, pro_name, responsible_name, test_user, dev_user, publish_app, simple_desc, other_desc):
        self.create(pro_name=pro_name, responsible_name=responsible_name, test_user=test_user, dev_user=dev_user
                    , publish_app=publish_app, simple_desc=simple_desc, other_desc=other_desc)

    def update_project(self, id, pro_name, responsible_name, test_user, dev_user, publish_app, simple_desc, other_desc):
        obj = self.get(id=int(id))
        obj.pro_name = pro_name
        obj.responsible_name = responsible_name
        obj.test_user = test_user
        obj.dev_user = dev_user
        obj.publish_app = publish_app
        obj.simple_desc = simple_desc
        obj.other_desc = other_desc

        obj.save()

    def get_pro_name(self, pro_name, type=True, id=None):
        if type:
            return self.filter(pro_name__exact=pro_name).count()
        else:
            if id is not None:
                return self.get(id=int(id)).pro_name
            return self.get(pro_name__exact=pro_name)

    def get_pro_info(self, type=True):
        if type:
            return self.all().values('pro_name')
        else:
            return self.all()


'''模块信息表操作'''


class ModuleInfoManager(models.Manager):
    def insert_module(self, module_name, belong_project, test_user, lifting_time, simple_desc, other_desc):
        self.create(module_name=module_name, belong_project=belong_project, test_user=test_user,
                    lifting_time=lifting_time,
                    simple_desc=simple_desc, other_desc=other_desc)

    def update_module(self, id, module_name, test_user, lifting_time, simple_desc, other_desc):
        obj = self.get(id=int(id))
        obj.module_name = module_name
        obj.test_user = test_user
        obj.lifting_time = lifting_time
        obj.simple_desc = simple_desc
        obj.other_desc = other_desc

        obj.save()

    def get_module_name(self, module_name, type=True, id=None, project=None):
        if type:
            return self.filter(module_name__exact=module_name).count()
        else:
            if id is not None:
                return self.get(id=int(id)).module_name
            return self.get(belong_project__pro_name__exact=project, module_name__exact=module_name)

    def get_module_info(self, belong_project):
        return self.filter(belong_project__pro_name__exact=belong_project).values_list('module_name',
                                                                                       flat=True).order_by(
            '-create_time')


'''用例信息表操作'''


class TestCaseInfoManager(models.Manager):
    def insert_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        self.create(name=kwargs.get('test').get('name'), belong_project=case_info.pop('project'),
                    belong_module=belong_module,
                    author=case_info.pop('author'), include=case_info.pop('include'), request=kwargs)

    def update_case(self, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        obj = self.get(id=int(case_info.pop('test_index')))
        obj.name = kwargs.get('test').get('name')
        obj.author = case_info.pop('author')
        obj.include = case_info.pop('include')
        obj.request = kwargs
        obj.save()

    def insert_config(self, belong_module, **kwargs):
        config_info = kwargs.get('config').pop('config_info')
        self.create(name=kwargs.get('config').get('name'), belong_project=config_info.pop('project'),
                    belong_module=belong_module,
                    author=config_info.pop('config_author'), type=2, request=kwargs)

    def update_config(self, **kwargs):
        config_info = kwargs.get('config').pop('config_info')
        obj = self.get(id=int(config_info.pop('test_index')))
        obj.name = kwargs.get('config').get('name')
        obj.author = config_info.pop('config_author')
        obj.request = kwargs
        obj.save()

    def get_case_name(self, name, module_name, belong_project):
        return self.filter(belong_module__module_name=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).count()

    def get_case_by_id(self, index, type=True):
        if type:
            return self.filter(id=index).all()
        else:
            return self.get(id=index).name
