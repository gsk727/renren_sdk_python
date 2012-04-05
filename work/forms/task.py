#-*- coding: utf-8 -*-
from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField, equal_to, ValidationError, SubmitInput,\
        SelectField, TextAreaField
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB
import time


db = getDB("app")
class TaskForm(Form):
    """
    显示的属性少一个配置
    """
    number = TextField(_(u"任务编号"), validators=[
                            required(message=_(u"有木有")), ])
    name = TextField(_(u"任务主题"), validators=[
                        required(message=_(u"必须的")), ])
    attach = TextField(_(u"附件"))
    des = TextField(_(u"任务说明"))
    createDate = TextField(_(u"任务创建日期"))
    begin = TextField(_(u"任务开始日期"))
    end = TextField(_(u"任务结束日期"))
    status = TextField(_(u"任务状态"))
    owner = TextField(_(u"任务所有者"))
    remark = TextField(_(u"备注"))
    content = TextAreaField(_(u"评论"))
    next = HiddenField()

    def validate_number(self, field):
        """
        验证唯一性
        """
        res = db.base.find_one({"number": field.data })
        if res is not None > 0:
            raise ValidationError, gettext(u"这个可以不重复的，在该一该吧！")


    def validate_createDate(self, field):
        field.data = time.strftime("%Y/%n/%d")

    def validata_status(self, field):
        field.data = len(field.data) > 0 or field.data and "1-free"

    def asDict(self):
        """比较不好的做法，数据产生拷贝了
        """
        return dict([(k, self[k].data) for k in self.showAttributes])


class HiddenTextField(TextField):
    def __init__(self, *args, **kwargs):
        super(HiddenTextField, self).__init__(*args, **kwargs)


    def __call__(self, **kwargs):
        kwargs.update({"type":"hidden"})
        return super(HiddenTextField, self).__call__(**kwargs)


class TaskUpdateForm(TaskForm):
    """属性的名字和数据库的key是一致的，
    如果有按钮总是submit, showAttribes 在html显示的属性
    """
    showAttributes = ["number", "name", "des", "createDate", "begin", "end", "status",
                        "owner", "remark"]

    button = SubmitField(_(u"更新"))
    submit = lambda this, **x: this.button(id="updateBtnOK", **x)
    number = HiddenTextField(_(""))    # 这个比较特殊, 快要疯了
    city = TextField(_(u"基地所在城市"))
    myID = "frmUpdate"  # 这么解决少看点代码或文档


    def __init__(self):
        super(TaskUpdateForm, self).__init__()


    def validate_number(self,  field):
        """
        验证唯一性
        """
        res = db.base.find_one({"number": field.data })
        print res
        if res is None:
            raise ValidationError, gettext(u"请更新存在的记录")


class TaskAddForm(TaskForm):
    showAttributes = ["number", "name", "des", "createDate", "begin", "end", "status",
                        "owner", "remark"]

    button = SubmitField(_(u"添加"))
    submit = lambda this, **x: this.button(id="addBtnOK", **x)
    myID = "frmAdd"


    def validate_name(self, field):
        res =  db.base.find_one({"name": field.data })
        if res is not None:
            raise ValidationError, gettext(u"这个可以不重复的，在该一该吧！")


    def __init__(self):
        super(TaskAddForm, self).__init__(id ="frmAdd")

class FormProxy(object):
    def asDict(self):
         return dict([(k, self[k].data) for k in self.showAttributes])

    def __init__(self, form):
        self.form = form        # 考虑弱引用
    def __getitem__(self, k):
        if k not in self.showAttributes:
            raise AttributeError("%s"%(k,))
        try:
            return getattr(self, k)
        except:
            return getattr(self.form, k)
    def __getattr__(self, k):
        return self.__getitem__(k)

class TaskShow(FormProxy):
    showSimpleAttr = ["number", "name", "des",  "status", "owner"] # 简单视图属性
    showAttributes = ["number", "name", "des", "createDate", "begin", "end", "status",
                        "owner", "remark"]
    def __init__(self, form):
        super(TaskShow, self).__init__(form)

class TaskMoveForm(Form):
    def asDict(self):
         return dict([(k, self[k].data) for k in self.showAttributes])
    showAttributes = ["owner", "remark"]
    stuffs = db.user.find({}, {"_id":0, "name":1, "email":1})
    owner = SelectField(_(u"移交员工"), choices=[(s.get("name", ""), s.get("email", "")) for s in stuffs])
    remark = TextAreaField(_(u"备注"))
    submit = SubmitField(_(u"更新"))
    myID = "taskmove"


class TaskContentForm(Form):
    next = HiddenField()
    showAttributes = ["content", ]
    mycontent = TextAreaField(_(u"评论"))
    content = lambda this, **x: x.update() or  this.mycontent(**x)
    submit = SubmitField(_(u"评论"))
    def __init__(self):
        super(TaskContentForm, self).__init__()

    def asDict(self):
        return dict([("content", self["mycontent"].data),])

