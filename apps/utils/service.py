class BaseService:
    @staticmethod
    def list(request, queryset):
        """过滤后,还需要过滤"""
        return queryset

    @staticmethod
    def create(request, instance):
        """新建对象后,还需要处理"""
        return instance

    @staticmethod
    def update(request, instance):
        """更新后,需要做些处理"""
        return instance

    @staticmethod
    def partial_update(request, instance):
        """更新后,需要做些处理"""
        return instance

    @staticmethod
    def destroy(request, instance):
        """删除前,需要做些处理"""
        return instance
