#-*- coding: utf-8 -*-

from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField, equal_to

from flaskext.babel import gettext, lazy_gettext as _

class LoginForm(Form):
    username = TextField(_(u"电子邮件"), validators=[
                        required(message=_(u"必须的")), ])
 
    password = PasswordField(_(u"密码"))
    remember = BooleanField(_(u"记住密码"))

    next = HiddenField()
    submit = SubmitField(_(u"登录"))

class EditPasswordForm(Form):
    originPassword = PasswordField(_(u"老密码"), validators=[
                                                       required(message=_(u"密码不能空"))])
    
    newPassword = PasswordField(_(u"新密码"), validators=[
                                                    required(message=_(u"密码真不能空"))])
    
    rePassword = PasswordField(_(u"再来一遍"), validators=[
                                                    equal_to("newPassword",  message=_(u"错了咋办")), ])
    
    submit  = SubmitField(_(u"提交"))

