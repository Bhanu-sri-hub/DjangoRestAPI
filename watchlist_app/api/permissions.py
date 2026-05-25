from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS

class AdminorReadOnly(BasePermission):
    def has_permission(self, request, view):
        admin_user = bool(request.user and request.user.is_staff)
        return request.method == "GET" or admin_user
    
class ReviewUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: # --> safe methods include get(read only request)
            return True
        else:
            return bool(obj.review_user == request.user)