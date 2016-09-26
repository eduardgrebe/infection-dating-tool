from user_management.forms import UserCreationForm
from django.contrib.auth.models import Group

class EddiUserCreationForm(UserCreationForm):
    
    def save(self, commit=True):
        
        user = super(EddiUserCreationForm, self).save(True)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
        outside_eddi_group.user_set.add(user)
        return user
