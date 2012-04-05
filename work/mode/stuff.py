#-*- coding: utf-8 -*-
import re
from mode import Mode


class StuffMode(Mode):
    _cName = "user"
    database = "app"
    keys=("email", )
    attributes = ["number", "email", 'name', "inDate", "outDate", 'departion', 'role' , 'duty', "info", "des"]

    def __init__(self):
        super(StuffMode, self).__init__()


    def compileQuery(self):
        """
        virtual 
        """
        email = self.doc["email"]  # :)
        p = re.compile(email, re.IGNORECASE)
        return {"email": p}
        
 
