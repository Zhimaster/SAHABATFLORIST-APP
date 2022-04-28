from . import db
from .models import Menu
from sqlalchemy.orm import aliased

def load_menu(usr_grp):
    Menu2 = aliased(Menu)
    subq = (db.session.query(db.func.count())
            .filter(Menu2.parent_menu==Menu.menu_code, Menu2.user_group==Menu.user_group)
            .label('child_count'))
    menus = (db.session.query(Menu.menu_code, Menu.menu_caption, Menu.menu_order, Menu.parent_menu, subq.label('child_count'))
            .filter(Menu.user_group==usr_grp,Menu.active_flag==True)
            .order_by(Menu.menu_order)
            .all())
    
    return menus

def get_data_scalar_by_id(Tbl, arg_col, key):
        x = str(Tbl.__name__).lower()           
        result = (db.session.query(getattr(Tbl, arg_col))
                .filter(getattr(Tbl, x+'_id')==key)
                .scalar())
        return result

def get_subq(Tbl, type, key):
        """Function to get id/code/name as SUBQUERY from Master Class
           if type is 'code / name' the key should be it's id
           and if type is 'id' the key should be the code
           
        Args:
                Tbl (Obj): Object Class of the Models
                type (String): String of id / code / name
                key (integer/string): Integer/String of the key to find the type

        Returns:
                Obj : Object as subquery.
        """
        x = str(Tbl.__name__).lower()
        if type == 'code':            
                result = (db.session.query(getattr(Tbl, x+'_code'))
                        .filter(getattr(Tbl, x+'_id')==key)
                        .label(x+'_'+type))
        elif type == 'id':
                result = (db.session.query(getattr(Tbl, x+'_id'))
                        .filter(getattr(Tbl, x+'_code')==key)
                        .label(x+'_'+type))
        else:
                result = (db.session.query(getattr(Tbl, x+'_name'))
                        .filter(getattr(Tbl, x+'_id')==key)
                        .label(x+'_'+type))
        return result