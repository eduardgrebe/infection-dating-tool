from django.conf import settings
from django import template
import string

register = template.Library()

def do_has_permission(parser, token):
    nodelist = parser.parse(('end_permission',))
    parser.delete_first_token()
    tag_name, perm_name = token.contents.split(None)
    return HasPermissionNode(nodelist, perm_name)

def do_has_not_permission(parser, token):
    nodelist = parser.parse(('end_permission',))
    parser.delete_first_token()
    tag_name, perm_name = token.contents.split(None)
    return HasPermissionNode(nodelist, perm_name, opposite=True)

register.tag('has_permission', do_has_permission)
register.tag('has_not_permission', do_has_not_permission)


class HasPermissionNode(template.Node):

    def __init__(self, nodelist, perm_names, opposite=False):
        self.nodelist = nodelist

        split_perm_names = perm_names.split(",")
        self.perm_names = []
        for p in split_perm_names:
            p = template.Variable(p)
            self.perm_names.append(p)

        self.opposite = opposite
        
    def render(self, context):

        has = False

        user = context.get('user', None)
        if user:
            try:
                if user.is_superuser:
                    has = True
                else:

                    for p in self.perm_names:
                        try:
                            has = p.resolve(context) in user.permissions
                        except:
                            has=False
                        if has:
                            break

            except AttributeError:
                has=False

        if self.opposite:
            has = not has

        if has:
            return self.nodelist.render(context)
        else:
            return ""
