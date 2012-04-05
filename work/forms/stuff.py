#-*- coding: utf-8 -*-
from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField, equal_to, ValidationError, SubmitInput, email
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB


db = getDB("app")
class StuffForm(Form):
    number = TextField(_(u"员工编号"), validators=[
                            required(message=_(u"有木有")), ])
    email = TextField(_(u"邮件"), validators=[
                        email(message=_(u"需要邮件地址")),  ])
    name = TextField(_(u"名字"), validators=[
                        required(message=_(u"必须的")), ])
    departion = TextField(_(u"部门"))               # 部门
    role = TextField(_(u"职位"))                       #  职位
    duty = TextField(_(u"任务"))                      #  职位
    des = TextField(_(u"描述信息"))
    info = TextField(_(u"乱七八糟"))                # 乱七八的信息，更具需要补充
    next = HiddenField()
    
    def validate_number(self, field):
        """
        验证唯一性
        """
        res = db.base.find_one({"number": field.data })
        if res is not None > 0:
            raise ValidationError,  gettext(u"这个可以不重复的，在该一该吧！")


    def asDict(self):
        """比较不好的做法，数据产生拷贝了
        """
        return dict([(k, self[k].data) for k in self.showAttributes if "noneInput" not in k])


class HiddenTextField(TextField):
    def __init__(self, *args, **kwargs):
        super(HiddenTextField, self).__init__(*args, **kwargs)

    def __call__(self, **kwargs):
        kwargs.update({"type":"hidden"})
        return super(HiddenTextField, self).__call__(**kwargs)


class StuffUpdateForm(StuffForm):
    """属性的名字和数据库的key是一致的
    如果有按钮总是submit, showAttribes 在html显示的属性, noneInput 纯属站位和显示的对其
    """
    showAttributes = ["number", "email", 'name', "noneInput", "noneInput", 'departion', 'role' , 'duty', "info", "des"]
    button = SubmitField(_(u"更新"))
    submit = lambda this, **x: this.button(id="updateBtnOK", **x)
    noneInput = HiddenTextField()
    number = HiddenTextField(_(""))    # 这个比较特殊, 快要疯了
    myID = "frmUpdate"  # 这么解决少看点代码或文档

    def __init__(self):
        super(StuffUpdateForm, self).__init__()

    def validate_number(self,  field):
        """
        验证唯一性
        """
        print "validate_number", field.data
        res = db.user.find_one({"number": field.data })
        print res
        if res is None:
            raise ValidationError, gettext(u"请更新存在的记录")


class StuffAddForm(StuffForm):
    showAttributes = ["number", "email", 'name', "inDate", "outDate", 'departion', 'role' , 'duty', "info", "des"]
    inDate = TextField(_(u"入职日期"))
    outDate = TextField(_(u"离职日期"))
    button = SubmitField(_(u"添加"))
    submit = lambda this, **x: this.button(id="addBtnOK", **x)
    myID = "frmAdd"

    def validate_name(self, field):
        res =  db.base.find_one({"name": field.data })
        if res is not None:
            raise ValidationError, gettext(u"这个可以不重复的，在该一该吧！")


    def __init__(self):
        super(StuffAddForm, self).__init__(id ="frmAdd")
