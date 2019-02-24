class Role:
    ORDINARY = 1
    ENTERPRISE = 2
    LABORATORY = 3
    ADMINISTRATOR = 4

    TYPE = (
        (ORDINARY, "求职者"),
        (ENTERPRISE, "企业"),
        (LABORATORY, "实验室"),
        (ADMINISTRATOR, "管理员"),
    )


class Gender:
    MAN = 1
    WOMEN = 2

    TYPE = (
        (MAN, "男"),
        (WOMEN, "女"),
    )


class ActivityType:
    MATCH = 1
    DYNAMIC = 2
    INTRODUCTION = 3
    RECRUITMENT = 4

    TYPE = (
        (MATCH, "比赛"),
        (DYNAMIC, "动态"),
        (INTRODUCTION, "实验室介绍"),
        (RECRUITMENT, "招聘信息"),
    )


class ActivityStatus:
    PREPARING = 1
    PROCESSING = 2
    END = 3
    NO = 4

    TYPE = (
        (PREPARING, "即将开始"),
        (PROCESSING, "进行中"),
        (END, "已结束"),
        (NO, "无状态"),
    )

# 角色对应有权限创建哪些活动
CreateDynamicPermission = {
    Role.ORDINARY: (ActivityType.DYNAMIC,),
    Role.ADMINISTRATOR: (ActivityType.MATCH, ActivityType.DYNAMIC, ActivityType.INTRODUCTION, ActivityType.RECRUITMENT),
    Role.LABORATORY: (ActivityType.DYNAMIC, ActivityType.INTRODUCTION, ActivityType.MATCH),
    Role.ENTERPRISE: (ActivityType.DYNAMIC, ActivityType.MATCH, ActivityType.RECRUITMENT),
}


class Action:
    LIKE = 1
    COLLECT = 2

    TYPE = (
        (LIKE, "点赞"),
        (COLLECT, "收藏"),
    )


class MessageContent:
    REGISTER = "欢迎注册！"
    LIKE = "%s点赞了你的%s"
    COLLECT = "%s收藏了你的%s"
    COMMENT = "%s评论了你的%s"
    REPLY = "%s回复了你的%s"
