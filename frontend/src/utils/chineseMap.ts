// 方面类别中英文映射
export const categoryMap: Record<string, string> = {
  'usability': '可用性',
  'general': '整体评价',
  'effectiveness': '有效性',
  'cost': '价格',
  'compatibility': '兼容性',
  'reliability': '可靠性',
  'efficiency': '效率',
  'security': '安全性',
  'safety': '安全',
  'enjoyability': '娱乐性',
  'learnability': '易学性',
  'aesthetics': '美观性'
}

// 情感中英文映射
export const sentimentMap: Record<string, string> = {
  'positive': '正面',
  'negative': '负面'
}

// 术语中英文映射
export const termMap: Record<string, string> = {
  'update': '更新',
  'page': '页面',
  'money': '价格',
  'text': '文本',
  'sync': '同步',
  'list': '列表',
  'photo': '照片',
  'notification': '通知',
  'version': '版本',
  'design': '设计',
  'chat': '聊天',
  'account': '账户',
  'group': '群组',
  'document': '文档',
  'functionality': '功能',
  'price': '价格',
  'interface': '界面',
  'tag': '标签',
  'color': '颜色',
  'sound': '声音'
}

// 通用转换函数
export const toChinese = (key: string, type: 'category' | 'sentiment' | 'term'): string => {
  if (type === 'category') return categoryMap[key] || key
  if (type === 'sentiment') return sentimentMap[key] || key
  if (type === 'term') return termMap[key] || key
  return key
}

// 获取所有类别（中文）
export const getCategoryOptions = () => {
  return Object.entries(categoryMap).map(([value, label]) => ({ value, label }))
}