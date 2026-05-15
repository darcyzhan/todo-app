from enum import IntEnum


class ErrorCode(IntEnum):
    # 通用错误 1000-1999
    UNKNOWN_ERROR = 1000
    VALIDATION_ERROR = 1001
    NOT_FOUND = 1002
    DUPLICATE_ERROR = 1003
    PERMISSION_DENIED = 1004
    RATE_LIMIT_EXCEEDED = 1005

    # 认证错误 2000-2999
    AUTH_FAILED = 2000
    TOKEN_EXPIRED = 2001
    TOKEN_INVALID = 2002
    WECHAT_AUTH_FAILED = 2003
    PHONE_BIND_FAILED = 2004

    # 用户错误 3000-3999
    USER_NOT_FOUND = 3000
    USER_ALREADY_EXISTS = 3001
    USER_UPDATE_FAILED = 3002

    # 任务错误 4000-4999
    TASK_NOT_FOUND = 4000
    TASK_CREATE_FAILED = 4001
    TASK_UPDATE_FAILED = 4002
    TASK_DELETE_FAILED = 4003
    TASK_BATCH_FAILED = 4004
    SUBTASK_NOT_FOUND = 4005

    # 项目错误 5000-5999
    PROJECT_NOT_FOUND = 5000
    PROJECT_CREATE_FAILED = 5001
    PROJECT_MEMBER_EXISTS = 5002
    PROJECT_MEMBER_NOT_FOUND = 5003

    # 标签错误 6000-6999
    TAG_NOT_FOUND = 6000
    TAG_CREATE_FAILED = 6001

    # 习惯错误 7000-7999
    HABIT_NOT_FOUND = 7000
    HABIT_ALREADY_LOGGED = 7001

    # AI 错误 8000-8999
    AI_PARSE_FAILED = 8000
    AI_SUGGEST_FAILED = 8001

    # 评论错误 9000-9999
    COMMENT_NOT_FOUND = 9000


ERROR_MESSAGES = {
    ErrorCode.UNKNOWN_ERROR: "未知错误",
    ErrorCode.VALIDATION_ERROR: "数据验证失败",
    ErrorCode.NOT_FOUND: "资源不存在",
    ErrorCode.DUPLICATE_ERROR: "资源已存在",
    ErrorCode.PERMISSION_DENIED: "权限不足",
    ErrorCode.RATE_LIMIT_EXCEEDED: "请求频率超限",
    ErrorCode.AUTH_FAILED: "认证失败",
    ErrorCode.TOKEN_EXPIRED: "Token 已过期",
    ErrorCode.TOKEN_INVALID: "Token 无效",
    ErrorCode.WECHAT_AUTH_FAILED: "微信授权失败",
    ErrorCode.PHONE_BIND_FAILED: "手机号绑定失败",
    ErrorCode.USER_NOT_FOUND: "用户不存在",
    ErrorCode.USER_ALREADY_EXISTS: "用户已存在",
    ErrorCode.USER_UPDATE_FAILED: "用户信息更新失败",
    ErrorCode.TASK_NOT_FOUND: "任务不存在",
    ErrorCode.TASK_CREATE_FAILED: "任务创建失败",
    ErrorCode.TASK_UPDATE_FAILED: "任务更新失败",
    ErrorCode.TASK_DELETE_FAILED: "任务删除失败",
    ErrorCode.TASK_BATCH_FAILED: "批量操作失败",
    ErrorCode.SUBTASK_NOT_FOUND: "子任务不存在",
    ErrorCode.PROJECT_NOT_FOUND: "项目不存在",
    ErrorCode.PROJECT_CREATE_FAILED: "项目创建失败",
    ErrorCode.PROJECT_MEMBER_EXISTS: "项目成员已存在",
    ErrorCode.PROJECT_MEMBER_NOT_FOUND: "项目成员不存在",
    ErrorCode.TAG_NOT_FOUND: "标签不存在",
    ErrorCode.TAG_CREATE_FAILED: "标签创建失败",
    ErrorCode.HABIT_NOT_FOUND: "习惯不存在",
    ErrorCode.HABIT_ALREADY_LOGGED: "今日已打卡",
    ErrorCode.AI_PARSE_FAILED: "AI 解析失败",
    ErrorCode.AI_SUGGEST_FAILED: "AI 建议失败",
    ErrorCode.COMMENT_NOT_FOUND: "评论不存在",
}
